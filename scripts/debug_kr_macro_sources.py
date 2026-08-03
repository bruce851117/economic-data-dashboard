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
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader

VERSION = "2026-08-03-kr-source-validation-v4-source-fixes"
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
    korea = frame[frame[area_col].astype(str).str.contains(r"(^|:)KOR($|:)|Korea", case=False, regex=True, na=False)].copy()
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


def run_retail_fallback() -> None:
    # Federal Reserve Bank of St. Louis distributes this OECD series without an API key.
    try:
        response = SESSION.get(FRED_RETAIL_CSV, timeout=120)
        response.raise_for_status()
        (OUT / "fred_oecd_korea_real_retail_yoy.csv").write_bytes(response.content)
        frame = pd.read_csv(io.BytesIO(response.content), dtype=str)
        date_col, value_col = frame.columns[:2]
        values = {}
        for raw_date, raw_value in zip(frame[date_col], frame[value_col]):
            period = period_month(str(raw_date)[:7])
            value = number(raw_value)
            if period and value is not None:
                values[period] = value
        if not values:
            raise RuntimeError("FRED/OECD retail CSV has no numeric observations")
        latest = max(values)
        RESULTS.append(Result("Real 零售 YoY", "OECD via Federal Reserve Bank of St. Louis", "official_csv_no_key", "OFFICIAL_FALLBACK", latest, values[latest], len(values), "Korea total retail trade volume, monthly, same-period YoY, seasonally adjusted", FRED_RETAIL_CSV, {"series_id": "KORSLRTTO01GYSAM", "latest": list(sorted(values.items()))[-12:]}))
    except Exception as exc:
        RESULTS.append(Result("Real 零售 YoY", "OECD via Federal Reserve Bank of St. Louis", "official_csv_no_key", "FETCH_ERROR", source_url=FRED_RETAIL_CSV, error=str(exc)))


# ---------------- KOSIS ----------------
KOSIS_ENDPOINT = "https://kosis.kr/openapi/Param/statisticsParameterData.do"


def kosis_table(tbl_id: str, start: str, end: str) -> list[dict[str, Any]]:
    if not KOSIS_KEY:
        raise RuntimeError("Repository secret KOSIS_API_KEY is not configured")
    params = {
        "method": "getList", "apiKey": KOSIS_KEY, "itmId": "ALL",
        "objL1": "ALL", "objL2": "ALL", "objL3": "ALL", "objL4": "ALL",
        "format": "json", "jsonVD": "Y", "prdSe": "M",
        "startPrdDe": start, "endPrdDe": end, "orgId": "101", "tblId": tbl_id,
    }
    response = get(KOSIS_ENDPOINT, params=params)
    payload = response.json()
    save_json(f"kosis_{tbl_id}_raw.json", payload)
    if isinstance(payload, dict) and payload.get("err"):
        raise RuntimeError(str(payload))
    if not isinstance(payload, list):
        raise RuntimeError(f"Unexpected KOSIS response: {type(payload).__name__}")
    return payload


def kosis_candidates(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    for row in rows:
        period = period_month(row.get("PRD_DE"))
        value = number(row.get("DT"))
        if not period or value is None:
            continue
        identity_parts = []
        for key in sorted(row):
            if key in {"DT", "PRD_DE", "PRD_SE", "UNIT_NM", "UNIT_NM_ENG", "TBL_ID", "TBL_NM", "TBL_NM_ENG"}:
                continue
            if key.endswith("_NM") or key in {"ITM_ID", "ITM_NM", "C1", "C1_NM", "C2", "C2_NM", "C3", "C3_NM"}:
                if row.get(key) not in (None, ""):
                    identity_parts.append(f"{key}={clean(row[key])}")
        identity = " | ".join(identity_parts)
        item = grouped.setdefault(identity, {"identity": identity, "metadata": row, "values": {}})
        item["values"][period] = value
    return sorted(grouped.values(), key=lambda x: (-len(x["values"]), x["identity"]))


def choose_candidate(candidates: list[dict[str, Any]], include: Iterable[str], exclude: Iterable[str] = ()) -> dict[str, Any]:
    include_n = [norm(x) for x in include]
    exclude_n = [norm(x) for x in exclude]
    scored = []
    for candidate in candidates:
        text = norm(candidate["identity"])
        score = sum(10 for token in include_n if token in text) - sum(20 for token in exclude_n if token in text)
        score += min(len(candidate["values"]), 120) / 120
        scored.append((score, candidate))
    scored.sort(key=lambda x: (-x[0], -len(x[1]["values"])))
    if not scored:
        raise RuntimeError("No KOSIS numeric series found")
    return scored[0][1]


def run_kosis() -> None:
    if not KOSIS_KEY or KOSIS_KEY in {"2", "sample", "test", "none", "null"}:
        run_oecd_labour_fallback()
        run_retail_fallback()
        return
    specs = [
        ("失業率", "DT_1DA7102S", ["계절조정", "실업률", "계"], ["남자", "여자"], "LEVEL", "全國、總計、季節調整失業率"),
        ("就業人數 YoY%", "DT_1DA7002S", ["취업자", "계"], ["계절조정", "남자", "여자"], "YOY", "全國未季調就業者人數，Level計算YoY"),
        ("Real 零售 YoY", "DT_1K41012", ["불변", "총지수"], ["경상", "계절조정"], "YOY", "總零售不變價原始指數，Level計算YoY"),
    ]
    for indicator, tbl, include, exclude, transform, definition in specs:
        try:
            rows = kosis_table(tbl, "201501", "202612")
            candidates = kosis_candidates(rows)
            save_json(f"kosis_{tbl}_candidates.json", [{"identity": c["identity"], "latest": list(sorted(c["values"].items()))[-6:], "points": len(c["values"])} for c in candidates[:50]])
            selected = choose_candidate(candidates, include, exclude)
            values = selected["values"]
            output = yoy(values) if transform == "YOY" else values
            latest_period = max(output)
            RESULTS.append(Result(indicator, f"KOSIS {tbl}", "official_json_api", "OFFICIAL_ONLY", latest_period, output[latest_period], len(output), definition, KOSIS_ENDPOINT, {"selected_identity": selected["identity"], "latest_level": list(sorted(values.items()))[-6:], "latest_output": list(sorted(output.items()))[-6:]}))
        except Exception as exc:
            RESULTS.append(Result(indicator, f"KOSIS {tbl}", "official_json_api", "FETCH_ERROR", definition=definition, source_url=KOSIS_ENDPOINT, error=str(exc)))


# ---------------- OECD SDMX ----------------
# OECD publishes a dedicated official dataflow for national core CPI YoY.
OECD_CORE_FLOW = "DSD_PRICES@DF_PRICES_N_TXCP01_NRG"
OECD_CORE_URLS = [
    "https://sdmx.oecd.org/public/rest/v2/data/dataflow/OECD.SDD.TPS/DSD_PRICES@DF_PRICES_N_TXCP01_NRG/1.0/all",
    "https://sdmx.oecd.org/public/rest/data/OECD.SDD.TPS,DSD_PRICES@DF_PRICES_N_TXCP01_NRG,1.0/all",
]


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
            korea = frame[frame[area_col].astype(str).str.contains(r"(^|:)KOR($|:)|Korea", case=False, regex=True, na=False)].copy()
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


def run_ecos() -> None:
    # Without a personal key, ECOS sample metadata is too narrow for full discovery.
    # Preserve an explicit official-page discovery artifact instead of reporting false candidates.
    public_urls = {
        "ECOS": "https://ecos.bok.or.kr/",
        "BOK snapshot": "https://snapshot.bok.or.kr/dashboard/C8",
        "BOK releases": "https://www.bok.or.kr/portal/bbs/B0000501/list.do?menuNo=200647",
    }
    discovery = []
    for name, url in public_urls.items():
        try:
            response = get(url)
            discovery.append({"name": name, "url": response.url, "status": response.status_code, "content_type": response.headers.get("Content-Type"), "length": len(response.content)})
            (OUT / f"bok_public_{re.sub(r'[^a-z0-9]+', '_', name.lower())}.html").write_bytes(response.content)
        except Exception as exc:
            discovery.append({"name": name, "url": url, "error": str(exc)})
    save_json("bok_public_sources_discovery.json", discovery)
    for indicator, spec in ECOS_SPECS.items():
        RESULTS.append(Result(indicator, "Bank of Korea public pages/releases", "official_html_attachment_no_key", "PUBLIC_SOURCE_DISCOVERY", definition=f"{spec['transform']}; API-key-free official endpoint/attachment discovery", source_url=public_urls["ECOS"], details={"discovery_file": "bok_public_sources_discovery.json"}))


# ---------------- MOLIT ----------------
def run_molit() -> None:
    try:
        response = get(SEOUL_HOUSING_URL)
        (OUT / "seoul_housing_transactions_page.html").write_bytes(response.content)
        soup = BeautifulSoup(response.text, "html.parser")
        forms = []
        for form in soup.find_all("form"):
            forms.append({
                "action": urljoin(response.url, form.get("action") or ""),
                "method": (form.get("method") or "GET").upper(),
                "inputs": [{"name": tag.get("name"), "value": tag.get("value"), "type": tag.get("type")} for tag in form.find_all(["input", "select", "button"]) if tag.get("name")],
            })
        scripts = [urljoin(response.url, tag.get("src")) for tag in soup.find_all("script") if tag.get("src")]
        inline_scripts = [clean(tag.get_text(" ", strip=True)) for tag in soup.find_all("script") if not tag.get("src") and clean(tag.get_text(" ", strip=True))]
        selects = {tag.get("name") or tag.get("id") or f"select_{idx}": [{"value": option.get("value"), "text": clean(option.get_text(" ", strip=True))} for option in tag.find_all("option")] for idx, tag in enumerate(soup.find_all("select"))}
        links = []
        for tag in soup.find_all(["a", "button"], href=True):
            text = clean(tag.get_text(" ", strip=True))
            href = urljoin(response.url, tag.get("href"))
            if any(token in norm(text + " " + href) for token in ["excel", "xls", "다운로드", "download"]):
                links.append({"text": text, "url": href})
        tables = []
        try:
            for idx, frame in enumerate(pd.read_html(io.StringIO(response.text))):
                path = OUT / f"seoul_housing_table_{idx}.csv"
                frame.to_csv(path, index=False, encoding="utf-8-sig")
                tables.append({"index": idx, "rows": len(frame), "columns": [str(c) for c in frame.columns], "preview": frame.head(5).fillna("").astype(str).to_dict("records")})
        except Exception as exc:
            tables.append({"parse_error": str(exc)})
        save_json("seoul_housing_transactions_discovery.json", {"url": response.url, "forms": forms, "select_options": selects, "inline_scripts": inline_scripts, "scripts": scripts, "download_links": links, "tables": tables})
        RESULTS.append(Result("首爾房市交易量", "Seoul Real Estate Information Plaza / Korea Real Estate Board", "official_html_excel_no_key", "DISCOVERY_AVAILABLE", definition="Monthly housing transactions by Seoul administrative district, reported-date basis", source_url=response.url, details={"forms": len(forms), "scripts": len(scripts), "download_links": len(links), "tables": len(tables)}))
    except Exception as exc:
        RESULTS.append(Result("首爾房市交易量", "Seoul Real Estate Information Plaza", "official_html_excel_no_key", "FETCH_ERROR", definition="Monthly Seoul housing transactions", source_url=SEOUL_HOUSING_URL, error=str(exc)))


# ---------------- KB official workbook discovery ----------------
def run_kb() -> None:
    landing = "https://data.kbland.kr/"
    try:
        response = get(landing)
        (OUT / "kb_datahub_landing.html").write_bytes(response.content)
        soup = BeautifulSoup(response.text, "html.parser")
        script_urls = [urljoin(landing, s.get("src")) for s in soup.find_all("script") if s.get("src")]
        candidates: set[str] = set(re.findall(r'https?[^"\']+\.(?:xlsx|xls)(?:\?[^"\']*)?', response.text, re.I))
        endpoint_candidates: set[str] = set()
        inspected = []
        for script_url in script_urls[:20]:
            try:
                body = get(script_url).text
                inspected.append({"url": script_url, "length": len(body)})
                for match in re.findall(r'https?[^"\']+\.(?:xlsx|xls)(?:\?[^"\']*)?', body, re.I):
                    candidates.add(match.replace("\\/", "/"))
                for match in re.findall(r'[^"\']*(?:월간시계열|월간통계|excel|xlsx|다운로드|download)[^"\']*', body, re.I):
                    if len(match) < 500:
                        candidates.add(match.replace("\\/", "/"))
                for match in re.findall(r'["\']((?:/|https?://)[^"\']{2,240}(?:api|stat|excel|download|file|timeseries|time-series|kbstats)[^"\']*)["\']', body, re.I):
                    endpoint_candidates.add(match.replace("\\/", "/"))
            except Exception as exc:
                inspected.append({"url": script_url, "error": str(exc)})
        save_json("kb_datahub_discovery.json", {"scripts": inspected, "candidates": sorted(candidates)[:300], "endpoint_candidates": sorted(endpoint_candidates)[:1000]})
        status = "DISCOVERY_NO_STAT_ENDPOINT"
        for indicator in ["首爾房價MoM", "房價MoM"]:
            RESULTS.append(Result(indicator, "KB Real Estate Data Hub monthly time-series workbook", "official_xlsx", status, definition="월간 주택매매가격; 서울/전국; index level or MoM", source_url=landing, details={"candidate_count": len(candidates), "endpoint_candidate_count": len(endpoint_candidates), "candidates": sorted(candidates)[:30], "endpoint_candidates": sorted(endpoint_candidates)[:50]}))
    except Exception as exc:
        for indicator in ["首爾房價MoM", "房價MoM"]:
            RESULTS.append(Result(indicator, "KB Real Estate Data Hub", "official_xlsx", "FETCH_ERROR", source_url=landing, error=str(exc)))


# ---------------- MOTIR releases ----------------
MOTIR_RELEASES = [
    ("2026-06", "https://www.motir.go.kr/kor/article/ATCL3f49a5a8c/172066/view"),
    ("2026-05", "https://www.motir.go.kr/kor/article/ATCL3f49a5a8c/171960/view"),
    ("2026-04", "https://www.motir.go.kr/kor/article/ATCL3f49a5a8c/171869/view"),
    ("2026-02", "https://www.motir.go.kr/kor/article/ATCL3f49a5a8c/171632/view"),
]


def run_motir() -> None:
    values: dict[str, float] = {}
    details = []
    for period, url in MOTIR_RELEASES:
        try:
            response = get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            text = clean(soup.get_text(" ", strip=True))
            compact = re.sub(r"\s+", "", text)
            (OUT / f"motir_retail_{period}.html").write_bytes(response.content)
            month = str(int(period[-2:]))
            # Locate the explicit monthly section, not half-year/YTD summary.
            section_markers = [f"’26년{month}월매출동향", f"'26년{month}월매출동향", f"26년{month}월매출동향"]
            positions = [compact.find(marker) for marker in section_markers if compact.find(marker) >= 0]
            monthly = compact[min(positions):min(positions)+7000] if positions else compact
            patterns = [
                rf"{month}월주요유통업체.*?전체매출은전년(?:동기)?보다([0-9]+(?:\.[0-9]+)?)%증가",
                rf"{month}월주요유통업체.*?전체매출[^0-9]{{0,60}}([0-9]+(?:\.[0-9]+)?)%증가",
                rf"전체매출은전년(?:동기)?보다([0-9]+(?:\.[0-9]+)?)%증가",
            ]
            value = None
            for pattern in patterns:
                match = re.search(pattern, monthly)
                if match:
                    value = float(match.group(1))
                    break
            if value is not None:
                values[period] = value
            details.append({"period": period, "url": url, "value": value, "monthly_section_found": bool(positions), "monthly_compact_head": monthly[:1800]})
        except Exception as exc:
            details.append({"period": period, "url": url, "error": str(exc)})
    save_json("motir_major_retailer_details.json", details)
    if values:
        period = max(values)
        RESULTS.append(Result("零售YoY", "MOTIR Sales Trends for Major Retailers", "official_html_pdf", "OFFICIAL_ONLY", period, values[period], len(values), "全體主要零售商單月銷售YoY，排除半年/YTD摘要", dict(MOTIR_RELEASES)[period], {"latest": list(sorted(values.items()))[-12:]}))
    else:
        RESULTS.append(Result("零售YoY", "MOTIR Sales Trends for Major Retailers", "official_html_pdf", "FETCH_ERROR", source_url=MOTIR_RELEASES[0][1], error="No monthly total major-retailer YoY parsed"))


# ---------------- S&P Global South Korea PMI ----------------
SP_RELEASE_CALENDARS = [
    "https://www.pmi.spglobal.com/Public/Release/PressReleases",
    "https://www.pmi.spglobal.com/Public/Home/PressRelease",
]
SP_KOREA_SEEDS = [
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


def sp_headline_pmi(text: str) -> float | None:
    # Skip chart header and search narrative sentences first.
    narrative_start = min([pos for pos in [text.lower().find("the headline"), text.lower().find("the seasonally adjusted")] if pos >= 0] or [0])
    narrative = text[narrative_start:]
    patterns = [
        r"headline S&P Global South Korea Manufacturing PMI[^.]{0,420}?\b(?:rose|fell|increased|decreased|was|posted|registered)\b[^0-9]{0,120}?([0-9]{2}(?:\.[0-9])?)",
        r"seasonally adjusted S&P Global South Korea Manufacturing Purchasing Managers(?:'|’)? Index[^.]{0,420}?\b(?:rose|fell|increased|decreased|was|posted|registered|at)\b[^0-9]{0,120}?([0-9]{2}(?:\.[0-9])?)",
        r"The PMI (?:rose|fell|increased|decreased) to\s+([0-9]{2}(?:\.[0-9])?)",
    ]
    for pattern in patterns:
        match = re.search(pattern, narrative, re.I)
        if match:
            value = float(match.group(1))
            if 30 <= value <= 70 and value != 50.0:
                return value
    return None


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
            value = sp_headline_pmi(text)
            parsed.append({**candidate, "final_url": response.url, "period": period, "value": value, "text_head": text[:1400]})
        except Exception as exc:
            parsed.append({**candidate, "error": str(exc)})
    save_json("sp_global_korea_parsed.json", parsed)
    valid = [x for x in parsed if x.get("period") and x.get("value") is not None]
    if valid:
        valid.sort(key=lambda x: x["period"])
        latest = valid[-1]
        RESULTS.append(Result(
            "製造業PMI", "S&P Global South Korea Manufacturing PMI", "official_html_pdf", "OFFICIAL_ONLY",
            latest["period"], latest["value"], len(valid),
            "Headline seasonally adjusted Manufacturing PMI; exclude Output/New Orders",
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
    lines += ["", "## Secret／代碼狀態", "", f"- `KOSIS_API_KEY`: {'已設定' if KOSIS_KEY else '未設定'}", f"- `ECOS_API_KEY`: {'已設定' if ECOS_KEY else '未設定'}", f"- `MOLIT_API_KEY`: {'已設定' if MOLIT_KEY else '未設定'}", "", "> CANDIDATE_FOUND 只表示 metadata 已定位候選，仍須以既有參考值核對後才能進正式 updater。"]
    (OUT / "korea_debug.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    print(f"[KR DEBUG] {VERSION}")
    tasks = [run_kosis, run_oecd_core, run_ecos, run_molit, run_kb, run_motir, run_sp_pmi]
    for task in tasks:
        print(f"[RUN] {task.__name__}")
        try:
            task()
        except Exception as exc:
            print(f"[UNHANDLED] {task.__name__}: {exc}")
            traceback.print_exc()
    write_outputs()
    print((OUT / "korea_debug.md").read_text(encoding="utf-8"))
    print(f"[DONE] {len(RESULTS)} indicators")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
