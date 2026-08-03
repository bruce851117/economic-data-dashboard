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

VERSION = "2026-08-03-kr-source-validation-v1"
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
OECD_FLOW = "OECD.SDD.TPS,DSD_PRICES@DF_PRICES_ALL"
OECD_STRUCTURE = "https://sdmx.oecd.org/public/rest/dataflow/OECD.SDD.TPS/DSD_PRICES@DF_PRICES_ALL/?references=all"
OECD_DATA = "https://sdmx.oecd.org/public/rest/data/OECD.SDD.TPS,DSD_PRICES@DF_PRICES_ALL"


def oecd_structure() -> tuple[list[str], dict[str, dict[str, str]]]:
    response = get(OECD_STRUCTURE, headers={"Accept": "application/vnd.sdmx.structure+xml;version=3.0"})
    (OUT / "oecd_prices_structure.xml").write_bytes(response.content)
    root = ET.fromstring(response.content)
    dims: list[str] = []
    codelists: dict[str, dict[str, str]] = {}
    for elem in root.iter():
        tag = elem.tag.split("}")[-1]
        if tag == "Dimension" and elem.attrib.get("id") and elem.attrib.get("id") not in dims:
            dims.append(elem.attrib["id"])
        if tag == "Codelist":
            cid = elem.attrib.get("id", "")
            codes: dict[str, str] = {}
            for code in elem:
                if code.tag.split("}")[-1] != "Code":
                    continue
                code_id = code.attrib.get("id", "")
                labels = [child.text or "" for child in code.iter() if child.tag.split("}")[-1] == "Name"]
                codes[code_id] = " | ".join(labels)
            if cid:
                codelists[cid] = codes
    # The dataflow structure order is also returned in CSV header if structural XML differs.
    return dims, codelists


def run_oecd_core() -> None:
    try:
        dims, codelists = oecd_structure()
        # First request all Korean observations; the server accepts wildcard dimensions.
        # Build a key only when REF_AREA is present in the discovered order.
        data_dims = [d for d in dims if d not in {"TIME_PERIOD", "OBS_VALUE"}]
        if "REF_AREA" not in data_dims:
            raise RuntimeError(f"REF_AREA not found in OECD dimensions: {data_dims}")
        key = [""] * len(data_dims)
        key[data_dims.index("REF_AREA")] = "KOR"
        url = f"{OECD_DATA}/" + ".".join(key)
        response = get(url, params={"startPeriod": "2015-01", "dimensionAtObservation": "AllDimensions"}, headers={"Accept": "application/vnd.sdmx.data+csv;version=2.0;labels=both"})
        (OUT / "oecd_core_cpi_kor_raw.csv").write_bytes(response.content)
        frame = pd.read_csv(io.BytesIO(response.content), dtype=str)
        save_json("oecd_core_cpi_columns.json", list(frame.columns))
        period_col = next((c for c in frame if c.split(":", 1)[0] == "TIME_PERIOD"), None)
        value_col = next((c for c in frame if c.split(":", 1)[0] == "OBS_VALUE"), None)
        if not period_col or not value_col:
            raise RuntimeError("OECD CSV missing TIME_PERIOD/OBS_VALUE")
        candidates = []
        identity_cols = [c for c in frame.columns if c not in {period_col, value_col} and not c.startswith("OBS_")]
        for identity, group in frame.groupby(identity_cols, dropna=False):
            if not isinstance(identity, tuple): identity = (identity,)
            meta = dict(zip(identity_cols, identity))
            text = norm(" | ".join(f"{k}={v}" for k, v in meta.items()))
            score = 0
            for token in ["kor", "monthly", "consumer price", "all items non-food non-energy", "growth rate over one year", "national"]:
                if token in text: score += 10
            if "quarter" in text: score -= 20
            values = {period_month(p): number(v) for p, v in zip(group[period_col], group[value_col])}
            values = {k: v for k, v in values.items() if k and v is not None}
            if values:
                candidates.append({"score": score, "metadata": meta, "values": values})
        candidates.sort(key=lambda x: (-x["score"], -len(x["values"])))
        save_json("oecd_core_cpi_candidates.json", [{"score": c["score"], "metadata": c["metadata"], "latest": list(sorted(c["values"].items()))[-6:]} for c in candidates[:30]])
        if not candidates:
            raise RuntimeError("No OECD Korean CPI candidates")
        selected = candidates[0]
        period = max(selected["values"])
        RESULTS.append(Result("Core CPI YoY", "OECD SDMX DSD_PRICES@DF_PRICES_ALL", "official_sdmx_csv", "OFFICIAL_ONLY", period, selected["values"][period], len(selected["values"]), "OECD CPI excluding food and energy, national methodology, YoY", url, {"metadata": selected["metadata"], "latest": list(sorted(selected["values"].items()))[-6:]}))
    except Exception as exc:
        RESULTS.append(Result("Core CPI YoY", "OECD SDMX DSD_PRICES@DF_PRICES_ALL", "official_sdmx_csv", "FETCH_ERROR", definition="OECD CPI excluding food and energy, YoY", source_url=OECD_STRUCTURE, error=str(exc)))


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
    if not ECOS_KEY:
        for indicator, spec in ECOS_SPECS.items():
            RESULTS.append(Result(indicator, "BOK ECOS", "official_json_api", "MISSING_SECRET", definition="metadata-first discovery required", source_url=ECOS_BASE, error="Add repository secret ECOS_API_KEY"))
        return
    try:
        payload = ecos_call("StatisticTableList", "1", "10000", "")
        tables = ecos_rows(payload, "StatisticTableList")
        save_json("ecos_statistic_table_list.json", tables)
    except Exception as exc:
        for indicator in ECOS_SPECS:
            RESULTS.append(Result(indicator, "BOK ECOS", "official_json_api", "FETCH_ERROR", source_url=ECOS_BASE, error=f"StatisticTableList failed: {exc}"))
        return

    for indicator, spec in ECOS_SPECS.items():
        try:
            table_candidates = []
            for row in tables:
                name = clean(row.get("STAT_NAME"))
                text = norm(name)
                cycle = clean(row.get("CYCLE"))
                if cycle and cycle != spec["cycle"]:
                    continue
                score = sum(8 for token in spec["table"] if norm(token) in text)
                if score:
                    end = clean(row.get("END_TIME"))
                    table_candidates.append((score, end, row))
            table_candidates.sort(key=lambda x: (x[0], x[1]), reverse=True)
            table_details = []
            for tscore, _, table in table_candidates[:12]:
                stat_code = clean(table.get("STAT_CODE"))
                item_payload = ecos_call("StatisticItemList", "1", "10000", stat_code)
                items = ecos_rows(item_payload, "StatisticItemList")
                for item in items:
                    item_name = clean(item.get("ITEM_NAME"))
                    text = norm(item_name)
                    score = tscore + sum(10 for token in spec["items"] if norm(token) in text) - sum(20 for token in spec["exclude"] if norm(token) in text)
                    if score > tscore:
                        table_details.append({"score": score, "table": table, "item": item})
            table_details.sort(key=lambda x: (x["score"], clean(x["table"].get("END_TIME"))), reverse=True)
            save_json(f"ecos_{re.sub(r'[^a-zA-Z0-9]+', '_', indicator)}_candidates.json", table_details[:50])
            if not table_details:
                raise RuntimeError("No ECOS table/item candidate matched metadata keywords")
            best = table_details[0]
            RESULTS.append(Result(indicator, "BOK ECOS metadata discovery", "official_json_api", "CANDIDATE_FOUND", definition=f"{spec['transform']}; exact series requires candidate validation", source_url=ECOS_BASE, details={"selected_candidate": best, "candidate_count": len(table_details)}))
        except Exception as exc:
            RESULTS.append(Result(indicator, "BOK ECOS metadata discovery", "official_json_api", "FETCH_ERROR", source_url=ECOS_BASE, error=str(exc)))


# ---------------- MOLIT ----------------
def run_molit() -> None:
    if not MOLIT_KEY:
        RESULTS.append(Result("首爾房市交易量", "MOLIT Statistics OpenAPI", "official_json_api", "MISSING_SECRET_OR_CODES", definition="주택매매거래량, 서울, monthly, 건", source_url="https://stat.molit.go.kr/portal/openapi/main.do", error="Add MOLIT_API_KEY and approve the target table; table/form codes are assigned in the portal and must not be guessed"))
        return
    RESULTS.append(Result("首爾房市交易量", "MOLIT Statistics OpenAPI", "official_json_api", "NEEDS_PORTAL_CODES", definition="주택매매거래량, 서울, monthly, 건", source_url="https://stat.molit.go.kr/portal/openapi/main.do", details={"key_configured": True, "note": "OpenAPI requires approved table/form/series codes. Save codes as repository variables after portal approval; each request window <= 5 years."}))


# ---------------- KB official workbook discovery ----------------
def run_kb() -> None:
    landing = "https://data.kbland.kr/"
    try:
        response = get(landing)
        (OUT / "kb_datahub_landing.html").write_bytes(response.content)
        soup = BeautifulSoup(response.text, "html.parser")
        script_urls = [urljoin(landing, s.get("src")) for s in soup.find_all("script") if s.get("src")]
        candidates: set[str] = set(re.findall(r'https?[^"\']+\.(?:xlsx|xls)(?:\?[^"\']*)?', response.text, re.I))
        inspected = []
        for script_url in script_urls[:20]:
            try:
                body = get(script_url).text
                inspected.append({"url": script_url, "length": len(body)})
                for match in re.findall(r'https?[^"\']+\.(?:xlsx|xls)(?:\?[^"\']*)?', body, re.I):
                    candidates.add(match.replace("\\/", "/"))
                for match in re.findall(r'[^"\']*(?:월간시계열|월간통계|excel|xlsx)[^"\']*', body, re.I):
                    if len(match) < 500:
                        candidates.add(match.replace("\\/", "/"))
            except Exception as exc:
                inspected.append({"url": script_url, "error": str(exc)})
        save_json("kb_datahub_discovery.json", {"scripts": inspected, "candidates": sorted(candidates)[:200]})
        status = "CANDIDATES_FOUND" if candidates else "DOWNLOAD_URL_NOT_FOUND"
        for indicator in ["首爾房價MoM", "房價MoM"]:
            RESULTS.append(Result(indicator, "KB Real Estate Data Hub monthly time-series workbook", "official_xlsx", status, definition="월간 주택매매가격; 서울/전국; index level or MoM", source_url=landing, details={"candidate_count": len(candidates), "candidates": sorted(candidates)[:30]}))
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
            text = clean(BeautifulSoup(response.text, "html.parser").get_text(" ", strip=True))
            (OUT / f"motir_retail_{period}.html").write_bytes(response.content)
            patterns = [
                rf"{period[-2:]}월[^.]*?전체 매출(?:은|이)?[^.]*?(?:전년[^.]*?)?([0-9]+(?:\.[0-9]+)?)% 증가",
                r"전체 매출\s*([0-9]+(?:\.[0-9]+)?)% 증가",
                r"전체 매출은 전년보다\s*([0-9]+(?:\.[0-9]+)?)% 증가",
            ]
            value = None
            for pattern in patterns:
                match = re.search(pattern, text)
                if match:
                    value = float(match.group(1)); break
            if value is not None:
                values[period] = value
            details.append({"period": period, "url": url, "value": value, "text_head": text[:700]})
        except Exception as exc:
            details.append({"period": period, "url": url, "error": str(exc)})
    save_json("motir_major_retailer_details.json", details)
    if values:
        period = max(values)
        RESULTS.append(Result("零售YoY", "MOTIR Sales Trends for Major Retailers", "official_html_pdf", "OFFICIAL_ONLY", period, values[period], len(values), "全體主要零售商銷售YoY；保存offline/online供除錯", dict(MOTIR_RELEASES)[period], {"latest": list(sorted(values.items()))[-6:]}))
    else:
        RESULTS.append(Result("零售YoY", "MOTIR Sales Trends for Major Retailers", "official_html_pdf", "FETCH_ERROR", source_url=MOTIR_RELEASES[0][1], error="No total major-retailer YoY parsed"))


# ---------------- S&P Global South Korea PMI ----------------
SP_RELEASES = "https://www.pmi.spglobal.com/Public/Release/PressReleases"

def sp_text(response: requests.Response) -> str:
    ctype = response.headers.get("Content-Type", "").lower()
    if "pdf" in ctype or response.content.startswith(b"%PDF"):
        reader = PdfReader(io.BytesIO(response.content))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    return BeautifulSoup(response.text, "html.parser").get_text("\n", strip=True)


def run_sp_pmi() -> None:
    try:
        calendar = get(SP_RELEASES)
        (OUT / "sp_global_release_calendar.html").write_bytes(calendar.content)
        soup = BeautifulSoup(calendar.text, "html.parser")
        candidates = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "PressRelease" not in href:
                continue
            context = clean(a.get_text(" ", strip=True) + " " + (a.parent.get_text(" ", strip=True) if a.parent else ""))
            if "south korea" in norm(context) and "pmi" in norm(context):
                candidates.append({"title": context[:400], "url": urljoin(SP_RELEASES, href)})
        # Also search raw page for release URLs near South Korea labels.
        save_json("sp_global_korea_candidates.json", candidates)
        parsed = []
        for candidate in candidates[:30]:
            try:
                response = get(candidate["url"])
                text = clean(sp_text(response))
                safe = re.sub(r"[^a-zA-Z0-9]+", "_", candidate["url"])[-80:]
                (OUT / f"sp_global_korea_{safe}.txt").write_text(text, encoding="utf-8")
                month_match = re.search(r"(?:data were collected|survey data collected|reporting on)\D{0,80}(January|February|March|April|May|June|July|August|September|October|November|December)\s+(20\d{2})", text, re.I)
                period = ""
                if month_match:
                    month = datetime.strptime(month_match.group(1), "%B").month
                    period = f"{month_match.group(2)}-{month:02d}"
                value = None
                patterns = [
                    r"South Korea Manufacturing PMI[^0-9]{0,120}([0-9]{2}(?:\.[0-9])?)",
                    r"seasonally adjusted[^.]{0,150}?PMI[^0-9]{0,80}([0-9]{2}(?:\.[0-9])?)",
                    r"PMI (?:rose|fell|increased|decreased)[^.]{0,80}?to\s+([0-9]{2}(?:\.[0-9])?)",
                ]
                for pattern in patterns:
                    match = re.search(pattern, text, re.I)
                    if match:
                        value = float(match.group(1)); break
                parsed.append({**candidate, "period": period, "value": value, "text_head": text[:900]})
            except Exception as exc:
                parsed.append({**candidate, "error": str(exc)})
        save_json("sp_global_korea_parsed.json", parsed)
        valid = [x for x in parsed if x.get("period") and x.get("value")]
        if not valid:
            raise RuntimeError("No South Korea Manufacturing PMI official release parsed")
        valid.sort(key=lambda x: x["period"])
        latest = valid[-1]
        RESULTS.append(Result("製造業PMI", "S&P Global South Korea Manufacturing PMI", "official_html_pdf", "OFFICIAL_ONLY", latest["period"], latest["value"], len(valid), "Headline seasonally adjusted Manufacturing PMI; exclude Output/New Orders", latest["url"], {"latest_releases": valid[-6:]}))
    except Exception as exc:
        RESULTS.append(Result("製造業PMI", "S&P Global", "official_html_pdf", "FETCH_ERROR", definition="Headline Manufacturing PMI", source_url=SP_RELEASES, error=str(exc)))


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
