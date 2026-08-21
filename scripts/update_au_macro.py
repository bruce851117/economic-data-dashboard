#!/usr/bin/env python3
"""Validate Australian macro sources against the user's AU_ECON reference values.

Source policy:
1. Official API / CSV / XLSX
2. Official PDF
3. Official HTML release only when no public structured series is available

Read-only diagnostic. It never modifies production JSON files.
"""
from __future__ import annotations

import csv
import html
import io
import json
import math
import re
import sys
import traceback
import time
from dataclasses import asdict, dataclass
from datetime import date, datetime
from datetime import timedelta as dt_timedelta
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, NavigableString
from openpyxl import load_workbook
from pypdf import PdfReader

VERSION = "2026-08-21-update-au-macro-v9-dynamic-sources"
OUT = Path("debug/au_macro_sources")
ABS_API = "https://data.api.abs.gov.au/rest/data"
SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (compatible; AUMacroSourceValidator/1.0; GitHub-Actions)",
    "Accept-Language": "en-AU,en;q=0.9",
})


@dataclass
class Point:
    period: str
    value: float
    source_url: str
    status: str = ""
    note: str = ""


@dataclass
class Target:
    label: str
    frequency: str
    expected: dict[str, float]
    source_tier: str
    source_name: str


def log(message: str) -> None:
    print(message, flush=True)


def clean(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def norm(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", " ", clean(value).lower()).strip()


def number(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        value = float(value)
        return value if math.isfinite(value) else None
    text = clean(value).replace("%", "").replace(",", "").replace("−", "-")
    match = re.search(r"[+-]?\d+(?:\.\d+)?", text)
    return float(match.group()) if match else None


def period_key(value: Any) -> str | None:
    # openpyxl returns ABS workbook date cells as datetime/date objects.
    if isinstance(value, (datetime, date)):
        month = value.month
        quarter = (month - 1) // 3 + 1
        # National accounts workbooks use Mar/Jun/Sep/Dec quarter dates.
        if month in {3, 6, 9, 12}:
            return f"{value.year:04d}-Q{quarter}"
        return f"{value.year:04d}-{month:02d}"
    text = clean(value)
    # Also accept displayed Excel timestamps and historical dates.
    timestamp = re.fullmatch(r"((?:19|20)\d{2})[-/](0?[1-9]|1[0-2])[-/](0?[1-9]|[12]\d|3[01])(?:[ T].*)?", text)
    if timestamp:
        year, month = int(timestamp.group(1)), int(timestamp.group(2))
        if month in {3, 6, 9, 12}:
            return f"{year:04d}-Q{(month - 1) // 3 + 1}"
        return f"{year:04d}-{month:02d}"
    monthly = re.fullmatch(r"((?:19|20)\d{2})[-/]?(0[1-9]|1[0-2])", text)
    if monthly:
        return f"{monthly.group(1)}-{monthly.group(2)}"
    quarterly = re.fullmatch(r"((?:19|20)\d{2})[- ]?[Qq]([1-4])", text)
    if quarterly:
        return f"{quarterly.group(1)}-Q{quarterly.group(2)}"
    named_quarter = re.fullmatch(
        r"(Mar|Jun|Sep|Dec)(?:ember)?(?:[- ]+Qtr)?[- ]+((?:19|20)\d{2})",
        text,
        re.I,
    )
    if named_quarter:
        quarter_map = {"mar": 1, "jun": 2, "sep": 3, "dec": 4}
        return f"{int(named_quarter.group(2)):04d}-Q{quarter_map[named_quarter.group(1)[:3].lower()]}"
    # ABS labels such as Jun-2026 or May-26.
    month_map = {name.lower(): index for index, name in enumerate(
        "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(), 1)}
    named = re.fullmatch(r"([A-Za-z]{3})[- ]((?:19|20)\d{2}|\d{2})", text)
    if named and named.group(1).lower() in month_map:
        year = int(named.group(2))
        if year < 100:
            year += 2000
        return f"{year:04d}-{month_map[named.group(1).lower()]:02d}"
    return None


def get(url: str, **kwargs: Any) -> requests.Response:
    """GET with bounded retries for S&P's transient 202/429 responses."""
    retry_statuses = {202, 429, 500, 502, 503, 504}
    last_response: requests.Response | None = None
    for attempt in range(5):
        response = SESSION.get(url, timeout=90, allow_redirects=True, **kwargs)
        last_response = response
        log(f"[HTTP] {response.status_code} {response.url} bytes={len(response.content)} attempt={attempt + 1}")
        if response.status_code not in retry_statuses and response.content:
            response.raise_for_status()
            return response
        if response.status_code == 200 and response.content:
            return response
        retry_after = response.headers.get("Retry-After", "")
        try:
            delay = max(float(retry_after), 1.5 * (attempt + 1)) if retry_after else 1.5 * (attempt + 1)
        except ValueError:
            delay = 1.5 * (attempt + 1)
        time.sleep(min(delay, 8.0))
    if last_response is not None:
        if last_response.status_code == 202 and not last_response.content:
            raise RuntimeError(f"Upstream still processing after retries: {last_response.url}")
        last_response.raise_for_status()
    raise RuntimeError(f"GET failed without response: {url}")


def dedupe(points: list[Point]) -> list[Point]:
    mapping = {point.period: point for point in points}
    return [mapping[key] for key in sorted(mapping)]


ABS_FLOW_ALIASES = {
    "LF": ["LF"],
    "JV": ["JV"],
    "WPI": ["WPI"],
    # Monthly CPI moved into the consolidated CPI flow. CPI_M is retained as a
    # fallback for historical metadata snapshots.
    "CPI_MONTHLY": ["CPI", "CPI_M"],
    "HSI_M": ["HSI_M", "MHSI", "HSI"],
    "ANA_AGG": ["ANA_AGG"],
}


def abs_csv(flow: str, start_period: str, *, last_n: int | None = None) -> tuple[list[dict[str, str]], str]:
    """Download ABS SDMX CSV using the official media-type labels syntax.

    ABS expects labels=both inside the Accept media type, not as a URL query
    parameter. The v1 diagnostic incorrectly sent labels=both in the query,
    which caused the common HTTP 400 responses.
    """
    params: dict[str, str] = {
        "startPeriod": start_period,
        "dimensionAtObservation": "TIME_PERIOD",
    }
    if last_n:
        params["lastNObservations"] = str(last_n)
    errors: list[str] = []
    for candidate in ABS_FLOW_ALIASES.get(flow, [flow]):
        url = f"{ABS_API}/ABS,{candidate}/all"
        response = SESSION.get(
            url,
            params=params,
            timeout=120,
            allow_redirects=True,
            headers={"Accept": "application/vnd.sdmx.data+csv;labels=both"},
        )
        log(f"[HTTP] {response.status_code} {response.url} bytes={len(response.content)}")
        safe_name = re.sub(r"[^a-z0-9]+", "_", candidate.lower()).strip("_")
        (OUT / f"abs_{safe_name}_http_{response.status_code}.txt").write_bytes(response.content)
        if response.status_code >= 400:
            errors.append(f"{candidate}: HTTP {response.status_code}: {response.text[:500]}")
            continue
        raw_path = OUT / f"abs_{safe_name}_raw.csv"
        raw_path.write_bytes(response.content)
        text = response.content.decode("utf-8-sig", "replace")
        reader = csv.DictReader(io.StringIO(text))
        raw_rows = list(reader)
        (OUT / f"abs_{safe_name}_columns.json").write_text(
            json.dumps({"columns": reader.fieldnames or []}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        rows = []
        for raw_row in raw_rows:
            row = {str(key).strip(): value for key, value in raw_row.items() if key is not None}
            # ABS SDMX-CSV responses may label observation columns differently
            # depending on representation. Provide canonical aliases.
            for key, value in list(row.items()):
                # labels=both produces headers such as
                # TIME_PERIOD:Time period and OBS_VALUE:Observation value.
                component_id = key.split(":", 1)[0].strip()
                compact = re.sub(r"[^A-Z0-9]", "", component_id.upper())
                if compact in {"TIMEPERIOD", "TIME", "PERIOD"} and not row.get("TIME_PERIOD"):
                    row["TIME_PERIOD"] = value
                if compact in {"OBSVALUE", "VALUE", "OBSERVATIONVALUE"} and not row.get("OBS_VALUE"):
                    row["OBS_VALUE"] = value
            rows.append(row)
        if rows:
            return rows, response.url
        errors.append(f"{candidate}: successful response contained no CSV rows")
    raise RuntimeError("ABS dataflow attempts failed: " + " | ".join(errors))

def component_id(key: str) -> str:
    return re.sub(r"[^A-Z0-9_]", "", key.split(":", 1)[0].strip().upper())


def row_text(row: dict[str, Any]) -> str:
    ignored = {"TIME_PERIOD", "OBS_VALUE", "OBS_STATUS", "OBS_COMMENT", "UNIT_MULT", "DECIMALS"}
    return norm(" ".join(
        str(value) for key, value in row.items()
        if component_id(str(key)) not in ignored
    ))


def series_identity(row: dict[str, Any]) -> str:
    # labels=both retains labelled source columns. TIME_PERIOD must be excluded
    # by SDMX component ID, otherwise each observation becomes its own series.
    ignored = {"TIME_PERIOD", "OBS_VALUE", "OBS_STATUS", "OBS_COMMENT", "UNIT_MULT", "DECIMALS"}
    return "|".join(
        f"{key}={row.get(key, '')}"
        for key in sorted(row)
        if component_id(str(key)) not in ignored
    )


def rank_abs_series(
    rows: list[dict[str, str]],
    include: list[str],
    exclude: list[str],
    expected: dict[str, float],
    *,
    transform: str = "level",
) -> tuple[list[Point], list[dict[str, Any]]]:
    """Rank every ABS series by numerical agreement, then metadata relevance.

    ABS label columns vary across dataflows, so requiring every English phrase
    to appear in one concatenated label incorrectly discarded valid series.
    The diagnostic now keeps every numeric series, compares common reference
    periods first, and uses metadata terms only as a secondary ranking signal.
    """
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault(series_identity(row), []).append(row)

    ranked: list[dict[str, Any]] = []
    for identity, series_rows in grouped.items():
        text = row_text(series_rows[0])
        include_hits = sum(1 for term in include if term in text)
        exclude_hits = sum(1 for term in exclude if term in text)
        metadata_score = include_hits * 10 - exclude_hits * 20

        levels: dict[str, float] = {}
        for row in series_rows:
            period = period_key(row.get("TIME_PERIOD"))
            value = number(row.get("OBS_VALUE"))
            if period and value is not None:
                levels[period] = value
        if not levels:
            continue

        values = levels
        if transform in {"mom_diff", "mom_diff_thousands"}:
            ordered = sorted(levels)
            divisor = 1000.0 if transform == "mom_diff_thousands" else 1.0
            values = {
                current: (levels[current] - levels[previous]) / divisor
                for previous, current in zip(ordered, ordered[1:])
            }
        elif transform == "yoy_pct_q":
            ordered = sorted(levels)
            values = {
                ordered[index]: (levels[ordered[index]] / levels[ordered[index - 4]] - 1.0) * 100.0
                for index in range(4, len(ordered))
                if levels[ordered[index - 4]] != 0
            }

        common = sorted(set(expected) & set(values))
        diffs = [abs(values[p] - expected[p]) for p in common]
        mae = sum(diffs) / len(diffs) if diffs else 999999.0
        max_error = max(diffs) if diffs else 999999.0
        ranked.append({
            "identity": identity,
            "description": text,
            "include_hits": include_hits,
            "include_total": len(include),
            "exclude_hits": exclude_hits,
            "metadata_score": metadata_score,
            "matches": len(common),
            "mae": mae,
            "max_error": max_error,
            "latest": [[period, values[period]] for period in sorted(values)[-12:]],
            "values": values,
        })

    ranked.sort(
        key=lambda item: (
            -item["matches"],
            item["mae"],
            item["max_error"],
            -item["metadata_score"],
            -len(item["values"]),
        )
    )
    if not ranked:
        raise RuntimeError("ABS response contained no numeric time series")

    best = ranked[0]
    points = [
        Point(period, value, "ABS Data API", note=best["description"])
        for period, value in sorted(best["values"].items())
    ]
    public_candidates = [
        {key: value for key, value in item.items() if key != "values"}
        for item in ranked[:50]
    ]
    return points, public_candidates

def fetch_abs_target(flow: str, start: str, include: list[str], exclude: list[str], expected: dict[str, float], transform: str = "level") -> tuple[list[Point], dict[str, Any]]:
    rows, url = abs_csv(flow, start)
    points, candidates = rank_abs_series(rows, include, exclude, expected, transform=transform)
    if flow == "JV":
        quarter_month = {"Q1": "02", "Q2": "05", "Q3": "08", "Q4": "11"}
        for point in points:
            match = re.fullmatch(r"(\d{4})-(Q[1-4])", point.period)
            if match:
                point.period = f"{match.group(1)}-{quarter_month[match.group(2)]}"
    for point in points:
        point.source_url = url
    return points, {"flow": flow, "request_url": url, "candidates": candidates}


def workbook_rows(content: bytes) -> list[dict[str, Any]]:
    if content.startswith(b"PK"):
        workbook = load_workbook(io.BytesIO(content), read_only=True, data_only=True)
        return [{"sheet": sheet.title, "rows": [list(row) for row in sheet.iter_rows(values_only=True)]} for sheet in workbook.worksheets]
    if content.startswith(bytes.fromhex("D0CF11E0")):
        import xlrd
        workbook = xlrd.open_workbook(file_contents=content)
        return [{"sheet": sheet.name, "rows": [sheet.row_values(row) for row in range(sheet.nrows)]} for sheet in workbook.sheets()]
    raise RuntimeError("Downloaded file is neither XLSX nor XLS")


def excel_period(value: Any, frequency: str = "Q") -> str | None:
    if isinstance(value, (int, float)) and 20000 <= float(value) <= 80000:
        converted = datetime(1899, 12, 30) + dt_timedelta(days=float(value))
        if frequency == "Q":
            return f"{converted.year:04d}-Q{(converted.month - 1) // 3 + 1}"
        return f"{converted.year:04d}-{converted.month:02d}"
    period = period_key(value)
    if period and frequency == "Q" and re.fullmatch(r"20\d{2}-\d{2}", period):
        year, month = map(int, period.split("-"))
        return f"{year:04d}-Q{(month - 1) // 3 + 1}"
    return period


def exact_series_from_workbook(content: bytes, series_id: str, source_url: str, frequency: str = "Q") -> tuple[list[Point], dict[str, Any]]:
    for book in workbook_rows(content):
        rows = book["rows"]
        for id_row, row in enumerate(rows):
            for value_col, cell in enumerate(row):
                if clean(cell).upper() != series_id.upper():
                    continue
                values: dict[str, float] = {}
                for data_row in rows[id_row + 1:]:
                    if not data_row:
                        continue
                    period = excel_period(data_row[0], frequency)
                    if period and value_col < len(data_row):
                        value = number(data_row[value_col])
                        if value is not None:
                            values[period] = value
                # ABS repeats each Series ID in the Index sheet and in Data1.
                # The Index occurrence only contains metadata, so keep scanning
                # until the occurrence followed by dated observations is found.
                if not values:
                    continue
                points = [Point(period, value, source_url, note=f"sheet={book['sheet']}; series={series_id}") for period, value in sorted(values.items())]
                return points, {"sheet": book["sheet"], "series_id": series_id, "series_id_row": id_row + 1, "value_col": value_col + 1, "observation_count": len(values)}
    raise RuntimeError(f"Series ID {series_id} was found only in metadata sheets or had no dated observations")


def month_shift(value: date, months: int) -> date:
    total = value.year * 12 + value.month - 1 + months
    return date(total // 12, total % 12 + 1, 1)


def discover_latest_anz_job_ads() -> tuple[requests.Response, dict[str, Any]]:
    """Find the newest ANZ-Indeed Job Ads workbook.

    ANZ publishes data for month T in the following month's folder.  Start with
    the latest theoretically available data month and step backwards.  The
    official release-dates page is retained in diagnostics, while generated
    URLs make the updater independent of a manually maintained month URL.
    """
    today = datetime.now(timezone.utc).date().replace(day=1)
    release_page = "https://www.anz.com.au/newsroom/media/release-dates/"
    discovery: dict[str, Any] = {"release_page": release_page, "attempts": []}
    try:
        page = get(release_page)
        soup = BeautifulSoup(page.text, "html.parser")
        for anchor in soup.find_all("a", href=True):
            href = urljoin(page.url, anchor.get("href", ""))
            if re.search(r"ANZ-Indeed.*Job.*Ads.*data.*\.xlsx(?:$|\?)", href, re.I):
                try:
                    response = get(href)
                    if response.content.startswith(b"PK"):
                        discovery["discovered_from_page"] = response.url
                        return response, discovery
                except Exception as error:
                    discovery["attempts"].append({"url": href, "error": f"{type(error).__name__}: {error}"})
    except Exception as error:
        discovery["release_page_error"] = f"{type(error).__name__}: {error}"

    # A release folder normally contains the prior month's data.  Test the
    # current release month first, then future/previous release folders to
    # tolerate early and delayed publication timing.
    release_months = [month_shift(today, offset) for offset in (1, 0, -1, -2, -3, -4)]
    hosts = ("www.anz.com.au", "www.exclusives.anz.com.au")
    for release_month in release_months:
        data_month = month_shift(release_month, -1)
        folder = release_month.strftime("%Y/%B").lower()
        data_tokens = [data_month.strftime("%b%y"), data_month.strftime("%B%y")]
        for host in hosts:
            for token in data_tokens:
                url = (
                    f"https://{host}/content/dam/anzcomau/mediacentre/pdfs/jobads/"
                    f"{folder}/ANZ-Indeed%20Australian%20Job%20Ads%20data_{token}.xlsx"
                )
                try:
                    response = get(url)
                    valid = response.content.startswith(b"PK")
                    discovery["attempts"].append({"url": response.url, "valid_xlsx": valid})
                    if valid:
                        discovery["selected_release_month"] = release_month.strftime("%Y-%m")
                        discovery["selected_data_month"] = data_month.strftime("%Y-%m")
                        return response, discovery
                except Exception as error:
                    discovery["attempts"].append({"url": url, "error": f"{type(error).__name__}: {error}"})
    raise RuntimeError("No current ANZ-Indeed Job Ads XLSX found")


def fetch_anz_job_ads(expected: dict[str, float]) -> tuple[list[Point], dict[str, Any]]:
    response, discovery = discover_latest_anz_job_ads()
    (OUT / "anz_job_ads_raw.xlsx").write_bytes(response.content)
    books = workbook_rows(response.content)
    candidates: list[dict[str, Any]] = []
    for book in books:
        rows = book["rows"]
        for date_col in range(0, min(5, max((len(row) for row in rows), default=0))):
            periods: dict[int, str] = {}
            for index, row in enumerate(rows):
                if date_col >= len(row):
                    continue
                value = row[date_col]
                if hasattr(value, "year") and hasattr(value, "month"):
                    periods[index] = f"{value.year:04d}-{value.month:02d}"
                else:
                    period = period_key(value)
                    if period:
                        periods[index] = period
            if len(periods) < 10:
                continue
            max_cols = max((len(row) for row in rows), default=0)
            for value_col in range(max_cols):
                values: dict[str, float] = {}
                for index, period in periods.items():
                    if value_col < len(rows[index]):
                        value = number(rows[index][value_col])
                        if value is not None:
                            values[period] = value
                common = sorted(set(values) & set(expected))
                if not common:
                    continue
                mae = sum(abs(values[p] - expected[p]) for p in common) / len(common)
                candidates.append({"sheet": book["sheet"], "date_col": date_col + 1, "value_col": value_col + 1, "matches": len(common), "mae": mae, "values": values})
    candidates.sort(key=lambda item: (-item["matches"], item["mae"]))
    if not candidates:
        raise RuntimeError("ANZ XLSX contained no series matching reference periods")
    best = candidates[0]
    points = [Point(period, value, response.url, note=f"sheet={best['sheet']}; col={best['value_col']}") for period, value in sorted(best["values"].items())]
    return points, {
        "request_url": response.url,
        "discovery": discovery,
        "candidates": [{k: v for k, v in item.items() if k != "values"} for item in candidates[:30]],
    }

def fetch_abs_workbook_candidate(
    urls: list[str],
    expected: dict[str, float],
    raw_name: str,
    note: str,
) -> tuple[list[Point], dict[str, Any]]:
    errors: list[str] = []
    for url in urls:
        try:
            response = get(url)
            (OUT / raw_name).write_bytes(response.content)
            books = workbook_rows(response.content)
            candidates: list[dict[str, Any]] = []
            for book in books:
                rows = book["rows"]
                max_cols = max((len(row) for row in rows), default=0)
                for date_col in range(max_cols):
                    dates: dict[int, str] = {}
                    for row_index, row in enumerate(rows):
                        if date_col >= len(row):
                            continue
                        period = period_key(row[date_col])
                        if period:
                            dates[row_index] = period
                    if not dates:
                        continue
                    for value_col in range(max_cols):
                        values: dict[str, float] = {}
                        for row_index, period in dates.items():
                            if value_col < len(rows[row_index]):
                                value = number(rows[row_index][value_col])
                                if value is not None:
                                    values[period] = value
                        # First compare a directly published YoY column.
                        common = sorted(set(values) & set(expected))
                        if common:
                            diffs = [abs(values[item] - expected[item]) for item in common]
                            candidates.append({
                                "sheet": book["sheet"], "date_col": date_col + 1,
                                "value_col": value_col + 1, "transform": "level",
                                "matches": len(common), "mae": sum(diffs) / len(diffs),
                                "values": values,
                            })
                        # Also test YoY calculated from quarterly level columns.
                        ordered = sorted(values)
                        yoy = {
                            ordered[index]: (values[ordered[index]] / values[ordered[index - 4]] - 1.0) * 100.0
                            for index in range(4, len(ordered))
                            if values[ordered[index - 4]] != 0
                        }
                        common_yoy = sorted(set(yoy) & set(expected))
                        if common_yoy:
                            diffs = [abs(yoy[item] - expected[item]) for item in common_yoy]
                            candidates.append({
                                "sheet": book["sheet"], "date_col": date_col + 1,
                                "value_col": value_col + 1, "transform": "yoy_pct_q",
                                "matches": len(common_yoy), "mae": sum(diffs) / len(diffs),
                                "values": yoy,
                            })
            candidates.sort(key=lambda item: (-item["matches"], item["mae"]))
            if not candidates:
                raise RuntimeError("workbook contained no quarterly candidate series")
            best = candidates[0]
            points = [
                Point(period, value, response.url, note=f"{note}; sheet={best['sheet']}; col={best['value_col']}; transform={best['transform']}")
                for period, value in sorted(best["values"].items())
            ]
            return points, {
                "request_url": response.url,
                "note": note,
                "candidates": [{key: value for key, value in item.items() if key != "values"} for item in candidates[:50]],
            }
        except Exception as error:
            errors.append(f"{url}: {type(error).__name__}: {error}")
    raise RuntimeError("ABS national accounts workbook attempts failed: " + " | ".join(errors))


def discover_abs_workbook(landing_urls: list[str], filename_stem: str, title_token: str, fallback_urls: list[str]) -> tuple[requests.Response, dict[str, Any]]:
    candidates: list[str] = []
    discovery: list[dict[str, Any]] = []
    for landing_url in landing_urls:
        try:
            page = get(landing_url)
            soup = BeautifulSoup(page.text, "html.parser")
            found: list[str] = []
            for anchor in soup.find_all("a", href=True):
                href = anchor.get("href", "")
                context = clean(" ".join([anchor.get_text(" ", strip=True), anchor.parent.get_text(" ", strip=True) if anchor.parent else ""]))
                filename_match = filename_stem.lower() in href.lower()
                title_match = title_token.lower() in context.lower()
                if (filename_match or title_match) and re.search(r"\.xlsx?$", href, re.I):
                    url = urljoin(page.url, href)
                    if url not in candidates:
                        candidates.append(url); found.append(url)
            discovery.append({"landing_url": page.url, "found": found})
        except Exception as error:
            discovery.append({"landing_url": landing_url, "error": f"{type(error).__name__}: {error}"})
    for url in fallback_urls:
        if url not in candidates:
            candidates.append(url)
    errors=[]
    for url in candidates:
        try:
            response=get(url)
            if response.content.startswith((b"PK", bytes.fromhex("D0CF11E0"))):
                return response, {"discovery": discovery, "candidates": candidates}
            errors.append(f"{url}: invalid workbook signature")
        except Exception as error:
            errors.append(f"{url}: {type(error).__name__}: {error}")
    raise RuntimeError("Official workbook discovery/download failed: " + " | ".join(errors))


def fetch_expected_to_leave_total() -> tuple[list[Point], dict[str, Any]]:
    response, discovery = discover_abs_workbook(
        [
            "https://www.abs.gov.au/statistics/labour/employment-and-unemployment/labour-force-australia/latest-release",
            "https://www.abs.gov.au/statistics/labour/employment-and-unemployment/labour-force-australia-detailed/latest-release",
        ],
        "6291017", "Table 17",
        ["https://www.abs.gov.au/statistics/labour/employment-and-unemployment/labour-force-australia-detailed/mar-2026/6291017.xlsx"],
    )
    (OUT / "abs_6291017_table17_raw.xlsx").write_bytes(response.content)
    points, selected = exact_series_from_workbook(response.content, "A85060262X", response.url, "Q")
    selected.update(discovery)
    selected["note"] = "ABS Table 17 Data1; Does not expect to be with current employer/business in 12 months; Employed total; Persons"
    return points, selected


def fetch_wpi_including_bonuses_yoy(series_id: str = "A2615579C") -> tuple[list[Point], dict[str, Any]]:
    response, discovery = discover_abs_workbook(
        ["https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/wage-price-index-australia/latest-release#data-downloads"],
        "634507b", "Table 7b",
        [],
    )
    suffix = ".xlsx" if response.content.startswith(b"PK") else ".xls"
    (OUT / f"abs_wpi_table_7b_raw{suffix}").write_bytes(response.content)
    levels, selected = exact_series_from_workbook(response.content, series_id, response.url, "Q")
    level_map = {point.period: point.value for point in levels}
    ordered = sorted(level_map)
    yoy = {ordered[index]: (level_map[ordered[index]] / level_map[ordered[index - 4]] - 1.0) * 100.0 for index in range(4, len(ordered)) if level_map[ordered[index - 4]] != 0}
    if not yoy:
        raise RuntimeError(f"ABS WPI series {series_id} found but YoY could not be calculated")
    points = [Point(period, value, response.url, note=f"Table 7b Data1; series={series_id}; calculated from quarterly index") for period, value in sorted(yoy.items())]
    selected.update(discovery)
    selected["latest_index_levels"] = [{"period": key, "value": level_map[key]} for key in ordered[-12:]]
    selected["note"] = "Official ABS Table 7b; A2615579C Total hourly rates including bonuses, Private and Public, original; YoY from index levels"
    return points, selected


def discover_westpac_consumer_sentiment_reports(months_back: int = 8) -> list[dict[str, Any]]:
    """Discover recent official Westpac-MI Consumer Sentiment PDFs.

    Westpac IQ article URLs are stable by reference month and link to the full
    official bulletin PDF.  Discover from the article rather than guessing the
    PDF publication day, then retain recent reports so revisions/history can be
    refreshed as well as the latest observation.
    """
    current_month = datetime.now(timezone.utc).date().replace(day=1)
    reports: list[dict[str, Any]] = []
    attempts: list[dict[str, Any]] = []
    seen_pdfs: set[str] = set()

    for offset in range(0, -months_back, -1):
        reference_date = month_shift(current_month, offset)
        period = reference_date.strftime("%Y-%m")
        month_name = reference_date.strftime("%B").lower()
        article_url = (
            f"https://www.westpaciq.com.au/economics/{reference_date:%Y/%m}/"
            f"consumer-sentiment-{month_name}-{reference_date:%Y}"
        )
        try:
            article = get(article_url)
            soup = BeautifulSoup(article.text, "html.parser")
            pdf_urls: list[str] = []
            for anchor in soup.find_all("a", href=True):
                href = urljoin(article.url, anchor.get("href", ""))
                anchor_text = clean(anchor.get_text(" ", strip=True))
                if re.search(r"BullConsumerSentiment\.pdf(?:$|\?)", href, re.I) or (
                    href.lower().endswith(".pdf")
                    and "consumer sentiment" in anchor_text.lower()
                ):
                    pdf_urls.append(href)
            attempts.append({"period": period, "article_url": article.url, "pdf_urls": pdf_urls})
            for pdf_url in pdf_urls:
                if pdf_url in seen_pdfs:
                    continue
                reports.append({
                    "period": period,
                    "month_name": reference_date.strftime("%B"),
                    "article_url": article.url,
                    "pdf_url": pdf_url,
                })
                seen_pdfs.add(pdf_url)
        except Exception as error:
            attempts.append({
                "period": period,
                "article_url": article_url,
                "error": f"{type(error).__name__}: {error}",
            })

    (OUT / "westpac_consumer_sentiment_discovery.json").write_text(
        json.dumps({"reports": reports, "attempts": attempts}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    if not reports:
        raise RuntimeError("No recent official Westpac-MI Consumer Sentiment PDF discovered")
    return reports


def extract_westpac_unemployment_expectations(text: str, month_name: str) -> float | None:
    """Extract the current-month Unemployment Expectations Index from a bulletin."""
    compact = clean(text).replace("−", "-").replace("–", "-")
    escaped_month = re.escape(month_name)
    patterns = [
        # Narrative wording, e.g. "increased to 135.7 in August from 129.9 in July".
        rf"(?:Westpac(?:-Melbourne Institute)?\s+)?Unemployment Expectations(?: Index)?"
        rf".{{0,180}}?\b(?:increased|decreased|rose|fell|lifted|declined|dropped|edged)\b"
        rf".{{0,120}}?\b(?:to|at|of)\s+([0-9]{{2,3}}(?:\.[0-9]+)?)\s+in\s+{escaped_month}\b",
        # Simpler narrative wording used in some older bulletins.
        r"Unemployment Expectations Index\s+(?:increased|decreased|rose|fell|lifted|declined|dropped)"
        r"(?:\s+[0-9]+(?:\.[0-9]+)?%)?\s+to\s+([0-9]{2,3}(?:\.[0-9]+)?)",
        # Table fallback: row label followed by historical columns and current-month value.
        r"Unemployment Expectations Index\s+"
        r"(?:[0-9]{2,3}(?:\.[0-9]+)?\s+){3,8}([0-9]{2,3}(?:\.[0-9]+)?)\s+"
        r"[+-]?[0-9]+(?:\.[0-9]+)?\s+[+-]?[0-9]+(?:\.[0-9]+)?",
    ]
    for priority, pattern in enumerate(patterns, 1):
        match = re.search(pattern, compact, re.I | re.S)
        if match:
            value = number(match.group(1))
            if value is not None and 50.0 <= value <= 250.0:
                log(f"[WESTPAC UNEMP PARSER] month={month_name} value={value} priority={priority}")
                return value
    return None


def fetch_westpac_unemployment_expectations() -> tuple[list[Point], dict[str, Any]]:
    reports = discover_westpac_consumer_sentiment_reports(months_back=8)
    points: list[Point] = []
    attempts: list[dict[str, Any]] = []

    for report in reports:
        try:
            response = get(report["pdf_url"])
            if not response.content.startswith(b"%PDF"):
                raise RuntimeError("Downloaded Westpac report is not a PDF")
            raw_name = f"westpac_consumer_sentiment_{report['period']}.pdf"
            (OUT / raw_name).write_bytes(response.content)
            reader = PdfReader(io.BytesIO(response.content))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
            value = extract_westpac_unemployment_expectations(text, report["month_name"])
            attempt = {
                **report,
                "resolved_pdf_url": response.url,
                "pages": len(reader.pages),
                "text_length": len(text),
                "value": value,
            }
            attempts.append(attempt)
            if value is not None:
                points.append(Point(
                    report["period"],
                    value,
                    response.url,
                    status="final",
                    note="Official Westpac-Melbourne Institute Consumer Sentiment Bulletin PDF",
                ))
        except Exception as error:
            attempts.append({**report, "error": f"{type(error).__name__}: {error}"})

    (OUT / "westpac_unemployment_expectations_parsed.json").write_text(
        json.dumps(attempts, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    points = dedupe(points)
    if not points:
        raise RuntimeError("No unemployment expectations value parsed from recent Westpac bulletins")
    return points, {
        "note": "Official Westpac IQ article discovery; linked Westpac-MI bulletin PDFs",
        "reports_processed": len(reports),
        "parsed_periods": [point.period for point in points],
        "attempts": attempts,
    }


def official_html_value(url: str, patterns: list[str], period: str, raw_name: str) -> list[Point]:
    response = get(url)
    (OUT / raw_name).write_bytes(response.content)
    visible_text = clean(BeautifulSoup(response.text, "html.parser").get_text(" ", strip=True)).replace("−", "-")
    raw_text = html.unescape(response.text).replace("−", "-")
    for haystack in (visible_text, raw_text):
        for pattern in patterns:
            match = re.search(pattern, haystack, re.I | re.S)
            if match:
                value = number(match.group(1))
                if value is not None:
                    return [Point(period, value, response.url)]
    raise RuntimeError("Official HTML value not parsed")



SP_RELEASES_URL = "https://www.pmi.spglobal.com/Public/Release/PressReleases"
SP_RELEASE_CANDIDATES_CACHE: list[dict[str, str]] | None = None
SP_RELEASE_TEXT_CACHE: dict[str, tuple[requests.Response, str]] = {}


def sp_response_to_text(response: requests.Response) -> str:
    content_type = (response.headers.get("content-type") or "").lower()
    if response.content.startswith(b"%PDF") or "application/pdf" in content_type:
        reader = PdfReader(io.BytesIO(response.content))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    return BeautifulSoup(response.text, "html.parser").get_text("\n", strip=True)


def sp_preceding_context(anchor: Any) -> str:
    parts: list[str] = []
    for element in anchor.previous_elements:
        if isinstance(element, NavigableString):
            text = clean(str(element))
            if text:
                parts.append(text)
        if len(" ".join(parts)) >= 320:
            break
    return " ".join(reversed(parts[-24:]))


def parse_sp_release_date(value: str) -> datetime | None:
    text = clean(value)
    if not text:
        return None
    for format_value in ("%B %d %Y", "%b %d %Y"):
        try:
            return datetime.strptime(text, format_value).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def month_name_to_period(month_name: str, year: str) -> str:
    month_map = {name.lower(): index for index, name in enumerate(
        "January February March April May June July August September October November December".split(), 1
    )}
    return f"{int(year):04d}-{month_map[month_name.lower()]:02d}"


def extract_sp_reference_month(text: str) -> str | None:
    """Extract the PMI survey reference month, never the publication month.

    Final sector reports are normally released in the following month.  The
    most reliable marker is S&P's "Data were collected ... <Month> <Year>"
    note.  Narrative references beside the headline index are second-best.
    Embargo/publication dates are used only to supply the year, never the month.
    """
    compact = clean(text).replace("™", "").replace("®", "")
    month = r"(January|February|March|April|May|June|July|August|September|October|November|December)"

    # 1. Highest confidence: survey collection dates explicitly identify the
    # reference month, e.g. "Data were collected 9-28 July 2026".
    collected_patterns = [
        rf"Data were collected.{{0,120}}?\b{month}\s+(20\d{{2}})\b",
        rf"Data collection.{{0,120}}?\b{month}\s+(20\d{{2}})\b",
        rf"Survey responses were collected.{{0,120}}?\b{month}\s+(20\d{{2}})\b",
    ]
    for pattern in collected_patterns:
        match = re.search(pattern, compact, re.I | re.S)
        if match:
            return month_name_to_period(match.group(1), match.group(2))

    # Determine the release year without using its month.  This handles final
    # July data released in August 2026.
    year_match = re.search(r"Embargoed until.{0,100}?\b(20\d{2})\b", compact, re.I | re.S)
    if not year_match:
        year_match = re.search(r"\b(20\d{2})\b", compact)
    release_year = year_match.group(1) if year_match else None

    # 2. Headline narrative: "posted 52.0 in July" or "increased ... 53.6 in July".
    narrative_patterns = [
        rf"Australia Manufacturing Purchasing Managers['’]? Index.{{0,240}}?\b(?:posted|registered|stood|rose|fell|increased|decreased)\b.{{0,140}}?\bin\s+{month}\b",
        rf"Australia Services PMI Business Activity Index.{{0,260}}?\b(?:posted|registered|stood|rose|fell|increased|decreased)\b.{{0,160}}?\bin\s+{month}\b",
        rf"Flash Australia (?:Composite|Services|Manufacturing) PMI.{{0,160}}?\bin\s+{month}\b",
    ]
    if release_year:
        for pattern in narrative_patterns:
            match = re.search(pattern, compact, re.I | re.S)
            if match:
                reference_month = match.group(1)
                reference_year = int(release_year)
                # January data may be released in February of the same year;
                # December data may be released in January of the next year.
                release_month_match = re.search(rf"Embargoed until.{{0,80}}?\b{month}\s+\d{{1,2}}\s+20\d{{2}}", compact, re.I | re.S)
                if release_month_match:
                    month_order = {name.lower(): i for i, name in enumerate(
                        "January February March April May June July August September October November December".split(), 1
                    )}
                    release_month_number = month_order[release_month_match.group(1).lower()]
                    reference_month_number = month_order[reference_month.lower()]
                    if release_month_number == 1 and reference_month_number == 12:
                        reference_year -= 1
                return month_name_to_period(reference_month, str(reference_year))

    # 3. Report-body month label after the title.  Keep the window tight and
    # reject a month equal to the embargo month when a prior-month label exists.
    title_patterns = [
        r"S&P Global Flash Australia PMI",
        r"S&P Global Australia Manufacturing PMI",
        r"S&P Global Australia Services PMI",
    ]
    for title_pattern in title_patterns:
        title_matches = list(re.finditer(title_pattern, compact, re.I))
        for title_match in reversed(title_matches):
            after_title = compact[title_match.end():title_match.end() + 700]
            reference_match = re.search(rf"\b{month}\s+(20\d{{2}})\b", after_title, re.I)
            if reference_match:
                return month_name_to_period(reference_match.group(1), reference_match.group(2))
    return None


def discover_australia_pmi_releases() -> list[dict[str, str]]:
    global SP_RELEASE_CANDIDATES_CACHE
    if SP_RELEASE_CANDIDATES_CACHE is not None:
        return SP_RELEASE_CANDIDATES_CACHE
    response = get(SP_RELEASES_URL)
    (OUT / "sp_global_release_calendar.html").write_bytes(response.content)
    soup = BeautifulSoup(response.text, "html.parser")
    candidates: list[dict[str, str]] = []
    seen: set[str] = set()
    for anchor in soup.find_all("a", href=True):
        href = anchor.get("href", "")
        if "/Public/Home/PressRelease/" not in href:
            continue
        url = urljoin(SP_RELEASES_URL, href)
        if url in seen:
            continue
        context = clean(" ".join(part for part in (
            anchor.get_text(" ", strip=True),
            anchor.parent.get_text(" ", strip=True) if anchor.parent else "",
            sp_preceding_context(anchor),
        ) if part))
        # Keep all three official Australia release types:
        # combined Flash, final Manufacturing, and final Services.
        title_match = re.search(
            r"((?:S&P Global\s+)?(?:Flash\s+)?Australia(?:\s+(?:Manufacturing|Services))?\s+PMI(?:[^|]{0,100})?)",
            context,
            re.I,
        )
        if not title_match:
            continue
        title = clean(title_match.group(1))
        release_date_match = re.search(
            r"([A-Za-z]+\s+\d{1,2},?\s+20\d{2})\s+\d{2}:\d{2}\s+UTC",
            context,
            re.I,
        )
        candidates.append({
            "title": title,
            "index_context": context,
            "url": url,
            "release_date": release_date_match.group(1).replace(",", "") if release_date_match else "",
        })
        seen.add(url)
    cutoff = datetime.now(timezone.utc) - timedelta(days=210)
    recent_candidates = [
        candidate for candidate in candidates
        if (parse_sp_release_date(candidate.get("release_date", "")) or datetime.min.replace(tzinfo=timezone.utc)) >= cutoff
    ]
    if not recent_candidates:
        recent_candidates = candidates[:60]
    recent_candidates.sort(
        key=lambda item: parse_sp_release_date(item.get("release_date", ""))
        or datetime.min.replace(tzinfo=timezone.utc),
        reverse=True,
    )
    (OUT / "sp_global_australia_release_candidates.json").write_text(
        json.dumps(recent_candidates, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    log(f"[S&P PMI] Australia discovered={len(candidates)} recent_to_process={len(recent_candidates)}")
    SP_RELEASE_CANDIDATES_CACHE = recent_candidates
    return recent_candidates


def fetch_sp_release_text(url: str) -> tuple[requests.Response, str]:
    cached = SP_RELEASE_TEXT_CACHE.get(url)
    if cached is not None:
        return cached
    response = get(url)
    text = sp_response_to_text(response)
    if not text.strip():
        raise RuntimeError(f"Empty S&P release body: {url}")
    SP_RELEASE_TEXT_CACHE[url] = (response, text)
    # Gentle pacing reduces transient HTTP 202 responses from S&P.
    time.sleep(0.35)
    return response, text


def classify_sp_australia_release(title: str, text: str) -> str | None:
    """Return flash, manufacturing_final, or services_final."""
    sample = clean(f"{title} {text[:2500]}").replace("™", "").replace("®", "")
    if re.search(r"S&P Global Flash Australia PMI|Flash Australia Composite PMI", sample, re.I):
        return "flash"
    if re.search(r"S&P Global Australia Manufacturing PMI", sample, re.I):
        return "manufacturing_final"
    if re.search(r"S&P Global Australia Services PMI", sample, re.I):
        return "services_final"
    return None


def extract_australia_pmi_value(text: str, sector: str, release_kind: str) -> float | None:
    compact = clean(text).replace("™", "").replace("®", "")
    number_pattern = r"([0-9]{1,2}(?:\.[0-9]+)?)"
    if sector == "manufacturing":
        patterns = []
        if release_kind == "flash":
            patterns.extend([
                rf"\bFlash Australia Manufacturing PMI\s*:\s*{number_pattern}\b",
                rf"\bFlash Australia Manufacturing PMI\b.{{0,80}}?{number_pattern}\b",
            ])
        patterns.extend([
            # Final release wording: "... Index (PMI) posted 52.0 in July"
            r"\bheadline seasonally adjusted S&P Global Australia Manufacturing Purchasing Managers['’]? Index"
            rf".{{0,180}}?\b(?:posted|registered|stood at|rose to|fell to)\s+{number_pattern}\b",
            r"\bS&P Global Australia Manufacturing PMI\b"
            rf".{{0,180}}?\b(?:posted|registered|stood at|rose to|fell to)\s+{number_pattern}\b",
        ])
    else:
        patterns = []
        if release_kind == "flash":
            patterns.extend([
                rf"\bFlash Australia Services PMI Business Activity Index\s*:\s*{number_pattern}\b",
                rf"\bFlash Australia Services PMI Business Activity Index\b.{{0,80}}?{number_pattern}\b",
            ])
        patterns.extend([
            # Final release wording: "... Index increased to a six-month high of 53.6 in July"
            r"\bseasonally adjusted S&P Global Australia Services PMI Business Activity Index\b"
            rf".{{0,220}}?\b(?:increased|decreased|rose|fell|posted|registered|stood)\b.{{0,100}}?\b(?:to|at|of)\s+{number_pattern}\b",
            r"\bS&P Global Australia Services PMI Business Activity Index\b"
            rf".{{0,220}}?\b(?:increased|decreased|rose|fell|posted|registered|stood)\b.{{0,100}}?\b(?:to|at|of)\s+{number_pattern}\b",
        ])
    for priority, pattern in enumerate(patterns, 1):
        for match in re.finditer(pattern, compact, re.I | re.S):
            value = float(match.group(1))
            context = compact[max(0, match.start() - 120):match.end() + 150]
            if 20.0 <= value <= 80.0 and not (value == 50.0 and re.search(r">\s*50|50\s*=", context)):
                log(f"[S&P PMI PARSER] kind={release_kind} sector={sector} value={value} priority={priority}")
                return value
    return None


def extract_previous_pmi_value(text: str, sector: str) -> tuple[str, float] | None:
    compact = clean(text).replace("™", "").replace("®", "")
    label = (
        r"Flash Australia Manufacturing PMI"
        if sector == "manufacturing"
        else r"Flash Australia Services PMI Business Activity Index"
    )
    match = re.search(
        label + r"\s*:\s*[0-9]{1,2}(?:\.[0-9]+)?\s*\(\s*([A-Za-z]{3})\s*:\s*([0-9]{1,2}(?:\.[0-9]+)?)\s*\)",
        compact,
        re.I,
    )
    if not match:
        return None
    month_map = {name.lower(): index for index, name in enumerate(
        "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(), 1
    )}
    month = month_map.get(match.group(1).lower())
    return (f"{month:02d}", float(match.group(2))) if month else None


def sp_australia_pmi(label: str) -> tuple[list[Point], dict[str, Any]]:
    """Fetch only the newest Australia flash PMI release.

    The production updater only needs the newest observation.  The former
    implementation opened every Australia PMI release from the last 210 days,
    then retried transient HTTP 202 responses five times.  That was useful for
    historical validation but unnecessarily slow for a routine update.

    This fast path scans at most the newest three release links, stops as soon
    as it finds a combined Flash Australia PMI release, and uses a short request
    timeout without retrying HTTP 202.  The same flash release contains both
    manufacturing and services values, so the in-memory cache makes the second
    PMI target effectively free during the same run.
    """
    sector = "manufacturing" if label == "製造業PMI" else "services"
    candidates = discover_australia_pmi_releases()[:3]
    attempts: list[dict[str, Any]] = []

    for candidate in candidates:
        url = candidate["url"]
        try:
            cached = SP_RELEASE_TEXT_CACHE.get(url)
            if cached is not None:
                response, text = cached
            else:
                started = time.perf_counter()
                response = SESSION.get(url, timeout=(2.5, 4.0), allow_redirects=True)
                elapsed = time.perf_counter() - started
                log(f"[S&P PMI FAST HTTP] {response.status_code} {response.url} bytes={len(response.content)} elapsed={elapsed:.3f}s")
                if response.status_code != 200 or not response.content:
                    attempts.append({
                        "url": response.url,
                        "status": response.status_code,
                        "error": "Skipped without retry; fast PMI mode",
                    })
                    continue
                response.raise_for_status()
                text = sp_response_to_text(response)
                if not text.strip():
                    attempts.append({"url": response.url, "error": "Empty release body"})
                    continue
                SP_RELEASE_TEXT_CACHE[url] = (response, text)

            release_kind = classify_sp_australia_release(candidate.get("title", ""), text)
            if release_kind != "flash":
                attempts.append({
                    "url": response.url,
                    "release_kind": release_kind,
                    "skipped": "Not the newest combined flash release",
                })
                continue

            reference_month = extract_sp_reference_month(text)
            value = extract_australia_pmi_value(text, sector, "flash")
            attempt = {
                "url": response.url,
                "title": candidate.get("title", ""),
                "release_date": candidate.get("release_date", ""),
                "release_kind": release_kind,
                "reference_month": reference_month,
                "value": value,
                "text_length": len(text),
            }
            attempts.append(attempt)
            if reference_month is None or value is None:
                continue

            point = Point(
                reference_month,
                value,
                response.url,
                status="flash",
                note=f"Latest S&P Flash Australia {sector} PMI; release={candidate.get('release_date', '')}",
            )
            (OUT / f"sp_global_australia_{sector}_release_parsed.json").write_text(
                json.dumps(attempts, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            return [point], {
                "note": "Fast mode: newest combined Flash Australia PMI only; maximum three release-page requests; no retry on HTTP 202",
                "sector": sector,
                "selected_release": attempt,
                "candidates_checked": len(attempts),
            }
        except (requests.Timeout, requests.ConnectionError) as error:
            attempts.append({"url": url, "error": f"{type(error).__name__}: {error}", "retry": False})
        except Exception as error:
            attempts.append({"url": url, "error": f"{type(error).__name__}: {error}"})

    (OUT / f"sp_global_australia_{sector}_release_parsed.json").write_text(
        json.dumps(attempts, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    raise RuntimeError(
        f"Fast PMI mode could not parse the latest Australia {sector} flash PMI from the newest three releases"
    )

def pdf_value(url: str, patterns: list[str], period: str, raw_name: str) -> list[Point]:
    response = get(url)
    (OUT / raw_name).write_bytes(response.content)
    reader = PdfReader(io.BytesIO(response.content))
    text = clean(" ".join(page.extract_text() or "" for page in reader.pages)).replace("−", "-")
    for pattern in patterns:
        match = re.search(pattern, text, re.I | re.S)
        if match:
            value = number(match.group(1))
            if value is not None:
                return [Point(period, value, response.url)]
    raise RuntimeError("Official PDF value not parsed")


def compare(expected: dict[str, float], points: list[Point], tolerance: float = 0.051) -> dict[str, Any]:
    mapping = {point.period: point for point in points}
    rows = []
    for period, expected_value in sorted(expected.items(), reverse=True):
        point = mapping.get(period)
        difference = None if point is None else point.value - expected_value
        rows.append({
            "period": period,
            "expected": expected_value,
            "official": None if point is None else point.value,
            "difference": difference,
            "match": point is not None and abs(difference) <= tolerance,
        })
    available = [row for row in rows if row["official"] is not None]
    if not expected:
        status = "OFFICIAL_ONLY" if points else "NO_DATA"
    elif len(available) == len(rows) and all(row["match"] for row in rows):
        status = "MATCH_ALL"
    elif available and all(row["match"] for row in available):
        status = "MATCH_AVAILABLE"
    elif available:
        status = "VALUE_MISMATCH"
    else:
        status = "NO_SAME_PERIOD"
    return {"status": status, "rows": rows}


TARGETS = [
    Target("就業新增", "M", {"2026-06": 76.3, "2026-05": 44.0, "2026-04": -38.6}, "API/CSV", "ABS LF"),
    Target("失業率", "M", {"2026-06": 4.428344, "2026-05": 4.3713481, "2026-04": 4.4904846}, "API/CSV", "ABS LF"),
    Target("職缺", "Q", {"2026-05": 329.5}, "API/CSV", "ABS JV"),
    Target("ANZ職缺廣告", "M", {"2026-06": 115.837847, "2026-05": 116.016520, "2026-04": 113.793843}, "XLSX", "ANZ official download"),
    Target("時薪YoY", "Q", {}, "API/CSV", "ABS WPI candidate"),
    Target("預計離職", "A", {}, "XLSX", "ABS Job Mobility"),
    Target("失業預期", "M", {"2026-07": 129.924065, "2026-06": 139.834025, "2026-05": 140.019870, "2026-04": 147.758451}, "HTML", "Westpac-Melbourne Institute official release"),
    Target("CPI YoY", "M", {"2026-06": 3.8, "2026-05": 4.0, "2026-04": 4.2}, "API/CSV", "ABS CPI_MONTHLY"),
    Target("Trimmed Mean YoY", "M", {"2026-06": 3.6, "2026-05": 3.6, "2026-04": 3.4}, "API/CSV", "ABS CPI_MONTHLY"),
    Target("零售", "M", {"2026-06": 7.0, "2026-05": 4.3}, "API/CSV", "ABS HSI_M Retail spending YoY original"),
    Target("NAB企業售價", "M", {"2026-06": 0.59057, "2026-05": 0.92126, "2026-04": 1.79622}, "PDF", "NAB Monthly Business Survey"),
    Target("消費信心", "M", {"2026-07": 83.933514, "2026-06": 80.612096, "2026-05": 82.978906, "2026-04": 80.149167}, "HTML", "Westpac-Melbourne Institute official release"),
    Target("製造業PMI", "M", {"2026-07": 51.7, "2026-06": 51.5, "2026-05": 50.7, "2026-04": 51.3}, "HTML", "S&P Global official releases"),
    Target("服務業PMI", "M", {"2026-07": 53.0, "2026-06": 50.5, "2026-05": 48.7, "2026-04": 50.7}, "HTML", "S&P Global official releases"),
    Target("GDP YoY", "Q", {"2026-Q1": 2.51974}, "API/CSV", "ABS ANA_AGG"),
    Target("GDP私人消費YoY", "Q", {"2026-Q1": 2.4728}, "API/CSV", "ABS ANA_AGG"),
    Target("GDP投資YoY", "Q", {"2026-Q1": 6.47494}, "API/CSV", "ABS ANA_AGG"),
]


def run_target(target: Target) -> tuple[list[Point], dict[str, Any]]:
    label = target.label
    if label == "就業新增":
        return fetch_abs_target("LF", "2025-01", ["employed", "persons", "australia", "seasonally adjusted"], ["rate", "hours", "state"], target.expected, "mom_diff")
    if label == "失業率":
        return fetch_abs_target("LF", "2025-01", ["unemployment rate", "australia", "seasonally adjusted"], ["state", "youth"], target.expected)
    if label == "職缺":
        return fetch_abs_target("JV", "2025-01", ["job vacancies", "australia", "seasonally adjusted", "private and public"], ["trend", "original"], target.expected)
    if label == "ANZ職缺廣告":
        return fetch_anz_job_ads(target.expected)
    if label == "時薪YoY":
        return fetch_wpi_including_bonuses_yoy("A2615579C")
    if label == "預計離職":
        return fetch_expected_to_leave_total()
    if label == "CPI YoY":
        return fetch_abs_target("CPI_MONTHLY", "2025-01", ["all groups", "australia", "annual"], ["trimmed", "quarterly"], target.expected)
    if label == "Trimmed Mean YoY":
        return fetch_abs_target("CPI_MONTHLY", "2025-01", ["trimmed mean", "australia", "annual"], [], target.expected)
    if label == "零售":
        return fetch_abs_target("HSI_M", "2025-01", ["retail spending", "australia", "original", "through the year"], ["seasonally adjusted", "trend", "monthly percentage change"], target.expected)
    if label == "NAB企業售價":
        # Discover recent official NAB Monthly Business Survey pages/PDFs instead
        # of keeping month-specific PDF URLs in the source code.
        current_month = datetime.now(timezone.utc).date().replace(day=1)
        points: list[Point] = []
        attempts: list[dict[str, Any]] = []
        patterns = [
            r"Product prices\s+(?:To\s*)?([+-]?\d+(?:\.\d+)?)%",
            r"product price growth.{0,160}?(?:at|to)\s*([+-]?\d+(?:\.\d+)?)%",
            r"product prices growth.{0,160}?(?:at|to)\s*([+-]?\d+(?:\.\d+)?)%",
        ]
        for offset in range(0, -4, -1):
            reference_date = month_shift(current_month, offset)
            period = reference_date.strftime("%Y-%m")
            month_slug = reference_date.strftime("%B").lower()
            page_urls = [
                f"https://www.nab.com.au/news/economy-markets/nab-business-survey-{month_slug}-{reference_date:%Y}",
                f"https://business.nab.com.au/nab-monthly-business-survey-{month_slug}-{reference_date:%Y}/",
            ]
            parsed = False
            for page_url in page_urls:
                try:
                    page = get(page_url)
                    soup = BeautifulSoup(page.text, "html.parser")
                    links = []
                    for anchor in soup.find_all("a", href=True):
                        href = urljoin(page.url, anchor.get("href", ""))
                        context = clean(anchor.get_text(" ", strip=True))
                        if href.lower().split("?")[0].endswith(".pdf") and (
                            "business survey" in context.lower() or "monthly business" in href.lower()
                        ):
                            links.append(href)
                    # Parse the HTML first, then its official report PDF if needed.
                    sources = [(page.url, clean(soup.get_text(" ", strip=True)), "html")]
                    for pdf_url in links[:2]:
                        response = get(pdf_url)
                        if response.content.startswith(b"%PDF"):
                            text = sp_response_to_text(response)
                            sources.append((response.url, clean(text), "pdf"))
                    for source_url, body, source_type in sources:
                        for pattern in patterns:
                            match = re.search(pattern, body, re.I | re.S)
                            if match:
                                value = number(match.group(1))
                                if value is not None:
                                    points.append(Point(period, value, source_url, status="final", note="Official NAB Monthly Business Survey; product prices quarterly rate"))
                                    attempts.append({"period": period, "url": source_url, "source_type": source_type, "value": value})
                                    parsed = True
                                    break
                        if parsed:
                            break
                    if parsed:
                        break
                except Exception as error:
                    attempts.append({"period": period, "url": page_url, "error": f"{type(error).__name__}: {error}"})
            if parsed:
                break
        if not points:
            raise RuntimeError("No latest NAB product prices value parsed from dynamically discovered official release")
        return points, {"note": "Dynamic official NAB release discovery; no month-specific URLs", "attempts": attempts}
    if label == "消費信心":
        # Reuse dynamic Westpac IQ discovery and parse the newest linked bulletin.
        reports = discover_westpac_consumer_sentiment_reports(months_back=4)
        points: list[Point] = []
        attempts: list[dict[str, Any]] = []
        patterns = [
            r"Consumer Sentiment Index\s+(?:rose|fell|increased|decreased|lifted|declined|dropped).{0,100}?\bto\s+([0-9]{2,3}(?:\.[0-9]+)?)",
            r"Consumer Sentiment Index.{0,100}?\b(?:at|of)\s+([0-9]{2,3}(?:\.[0-9]+)?)",
        ]
        for report in sorted(reports, key=lambda item: item["period"], reverse=True):
            try:
                response = get(report["pdf_url"])
                if not response.content.startswith(b"%PDF"):
                    raise RuntimeError("Downloaded Westpac report is not a PDF")
                text = clean(sp_response_to_text(response))
                value = None
                for pattern in patterns:
                    match = re.search(pattern, text, re.I | re.S)
                    if match:
                        value = number(match.group(1))
                        if value is not None:
                            break
                attempts.append({"period": report["period"], "url": response.url, "value": value})
                if value is not None:
                    points.append(Point(report["period"], value, response.url, status="final", note="Official Westpac-Melbourne Institute Consumer Sentiment Bulletin"))
                    break
            except Exception as error:
                attempts.append({**report, "error": f"{type(error).__name__}: {error}"})
        if not points:
            raise RuntimeError("No latest consumer sentiment value parsed from dynamically discovered Westpac bulletin")
        return points, {"note": "Dynamic Westpac IQ article and linked bulletin discovery; no month-specific URLs", "attempts": attempts}
    if label == "失業預期":
        return fetch_westpac_unemployment_expectations()
    if label in {"製造業PMI", "服務業PMI"}:
        return sp_australia_pmi(label)
    if label == "GDP YoY":
        return fetch_abs_target("ANA_AGG", "2024-Q1", ["gross domestic product", "chain volume", "index", "seasonally adjusted"], ["per capita", "percentage changes"], target.expected, "yoy_pct_q")
    if label == "GDP私人消費YoY":
        response, discovery = discover_abs_workbook(
            ["https://www.abs.gov.au/statistics/economy/national-accounts/australian-national-accounts-national-income-expenditure-and-product/latest-release#data-downloads"],
            "5206008", "Table 8", [],
        )
        points, diagnostics = fetch_abs_workbook_candidate(
            [response.url], target.expected, "abs_5206008_household_consumption.xlsx",
            "ABS Table 8 Household Final Consumption Expenditure official XLSX",
        )
        diagnostics.update(discovery)
        return points, diagnostics
    if label == "GDP投資YoY":
        response, discovery = discover_abs_workbook(
            ["https://www.abs.gov.au/statistics/economy/national-accounts/australian-national-accounts-national-income-expenditure-and-product/latest-release#data-downloads"],
            "5206002", "Table 2", [],
        )
        points, diagnostics = fetch_abs_workbook_candidate(
            [response.url], target.expected, "abs_5206002_expenditure_volume_measures.xlsx",
            "ABS Table 2 Expenditure on GDP, chain volume measures official workbook",
        )
        diagnostics.update(discovery)
        return points, diagnostics
    raise RuntimeError(f"No test mapping for {label}")



DATA_FILE = Path("data/au_macro.json")
MD_FILE = Path("au_macro_all_data.md")

SERIES_MAP = {
    "就業新增": "auempchg", "失業率": "auunemp", "職缺": "auvacancy",
    "ANZ職缺廣告": "auanzjobads", "時薪YoY": "auwageyoy",
    "預計離職": "auexitleave", "失業預期": "auunempexp",
    "CPI YoY": "aucpi", "Trimmed Mean YoY": "autrimmed", "零售": "auretail",
    "NAB企業售價": "aunabprices", "消費信心": "auconsconf",
    "製造業PMI": "aumanpmi", "服務業PMI": "auservpmi",
    "GDP YoY": "augdpyoy", "GDP私人消費YoY": "auconsumptionyoy",
    "GDP投資YoY": "auinvestmentyoy",
}
AUTHORITATIVE = {
    "就業新增", "失業率", "職缺", "ANZ職缺廣告", "時薪YoY", "預計離職",
    "CPI YoY", "Trimmed Mean YoY", "零售", "GDP YoY", "GDP私人消費YoY", "GDP投資YoY",
    "製造業PMI", "服務業PMI",
}

def point_date(period: str) -> str:
    if re.fullmatch(r"\d{4}-\d{2}", period):
        return period + "-01"
    match = re.fullmatch(r"(\d{4})-Q([1-4])", period)
    if match:
        return f"{match.group(1)}-{int(match.group(2))*3:02d}-01"
    raise ValueError(f"Unsupported period: {period}")

def by_id(database: dict[str, Any], series_id: str) -> dict[str, Any]:
    for item in database.get("series", []):
        if item.get("id") == series_id:
            return item
    raise KeyError(series_id)

def merge_points(database: dict[str, Any], series_id: str, points: list[Point], authoritative: bool) -> tuple[int,int]:
    series=by_id(database,series_id)
    old={str(row["date"])[:7]:dict(row) for row in series.get("data",[]) if row.get("date")}
    incoming={point_date(p.period)[:7]:{
        "date":point_date(p.period), "value":float(p.value), "source_url":p.source_url,
        **({"release_type":p.status} if p.status else {}), **({"note":p.note} if p.note else {})
    } for p in points}
    if not incoming: return 0,0

    # Repair PMI rows previously assigned to the PDF publication month instead
    # of the survey reference month.  If the newest parsed official observation
    # is July, any later S&P PMI row already stored in August is stale and must
    # be removed before the July final replaces the July flash.
    if series_id in {"aumanpmi", "auservpmi"}:
        latest_incoming = max(incoming)
        stale_keys = [
            key for key, row in old.items()
            if key > latest_incoming
            and "pmi.spglobal.com" in str(row.get("source_url", "")).lower()
        ]
        for key in stale_keys:
            log(f"[PMI CLEANUP] {series_id} remove stale publication-month row {key}")
            old.pop(key, None)

    if authoritative:
        earliest=min(old) if old else min(incoming)
        keys=[k for k in incoming if k>=earliest]
    else:
        latest=max(old) if old else ""
        keys=[k for k in incoming if not latest or k>=latest]
    added=revised=0
    for key in sorted(keys):
        candidate=incoming[key]; current=old.get(key)
        if current is None:
            old[key]=candidate; added+=1
        elif current.get("release_type")=="final" and candidate.get("release_type")=="flash":
            continue
        elif current.get("value")!=candidate.get("value") or current.get("release_type")!=candidate.get("release_type"):
            old[key]={**current,**candidate}; revised+=1
        elif authoritative:
            old[key]={**current,**candidate}
    series["data"]=sorted(old.values(),key=lambda x:x["date"])
    return added,revised

def write_markdown(database: dict[str, Any], logs: list[dict[str, Any]]) -> None:
    """Write a compact Excel-style heatmap matrix for quick data validation.

    GitHub Markdown supports embedded HTML tables.  The MD therefore uses an
    HTML table so categories can use rowspans and cells can display background
    colours similar to the reference spreadsheet.
    """
    import calendar
    from html import escape

    monthly_groups = [
        ("就業", [
            "auempchg", "auunemp", "auvacancy", "auanzjobads",
            "auwageyoy", "auexitleave", "auunempexp",
        ]),
        ("通膨", ["aucpi", "autrimmed", "auretail"]),
        ("調查", ["aunabprices", "auconsconf", "aumanpmi", "auservpmi"]),
    ]
    quarterly_groups = [
        ("GDP", ["augdpyoy", "auconsumptionyoy", "auinvestmentyoy"]),
    ]

    display_names = {
        "auempchg": "就業新增",
        "auunemp": "失業率",
        "auvacancy": "職缺",
        "auanzjobads": "ANZ職缺廣告數",
        "auwageyoy": "時薪YoY",
        "auexitleave": "預計離職",
        "auunempexp": "失業預期",
        "aucpi": "CPI",
        "autrimmed": "Trim mean",
        "auretail": "零售",
        "aunabprices": "NAB企業調查 售價",
        "auconsconf": "消費信心",
        "aumanpmi": "PMI製造業",
        "auservpmi": "PMI服務業",
        "augdpyoy": "GDP",
        "auconsumptionyoy": "GDP 私人消費",
        "auinvestmentyoy": "GDP投資",
    }

    # False means a higher value is rendered red, matching the reference heat
    # map.  Consumer confidence is the exception: a higher value is green.
    high_is_green = {"auconsconf"}

    decimals = {
        "auempchg": 0,
        "auunemp": 2,
        "auvacancy": 0,
        "auanzjobads": 0,
        "auwageyoy": 2,
        "auexitleave": 0,
        "auunempexp": 1,
        "aucpi": 2,
        "autrimmed": 2,
        "auretail": 2,
        "aunabprices": 2,
        "auconsconf": 2,
        "aumanpmi": 1,
        "auservpmi": 1,
        "augdpyoy": 2,
        "auconsumptionyoy": 2,
        "auinvestmentyoy": 2,
    }

    series_map = {item.get("id"): item for item in database.get("series", [])}

    def month_key(date_text: str) -> str:
        return str(date_text)[:7]

    def series_values(series_id: str) -> dict[str, float]:
        result = {}
        series = series_map.get(series_id, {})
        for point in series.get("data", []):
            try:
                result[month_key(point.get("date", ""))] = float(point.get("value"))
            except (TypeError, ValueError):
                continue
        return result

    def latest_periods(series_ids: list[str], count: int) -> list[str]:
        periods = set()
        for series_id in series_ids:
            periods.update(series_values(series_id))
        return sorted(periods, reverse=True)[:count]

    def period_label(period: str) -> str:
        year, month = map(int, period.split("-"))
        last_day = calendar.monthrange(year, month)[1]
        return f"{year}/{month}/{last_day}"

    def format_value(series_id: str, value: float) -> str:
        places = decimals.get(series_id, 2)
        if places == 0:
            return f"{value:.0f}"
        return f"{value:.{places}f}"

    def blend(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
        t = min(1.0, max(0.0, t))
        return tuple(round(x + (y - x) * t) for x, y in zip(a, b))

    def heat_color(series_id: str, value: float, visible_values: list[float]) -> str:
        if len(visible_values) < 2 or max(visible_values) == min(visible_values):
            return "#ffffff"
        low = min(visible_values)
        high = max(visible_values)
        position = (value - low) / (high - low)
        if series_id in high_is_green:
            position = 1.0 - position
        green = (99, 190, 123)
        white = (255, 255, 255)
        red = (248, 105, 113)
        if position <= 0.5:
            rgb = blend(green, white, position / 0.5)
        else:
            rgb = blend(white, red, (position - 0.5) / 0.5)
        return "#%02x%02x%02x" % rgb

    def render_table(groups: list[tuple[str, list[str]]], periods: list[str]) -> list[str]:
        lines = [
            '<table>',
            '  <thead>',
            '    <tr>',
            '      <th style="min-width:60px"></th>',
            '      <th style="min-width:180px"></th>',
        ]
        for period in periods:
            lines.append(f'      <th align="center" style="min-width:90px">{escape(period_label(period))}</th>')
        lines += ['    </tr>', '  </thead>', '  <tbody>']

        for group_name, series_ids in groups:
            for row_index, series_id in enumerate(series_ids):
                values = series_values(series_id)
                visible = [values[p] for p in periods if p in values]
                lines.append('    <tr>')
                if row_index == 0:
                    lines.append(
                        f'      <th rowspan="{len(series_ids)}" align="center" '
                        f'valign="middle">{escape(group_name)}</th>'
                    )
                lines.append(f'      <td>{escape(display_names.get(series_id, series_id))}</td>')
                for period in periods:
                    if period not in values:
                        lines.append('      <td align="right"></td>')
                        continue
                    value = values[period]
                    color = heat_color(series_id, value, visible)
                    lines.append(
                        f'      <td align="right" bgcolor="{color}">'
                        f'{escape(format_value(series_id, value))}</td>'
                    )
                lines.append('    </tr>')
        lines += ['  </tbody>', '</table>']
        return lines

    monthly_ids = [sid for _, ids in monthly_groups for sid in ids]
    quarterly_ids = [sid for _, ids in quarterly_groups for sid in ids]
    monthly_periods = latest_periods(monthly_ids, 4)
    quarterly_periods = latest_periods(quarterly_ids, 4)

    lines = [
        "# 澳洲總體資料 Debug 表",
        "",
        f"更新時間：{database.get('generated_at', '')}",
        "",
        "> 色階用於快速檢查近期數值。多數指標數值越高越偏紅、越低越偏綠；消費信心則反向顯示。空白代表該期尚無資料。",
        "",
    ]
    lines.extend(render_table(monthly_groups, monthly_periods))
    lines += ["", "<br>", ""]
    lines.extend(render_table(quarterly_groups, quarterly_periods))
    lines += ["", "## 更新狀態", "", "| 指標 | 狀態 | 新增 | 修訂 | 官方最新期 | 官方最新值 | 錯誤 |", "|---|---|---:|---:|---|---:|---|"]
    for row in logs:
        cells = [
            row.get("label", ""), row.get("status", ""), row.get("added", ""),
            row.get("revised", ""), row.get("latest_period", ""),
            row.get("latest_value", ""), row.get("error", ""),
        ]
        lines.append("| " + " | ".join(str(v).replace("|", "\\|") for v in cells) + " |")

    MD_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")

def main() -> int:
    OUT.mkdir(parents=True,exist_ok=True)
    database=json.loads(DATA_FILE.read_text(encoding="utf-8"))
    logs=[]
    for target in TARGETS:
        series_id=SERIES_MAP[target.label]
        target_started=time.perf_counter()
        started_at=datetime.now(timezone.utc).isoformat()
        log(f"\n[UPDATE] {target.label} -> {series_id}")
        log(f"[TIMER START] {target.label} started_at={started_at}")
        try:
            points,diagnostics=run_target(target)
            points=dedupe(points)
            added,revised=merge_points(database,series_id,points,target.label in AUTHORITATIVE)
            latest=points[-1] if points else None
            entry={"label":target.label,"series_id":series_id,"status":"OK","added":added,"revised":revised,
                   "latest_period":latest.period if latest else "","latest_value":latest.value if latest else "","error":""}
            (OUT/f"{series_id}_diagnostics.json").write_text(json.dumps(diagnostics,ensure_ascii=False,indent=2),encoding="utf-8")
        except Exception as error:
            entry={"label":target.label,"series_id":series_id,"status":"ERROR","added":0,"revised":0,
                   "latest_period":"","latest_value":"","error":f"{type(error).__name__}: {error}"}
            log(f"[ERROR] {entry['error']}")
        finally:
            elapsed_seconds=time.perf_counter()-target_started
            entry["started_at"]=started_at
            entry["elapsed_seconds"]=round(elapsed_seconds,3)
            log(
                f"[TIMER END] {target.label} -> {series_id} "
                f"status={entry['status']} elapsed={elapsed_seconds:.3f}s"
            )
        logs.append(entry)
    database["generated_at"]=datetime.now(timezone.utc).isoformat()
    database["script_version"]=VERSION
    DATA_FILE.write_text(json.dumps(database,ensure_ascii=False,indent=2),encoding="utf-8")
    write_markdown(database,logs)
    (OUT/"update_summary.json").write_text(json.dumps(logs,ensure_ascii=False,indent=2),encoding="utf-8")
    log(f"[DONE] wrote {DATA_FILE} and {MD_FILE}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
