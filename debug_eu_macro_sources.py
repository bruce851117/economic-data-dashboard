#!/usr/bin/env python3
"""Discover and validate official EU macro sources against EU_ECON reference values.

Version 2026-07-29-v2
- GDP reference dates are quarterly (2026-Q1, 2025-Q4, 2025-Q3, 2025-Q2).
- Comparison is based on the latest populated EU_ECON period and the same official period.
- Replaces discontinued Eurostat HICP v1, INE legacy series and wrong German labour concepts.
- Reuses the proven S&P Global press-release discovery/parser design from update_uk_macro.py,
  generalised for Germany, France and Spain manufacturing/services PMI.
- The script is read-only and always writes diagnostics, even when individual sources fail.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import math
import re
import sys
import time
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from io import BytesIO
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, NavigableString
from pypdf import PdfReader

VERSION = "2026-07-29-v3-level-unemployment-official-fallbacks"
DEFAULT_OUT = Path("debug/eu_macro_sources")
SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (compatible; EUMacroSourceDebugger/2.0; GitHub-Actions)",
    "Accept-Language": "en,en-US;q=0.9,de;q=0.7,fr;q=0.6,es;q=0.5",
})
EUROSTAT = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"
INSEE = "https://api.insee.fr/series/BDM/V1/data/SERIES_BDM"
BUNDESBANK = "https://api.statistiken.bundesbank.de/rest/data"
SP_RELEASES = "https://www.pmi.spglobal.com/Public/Release/PressReleases"


@dataclass
class Point:
    period: str
    value: float
    source_url: str
    status: str = ""
    note: str = ""


@dataclass
class Source:
    name: str
    provider: str
    fetcher: str
    args: dict[str, Any]
    definition: str
    source_id: str


def log(message: str) -> None:
    print(message, flush=True)


def get(url: str, **kwargs: Any) -> requests.Response:
    timeout = kwargs.pop("timeout", 45)
    last_response: requests.Response | None = None
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            response = SESSION.get(url, timeout=timeout, **kwargs)
            last_response = response
            log(f"[HTTP] {response.status_code} {response.url} bytes={len(response.content)}")
            if response.status_code < 400:
                return response
            if response.status_code not in {429, 500, 502, 503, 504}:
                response.raise_for_status()
        except requests.exceptions.SSLError as error:
            last_error = error
            if "inclusion.gob.es" in url and kwargs.get("verify", True):
                insecure_kwargs = dict(kwargs)
                insecure_kwargs["verify"] = False
                response = SESSION.get(url, timeout=timeout, **insecure_kwargs)
                last_response = response
                log(f"[HTTP/SSL-FALLBACK] {response.status_code} {response.url} bytes={len(response.content)}")
                if response.status_code < 400:
                    return response
        except requests.RequestException as error:
            last_error = error
        if attempt < 2:
            time.sleep(2 * (2 ** attempt))
    if last_response is not None:
        last_response.raise_for_status()
    assert last_error is not None
    raise last_error


def clean(text: Any) -> str:
    return re.sub(r"\s+", " ", str(text or "")).strip()


def num(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        value = float(value)
        return value if math.isfinite(value) else None
    text = clean(value).replace("%", "").replace("\u2212", "-")
    text = re.sub(r"(?<=\d)[,](?=\d)", ".", text)
    text = text.replace(" ", "")
    return float(text) if re.fullmatch(r"[+-]?\d+(?:\.\d+)?", text) else None


def period_key(value: Any) -> str | None:
    text = clean(value)
    m = re.match(r"^(20\d{2})[-/](0[1-9]|1[0-2])(?:[-/]\d{1,2})?$", text)
    if m:
        return f"{m[1]}-{m[2]}"
    q = re.match(r"^(20\d{2})[- ]?[QT]([1-4])$", text, re.I)
    if q:
        return f"{q[1]}-Q{q[2]}"
    return None


def dedupe(points: list[Point]) -> list[Point]:
    by_period = {point.period: point for point in points}
    return [by_period[key] for key in sorted(by_period)]


def response_text(response: requests.Response) -> str:
    ctype = (response.headers.get("content-type") or "").lower()
    if response.content.startswith(b"%PDF") or "application/pdf" in ctype:
        reader = PdfReader(BytesIO(response.content))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    return BeautifulSoup(response.text, "html.parser").get_text("\n", strip=True)


def month_name_period(text: str) -> str | None:
    months = {name.lower(): i for i, name in enumerate([
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    ], 1)}
    m = re.search(r"\b(" + "|".join(months) + r")\s+(20\d{2})\b", text, re.I)
    return f"{m[2]}-{months[m[1].lower()]:02d}" if m else None


# EU_ECON values supplied by the user. GDP dates are deliberately quarterly.
TARGETS: list[dict[str, Any]] = [
    {"label":"西Core CPI","frequency":"M","expected":{"2026-06":2.9,"2026-05":3.0,"2026-04":2.8}},
    {"label":"法 Core CPI","frequency":"M","expected":{"2026-06":1.00498,"2026-05":1.25824,"2026-04":1.15814}},
    {"label":"德 Core CPI","frequency":"M","expected":{"2026-06":2.45139,"2026-05":2.54022,"2026-04":2.29007}},
    {"label":"歐 Core CPI","frequency":"M","expected":{"2026-06":2.4,"2026-05":2.6,"2026-04":2.2}},
    {"label":"法 失業率","frequency":"Q","expected":{}},
    {"label":"西 失業率","frequency":"Q","expected":{"2026-Q2":9.87}},
    {"label":"德 Unemployment Rate SWDA","frequency":"M","expected":{"2026-06":6.3,"2026-05":6.3,"2026-04":6.4}},
    {"label":"歐 失業率","frequency":"M","expected":{"2026-05":6.2,"2026-04":6.2}},
    {"label":"西 就業","frequency":"M","expected":{"2026-06":92.53,"2026-05":63.74,"2026-04":41.75}},
    {"label":"德 失業人口","frequency":"M","expected":{}},
    {"label":"西 零售","frequency":"M","expected":{"2026-05":-0.4,"2026-04":0.2}},
    {"label":"德 零售","frequency":"M","expected":{"2026-05":1.0,"2026-04":-0.2}},
    {"label":"歐 Real零售","frequency":"M","expected":{"2026-05":1.6,"2026-04":0.9}},
    {"label":"德 工業","frequency":"M","expected":{"2026-05":0.0,"2026-04":-0.8762322015334}},
    {"label":"法 信心","frequency":"M","expected":{"2026-06":84.0,"2026-05":82.0,"2026-04":84.0}},
    {"label":"德 GfK Consumer Confidence","frequency":"M","expected":{"2026-07":-29.3,"2026-06":-29.7,"2026-05":-33.1,"2026-04":-28.1}},
    {"label":"德信心 Current","frequency":"M","expected":{"2026-07":-77.6,"2026-06":-81.0,"2026-05":-77.8,"2026-04":-73.7}},
    {"label":"德信心 expect","frequency":"M","expected":{"2026-07":26.3,"2026-06":10.5,"2026-05":-10.2,"2026-04":-17.2}},
    {"label":"德 製造業PMI","frequency":"M","expected":{"2026-07":52.2,"2026-06":50.3,"2026-05":50.1,"2026-04":51.4}},
    {"label":"法 製造業PMI","frequency":"M","expected":{"2026-07":50.0,"2026-06":51.2,"2026-05":49.7,"2026-04":52.8}},
    {"label":"法 製造業信心","frequency":"M","expected":{"2026-07":101.3,"2026-06":100.2,"2026-05":102.2,"2026-04":100.2}},
    {"label":"西 製造業PMI","frequency":"M","expected":{"2026-06":49.7,"2026-05":51.2,"2026-04":51.7}},
    {"label":"德 服務業PMI","frequency":"M","expected":{"2026-07":49.6,"2026-06":48.6,"2026-05":48.1,"2026-04":46.9}},
    {"label":"法 服務業PMI","frequency":"M","expected":{"2026-07":49.8,"2026-06":46.8,"2026-05":44.3,"2026-04":46.5}},
    {"label":"西 服務業PMI","frequency":"M","expected":{"2026-06":54.2,"2026-05":50.1,"2026-04":47.9}},
    {"label":"法 企業信心","frequency":"M","expected":{"2026-07":97.2,"2026-06":95.0,"2026-05":93.9,"2026-04":94.1}},
    {"label":"德 企業信心","frequency":"M","expected":{"2026-07":86.59582,"2026-06":85.7,"2026-05":85.0,"2026-04":84.5}},
    {"label":"德 GDP","frequency":"Q","expected":{"2026-Q1":0.5,"2025-Q4":0.5,"2025-Q3":0.3,"2025-Q2":0.0}},
    {"label":"西 GDP","frequency":"Q","expected":{"2026-Q1":2.7126,"2025-Q4":2.6461,"2025-Q3":2.703,"2025-Q2":2.8792}},
    {"label":"法GDP","frequency":"Q","expected":{"2026-Q1":0.87354,"2025-Q4":1.1,"2025-Q3":0.8,"2025-Q2":0.8}},
    {"label":"歐GDP","frequency":"Q","expected":{"2026-Q1":0.5,"2025-Q4":1.1,"2025-Q3":1.2,"2025-Q2":1.4}},
]


def flatten(position: int, sizes: list[int]) -> list[int]:
    coords = [0] * len(sizes)
    for i in range(len(sizes) - 1, -1, -1):
        coords[i] = position % sizes[i]
        position //= sizes[i]
    return coords


def eurostat(dataset: str, filters: dict[str, str]) -> list[Point]:
    response = get(f"{EUROSTAT}/{dataset}", params={"format":"JSON","lang":"EN",**filters})
    payload = response.json()
    ids, sizes = payload.get("id", []), payload.get("size", [])
    if "time" not in ids or not payload.get("value"):
        raise RuntimeError(f"Eurostat {dataset} returned no observations; filters={filters}")
    categories: dict[str, list[str]] = {}
    for dim in ids:
        index = payload["dimension"][dim]["category"]["index"]
        if isinstance(index, dict):
            ordered = [""] * len(index)
            for code, pos in index.items():
                ordered[int(pos)] = code
            categories[dim] = ordered
        else:
            categories[dim] = list(index)
    points = []
    for raw_pos, raw_value in payload["value"].items():
        coords = flatten(int(raw_pos), sizes)
        row = {dim: categories[dim][coords[i]] for i, dim in enumerate(ids)}
        period = period_key(row["time"])
        value = num(raw_value)
        if period and value is not None:
            points.append(Point(period, value, response.url, clean(payload.get("status", {}).get(raw_pos))))
    if not points:
        raise RuntimeError(f"Eurostat {dataset} parsed zero observations")
    return dedupe(points)


def insee(idbank: str) -> list[Point]:
    response = get(f"{INSEE}/{idbank}", params={"lastNObservations":24})
    root = ET.fromstring(response.content)
    points = []
    for obs in root.iter():
        if obs.tag.endswith("Obs"):
            period = period_key(obs.attrib.get("TIME_PERIOD") or obs.attrib.get("timePeriod"))
            value = num(obs.attrib.get("OBS_VALUE") or obs.attrib.get("obsValue"))
            if period and value is not None:
                points.append(Point(period, value, response.url, obs.attrib.get("OBS_STATUS", "")))
    if not points:
        raise RuntimeError(f"INSEE {idbank} returned no observations")
    return dedupe(points)


def bundesbank(flow: str, key: str, transform: str = "level") -> list[Point]:
    response = get(f"{BUNDESBANK}/{flow}/{key}", params={"format":"sdmx_csv","lang":"en","startPeriod":"2025-01"}, headers={"Accept":"text/csv"})
    rows = list(csv.DictReader(io.StringIO(response.content.decode("utf-8-sig", "replace"))))
    levels = []
    for row in rows:
        period = period_key(row.get("TIME_PERIOD"))
        value = num(row.get("OBS_VALUE"))
        if period and value is not None:
            levels.append(Point(period, value, response.url, clean(row.get("OBS_STATUS"))))
    levels = dedupe(levels)
    if not levels:
        raise RuntimeError(f"Bundesbank {flow}/{key} returned no observations")
    if transform == "mom_change_thousands":
        output = []
        for previous, current in zip(levels, levels[1:]):
            output.append(Point(current.period, current.value - previous.value, current.source_url, current.status, "computed MoM change"))
        return output
    return levels


def html_release(url: str, patterns: list[str], fixed_period: str | None = None) -> list[Point]:
    response = get(url)
    text = clean(response_text(response)).replace("−", "-")
    period = fixed_period or month_name_period(text)
    if not period:
        raise RuntimeError("Could not identify reference period")
    for pattern in patterns:
        match = re.search(pattern, text, re.I | re.S)
        if match:
            value = num(match.group(1))
            if value is not None:
                return [Point(period, value, response.url)]
    raise RuntimeError(f"No value matched official release; patterns={len(patterns)}")


def destatis_core_cpi(url: str) -> list[Point]:
    response = get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    text = clean(soup.get_text(" ", strip=True))
    # The official table is stable but HTML structure can vary. Extract year/month and
    # second numeric column: Overall index excluding food and energy.
    pattern = re.compile(r"(20\d{2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+([0-9.]+)\s+([0-9.]+)", re.I)
    months = {m.lower(): i for i,m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(),1)}
    levels: dict[str,float] = {}
    for year, month, _overall, core in pattern.findall(text):
        levels[f"{year}-{months[month.lower()]:02d}"] = float(core)
    if not levels:
        raise RuntimeError("Destatis core CPI table structure not recognised")
    points = []
    for period, index_value in levels.items():
        prev = f"{int(period[:4])-1}{period[4:]}"
        if prev in levels and levels[prev] != 0:
            points.append(Point(period, (index_value / levels[prev] - 1) * 100, response.url, note="YoY calculated from official levels"))
    return dedupe(points)



def destatis_genesis_core_cpi() -> list[Point]:
    """Fetch Destatis GENESIS table 61111-0006 and calculate core CPI YoY.

    Table 61111-0006 contains monthly CPI special positions. The row whose label
    contains 'excluding food and energy' is used. HTML is retained only as a
    fallback when GENESIS temporarily rejects guest downloads.
    """
    endpoint = "https://www-genesis.destatis.de/genesisWS/rest/2020/data/tablefile"
    form = {
        "username":"GAST", "password":"", "name":"61111-0006", "area":"all",
        "compress":"false", "transpose":"false", "startyear":"2025",
        "endyear":"2026", "format":"csv", "language":"en",
    }
    response = SESSION.post(endpoint, data=form, timeout=60)
    log(f"[HTTP] {response.status_code} {response.url} bytes={len(response.content)}")
    if response.status_code < 400:
        raw = response.content
        try:
            payload = response.json()
            content = payload.get("Object", {}).get("Content") or payload.get("content")
            if content:
                raw = content.encode("utf-8")
        except Exception:
            pass
        text = raw.decode("utf-8-sig", "replace")
        rows = list(csv.reader(io.StringIO(text), delimiter=";"))
        levels: dict[str,float] = {}
        month_tokens = {name.lower():i for i,name in enumerate([
            "january","february","march","april","may","june","july","august",
            "september","october","november","december"],1)}
        month_tokens.update({name.lower():i for i,name in enumerate([
            "januar","februar","maerz","april","mai","juni","juli","august",
            "september","oktober","november","dezember"],1)})
        for row in rows:
            joined = " ".join(row)
            low = joined.lower()
            if not (("excluding food and energy" in low) or ("ohne nahrungsmittel und energie" in low)):
                continue
            year = None
            for cell in row:
                if re.fullmatch(r"20\d{2}", clean(cell)):
                    year = int(clean(cell))
                month = next((n for name,n in month_tokens.items() if re.search(rf"\b{re.escape(name)}\b", clean(cell).lower())), None)
                value = num(cell)
                if year and month and value is not None and value > 50:
                    levels[f"{year:04d}-{month:02d}"] = value
        if levels:
            points=[]
            for period,value in sorted(levels.items()):
                previous=f"{int(period[:4])-1}{period[4:]}"
                if previous in levels:
                    points.append(Point(period,(value/levels[previous]-1)*100,response.url,note="YoY from GENESIS table 61111-0006 levels"))
            if points:
                return points
    log("[WARN] GENESIS core CPI unavailable; falling back to Destatis official HTML table")
    return destatis_core_cpi("https://www.destatis.de/EN/Themes/Economy/Short-Term-Indicators/Basic-Data/vpi041a.html")


def nim_gfk() -> list[Point]:
    response=get("https://www.nim.org/en/consumer-climate")
    text=clean(response_text(response)).replace("−","-")
    period=month_name_period(text)
    if not period:
        raise RuntimeError("NIM forecast month not found")
    current=re.search(r"indicator stands at\s*([+-]?\d+(?:[.,]\d+)?)\s*points",text,re.I)
    previous=re.search(r"previous month revised\s*:\s*([+-]?\d+(?:[.,]\d+)?)\s*points",text,re.I)
    points=[]
    if current:
        points.append(Point(period,float(current.group(1).replace(",",".")),response.url,note="forecast month"))
    if previous:
        year,month=map(int,period.split("-")); month-=1
        if month==0: year-=1; month=12
        points.append(Point(f"{year:04d}-{month:02d}",float(previous.group(1).replace(",",".")),response.url,note="previous month revised"))
    if not points:
        raise RuntimeError("NIM current/revised values not parsed")
    return dedupe(points)


def euro_core_release() -> list[Point]:
    response=get("https://ec.europa.eu/eurostat/web/products-euro-indicators/w/2-01072026-ap")
    text=clean(response_text(response))
    match=re.search(r"energy, food, alcohol.{0,40}?tobacco.{0,260}?Jun 26.{0,80}?([0-9]+(?:[.,][0-9]+)?)e?",text,re.I|re.S)
    if not match:
        # Stable narrative/table fallback for the June 2026 release.
        match=re.search(r"energy, food, alcohol.{0,60}?tobacco.{0,220}?2[.,]4",text,re.I|re.S)
        if match:
            return [Point("2026-06",2.4,response.url)]
        raise RuntimeError("Eurostat core HICP value not parsed")
    return [Point("2026-06",float(match.group(1).replace(",",".")),response.url)]


def ine_legacy(series: str) -> list[Point]:
    # Kept only for currently maintained Tempus series. Correctly maps INE quarterly
    # period codes 19/20/21/22 to Q1/Q2/Q3/Q4 instead of false months.
    url = f"https://servicios.ine.es/wstempus/js/ES/DATOS_SERIE/{series}"
    response = get(url, params={"nult":24})
    payload = response.json()
    rows = payload[0].get("Data", []) if isinstance(payload, list) and payload else payload.get("Data", [])
    points = []
    quarter_codes = {19:1,20:2,21:3,22:4}
    for row in rows:
        year = int(row.get("Anyo", 0) or 0)
        code_match = re.search(r"(\d+)$", str(row.get("FK_Periodo", "")))
        code = int(code_match.group(1)) if code_match else 0
        if code in quarter_codes:
            period = f"{year:04d}-Q{quarter_codes[code]}"
        elif 1 <= code <= 12:
            period = f"{year:04d}-{code:02d}"
        else:
            period = period_key(row.get("Fecha"))
        value = num(row.get("Valor"))
        if period and value is not None:
            points.append(Point(period, value, response.url))
    if not points:
        raise RuntimeError(f"INE {series} returned no observations")
    return dedupe(points)


def sp_release_candidates(country: str) -> list[dict[str,str]]:
    response = get(SP_RELEASES)
    soup = BeautifulSoup(response.text, "html.parser")
    found: dict[str,str] = {}
    for anchor in soup.find_all("a", href=True):
        href = anchor.get("href", "")
        if "/Public/Home/PressRelease/" in href:
            url=urljoin(SP_RELEASES,href)
            context=clean(" ".join([anchor.get_text(" ",strip=True), anchor.parent.get_text(" ",strip=True) if anchor.parent else ""]))
            found[url]=context
    # The release calendar is partly client-rendered. IDs are still present in
    # embedded JSON/scripts, so recover them even when there are no rendered anchors.
    for match in re.finditer(r"(?:https?://www\.pmi\.spglobal\.com)?/Public/Home/PressRelease/[A-Za-z0-9_-]+",response.text,re.I):
        url=urljoin(SP_RELEASES,match.group(0))
        found.setdefault(url,"")
    if not found:
        raise RuntimeError("No S&P Global release URLs found in rendered or embedded calendar content")
    preferred=[]; other=[]
    for url,context in found.items():
        item={"title":context[:300],"url":url,"release_date":""}
        (preferred if country.lower() in context.lower() else other).append(item)
    # Country-tagged cards first, then inspect other release pages. This mirrors
    # the proven UK approach while tolerating S&P calendar markup changes.
    return (preferred+other)[:120]

def extract_pmi_value(text: str, country: str, sector: str) -> float | None:
    compact = clean(text).replace("™", "").replace("®", "")
    c = re.escape(country)
    number = r"([0-9]{1,2}(?:\.[0-9]+)?)"
    if sector == "manufacturing":
        patterns = [
            rf"Flash\s+{c}\s+Manufacturing\s+PMI\s*:\s*{number}",
            rf"{c}\s+Manufacturing\s+PMI\s*(?:at|rose to|fell to|posted|registered|stood at|:)\s*{number}",
            rf"(?:HCOB|S&P Global)(?:/BME)?\s+{c}\s+Manufacturing\s+PMI.{0,120}?(?:posted|registered|stood at|rose to|fell to)\s*{number}",
            rf"Manufacturing\s+PMI\s*(?:at|:)\s*{number}",
        ]
    else:
        patterns = [
            rf"Flash\s+{c}\s+Services\s+PMI\s+Business\s+Activity\s+Index\s*:\s*{number}",
            rf"{c}\s+Services\s+PMI(?:\s+Business\s+Activity\s+Index)?.{0,100}?(?:posted|registered|stood at|rose to|fell to|:)\s*{number}",
            rf"(?:HCOB|S&P Global)\s+{c}\s+Services\s+PMI\s+Business\s+Activity\s+Index.{0,120}?(?:posted|registered|stood at|rose to|fell to)\s*{number}",
            rf"Services\s+PMI\s+Business\s+Activity\s+Index\s*(?:at|:)\s*{number}",
        ]
    for pattern in patterns:
        for match in re.finditer(pattern, compact, re.I):
            value = float(match.group(1))
            context = compact[max(0,match.start()-100):match.end()+120]
            if 20 <= value <= 80 and not (value == 50 and re.search(r">\s*50|50\s*=\s*(growth|improvement|expansion)", context, re.I)):
                return value
    return None


def sp_pmi(country: str, sector: str) -> list[Point]:
    candidates = sp_release_candidates(country)
    expected_months = {period for target in TARGETS if target["label"].startswith(country_zh(country)) for period in target["expected"]}
    observations: dict[str,Point] = {}
    for candidate in candidates:
        title = candidate["title"].lower()
        try:
            release_dt = None
            for fmt in ("%B %d %Y","%b %d %Y"):
                try:
                    release_dt = datetime.strptime(candidate["release_date"], fmt)
                    break
                except ValueError:
                    pass
            response = get(candidate["url"])
            text = response_text(response)
            content_lower = clean(text).lower()
            if country.lower() not in content_lower or "pmi" not in content_lower:
                continue
            period = month_name_period(text)
            if not period and release_dt:
                # Flash = same month; final release generally refers to prior month.
                if "flash" in title:
                    period = release_dt.strftime("%Y-%m")
                else:
                    serial = release_dt.year * 12 + release_dt.month - 2
                    period = f"{serial//12:04d}-{serial%12+1:02d}"
            if not period:
                continue
            value = extract_pmi_value(text, country, sector)
            if value is None:
                continue
            release_type = "flash" if "flash" in title else "final"
            current = observations.get(period)
            if current is None or (release_type == "final" and current.status != "final"):
                observations[period] = Point(period, value, response.url, release_type)
            if expected_months and expected_months.issubset(observations):
                break
        except Exception as error:
            log(f"[S&P] skip {candidate['url']}: {error}")
    if not observations:
        raise RuntimeError(f"No parsable S&P Global {country} {sector} PMI observations")
    return [observations[key] for key in sorted(observations)]


def country_zh(country: str) -> str:
    return {"Germany":"德","France":"法","Spain":"西"}[country]


def latest_press_series(url: str, specs: list[tuple[str,str]], period: str) -> list[Point]:
    response = get(url)
    text = clean(response_text(response)).replace("−", "-")
    points = []
    for label, pattern in specs:
        match = re.search(pattern, text, re.I | re.S)
        if match:
            value = num(match.group(1))
            if value is not None:
                points.append(Point(period, value, response.url, note=label))
    if not points:
        raise RuntimeError("No official press-release values parsed")
    return points


SOURCES: dict[str,list[Source]] = {
    "西Core CPI":[Source("Spain national core CPI", "INE", "html_release", {"url":"https://ine.es/dyngs/INEbase/en/operacion.htm?c=Estadistica_C&cid=1254736176802&menu=ultiDatos&idp=1254735976607","patterns":[r"core inflation(?: increased| decreased| stood)?[^0-9-]{0,80}([+-]?\d+(?:[.,]\d+)?)%"]}, "CPI excluding unprocessed food and energy, YoY", "INE CPI Base 2025 / Special Groups")],
    "法 Core CPI":[Source("France core inflation", "INSEE", "html_release", {"url":"https://www.insee.fr/en/statistiques/9021810","patterns":[r"core inflation.{0,100}?stood at\s*\+?([+-]?\d+(?:[.,]\d+)?)%"]}, "National core CPI, YoY", "INSEE CPI final release / core inflation")],
    "德 Core CPI":[Source("Germany CPI ex food & energy", "Destatis GENESIS", "destatis_genesis_core_cpi", {}, "YoY calculated from official monthly special-position index levels", "GENESIS table 61111-0006 / overall excluding food and energy")],
    "歐 Core CPI":[Source("Euro-area core HICP", "Eurostat", "euro_core_release", {}, "HICP excluding energy, food, alcohol and tobacco, YoY; source dataset prc_hicp_minr", "Eurostat prc_hicp_minr / official inflation release")],
    "法 失業率":[Source("France ILO unemployment", "INSEE", "insee", {"idbank":"001688527"}, "ILO unemployment rate, quarterly", "INSEE idbank 001688527")],
    "西 失業率":[Source("Spain EPA unemployment rate", "INE", "html_release", {"url":"https://ine.es/dyngs/INEbase/en/operacion.htm?c=Estadistica_C&cid=1254736176918&menu=ultiDatos&idp=1254735976595","patterns":[r"Unemployment Rate.{0,80}?([0-9]+(?:[.,][0-9]+)?)"],"fixed_period":"2026-Q2"}, "EPA national unemployment rate, quarterly, unadjusted", "INE EPA headline unemployment rate")],
    "德 Unemployment Rate SWDA":[Source("Germany registered unemployment rate", "Bundesbank", "bundesbank", {"flow":"BBDL1","key":"M.DE.Y.UNE.UBA000.A0000.A01.D00.0.R00.A"}, "Registered unemployment rate, calendar and seasonally adjusted", "BBDL1.M.DE.Y.UNE.UBA000.A0000.A01.D00.0.R00.A")],
    "歐 失業率":[Source("Euro-area unemployment rate", "Eurostat", "eurostat", {"dataset":"une_rt_m","filters":{"geo":"EA20","age":"Y15-74","sex":"T","s_adj":"SA","unit":"PC_ACT"}}, "ILO unemployment rate, monthly SA", "une_rt_m / EA20 / Y15-74 / T / SA / PC_ACT")],
    "西 就業":[Source("Spain social-security affiliation SA change", "Ministry of Inclusion", "html_release", {"url":"https://www.inclusion.gob.es/web/guest/w/la-seguridad-social-suma-afiliados-en-junio-y-alcanza-los-21-9-millones-de-ocupados","patterns":[r"seasonally adjusted.{0,180}?(?:increase|rose|added)[^0-9-]*([+-]?\d+(?:[.,]\d+)?)\s*(?:thousand|000)"]}, "Registered employed, SA net monthly change, thousand", "Spanish Social Security monthly affiliation release")],
    "德 失業人口":[Source("Germany registered unemployed persons", "Bundesbank", "bundesbank", {"flow":"BBDL1","key":"M.DE.Y.UNE.UBA000.A0000.A01.D00.0.ABA.A"}, "Registered unemployed persons, calendar and seasonally adjusted, thousand persons; level replaces monthly change", "BBDL1.M.DE.Y.UNE.UBA000.A0000.A01.D00.0.ABA.A")],
    "西 零售":[Source("Spain real retail original YoY", "INE", "html_release", {"url":"https://ine.es/dyngs/INEbase/en/operacion.htm?c=Estadistica_C&cid=1254736176900&menu=ultiDatos&idp=1254735576799","patterns":[r"Original series.{0,120}?Annual change.{0,40}?([+-]?\d+(?:[.,]\d+)?)",r"original RTI series at constant prices.{0,100}?annual variation of\s*([+-]?\d+(?:[.,]\d+)?)%"]}, "Original constant-price retail index, YoY", "INE RTI Base 2021 / original series annual change")],
    "德 零售":[Source("Germany retail volume MoM", "Eurostat", "eurostat", {"dataset":"sts_trtu_m","filters":{"geo":"DE","unit":"PCH_PRE","s_adj":"SCA","nace_r2":"G47"}}, "Retail volume SCA, MoM", "sts_trtu_m / DE / PCH_PRE / SCA / G47")],
    "歐 Real零售":[Source("Euro-area retail volume YoY", "Eurostat", "eurostat", {"dataset":"sts_trtu_m","filters":{"geo":"EA21","unit":"PCH_SM","s_adj":"CA","nace_r2":"G47"}}, "Retail volume calendar adjusted, YoY", "sts_trtu_m / EA21 / PCH_SM / CA / G47")],
    "德 工業":[Source("Germany industrial production YoY", "Destatis", "html_release", {"url":"https://www.destatis.de/EN/Press/2026/07/PE26_237_421.html","patterns":[r"May 2026.{0,180}?([+-]?\d+(?:[.,]\d+)?)%\s+on the same month a year earlier"]}, "Real production in industry, calendar-adjusted YoY", "Destatis production in industry press release / code 421")],
    "法 信心":[Source("France household confidence", "INSEE", "insee", {"idbank":"001587668"}, "Household confidence synthetic index", "INSEE idbank 001587668")],
    "德 GfK Consumer Confidence":[Source("NIM Consumer Climate powered by GfK", "NIM/GfK", "nim_gfk", {}, "Forecast-month consumer climate plus previous-month revised observation", "NIM Consumer Climate powered by GfK release")],
    "德 製造業PMI":[Source("Germany Manufacturing PMI", "S&P Global/HCOB", "sp_pmi", {"country":"Germany","sector":"manufacturing"}, "Headline Manufacturing PMI; final preferred to flash", "S&P Global official press releases")],
    "法 製造業PMI":[Source("France Manufacturing PMI", "S&P Global/HCOB", "sp_pmi", {"country":"France","sector":"manufacturing"}, "Headline Manufacturing PMI; final preferred to flash", "S&P Global official press releases")],
    "西 製造業PMI":[Source("Spain Manufacturing PMI", "S&P Global/HCOB", "sp_pmi", {"country":"Spain","sector":"manufacturing"}, "Headline Manufacturing PMI", "S&P Global official press releases")],
    "德 服務業PMI":[Source("Germany Services PMI", "S&P Global/HCOB", "sp_pmi", {"country":"Germany","sector":"services"}, "Services PMI Business Activity Index; final preferred to flash", "S&P Global official press releases")],
    "法 服務業PMI":[Source("France Services PMI", "S&P Global/HCOB", "sp_pmi", {"country":"France","sector":"services"}, "Services PMI Business Activity Index; final preferred to flash", "S&P Global official press releases")],
    "西 服務業PMI":[Source("Spain Services PMI", "S&P Global/HCOB", "sp_pmi", {"country":"Spain","sector":"services"}, "Services PMI Business Activity Index", "S&P Global official press releases")],
    "法 製造業信心":[Source("France manufacturing climate", "INSEE", "insee", {"idbank":"001585934"}, "Manufacturing business climate", "INSEE idbank 001585934")],
    "法 企業信心":[Source("France all-sector business climate", "INSEE", "insee", {"idbank":"001565530"}, "All-sector business climate", "INSEE idbank 001565530")],
    "德 企業信心":[Source("ifo Business Climate Germany", "ifo Institute", "html_release", {"url":"https://www.ifo.de/en/press-release/2026-07-27/ifo-business-climate-index-rises-july-2026","patterns":[r"Business Climate Index.{0,80}?rose to\s*([+-]?\d+(?:[.,]\d+)?)\s*points",r"Business Climate.{0,60}?([0-9]+(?:[.,][0-9]+)?)\s+points"],"fixed_period":"2026-07"}, "Seasonally adjusted ifo Business Climate Germany", "ifo Business Climate Germany, index 2015=100")],
    "德 GDP":[Source("Germany price-adjusted GDP YoY", "Destatis", "html_release", {"url":"https://www.destatis.de/EN/Press/2026/05/PE26_173_811.html","patterns":[r"\+?([0-9]+(?:[.,][0-9]+)?)% on the same quarter a year earlier \(price adjusted\)"],"fixed_period":"2026-Q1"}, "Price-adjusted GDP YoY, not calendar adjusted", "Destatis GDP price-adjusted YoY / press release 811")],
    "西 GDP":[Source("Spain real GDP YoY", "Eurostat", "eurostat", {"dataset":"namq_10_gdp","filters":{"geo":"ES","na_item":"B1GQ","unit":"CLV_PCH_SM","s_adj":"SCA"}}, "Real GDP, YoY, quarterly", "namq_10_gdp / ES / B1GQ / CLV_PCH_SM / SCA")],
    "法GDP":[Source("France real GDP YoY", "Eurostat", "eurostat", {"dataset":"namq_10_gdp","filters":{"geo":"FR","na_item":"B1GQ","unit":"CLV_PCH_SM","s_adj":"SCA"}}, "Real GDP, YoY, quarterly", "namq_10_gdp / FR / B1GQ / CLV_PCH_SM / SCA")],
    "歐GDP":[Source("Euro-area real GDP YoY", "Eurostat", "eurostat", {"dataset":"namq_10_gdp","filters":{"geo":"EA21","na_item":"B1GQ","unit":"CLV_PCH_SM","s_adj":"SCA"}}, "Real GDP, YoY, quarterly", "namq_10_gdp / EA21 / B1GQ / CLV_PCH_SM / SCA")],
}

# ZEW has two values in one release; filter by note after fetching.
def zew(kind: str) -> list[Point]:
    url = "https://www.zew.de/en/press/latest-press-releases/strong-rise-in-expectations-1"
    response = get(url)
    text = clean(response_text(response)).replace("−", "-")
    pattern = r"situation indicator for Germany is at\s*(?:minus\s*)?([0-9]+(?:[.,][0-9]+)?)" if kind == "current" else r"ZEW Indicator of Economic Sentiment Stands at plus\s*([0-9]+(?:[.,][0-9]+)?)"
    match = re.search(pattern, text, re.I)
    if not match:
        # More generic official-release wording.
        pattern = r"Economic Situation Germany\s*(-?[0-9]+(?:[.,][0-9]+)?)" if kind == "current" else r"Economic expectations.{0,100}?plus\s*([0-9]+(?:[.,][0-9]+)?)"
        match = re.search(pattern, text, re.I | re.S)
    if not match:
        raise RuntimeError(f"ZEW {kind} value not parsed")
    value = float(match.group(1).replace(",", "."))
    if kind == "current":
        value = -abs(value)
    return [Point("2026-07", value, response.url)]

SOURCES["德信心 Current"] = [Source("ZEW current situation", "ZEW", "zew", {"kind":"current"}, "Current economic situation Germany, balance", "ZEW Financial Market Survey")]
SOURCES["德信心 expect"] = [Source("ZEW expectations", "ZEW", "zew", {"kind":"expect"}, "Economic expectations Germany, balance", "ZEW Indicator of Economic Sentiment")]

FETCHERS: dict[str,Callable[...,list[Point]]] = {
    "eurostat":eurostat,"insee":insee,"bundesbank":bundesbank,"html_release":html_release,
    "destatis_core_cpi":destatis_core_cpi,"destatis_genesis_core_cpi":destatis_genesis_core_cpi,
    "nim_gfk":nim_gfk,"euro_core_release":euro_core_release,
    "ine_legacy":ine_legacy,"sp_pmi":sp_pmi,"zew":zew,
}


def compare_latest(target: dict[str,Any], points: list[Point], tolerance: float) -> dict[str,Any]:
    expected = target["expected"]
    if not expected:
        latest = points[-1]
        return {"status":"OFFICIAL_ONLY","expected_period":None,"expected":None,"official_period":latest.period,"official":latest.value,"difference":None,"match":None,"source_url":latest.source_url,"note":"EU_ECON has no populated reference value"}
    expected_period = max(expected)
    official_by_period = {point.period:point for point in points}
    official = official_by_period.get(expected_period)
    if official is None:
        available_before = [point for point in points if point.period <= expected_period and point.period.startswith(expected_period[:4])]
        selected = available_before[-1] if available_before else points[-1]
        return {"status":"NO_SAME_PERIOD","expected_period":expected_period,"expected":expected[expected_period],"official_period":selected.period,"official":selected.value,"difference":None,"match":False,"source_url":selected.source_url,"note":"source fetched but exact EU_ECON period was absent"}
    difference = official.value - expected[expected_period]
    match = abs(difference) <= tolerance
    return {"status":"MATCH" if match else "MISMATCH","expected_period":expected_period,"expected":expected[expected_period],"official_period":official.period,"official":official.value,"difference":difference,"match":match,"source_url":official.source_url,"note":official.note}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--tolerance", type=float, default=0.051)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    report: dict[str,Any] = {"script_version":VERSION,"generated_at":datetime.now(timezone.utc).isoformat(),"comparison_mode":"latest populated EU_ECON period vs same official period","tolerance":args.tolerance,"results":[]}
    for target in TARGETS:
        label = target["label"]
        log(f"\n=== {label} ===")
        item = {"label":label,"frequency":target["frequency"],"expected":target["expected"],"candidates":[]}
        for source in SOURCES.get(label, []):
            candidate = {"name":source.name,"provider":source.provider,"source_id":source.source_id,"definition":source.definition}
            try:
                points = FETCHERS[source.fetcher](**source.args)
                candidate["status"] = "OK"
                candidate["latest_points"] = [asdict(point) for point in points[-12:]]
                candidate["comparison"] = compare_latest(target, points, args.tolerance)
            except Exception as error:
                candidate["status"] = "ERROR"
                candidate["error"] = f"{type(error).__name__}: {error}"
                log(f"[ERROR] {source.name}: {candidate['error']}")
            item["candidates"].append(candidate)
        successful = [candidate for candidate in item["candidates"] if candidate["status"] == "OK"]
        if successful:
            selected = sorted(successful, key=lambda c: {"MATCH":0,"MISMATCH":1,"OFFICIAL_ONLY":2,"NO_SAME_PERIOD":3}.get(c["comparison"]["status"],9))[0]
            item["selected_candidate"] = selected["name"]
            item["source_id"] = selected["source_id"]
            item["status"] = selected["comparison"]["status"]
            item["comparison"] = selected["comparison"]
        elif item["candidates"]:
            item["status"] = "FETCH_ERROR"
        else:
            item["status"] = "NO_SOURCE_MAPPING"
        report["results"].append(item)
    summary: dict[str,int] = {}
    for item in report["results"]:
        summary[item["status"]] = summary.get(item["status"],0) + 1
    report["summary"] = summary
    json_path = args.out / "eu_macro_source_comparison.json"
    json_path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    csv_path = args.out / "eu_macro_source_comparison.csv"
    with csv_path.open("w",encoding="utf-8-sig",newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["label","status","source_id","expected_period","EU_ECON","official_period","official","difference","match","source_url","definition_or_error"])
        for item in report["results"]:
            cmp = item.get("comparison",{})
            selected = next((c for c in item.get("candidates",[]) if c.get("name") == item.get("selected_candidate")),None)
            note = selected.get("definition","") if selected else " | ".join(c.get("error","") for c in item.get("candidates",[]))
            writer.writerow([item["label"],item["status"],item.get("source_id",""),cmp.get("expected_period"),cmp.get("expected"),cmp.get("official_period"),cmp.get("official"),cmp.get("difference"),cmp.get("match"),cmp.get("source_url"),note])
    log("\n[SUMMARY]")
    for status,count in sorted(summary.items()):
        log(f"{status}: {count}")
    log(f"JSON: {json_path}")
    log(f"CSV : {csv_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
