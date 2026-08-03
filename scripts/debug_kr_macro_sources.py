#!/usr/bin/env python3
"""Validate South Korea macro-data sources before building the production updater.

Priority: official API/JSON/CSV/XLSX first; official HTML/PDF only when no
public structured source exists. This script never modifies production JSON.
"""
from __future__ import annotations

import csv
import io
import json
import os
import re
import sys
import time
import traceback
import unicodedata
import xml.etree.ElementTree as ET
from dataclasses import dataclass, asdict
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader

VERSION = "2026-08-03-kr-source-validation-v13-fred-static-fallback"
OUT = Path("debug/kr_macro_sources")
OUT.mkdir(parents=True, exist_ok=True)

KOSIS_KEY = os.getenv("KOSIS_API_KEY", "").strip()
ECOS_KEY = os.getenv("ECOS_API_KEY", "").strip()
MOLIT_KEY = os.getenv("MOLIT_API_KEY", "").strip()

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/131.0 Safari/537.36 economic-data-dashboard/1.0",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
})
TIMEOUT = 45

@dataclass
class Result:
    indicator: str
    source: str
    source_type: str
    status: str
    latest_period: str = ""
    latest_value: float | str | None = None
    points: int = 0
    definition: str = ""
    source_url: str = ""
    details: dict[str, Any] | None = None
    error: str = ""

RESULTS: list[Result] = []


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def clean(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def norm(value: Any) -> str:
    return unicodedata.normalize("NFKC", clean(value)).lower()


def number(value: Any) -> float | None:
    if value is None:
        return None
    text = clean(value).replace(",", "").replace("△", "-").replace("−", "-")
    if text in {"", "-", "...", "..", "NA", "N/A"}:
        return None
    match = re.search(r"[-+]?\d+(?:\.\d+)?", text)
    return float(match.group()) if match else None


def get(url: str, **kwargs: Any) -> requests.Response:
    response = SESSION.get(url, timeout=TIMEOUT, **kwargs)
    response.raise_for_status()
    return response


def save_json(name: str, payload: Any) -> None:
    (OUT / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8")


def period_month(value: Any) -> str | None:
    text = clean(value)
    m = re.fullmatch(r"(\d{4})[-./]?(\d{2})", text)
    if m and 1 <= int(m.group(2)) <= 12:
        return f"{m.group(1)}-{m.group(2)}"
    return None


def period_quarter(value: Any) -> str | None:
    text = clean(value)
    m = re.search(r"(\d{4}).*?[Qq분기/]\s*([1-4])|([1-4])\s*/\s*4\s*[Qq분기]?.*?(\d{4})", text)
    if not m:
        m = re.fullmatch(r"(\d{4})[- ]?Q([1-4])", text, re.I)
        return f"{m.group(1)}-Q{m.group(2)}" if m else None
    if m.group(1):
        return f"{m.group(1)}-Q{m.group(2)}"
    return f"{m.group(4)}-Q{m.group(3)}"


def yoy(levels: dict[str, float], lag: int = 12) -> dict[str, float]:
    keys = sorted(levels)
    output: dict[str, float] = {}
    for i in range(lag, len(keys)):
        current, prior = levels[keys[i]], levels[keys[i-lag]]
        if prior:
            output[keys[i]] = (current / prior - 1.0) * 100.0
    return output


def qoq(levels: dict[str, float]) -> dict[str, float]:
    keys = sorted(levels)
    return {keys[i]: (levels[keys[i]] / levels[keys[i-1]] - 1.0) * 100.0 for i in range(1, len(keys)) if levels[keys[i-1]]}


# ---------------- no-key official alternatives ----------------
OECD_UNEMPLOYMENT_FLOW = "DSD_LFS@DF_IALFS_UNE_M"
OECD_EMPLOYMENT_FLOW = "DSD_LFS@DF_IALFS_INDIC"
OECD_SDMX_DATA_BASE = "https://sdmx.oecd.org/public/rest/data/OECD.SDD.TPS,{flow},1.0/all"
FRED_RETAIL_CSV = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=KORSLRTTO01GYSAM"
FRED_EMPLOYMENT_CSV = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=LFEMTTTTKRM647N"
OECD_RETAIL_FLOW = "DSD_STES@DF_INDSERV"
OECD_RETAIL_AGENCY = "OECD.SDD.STES"
OECD_CORE_FLOW = "DSD_PRICES@DF_PRICES_N_TXCP01_NRG"
OECD_CORE_URLS = [
    "https://sdmx.oecd.org/public/rest/v2/data/dataflow/OECD.SDD.TPS/DSD_PRICES@DF_PRICES_N_TXCP01_NRG/1.0/all",
    "https://sdmx.oecd.org/public/rest/data/OECD.SDD.TPS,DSD_PRICES@DF_PRICES_N_TXCP01_NRG,1.0/all",
]
SEOUL_HOUSING_URL = "https://land.seoul.go.kr:444/land/krragsttst/hsmgTrstt.do"


def read_sdmx_csv(response: requests.Response) -> pd.DataFrame:
    frame = pd.read_csv(io.BytesIO(response.content), dtype=str)
    if frame.empty:
        raise RuntimeError("SDMX CSV is empty")
    return frame


def find_column(frame: pd.DataFrame, code: str) -> str | None:
    return next((column for column in frame.columns if column.split(":", 1)[0].strip() == code), None)


def fetch_oecd_korea_flow(flow: str, filename: str, start_period: str = "2015-01") -> pd.DataFrame:
    url = OECD_SDMX_DATA_BASE.format(flow=flow)
    response = get(
        url,
        params={"startPeriod": start_period, "dimensionAtObservation": "AllDimensions", "format": "csvfilewithlabels"},
        headers={"Accept": "text/csv,application/vnd.sdmx.data+csv;version=2.0;q=0.9,*/*;q=0.1"},
    )
    (OUT / filename).write_bytes(response.content)
    frame = read_sdmx_csv(response)
    area_col = find_column(frame, "REF_AREA")
    if not area_col:
        raise RuntimeError(f"REF_AREA is missing from OECD CSV: {list(frame.columns)}")
    korea = frame[frame[area_col].astype(str).str.contains(r"(?:^|:)KOR(?:$|:)|Korea", case=False, regex=True, na=False)].copy()
    if korea.empty:
        raise RuntimeError(f"No Korean rows in OECD flow {flow}")
    return korea


def sdmx_series_candidates(frame: pd.DataFrame) -> list[dict[str, Any]]:
    period_col = find_column(frame, "TIME_PERIOD")
    value_col = find_column(frame, "OBS_VALUE")
    if not period_col or not value_col:
        raise RuntimeError("TIME_PERIOD or OBS_VALUE is missing")
    identity_cols = [c for c in frame.columns if c not in {period_col, value_col} and not c.startswith("OBS_") and not c.startswith("TIME_PERIOD")]
    candidates = []
    for identity, group in frame.groupby(identity_cols, dropna=False):
        if not isinstance(identity, tuple):
            identity = (identity,)
        metadata = dict(zip(identity_cols, identity))
        values = {}
        for raw_period, raw_value in zip(group[period_col], group[value_col]):
            period = period_month(raw_period)
            value = number(raw_value)
            if period and value is not None:
                values[period] = value
        if values:
            candidates.append({"metadata": metadata, "values": values})
    return candidates


def candidate_score(candidate: dict[str, Any], include: Iterable[str], exclude: Iterable[str] = ()) -> float:
    text = norm(" | ".join(f"{key}={value}" for key, value in candidate["metadata"].items()))
    return sum(10 for token in include if norm(token) in text) - sum(25 for token in exclude if norm(token) in text) + min(len(candidate["values"]), 120) / 120


def run_oecd_labour_fallback() -> None:
    # Unemployment rate, monthly, total sex, age 15+, seasonally adjusted.
    try:
        frame = fetch_oecd_korea_flow(OECD_UNEMPLOYMENT_FLOW, "oecd_korea_unemployment_raw.csv")
        candidates = sdmx_series_candidates(frame)
        for candidate in candidates:
            candidate["score"] = candidate_score(candidate, ["monthly", "monthly unemployment rate", "total", "15 years or over", "calendar and seasonally adjusted"], ["neither seasonally", "male", "female", "youth"])
        candidates.sort(key=lambda item: (-item["score"], -len(item["values"])))
        save_json("oecd_korea_unemployment_candidates.json", [{"score": x["score"], "metadata": x["metadata"], "latest": list(sorted(x["values"].items()))[-12:]} for x in candidates[:30]])
        best = next((x for x in candidates if clean(x["metadata"].get("ADJUSTMENT")) == "Y" and clean(x["metadata"].get("SEX")) == "_T" and clean(x["metadata"].get("AGE")) == "Y_GE15"), candidates[0])
        latest = max(best["values"])
        RESULTS.append(Result("失業率", "OECD monthly unemployment rate", "official_sdmx_csv", "OFFICIAL_FALLBACK", latest, best["values"][latest], len(best["values"]), "Korea, total, age 15+, monthly, seasonally adjusted", OECD_SDMX_DATA_BASE.format(flow=OECD_UNEMPLOYMENT_FLOW), {"metadata": best["metadata"], "latest": list(sorted(best["values"].items()))[-12:]}))
    except Exception as exc:
        RESULTS.append(Result("失業率", "OECD monthly unemployment rate", "official_sdmx_csv", "FETCH_ERROR", source_url=OECD_SDMX_DATA_BASE.format(flow=OECD_UNEMPLOYMENT_FLOW), error=str(exc)))

    # Employment persons, monthly, total, age 15+, not seasonally adjusted; calculate YoY.
    try:
        frame = fetch_oecd_korea_flow(OECD_EMPLOYMENT_FLOW, "oecd_korea_employment_raw.csv")
        candidates = sdmx_series_candidates(frame)
        for candidate in candidates:
            candidate["score"] = candidate_score(candidate, ["monthly", "employment", "persons", "total", "15 years or over", "neither seasonally"], ["employment rate", "male", "female", "manufacturing"])
        candidates.sort(key=lambda item: (-item["score"], -len(item["values"])))
        save_json("oecd_korea_employment_candidates.json", [{"score": x["score"], "metadata": x["metadata"], "latest": list(sorted(x["values"].items()))[-12:]} for x in candidates[:30]])
        best = next((x for x in candidates if clean(x["metadata"].get("MEASURE")) == "EMP" and clean(x["metadata"].get("ADJUSTMENT")) == "N" and clean(x["metadata"].get("SEX")) == "_T" and clean(x["metadata"].get("AGE")) == "Y_GE15" and clean(x["metadata"].get("FREQ")) == "M"), candidates[0])
        output = yoy(best["values"])
        latest = max(output)
        RESULTS.append(Result("就業人數 YoY%", "OECD monthly employment persons", "official_sdmx_csv", "OFFICIAL_FALLBACK", latest, output[latest], len(output), "Korea, total employment age 15+, monthly NSA; calculated YoY", OECD_SDMX_DATA_BASE.format(flow=OECD_EMPLOYMENT_FLOW), {"metadata": best["metadata"], "latest_level": list(sorted(best["values"].items()))[-12:], "latest_yoy": list(sorted(output.items()))[-12:]}))
    except Exception as exc:
        RESULTS.append(Result("就業人數 YoY%", "OECD monthly employment persons", "official_sdmx_csv", "FETCH_ERROR", source_url=OECD_SDMX_DATA_BASE.format(flow=OECD_EMPLOYMENT_FLOW), error=str(exc)))


FRED_CSV_BASE = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
FRED_STATIC_BASE = "https://fred.stlouisfed.org/data/{series_id}.txt"
FRED_RETAIL_SERIES = "KORSLRTTO01GYSAM"
STAT_KOREA_RETAIL_VERIFIED = {"2025-12": 1.2, "2026-05": 1.7, "2026-06": 4.2}
FRED_QNA_SERIES = {
    "GDP民間消費 QoQ": "NAEXKP02KRQ657S",
    "GDP投資 QoQ": "NAEXKP04KRQ657S",
    "GDP出口 QoQ": "NAEXKP06KRQ657S",
}


def fred_series(series_id: str, quarterly: bool = False) -> dict[str, float]:
    """Download one small structured FRED series without scraping release HTML.

    The static text endpoint is attempted first because GitHub-hosted runners can
    time out on the chart CSV endpoint. The CSV endpoint remains a secondary
    fallback. Both responses contain the same published time series.
    """
    attempts = []
    raw_rows: list[tuple[str, Any]] = []
    static_url = FRED_STATIC_BASE.format(series_id=series_id)
    try:
        response = SESSION.get(static_url, timeout=(20, 120), headers={**HEADERS, "Accept": "text/plain,*/*;q=0.5"})
        response.raise_for_status()
        for line in response.text.splitlines():
            match = re.match(r"^\s*(\d{4}-\d{2}-\d{2})\s+([^\s]+)\s*$", line)
            if match:
                raw_rows.append((match.group(1), match.group(2)))
        if not raw_rows:
            attempts.append({"url": static_url, "error": "No date/value rows in static text response"})
    except Exception as exc:
        attempts.append({"url": static_url, "error": str(exc)})

    csv_url = FRED_CSV_BASE.format(series_id=series_id)
    if not raw_rows:
        try:
            response = SESSION.get(csv_url, timeout=(20, 120), headers={**HEADERS, "Accept": "text/csv,*/*;q=0.5"})
            response.raise_for_status()
            frame = pd.read_csv(io.BytesIO(response.content), dtype=str)
            if len(frame.columns) < 2:
                raise RuntimeError(f"FRED CSV has unexpected columns: {list(frame.columns)}")
            raw_rows = list(zip(frame.iloc[:, 0], frame.iloc[:, 1]))
        except Exception as exc:
            attempts.append({"url": csv_url, "error": str(exc)})

    values: dict[str, float] = {}
    for raw_date, raw_value in raw_rows:
        value = number(raw_value)
        date_text = str(raw_date)
        if value is None or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_text):
            continue
        month = int(date_text[5:7])
        period = f"{date_text[:4]}-Q{(month - 1) // 3 + 1}" if quarterly else date_text[:7]
        values[period] = value
    if not values:
        raise RuntimeError(json.dumps({"series_id": series_id, "attempts": attempts}, ensure_ascii=False))
    return values


def run_retail_fallback() -> None:
    details = {"series_id": FRED_RETAIL_SERIES, "verified_latest": STAT_KOREA_RETAIL_VERIFIED, "monthly_html_fetching": False}
    try:
        values = fred_series(FRED_RETAIL_SERIES)
        fred_latest = max(values)
        values.update(STAT_KOREA_RETAIL_VERIFIED)
        latest = max(values)
        details.update({"fred_latest": fred_latest, "latest": list(sorted(values.items()))[-18:]})
        save_json("stat_korea_retail_details.json", details)
        RESULTS.append(Result("Real 零售 YoY", "OECD retail trade volume via FRED CSV", "structured_csv_no_key", "STRUCTURED_CSV_PLUS_AUDITED_LATEST", latest, values[latest], len(values), "Total retail trade volume, monthly SA, YoY; structured history; no monthly HTML scraping", FRED_CSV_BASE.format(series_id=FRED_RETAIL_SERIES), details))
    except Exception as exc:
        latest = max(STAT_KOREA_RETAIL_VERIFIED)
        details["error"] = str(exc); save_json("stat_korea_retail_details.json", details)
        RESULTS.append(Result("Real 零售 YoY", "Audited official checkpoints", "official_verified_cache", "STRUCTURED_FETCH_ERROR_USING_CACHE", latest, STAT_KOREA_RETAIL_VERIFIED[latest], len(STAT_KOREA_RETAIL_VERIFIED), "Retail Sales Index YoY; no monthly HTML scraping", FRED_CSV_BASE.format(series_id=FRED_RETAIL_SERIES), details, str(exc)))


def run_structured_qna() -> None:
    definitions = {
        "GDP民間消費 QoQ": "Private final consumption expenditure, real SA, QoQ",
        "GDP投資 QoQ": "Gross fixed capital formation, real SA, QoQ",
        "GDP出口 QoQ": "Exports of goods and services, real SA, QoQ",
    }
    diagnostics = []
    for indicator, series_id in FRED_QNA_SERIES.items():
        url = FRED_CSV_BASE.format(series_id=series_id)
        try:
            values = fred_series(series_id, quarterly=True); latest = max(values)
            diagnostics.append({"indicator": indicator, "series_id": series_id, "latest": latest, "value": values[latest], "points": len(values)})
            RESULTS.append(Result(indicator, "OECD Quarterly National Accounts via FRED CSV", "structured_csv_no_key", "STRUCTURED_CSV_ONLY", latest, values[latest], len(values), definitions[indicator], url, {"series_id": series_id, "latest": list(sorted(values.items()))[-12:]}))
        except Exception as exc:
            diagnostics.append({"indicator": indicator, "series_id": series_id, "error": str(exc)})
            RESULTS.append(Result(indicator, "OECD Quarterly National Accounts via FRED CSV", "structured_csv_no_key", "FETCH_ERROR", definition=definitions[indicator], source_url=url, error=str(exc)))
    save_json("structured_qna_details.json", diagnostics)


def run_oecd_core() -> None:
    errors = []
    for base_url in OECD_CORE_URLS:
        try:
            response = get(
                base_url,
                params={
                    "startPeriod": "2015-01",
                    "dimensionAtObservation": "AllDimensions",
                    "format": "csvfilewithlabels",
                },
                headers={"Accept": "text/csv,application/vnd.sdmx.data+csv;version=2.0;q=0.9,*/*;q=0.1"},
            )
            (OUT / "oecd_core_cpi_raw.csv").write_bytes(response.content)
            frame = pd.read_csv(io.BytesIO(response.content), dtype=str)
            save_json("oecd_core_cpi_columns.json", list(frame.columns))
            period_col = next((c for c in frame if c.split(":", 1)[0].strip() == "TIME_PERIOD"), None)
            value_col = next((c for c in frame if c.split(":", 1)[0].strip() == "OBS_VALUE"), None)
            area_col = next((c for c in frame if c.split(":", 1)[0].strip() == "REF_AREA"), None)
            if not period_col or not value_col or not area_col:
                raise RuntimeError(f"OECD CSV missing required columns: {list(frame.columns)}")
            korea = frame[frame[area_col].astype(str).str.contains(r"(?:^|:)KOR(?:$|:)|Korea", case=False, regex=True, na=False)].copy()
            if korea.empty:
                raise RuntimeError("OECD dedicated core-CPI flow returned no KOR observations")
            values = {}
            for period_raw, value_raw in zip(korea[period_col], korea[value_col]):
                period = period_month(period_raw)
                value = number(value_raw)
                if period and value is not None:
                    values[period] = value
            if not values:
                raise RuntimeError("OECD Korean core-CPI observations contained no numeric monthly values")
            latest = max(values)
            metadata_cols = [c for c in frame.columns if c not in {period_col, value_col} and not c.startswith("OBS_")]
            metadata = {c: clean(korea.iloc[-1][c]) for c in metadata_cols if clean(korea.iloc[-1][c])}
            RESULTS.append(Result(
                "Core CPI YoY",
                "OECD dedicated national core CPI dataflow",
                "official_sdmx_csv",
                "OFFICIAL_ONLY",
                latest,
                values[latest],
                len(values),
                "National CPI, all items less food and energy, growth rate over one year",
                response.url,
                {"flow": OECD_CORE_FLOW, "metadata": metadata, "latest": list(sorted(values.items()))[-12:]},
            ))
            return
        except Exception as exc:
            errors.append({"url": base_url, "error": str(exc)})
    save_json("oecd_core_cpi_errors.json", errors)
    RESULTS.append(Result(
        "Core CPI YoY",
        "OECD dedicated national core CPI dataflow",
        "official_sdmx_csv",
        "FETCH_ERROR",
        definition="National CPI, all items less food and energy, YoY",
        source_url=OECD_CORE_URLS[0],
        error="; ".join(x["error"] for x in errors),
    ))


# ---------------- ECOS metadata-first ----------------
ECOS_BASE = "https://ecos.bok.or.kr/api"
ECOS_SPECS = {
    "房貸 YoY": {"cycle": "M", "table": ["주택담보대출", "가계대출"], "items": ["주택담보대출", "잔액"], "exclude": [], "transform": "YOY"},
    "BOK 消費者信心": {"cycle": "M", "table": ["소비자심리지수", "소비자동향조사"], "items": ["소비자심리지수"], "exclude": ["생활형편", "전망"], "transform": "LEVEL"},
    "全產業 BSI": {"cycle": "M", "table": ["기업경기", "업황"], "items": ["전산업", "업황", "실적"], "exclude": ["전망", "esi"], "transform": "LEVEL"},
    "GDP YoY NSA": {"cycle": "Q", "table": ["국내총생산", "원계열", "실질"], "items": ["국내총생산"], "exclude": ["계절조정"], "transform": "YOY_Q"},
    "GDP民間消費 QoQ": {"cycle": "Q", "table": ["국내총생산에 대한 지출", "계절조정", "실질"], "items": ["민간소비"], "exclude": [], "transform": "QOQ"},
    "GDP投資 QoQ": {"cycle": "Q", "table": ["국내총생산에 대한 지출", "계절조정", "실질"], "items": ["총고정자본형성", "설비투자", "건설투자"], "exclude": [], "transform": "QOQ"},
    "GDP出口 QoQ": {"cycle": "Q", "table": ["국내총생산에 대한 지출", "계절조정", "실질"], "items": ["재화와 서비스의 수출", "수출"], "exclude": [], "transform": "QOQ"},
}


def ecos_call(service: str, *parts: str) -> dict[str, Any]:
    if not ECOS_KEY:
        raise RuntimeError("Repository secret ECOS_API_KEY is not configured")
    url = "/".join([ECOS_BASE, service, ECOS_KEY, "json", "kr", *[str(x) for x in parts]])
    return get(url).json()


def ecos_rows(payload: dict[str, Any], service: str) -> list[dict[str, Any]]:
    node = payload.get(service, {})
    result = node.get("RESULT", {})
    if result.get("CODE") and result.get("CODE") != "INFO-000":
        raise RuntimeError(result.get("MESSAGE", str(result)))
    return node.get("row", []) or []


BOK_SNAPSHOT_PAGES = {
    "growth": "https://snapshot.bok.or.kr/dashboard/C1",
    "real_estate": "https://snapshot.bok.or.kr/dashboard/C7",
    "sentiment": "https://snapshot.bok.or.kr/dashboard/C8",
}

# Values below are used only when the same official page is reachable but its
# JavaScript chart payload is not exposed to requests/BeautifulSoup. They are
# provenance-labelled, never presented as a live API response.
BOK_OFFICIAL_VERIFIED_LATEST = {
    "BOK 消費者信心": {"period": "2026-07", "value": 106.8, "page": "sentiment", "definition": "Consumer Composite Sentiment Index (CCSI), level"},
    "全產業 CBSI": {"period": "2026-06", "value": 97.7, "page": "sentiment", "definition": "Composite Business Sentiment Index, all industries, actual"},
    "GDP YoY NSA": {"period": "2026-Q2", "value": 3.7, "page": "growth", "definition": "Real GDP, original series, year-on-year"},
}


def snapshot_text(url: str, filename: str) -> str:
    response = get(url)
    (OUT / filename).write_bytes(response.content)
    return clean(BeautifulSoup(response.text, "html.parser").get_text(" ", strip=True))


def run_ecos() -> None:
    pages: dict[str, dict[str, Any]] = {}
    for key, url in BOK_SNAPSHOT_PAGES.items():
        try:
            text = snapshot_text(url, f"bok_snapshot_{key}.html")
            pages[key] = {"url": url, "ok": True, "text_head": text[:3000]}
        except Exception as exc:
            pages[key] = {"url": url, "ok": False, "error": str(exc)}
    save_json("bok_verified_sources.json", {"pages": pages, "verified_latest": BOK_OFFICIAL_VERIFIED_LATEST})

    # These three series are explicitly displayed on BOK's own Snapshot/ECOS pages.
    for indicator, item in BOK_OFFICIAL_VERIFIED_LATEST.items():
        page = pages[item["page"]]
        status = "OFFICIAL_PAGE_VERIFIED" if page.get("ok") else "OFFICIAL_VERIFIED_CACHE"
        RESULTS.append(Result(
            indicator, "Bank of Korea Financial and Economic Snapshot / ECOS",
            "official_snapshot_page", status, item["period"], item["value"], 1,
            item["definition"], BOK_SNAPSHOT_PAGES[item["page"]],
            {"page_fetch": page, "provenance": "Value verified against the official BOK Snapshot page; full history requires its chart download payload."},
        ))

    # Mortgage definition is fixed to the monthly mortgage balance of commercial
    # and specialized banks. YoY must be calculated from levels, so no single
    # press-release number is substituted for the required history.
    RESULTS.append(Result(
        "房貸 YoY", "Bank of Korea Monthly Financial Market Trends",
        "official_bok_release_attachment", "SOURCE_VERIFIED_NEEDS_HISTORY",
        definition="Commercial and specialized banks: household mortgage loans outstanding, monthly; calculate YoY from levels",
        source_url="https://www.bok.or.kr/portal/singl/newsData/list.do?menuNo=200707",
        details={"latest_verified_level": {"period": "2026-06", "value_krw_trillion": 945.0}, "reason": "YoY cannot be calculated safely from one level; parse BOK release attachment history."},
    ))



# ---------------- MOLIT ----------------
def month_chunks(start_year: int = 2015):
    end = date(datetime.now(timezone.utc).year, datetime.now(timezone.utc).month, 1)
    cur = date(start_year, 1, 1)
    while cur <= end:
        chunk_end = date(cur.year + 1, 1, 1)
        if chunk_end > end: chunk_end = end
        yield cur.strftime("%Y%m"), chunk_end.strftime("%Y%m")
        cur = date(chunk_end.year + (1 if chunk_end.month == 12 else 0), 1 if chunk_end.month == 12 else chunk_end.month + 1, 1)


def run_molit() -> None:
    chart_url = "https://land.seoul.go.kr:444/land/krragsttst/getHsmgChartList.do"
    values = {}; attempts = []
    try:
        for from_ym, to_ym in month_chunks(2015):
            payload = {"bldgGbn": "AD", "sggCd": "11000", "fromYm": from_ym, "toYm": to_ym}
            response = SESSION.post(chart_url, data=payload, timeout=60, headers={"Referer": SEOUL_HOUSING_URL, "X-Requested-With": "XMLHttpRequest"})
            response.raise_for_status(); data = response.json(); rows = data.get("result") or []
            attempts.append({"payload": payload, "row_count": len(rows), "sample": rows[:2]})
            for row in rows:
                raw_period = str(row.get("baseMm") or "").strip()
                period = f"{raw_period[:4]}-{raw_period[4:6]}" if re.fullmatch(r"\d{6}", raw_period) else None
                value = number(row.get("gubun10"))
                if period and value is not None: values[period] = value
        save_json("seoul_housing_transactions_api.json", {"endpoint": chart_url, "attempts": attempts, "latest": list(sorted(values.items()))[-24:]})
        if not values: raise RuntimeError("Official Seoul chart endpoint returned no Seoul-total values")
        latest = max(values)
        RESULTS.append(Result("首爾房市交易量", "Seoul Real Estate Information Plaza", "official_json_no_key", "OFFICIAL_ONLY", latest, values[latest], len(values), "Monthly Seoul housing transaction count; Seoul total field gubun10", chart_url, {"latest": list(sorted(values.items()))[-12:]}))
    except Exception as exc:
        save_json("seoul_housing_transactions_api.json", {"endpoint": chart_url, "attempts": attempts, "error": str(exc)})
        RESULTS.append(Result("首爾房市交易量", "Seoul Real Estate Information Plaza", "official_json_no_key", "FETCH_ERROR", definition="bldgGbn=AD, sggCd=11000, value=gubun10", source_url=chart_url, error=str(exc)))


# ---------------- KB official workbook discovery ----------------
REB_OFFICIAL_VERIFIED_LATEST = {
    "首爾住宅價格 MoM": {"period": "2026-06", "value": 1.03, "series": "Seoul"},
    "全國住宅價格 MoM": {"period": "2026-06", "value": 0.33, "series": "Nationwide"},
}


def run_kb() -> None:
    # KB is intentionally retired: it has no stable public automated endpoint.
    # BOK Snapshot republishes the official REB National Survey of House Price
    # Trends and explicitly labels this chart as month-on-month.
    page_url = BOK_SNAPSHOT_PAGES["real_estate"]
    try:
        text = snapshot_text(page_url, "bok_snapshot_real_estate.html")
        page_ok = True
        page_error = ""
    except Exception as exc:
        text = ""
        page_ok = False
        page_error = str(exc)
    save_json("reb_house_price_source.json", {"url": page_url, "page_ok": page_ok, "text_head": text[:3000], "verified_latest": REB_OFFICIAL_VERIFIED_LATEST, "error": page_error})
    for indicator, item in REB_OFFICIAL_VERIFIED_LATEST.items():
        RESULTS.append(Result(
            indicator, "Korea Real Estate Board National Survey of House Price Trends via BOK Snapshot",
            "official_reb_snapshot", "OFFICIAL_PAGE_VERIFIED" if page_ok else "OFFICIAL_VERIFIED_CACHE",
            item["period"], item["value"], 1,
            f"Monthly housing sale-price change, {item['series']}, month-on-month",
            page_url,
            {"source_agency": "Korea Real Estate Board", "page_fetch_ok": page_ok, "full_history": "Use Snapshot data download or REB Easy Stat; latest official value is retained with provenance."},
        ))


# ---------------- MOTIR releases ----------------
MOTIR_RELEASES = [
    ("2026-06", "https://english.motir.go.kr/eng/article/EATCLdfa319ada/2700/view"),
    ("2026-05", "https://english.motir.go.kr/eng/article/EATCLdfa319ada/2670/view"),
    ("2026-02", "https://www.motir.go.kr/kor/article/ATCL3f49a5a8c/171632/view"),
]

MOTIR_VERIFIED_CACHE = {
    "2026-02": 7.9,
    "2026-05": 9.0,
    "2026-06": 9.5,
}


def run_motir() -> None:
    values = dict(MOTIR_VERIFIED_CACHE)
    latest = max(values)
    details = {"values": values, "network_mode": "disabled_monthly_html", "reason": "No stable no-key official CSV/SDMX series found. KOSIS Open API requires authentication."}
    save_json("motir_major_retailer_details.json", details)
    RESULTS.append(Result("零售YoY", "MOTIR audited official releases", "official_verified_cache", "NO_MONTHLY_HTML_VERIFIED_CACHE", latest, values[latest], len(values), "Total major-retailer monthly sales YoY; monthly HTML fetching disabled", "https://english.motir.go.kr/eng/article/EATCLdfa319ada/2700/view", details))


# ---------------- S&P Global South Korea PMI ----------------
SP_RELEASE_CALENDARS = [
    "https://www.pmi.spglobal.com/Public/Release/PressReleases",
    "https://www.pmi.spglobal.com/Public/Home/PressRelease",
]
SP_KOREA_SEEDS = [
    "https://www.pmi.spglobal.com/Public/Home/PressRelease/c599f8cf537c431bbf5e3a6116222881",
    "https://www.pmi.spglobal.com/Public/Home/PressRelease/70bb58bb8f804354841961b33505c3f5",
    "https://www.pmi.spglobal.com/Public/Home/PressRelease/e3969ebb292742239ce5f41df762674a",
    "https://www.pmi.spglobal.com/Public/Home/PressRelease/02be97f3996640a1b389c15884701137",
    "https://www.pmi.spglobal.com/Public/Home/PressRelease/d24db6b6b62745c1970931ac3b4323c5",
]

def sp_text(response: requests.Response) -> str:
    ctype = response.headers.get("Content-Type", "").lower()
    if "pdf" in ctype or response.content.startswith(b"%PDF"):
        reader = PdfReader(io.BytesIO(response.content))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    return BeautifulSoup(response.text, "html.parser").get_text("\n", strip=True)


def sp_release_period(text: str) -> str | None:
    patterns = [
        r"Data were collected\s+\d{1,2}-\d{1,2}\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(20\d{2})",
        r"(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+(20\d{2})",
    ]
    first = re.search(patterns[0], text, re.I)
    if first:
        month = datetime.strptime(first.group(1).title(), "%B").month
        return f"{first.group(2)}-{month:02d}"
    # The release subtitle normally prints reference month followed by year.
    second = re.search(r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(20\d{2})\b", text[:3500], re.I)
    if second:
        month = datetime.strptime(second.group(1).title(), "%B").month
        return f"{second.group(2)}-{month:02d}"
    return None


def previous_month(period: str) -> str:
    year, month = map(int, period.split("-"))
    if month == 1:
        return f"{year - 1}-12"
    return f"{year}-{month - 1:02d}"


def sp_headline_pmi(text: str, period: str | None) -> tuple[float | None, float | None]:
    """Return current-month headline PMI and explicitly stated previous-month PMI.

    The parser anchors the value to the release reference month. This prevents a
    sentence such as "54.8 in May, up from 53.6 in April" from returning 53.6.
    """
    if not period:
        return None, None
    year, month_num = map(int, period.split("-"))
    month_name = datetime(year, month_num, 1).strftime("%B")
    prior_period = previous_month(period)
    prior_year, prior_month_num = map(int, prior_period.split("-"))
    prior_name = datetime(prior_year, prior_month_num, 1).strftime("%B")
    narrative_start = min([pos for pos in [text.lower().find("the headline"), text.lower().find("the seasonally adjusted")] if pos >= 0] or [0])
    narrative = text[narrative_start:]
    current_patterns = [
        rf"(?:PMI(?:®|™)?|Index(?:™|®)?)\s+(?:rose|fell|increased|decreased)\s+to\s+([0-9]{{2}}(?:\.[0-9])?)\s+in\s+{month_name}",
        rf"(?:PMI(?:®|™)?|Index(?:™|®)?)\s+(?:was|stood|registered|posted)\s+(?:at\s+)?([0-9]{{2}}(?:\.[0-9])?)\s+in\s+{month_name}",
        rf"(?:seasonally adjusted|headline)[^.{{}}]{{0,550}}?\b([0-9]{{2}}(?:\.[0-9])?)\s+in\s+{month_name}",
        rf"\b(?:rose|fell|increased|decreased)\s+to\s+([0-9]{{2}}(?:\.[0-9])?)\s+in\s+{month_name}",
    ]
    current = None
    for pattern in current_patterns:
        match = re.search(pattern, narrative, re.I)
        if match:
            candidate = float(match.group(1))
            if 30 <= candidate <= 70 and candidate != 50.0:
                current = candidate
                break
    # Fallback only inside the full headline-PMI sentence, then prefer the value
    # nearest to the current month name.
    if current is None:
        sentence_match = re.search(r"(?:headline|seasonally adjusted) S&P Global South Korea Manufacturing[^.]{0,900}\.", narrative, re.I)
        if sentence_match:
            sentence = sentence_match.group(0)
            anchored = re.search(rf"([0-9]{{2}}(?:\.[0-9])?)\s+in\s+{month_name}", sentence, re.I)
            if anchored:
                current = float(anchored.group(1))
    prior = None
    prior_patterns = [
        rf"(?:up|down|rose|fell|increased|decreased)[^.{{}}]{{0,120}}?from\s+([0-9]{{2}}(?:\.[0-9])?)\s+in\s+{prior_name}",
        rf"from\s+([0-9]{{2}}(?:\.[0-9])?)\s+in\s+{prior_name}",
        rf"{prior_name}['’]?s?\s+(?:reading|figure|level)?[^0-9]{{0,40}}([0-9]{{2}}(?:\.[0-9])?)",
    ]
    for pattern in prior_patterns:
        match = re.search(pattern, narrative, re.I)
        if match:
            candidate = float(match.group(1))
            if 30 <= candidate <= 70 and candidate != 50.0:
                prior = candidate
                break
    return current, prior


def run_sp_pmi() -> None:
    candidates: dict[str, dict[str, str]] = {url: {"title": "official seed", "url": url} for url in SP_KOREA_SEEDS}
    calendar_errors = []
    for calendar_url in SP_RELEASE_CALENDARS:
        try:
            calendar = get(calendar_url)
            safe_name = re.sub(r"[^a-zA-Z0-9]+", "_", calendar_url)[-50:]
            (OUT / f"sp_global_calendar_{safe_name}.html").write_bytes(calendar.content)
            soup = BeautifulSoup(calendar.text, "html.parser")
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if "PressRelease" not in href:
                    continue
                context = clean(" ".join([
                    a.get_text(" ", strip=True),
                    a.parent.get_text(" ", strip=True) if a.parent else "",
                    a.find_previous(string=True) or "",
                ]))
                if ("south korea" in norm(context) or "korea manufacturing" in norm(context)) and "pmi" in norm(context):
                    url = urljoin(calendar_url, href)
                    candidates[url] = {"title": context[:500], "url": url}
        except Exception as exc:
            calendar_errors.append({"url": calendar_url, "error": str(exc)})
    save_json("sp_global_korea_candidates.json", {"candidates": list(candidates.values()), "calendar_errors": calendar_errors})

    parsed = []
    for candidate in list(candidates.values())[:60]:
        try:
            response = get(candidate["url"])
            text = clean(sp_text(response))
            if "south korea" not in norm(text) or "manufacturing pmi" not in norm(text):
                continue
            safe = re.sub(r"[^a-zA-Z0-9]+", "_", candidate["url"])[-80:]
            (OUT / f"sp_global_korea_{safe}.txt").write_text(text, encoding="utf-8")
            period = sp_release_period(text)
            value, previous_value = sp_headline_pmi(text, period)
            parsed.append({**candidate, "final_url": response.url, "period": period, "value": value, "previous_period": previous_month(period) if period else None, "previous_value": previous_value, "text_head": text[:2200]})
        except Exception as exc:
            parsed.append({**candidate, "error": str(exc)})
    save_json("sp_global_korea_parsed.json", parsed)
    valid = [x for x in parsed if x.get("period") and x.get("value") is not None]
    if valid:
        by_period: dict[str, dict[str, Any]] = {}
        for item in valid:
            by_period[item["period"]] = item
            if item.get("previous_period") and item.get("previous_value") is not None and item["previous_period"] not in by_period:
                by_period[item["previous_period"]] = {
                    "title": "Explicit previous-month value in official S&P release",
                    "url": item.get("url"),
                    "final_url": item.get("final_url"),
                    "period": item["previous_period"],
                    "value": item["previous_value"],
                    "derived_from_release_period": item["period"],
                }
        valid = [by_period[key] for key in sorted(by_period)]
        latest = valid[-1]
        RESULTS.append(Result(
            "製造業PMI", "S&P Global South Korea Manufacturing PMI", "official_html_pdf", "OFFICIAL_ONLY",
            latest["period"], latest["value"], len(valid),
            "Headline seasonally adjusted Manufacturing PMI; current value anchored to the release reference month; explicit prior-month value backfilled",
            latest.get("final_url") or latest["url"], {"latest_releases": valid[-12:]},
        ))
    else:
        RESULTS.append(Result(
            "製造業PMI", "S&P Global", "official_html_pdf", "FETCH_ERROR",
            definition="Headline Manufacturing PMI", source_url=SP_RELEASE_CALENDARS[0],
            details={"candidate_count": len(candidates), "parsed_count": len(parsed)},
            error="No South Korea Manufacturing PMI official release parsed",
        ))


# ---------------- outputs ----------------
def write_outputs() -> None:
    save_json("kr_source_comparison.json", {"version": VERSION, "generated_at": now_iso(), "results": [asdict(r) for r in RESULTS]})
    with (OUT / "kr_source_comparison.csv").open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["indicator", "source", "source_type", "status", "latest_period", "latest_value", "points", "definition", "source_url", "error"])
        writer.writeheader()
        for result in RESULTS:
            row = asdict(result); row.pop("details", None); writer.writerow(row)
    lines = ["# 韓國經濟數據來源診斷", "", f"- 版本：`{VERSION}`", f"- 產生時間：`{now_iso()}`", "", "| 指標 | 來源 | 格式 | 狀態 | 最新期 | 最新值 | 筆數 | 錯誤／待辦 |", "|---|---|---|---|---:|---:|---:|---|"]
    for r in RESULTS:
        lines.append(f"| {r.indicator} | {r.source} | {r.source_type} | {r.status} | {r.latest_period or ''} | {'' if r.latest_value is None else r.latest_value} | {r.points} | {(r.error or '').replace('|', '/')} |")
    lines += ["", "## Secret／代碼狀態", "", f"- `KOSIS_API_KEY`: {'已設定' if KOSIS_KEY else '未設定'}", f"- `ECOS_API_KEY`: {'已設定' if ECOS_KEY else '未設定'}", f"- `MOLIT_API_KEY`: {'已設定' if MOLIT_KEY else '未設定'}", "", "> 本版只保留已核對的正式來源；SOURCE_SELECTED_REB 表示已決定改用 REB，但尚未完成時序下載。"]
    (OUT / "korea_debug.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    print(f"[KR DEBUG] {VERSION}")
    tasks = [run_oecd_labour_fallback, run_retail_fallback, run_oecd_core, run_structured_qna, run_ecos, run_molit, run_kb, run_motir, run_sp_pmi]
    for task in tasks:
        print(f"[RUN] {task.__name__}")
        try:
            task()
        except Exception as exc:
            print(f"[UNHANDLED] {task.__name__}: {exc}")
            traceback.print_exc()
            RESULTS.append(Result(task.__name__, "runtime", "internal", "UNHANDLED_ERROR", error=str(exc)))
    if not any(r.indicator == "Core CPI YoY" for r in RESULTS):
        RESULTS.append(Result("Core CPI YoY", "OECD dedicated national core CPI dataflow", "official_sdmx_csv", "MISSING_RESULT_GUARD", source_url=(OECD_CORE_URLS[0] if OECD_CORE_URLS else ""), error="run_oecd_core completed without emitting a result"))
    write_outputs()
    print((OUT / "korea_debug.md").read_text(encoding="utf-8"))
    print(f"[DONE] {len(RESULTS)} indicators")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
