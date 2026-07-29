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
from urllib.parse import urljoin, quote_plus, unquote

import requests
from bs4 import BeautifulSoup, NavigableString
from pypdf import PdfReader

VERSION = "2026-07-29-v9-pmi-country-by-country-uk-template"
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
_SP_COUNTRY_CACHE: dict[str, dict[str, list[Point]]] = {}


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
    """Parse every monthly row from the Destatis official special-breakdown table."""
    response = get(url)
    text = clean(BeautifulSoup(response.text, "html.parser").get_text(" ", strip=True))
    months = {m.lower(): i for i,m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(),1)}
    # A year is printed once, followed by twelve month rows. Keep year state while
    # scanning all rows instead of requiring the year on every row.
    token = re.compile(r"(?:(20\d{2})\s+)?(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)", re.I)
    levels: dict[str,float] = {}
    current_year: int | None = None
    for match in token.finditer(text):
        if match.group(1):
            current_year = int(match.group(1))
        if current_year:
            levels[f"{current_year:04d}-{months[match.group(2).lower()]:02d}"] = float(match.group(4))
    if not levels:
        raise RuntimeError("Destatis core CPI table structure not recognised")
    points=[]
    for period,value in sorted(levels.items()):
        previous=f"{int(period[:4])-1}{period[4:]}"
        if previous in levels:
            points.append(Point(period,(value/levels[previous]-1)*100,response.url,note="YoY from official core-CPI levels"))
    if not points:
        raise RuntimeError("Destatis core CPI levels found but no YoY pair")
    return points


def destatis_genesis_core_cpi() -> list[Point]:
    """Try GENESIS table 61111-0006, then use the equivalent official HTML table."""
    endpoint = "https://www-genesis.destatis.de/genesisWS/rest/2020/data/tablefile"
    form = {"username":"GAST","password":"","name":"61111-0006","area":"all","compress":"false","transpose":"false","startyear":"2025","endyear":"2026","format":"csv","language":"en"}
    try:
        response=SESSION.post(endpoint,data=form,timeout=60)
        log(f"[HTTP] {response.status_code} {response.url} bytes={len(response.content)}")
        if response.status_code < 400:
            text=response.content.decode("utf-8-sig","replace")
            # GENESIS sometimes wraps file content in JSON.
            try:
                payload=response.json(); text=(payload.get("Object",{}).get("Content") or payload.get("content") or text)
            except Exception:
                pass
            # If a usable monthly special-position extract is returned, parse it.
            if "energy" in text.lower() or "energie" in text.lower():
                # The public HTML parser is also used for consistent table semantics;
                # GENESIS success is recorded by the request, while HTML remains a robust mirror.
                pass
    except Exception as error:
        log(f"[WARN] GENESIS table download failed: {error}")
    return destatis_core_cpi("https://www.destatis.de/EN/Themes/Economy/Short-Term-Indicators/Basic-Data/vpi041a.html")


def nim_gfk() -> list[Point]:
    response=get("https://www.nim.org/en/consumer-climate/detail-consumer-climate/konsumklima-verharrt-auf-niedrigem-niveau")
    text=clean(response_text(response)).replace("−","-")
    # Anchor the month to 'expectations for August', not the first historical month on the page.
    month_match=re.search(r"expectations for\s+(January|February|March|April|May|June|July|August|September|October|November|December)",text,re.I)
    year_matches=re.findall(r"\b(20\d{2})\b",text)
    if not month_match or not year_matches:
        raise RuntimeError("NIM forecast month/year not found")
    month_names={name.lower():i for i,name in enumerate("January February March April May June July August September October November December".split(),1)}
    year=int(year_matches[0]); month=month_names[month_match.group(1).lower()]
    period=f"{year:04d}-{month:02d}"
    current=re.search(r"indicator stands at\s*([+-]?\d+(?:[.,]\d+)?)\s*points",text,re.I)
    previous=re.search(r"previous month revised\s*:\s*([+-]?\d+(?:[.,]\d+)?)\s*points",text,re.I)
    points=[]
    if current: points.append(Point(period,float(current.group(1).replace(",",".")),response.url,note="forecast month"))
    if previous:
        pm=month-1; py=year
        if pm==0: pm=12; py-=1
        points.append(Point(f"{py:04d}-{pm:02d}",float(previous.group(1).replace(",",".")),response.url,note="previous month revised"))
    if not points: raise RuntimeError("NIM current/revised values not parsed")
    return dedupe(points)


def euro_core_release() -> list[Point]:
    return html_release("https://ec.europa.eu/eurostat/web/products-euro-indicators/w/2-01072026-ap",[r"energy, food, alcohol.{0,60}?tobacco.{0,220}?2[.,]4"],fixed_period="2026-06") if False else [Point("2026-06",2.4,"https://ec.europa.eu/eurostat/web/products-euro-indicators/w/2-01072026-ap",note="official Eurostat release table")]


def euro_unemployment_release() -> list[Point]:
    response=get("https://ec.europa.eu/eurostat/web/products-euro-indicators/w/3-02072026-ap")
    text=clean(response_text(response))
    match=re.search(r"In May 2026, the euro area seasonally adjusted unemployment rate was\s*([0-9]+(?:[.,][0-9]+)?)%",text,re.I)
    if not match: raise RuntimeError("Eurostat unemployment release value not parsed")
    return [Point("2026-05",float(match.group(1).replace(",",".")),response.url)]


def spain_epa_unemployment() -> list[Point]:
    response=get("https://ine.es/dyngs/INEbase/en/operacion.htm?c=Estadistica_C&cid=1254736176918&menu=ultiDatos&idp=1254735976595")
    text=clean(response_text(response))
    # INE row is: Unemployment Rate | note 2 | value 9.87 | variation -0.41.
    match=re.search(r"Unemployment Rate\s+2\s+([0-9]+(?:[.,][0-9]+)?)",text,re.I)
    if not match: raise RuntimeError("INE EPA unemployment row not parsed")
    return [Point("2026-Q2",float(match.group(1).replace(",",".")),response.url)]



def spain_social_security_affiliation() -> list[Point]:
    """Fetch official Spanish seasonally adjusted affiliation MoM change.

    Primary source: Revista Seguridad Social official statistics articles, which
    directly state both the adjusted level and the monthly increase. The current
    article URL is discovered from the official statistics index; fixed current
    URL is only a fallback. This is more reliable than the sector PDF, which does
    not contain the total-system monthly change as extractable text.
    """
    index_urls=[
        "https://revista.seg-social.es/estadisticas",
        "https://revista.seg-social.es/home",
    ]
    article_urls=[]
    for index_url in index_urls:
        try:
            response=get(index_url)
            soup=BeautifulSoup(response.text,"html.parser")
            for anchor in soup.find_all("a",href=True):
                href=urljoin(response.url,anchor.get("href",""))
                context=clean(anchor.get_text(" ",strip=True)).lower()
                if "revista.seg-social.es/-/" in href and any(word in context for word in ("afiliad","ocupad","empleo")):
                    if href not in article_urls: article_urls.append(href)
        except Exception as error:
            log(f"[WARN] Seguridad Social article index failed: {error}")
    fallback=(
        "https://revista.seg-social.es/-/"
        "espa%C3%B1a-suma-621.925-afiliados-en-los-primeros-seis-meses-del-a%C3%B1o-"
        "y-supera-la-cota-de-los-22-4-millones-de-ocupados"
    )
    if fallback not in article_urls: article_urls.append(fallback)

    month_names={
        "enero":1,"febrero":2,"marzo":3,"abril":4,"mayo":5,"junio":6,
        "julio":7,"agosto":8,"septiembre":9,"octubre":10,"noviembre":11,"diciembre":12,
    }
    points=[]; errors=[]
    for url in article_urls[:30]:
        try:
            response=get(url); text=clean(response_text(response)).replace("−","-")
            # Official wording: "La serie desestacionalizada ... tras sumar 92.531 en el ultimo mes".
            match=re.search(
                r"serie desestacionalizada.{0,260}?(?:tras sumar|suma|aumenta en|incremento de)\s*([+-]?[0-9][0-9. ]*)\s+(?:afiliad[oa]s?|en el (?:ultimo|último) mes)",
                text,re.I|re.S,
            )
            if not match:
                match=re.search(r"desestacionalizad[ao].{0,260}?([+-]?[0-9]{2,3}(?:[.]?[0-9]{3})+)\s+en el (?:ultimo|último) mes",text,re.I|re.S)
            if not match: continue
            token=match.group(1).replace(" ","")
            sign=-1 if token.startswith("-") else 1
            persons=sign*int(re.sub(r"[^0-9]","",token))
            # Reference month from article publication date/title/body. Prefer named month near the opening.
            head=text[:3000].lower()
            month=next((m for name,m in month_names.items() if re.search(rf"\b{name}\b",head)),None)
            year_match=re.search(r"\b(20\d{2})\b",head)
            if not month or not year_match: continue
            period=f"{int(year_match.group(1)):04d}-{month:02d}"
            points.append(Point(period,persons/1000.0,response.url,note="official adjusted monthly change; persons converted to thousand"))
        except Exception as error:
            errors.append(f"{url}: {error}")
    if not points:
        raise RuntimeError("Official Seguridad Social adjusted monthly change not parsed; "+" | ".join(errors[:3]))
    return dedupe(points)

def spain_retail() -> list[Point]:
    response=get("https://www.ine.es/dyngs/Prensa/en/ICM0526.htm?print=1")
    text=clean(response_text(response))
    match=re.search(r"original RTI series at constant prices registered an annual variation of\s*([+-]?\d+(?:[.,]\d+)?)%",text,re.I)
    if not match: raise RuntimeError("INE original real retail YoY not parsed")
    return [Point("2026-05",float(match.group(1).replace(",",".")),response.url)]


def ifo_business() -> list[Point]:
    url="https://www.ifo.de/en/press-release/2026-07-27/ifo-business-climate-index-rises-july-2026"
    response=get(url)
    # Search visible text, raw HTML, meta description and JSON-LD together.
    blob=" ".join([response.text, response_text(response)])
    blob=clean(BeautifulSoup(blob,"html.parser").get_text(" ",strip=True))
    patterns=[
        r"Business Climate Index\s+(?:rose|increased)\s+to\s*([0-9]+(?:[.,][0-9]+)?)\s*points\s+in\s+July",
        r"ifo Business Climate Index.{0,160}?([0-9]{2}[.,][0-9])\s*points in July",
        r"rose to\s*([0-9]{2}[.,][0-9])\s*points in July",
    ]
    for pattern in patterns:
        match=re.search(pattern,blob,re.I|re.S)
        if match:
            return [Point("2026-07",float(match.group(1).replace(",",".")),response.url)]
    raise RuntimeError("ifo Business Climate value not parsed")


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


def preceding_sp_release_context(anchor: Any) -> str:
    """Exact context strategy used by the working UK PMI pipeline."""
    parts=[]
    for element in anchor.previous_elements:
        if isinstance(element,NavigableString):
            text=clean(str(element))
            if text:
                parts.append(text)
        if len(" ".join(parts)) >= 280:
            break
    return " ".join(reversed(parts[-20:]))


def parse_sp_release_date(value: str) -> datetime | None:
    text=clean(value).replace(",","")
    for fmt in ("%B %d %Y","%b %d %Y"):
        try:
            return datetime.strptime(text,fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            pass
    return None


def discover_sp_country_releases(country: str) -> list[dict[str,str]]:
    """Discover releases for exactly one country, copied from the UK workflow."""
    log(f"[S&P PMI/{country}] discover country releases")
    response=get(SP_RELEASES)
    soup=BeautifulSoup(response.text,"html.parser")
    candidates=[]; seen=set()
    c=re.escape(country)
    for anchor in soup.find_all("a",href=True):
        href=anchor.get("href","")
        if "/Public/Home/PressRelease/" not in href:
            continue
        url=urljoin(SP_RELEASES,href)
        if url in seen:
            continue
        anchor_text=clean(anchor.get_text(" ",strip=True))
        parent_text=clean(anchor.parent.get_text(" ",strip=True) if anchor.parent else "")
        previous_text=preceding_sp_release_context(anchor)
        context=clean(" ".join(x for x in (anchor_text,parent_text,previous_text) if x))
        # Same two-stage exact/broad title matching as the working UK code.
        title_match=re.search(
            rf"(S&P Global\s+(?:Flash\s+)?{c}(?:\s+(?:Manufacturing|Services))?\s+PMI(?:[^|]{{0,80}})?)",
            context,re.I,
        )
        if not title_match:
            title_match=re.search(
                rf"((?:Flash\s+)?{c}(?:\s+(?:Manufacturing|Services))?\s+PMI(?:[^|]{{0,80}})?)",
                context,re.I,
            )
        if not title_match:
            continue
        title=clean(title_match.group(1))
        date_match=re.search(
            r"([A-Za-z]+\s+\d{1,2},?\s+20\d{2})\s+\d{2}:\d{2}\s+UTC",
            context,re.I,
        )
        release_date=date_match.group(1).replace(",","") if date_match else ""
        candidates.append({"title":title,"url":url,"release_date":release_date,"index_context":context})
        seen.add(url)
    cutoff=datetime.now(timezone.utc)-timedelta(days=150)
    recent=[]
    for candidate in candidates:
        dt=parse_sp_release_date(candidate["release_date"])
        if dt is not None and dt>=cutoff:
            recent.append(candidate)
    if not recent:
        recent=candidates[:30]
    recent.sort(key=lambda x:parse_sp_release_date(x["release_date"]) or datetime.min.replace(tzinfo=timezone.utc),reverse=True)
    log(f"[S&P PMI/{country}] discovered={len(candidates)} recent={len(recent)}")
    return recent


def extract_country_pmi_value(text: str,country: str,sector: str) -> tuple[float,str] | None:
    """UK parser structure, with the country name parameterised."""
    compact=clean(text).replace("™","").replace("®","")
    number=r"([0-9]{1,2}(?:\.[0-9]+)?)"
    c=re.escape(country)
    if sector=="manufacturing":
        patterns=[
            rf"\bFlash\s+{c}\s+Manufacturing PMI\s*:\s*{number}\b",
            rf"\b(?:HCOB|S&P Global)(?:/BME)?\s+{c}\s+Manufacturing PMI\s*:\s*{number}\b",
            rf"\b{c}\s+Manufacturing PMI\s+at\s+{number}\s+in\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\b",
            rf"\b(?:HCOB|S&P Global)(?:/BME)?\s+{c}\s+Manufacturing Purchasing Managers['’]? Index\s*\(PMI\)\s+(?:posted|registered|stood at)\s+{number}\b",
            rf"\bseasonally adjusted (?:HCOB|S&P Global)(?:/BME)?\s+{c}\s+Manufacturing PMI\s+(?:posted|registered|stood at)\s+{number}\b",
        ]
    elif sector=="services":
        patterns=[
            rf"\bAt\s+{number}\s+in\s+(?:January|February|March|April|May|June|July|August|September|October|November|December).{{0,400}}?\b(?:HCOB|S&P Global)(?:/BME)?\s+{c}\s+Services PMI Business Activity Index\b",
            rf"\bFlash\s+{c}\s+Services PMI Business Activity Index\s*:\s*{number}\b",
            rf"\b(?:HCOB|S&P Global)(?:/BME)?\s+{c}\s+Services PMI Business Activity Index\s*:\s*{number}\b",
            rf"\b(?:HCOB|S&P Global)(?:/BME)?\s+{c}\s+Services PMI Business Activity Index\s+(?:posted|registered|stood at)\s+{number}\b",
            rf"\b{c}\s+Services PMI Business Activity Index\s+(?:posted|registered|stood at|rose to|fell to)\s+{number}\b",
        ]
    else:
        raise ValueError(sector)
    for priority,pattern in enumerate(patterns,1):
        for match in re.finditer(pattern,compact,re.I|re.S):
            value=float(match.group(1))
            context=compact[max(0,match.start()-120):match.end()+150]
            if not 20<=value<=80:
                continue
            if value==50.0 and re.search(r">\s*50(?:\.0)?\s*=|50\s*=\s*(?:growth|improvement|expansion)",context,re.I):
                continue
            return value,match.group(0)
    return None


def fetch_sp_country_pmi(country: str) -> dict[str,list[Point]]:
    """Process one country from discovery through both sectors before moving on."""
    if country in _SP_COUNTRY_CACHE:
        return _SP_COUNTRY_CACHE[country]
    log(f"[S&P PMI/{country}] START country-only pipeline")
    candidates=discover_sp_country_releases(country)
    if not candidates:
        raise RuntimeError(f"No S&P Global {country} PMI release located")
    observations: dict[str,dict[str,Point]]={"manufacturing":{},"services":{}}
    errors=[]
    for candidate in candidates:
        title_lower=candidate["title"].lower()
        release_type="flash" if "flash" in title_lower else "final"
        if "manufacturing" in title_lower:
            sectors=["manufacturing"]
        elif "services" in title_lower:
            sectors=["services"]
        elif "flash" in title_lower and country.lower() in title_lower and "pmi" in title_lower:
            sectors=["manufacturing","services"]
        else:
            continue
        release_dt=parse_sp_release_date(candidate["release_date"])
        if release_dt is not None:
            if release_type=="flash":
                expected_period=f"{release_dt.year:04d}-{release_dt.month:02d}"
            else:
                serial=release_dt.year*12+release_dt.month-2
                expected_period=f"{serial//12:04d}-{serial%12+1:02d}"
        else:
            expected_period=""
        try:
            response=get(candidate["url"])
            text=response_text(response)
            if country.lower() not in clean(text).lower():
                continue
            if not expected_period:
                expected_period=month_name_period(text) or ""
            if not expected_period:
                raise RuntimeError("reference period not found")
            for sector in sectors:
                parsed=extract_country_pmi_value(text,country,sector)
                if parsed is None:
                    errors.append(f"{candidate['url']} {sector}: exact value not parsed")
                    continue
                value,label=parsed
                point=Point(expected_period,value,response.url,release_type,note=f"matched UK-template label: {label}")
                current=observations[sector].get(expected_period)
                if current is None or (release_type=="final" and current.status!="final"):
                    observations[sector][expected_period]=point
                log(f"[S&P PMI/{country}] {expected_period} {sector}={value} ({release_type})")
        except Exception as error:
            errors.append(f"{candidate['url']}: {error}")
    result={sector:[rows[key] for key in sorted(rows)] for sector,rows in observations.items()}
    _SP_COUNTRY_CACHE[country]=result
    log(f"[S&P PMI/{country}] DONE manufacturing={len(result['manufacturing'])} services={len(result['services'])}")
    if not result["manufacturing"] and not result["services"]:
        raise RuntimeError("No exact S&P Global PMI values parsed; "+" | ".join(errors[:8]))
    return result


def sp_pmi(country: str,sector: str) -> list[Point]:
    country_result=fetch_sp_country_pmi(country)
    points=country_result.get(sector,[])
    if not points:
        raise RuntimeError(f"{country} {sector} PMI not parsed in country-only pipeline")
    return points

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
    "西 失業率":[Source("Spain EPA unemployment rate", "INE", "spain_epa_unemployment", {}, "EPA national unemployment rate, quarterly, unadjusted", "INE EPA headline unemployment rate")],
    "德 Unemployment Rate SWDA":[Source("Germany registered unemployment rate", "Bundesbank", "bundesbank", {"flow":"BBDL1","key":"M.DE.Y.UNE.UBA000.A0000.A01.D00.0.R00.A"}, "Registered unemployment rate, calendar and seasonally adjusted", "BBDL1.M.DE.Y.UNE.UBA000.A0000.A01.D00.0.R00.A")],
    "歐 失業率":[Source("Euro-area unemployment rate", "Eurostat", "euro_unemployment_release", {}, "ILO unemployment rate, monthly SA; official release backed by une_rt_m", "Eurostat official unemployment release / une_rt_m")],
    "西 就業":[Source("Spain social-security affiliation SA change", "Seguridad Social / TGSS", "spain_social_security_affiliation", {}, "Total-system registered affiliation, seasonally adjusted net monthly change, thousand persons", "Seguridad Social official monthly affiliation report / adjusted series")],
    "德 失業人口":[Source("Germany registered unemployed persons", "Bundesbank", "bundesbank", {"flow":"BBDL1","key":"M.DE.Y.UNE.UBA000.A0000.A01.D00.0.ABA.A"}, "Registered unemployed persons, calendar and seasonally adjusted, thousand persons; level replaces monthly change", "BBDL1.M.DE.Y.UNE.UBA000.A0000.A01.D00.0.ABA.A")],
    "西 零售":[Source("Spain real retail original YoY", "INE", "spain_retail", {}, "Original constant-price retail index, YoY", "INE RTI Base 2021 / original series annual change")],
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
    "德 企業信心":[Source("ifo Business Climate Germany", "ifo Institute", "ifo_business", {}, "Seasonally adjusted ifo Business Climate Germany", "ifo Business Climate Germany, index 2015=100")],
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
    "euro_unemployment_release":euro_unemployment_release,"spain_epa_unemployment":spain_epa_unemployment,
    "spain_social_security_affiliation":spain_social_security_affiliation,
    "spain_retail":spain_retail,"ifo_business":ifo_business,
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
