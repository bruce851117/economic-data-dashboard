#!/usr/bin/env python3
"""GDP-only diagnostics for the EU macro pipeline.

Purpose
-------
1. Download the exact structured GDP sources used by update_eu_macro.py.
2. Preserve raw responses for Germany, Spain, France, and the euro area.
3. Show the last 8 parsed quarters and whether 2026-Q2 exists.
4. Compare source output with data/eu_macro.json.
5. Test the quarterly period -> JSON date conversion used by the production merge.
6. Inspect national flash releases when the complete historical source has not yet
   published 2026-Q2.

This script is read-only. It never changes eu_macro.json.
"""
from __future__ import annotations

import csv
import io
import json
import re
import sys
import traceback
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup

VERSION = "2026-07-30-eu-gdp-debug-v1"
OUT = Path("debug/eu_gdp_sources")
EUROSTAT = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"
SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (compatible; EUGDPDebugger/1.0; GitHub-Actions)",
    "Accept-Language": "en-US,en;q=0.9,de;q=0.8,fr;q=0.7,es;q=0.6",
})


@dataclass
class Point:
    period: str
    value: float
    source_url: str
    note: str = ""


def log(message: str) -> None:
    print(message, flush=True)


def clean(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def number(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = clean(value).replace("%", "").replace("−", "-")
    text = re.sub(r"(?<=\d),(?=\d)", ".", text)
    text = text.replace(" ", "")
    return float(text) if re.fullmatch(r"[+-]?\d+(?:\.\d+)?", text) else None


def get(url: str, **kwargs: Any) -> requests.Response:
    response = SESSION.get(url, timeout=60, allow_redirects=True, **kwargs)
    log(f"[HTTP] {response.status_code} {response.url} bytes={len(response.content)}")
    response.raise_for_status()
    return response


def period_key(value: Any) -> str | None:
    text = clean(value)
    match = re.fullmatch(r"(20\d{2})[- ]?[QT]([1-4])", text, re.I)
    if match:
        return f"{match.group(1)}-Q{match.group(2)}"
    return None


def quarter_to_json_date(period: str) -> str | None:
    match = re.fullmatch(r"(20\d{2})-Q([1-4])", clean(period), re.I)
    if not match:
        return None
    return f"{int(match.group(1)):04d}-{int(match.group(2)) * 3:02d}-01"


def dedupe(points: list[Point]) -> list[Point]:
    by_period = {point.period: point for point in points}
    return [by_period[key] for key in sorted(by_period)]


def flatten(position: int, sizes: list[int]) -> list[int]:
    coords = [0] * len(sizes)
    for index in range(len(sizes) - 1, -1, -1):
        coords[index] = position % sizes[index]
        position //= sizes[index]
    return coords


def eurostat_gdp(geo: str, raw_name: str) -> tuple[list[Point], dict[str, Any], str]:
    filters = {
        "format": "JSON",
        "lang": "EN",
        "geo": geo,
        "na_item": "B1GQ",
        "unit": "CLV_PCH_SM",
        "s_adj": "SCA",
        "sinceTimePeriod": "2024-Q1",
        "untilTimePeriod": "2026-Q2",
    }
    response = get(f"{EUROSTAT}/namq_10_gdp", params=filters)
    OUT.joinpath(raw_name).write_bytes(response.content)
    payload = response.json()
    ids = payload.get("id", [])
    sizes = payload.get("size", [])
    values = payload.get("value") or {}
    if "time" not in ids or not values:
        raise RuntimeError(f"Eurostat returned no observations; dimensions={ids}; filters={filters}")

    categories: dict[str, list[str]] = {}
    for dim in ids:
        index = payload["dimension"][dim]["category"]["index"]
        if isinstance(index, dict):
            ordered = [""] * len(index)
            for code, position in index.items():
                ordered[int(position)] = code
            categories[dim] = ordered
        else:
            categories[dim] = list(index)

    points: list[Point] = []
    rows: list[dict[str, Any]] = []
    for raw_position, raw_value in values.items():
        coords = flatten(int(raw_position), sizes)
        row = {dim: categories[dim][coords[index]] for index, dim in enumerate(ids)}
        row["value"] = raw_value
        rows.append(row)
        period = period_key(row.get("time"))
        value = number(raw_value)
        if period and value is not None:
            points.append(Point(period, value, response.url, "Eurostat namq_10_gdp / B1GQ / CLV_PCH_SM / SCA"))

    diagnostics = {
        "request_url": response.url,
        "dimensions": ids,
        "sizes": sizes,
        "rows": rows,
        "status": payload.get("status", {}),
        "updated": payload.get("updated"),
    }
    return dedupe(points), diagnostics, response.url


def germany_gdp_csv() -> tuple[list[Point], dict[str, Any], str]:
    url = "https://genesis.destatis.de/genesisWS/downloads/00/tables/81000-0002_00.csv"
    response = get(url)
    OUT.joinpath("germany_81000-0002_raw.csv").write_bytes(response.content)
    text = response.content.decode("utf-8-sig", "replace")
    rows = list(csv.reader(io.StringIO(text), delimiter=";"))

    year_row = None
    quarter_row = None
    candidates: list[dict[str, Any]] = []
    target_row = None
    for row_index, row in enumerate(rows):
        normalized = [clean(cell).lower() for cell in row]
        if sum(bool(re.fullmatch(r"20\d{2}", cell)) for cell in normalized) >= 2:
            year_row = row
        if sum("quartal" in cell for cell in normalized) >= 2:
            quarter_row = row
        joined = " | ".join(normalized)
        if "bruttoinlandsprodukt" in joined and "veränderung in %" in joined:
            candidates.append({"row": row_index + 1, "preview": row[:18]})
        if (
            normalized
            and normalized[0] == "originalwerte"
            and "preisbereinigt, kettenindex" in joined
            and "bruttoinlandsprodukt (veränderung in %)" in joined
        ):
            target_row = row

    if year_row is None or quarter_row is None or target_row is None:
        raise RuntimeError("Destatis target row/header not found")

    points: list[Point] = []
    current_year: int | None = None
    column_debug: list[dict[str, Any]] = []
    width = max(len(year_row), len(quarter_row), len(target_row))
    for column in range(width):
        year_cell = clean(year_row[column] if column < len(year_row) else "")
        if re.fullmatch(r"20\d{2}", year_cell):
            current_year = int(year_cell)
        quarter_cell = clean(quarter_row[column] if column < len(quarter_row) else "")
        quarter_match = re.search(r"([1-4])\.\s*quartal", quarter_cell, re.I)
        value = number(target_row[column] if column < len(target_row) else None)
        column_debug.append({
            "column": column + 1,
            "year_cell": year_cell,
            "effective_year": current_year,
            "quarter_cell": quarter_cell,
            "value": value,
        })
        if current_year and quarter_match and value is not None:
            points.append(Point(
                f"{current_year:04d}-Q{quarter_match.group(1)}",
                value,
                response.url,
                "Destatis 81000-0002 original, price-adjusted GDP YoY",
            ))

    diagnostics = {
        "request_url": response.url,
        "candidate_rows": candidates,
        "target_row_preview": target_row[:24],
        "year_row_preview": year_row[:24],
        "quarter_row_preview": quarter_row[:24],
        "column_debug": column_debug,
    }
    return dedupe(points), diagnostics, response.url


def html_text(url: str, raw_name: str) -> tuple[str, str]:
    response = get(url)
    OUT.joinpath(raw_name).write_bytes(response.content)
    text = BeautifulSoup(response.text, "html.parser").get_text(" ", strip=True)
    return clean(text).replace("−", "-"), response.url


def germany_flash() -> list[Point]:
    text, final_url = html_text(
        "https://www.destatis.de/EN/Press/2026/07/PE26_269_811.html",
        "germany_q2_release.html",
    )
    patterns = [
        r"second quarter of 2026.{0,500}?price adjusted.{0,100}?([+-]?\d+(?:[.,]\d+)?)\s*%\s+higher than in the second quarter of 2025",
        r"GDP.{0,300}?2nd quarter 2026.{0,200}?([+-]?\d+(?:[.,]\d+)?)\s*%\s+on the same quarter a year earlier",
        r"\+?([0-9]+(?:[.,][0-9]+)?)\s*%\s+on the same quarter a year earlier\s*\(price adjusted\)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.I | re.S)
        if match:
            value = number(match.group(1))
            if value is not None:
                return [Point("2026-Q2", value, final_url, "Destatis Q2 flash release")]
    raise RuntimeError("Germany Q2 YoY not parsed from official release")


def spain_flash() -> list[Point]:
    text, final_url = html_text(
        "https://ine.es/dyngs/Prensa/en/avCNTR2T26.htm",
        "spain_q2_release.html",
    )
    patterns = [
        r"annual change of GDP was\s*([+-]?\d+(?:[.,]\d+)?)%",
        r"GDP at market prices.{0,120}?Annual change.{0,80}?([+-]?\d+(?:[.,]\d+)?)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.I | re.S)
        if match:
            value = number(match.group(1))
            if value is not None:
                return [Point("2026-Q2", value, final_url, "INE Q2 advance estimate")]
    raise RuntimeError("Spain Q2 YoY not parsed from official release")


def france_release_probe() -> tuple[list[Point], dict[str, Any]]:
    text, final_url = html_text(
        "https://www.insee.fr/en/statistiques/9033400",
        "france_q2_release.html",
    )
    # Do not confuse the published QoQ value with the requested YoY series.
    yoy_patterns = [
        r"GDP.{0,250}?year-on-year.{0,80}?([+-]?\d+(?:[.,]\d+)?)\s*%",
        r"compared with the second quarter of 2025.{0,80}?([+-]?\d+(?:[.,]\d+)?)\s*%",
    ]
    points: list[Point] = []
    for pattern in yoy_patterns:
        match = re.search(pattern, text, re.I | re.S)
        if match:
            value = number(match.group(1))
            if value is not None:
                points.append(Point("2026-Q2", value, final_url, "INSEE Q2 release YoY"))
                break
    diagnostics = {
        "request_url": final_url,
        "contains_q2": "Q2 2026" in text or "second quarter of 2026" in text.lower(),
        "qoq_mentions": re.findall(r"[+-]?\d+(?:[.,]\d+)?%", text[:5000])[:30],
        "note": "No value is treated as YoY unless an explicit year-on-year phrase is matched.",
    }
    return points, diagnostics


def load_json_database() -> tuple[dict[str, Any] | None, str | None]:
    candidates = [Path("data/eu_macro.json"), Path("eu_macro.json"), Path("/mnt/data/eu_macro.json")]
    for path in candidates:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8")), str(path)
    return None, None


def json_series_latest(database: dict[str, Any] | None, series_id: str) -> dict[str, Any]:
    if not database:
        return {"found": False, "reason": "eu_macro.json not found"}
    series = next((item for item in database.get("series", []) if item.get("id") == series_id), None)
    if not series:
        return {"found": False, "reason": f"series {series_id} not found"}
    rows = sorted(series.get("data", []), key=lambda item: item.get("date", ""))
    return {
        "found": True,
        "name": series.get("name"),
        "frequency": series.get("frequency"),
        "latest_rows": rows[-8:],
        "has_2026_q2_date": any(item.get("date") == "2026-06-01" for item in rows),
    }


def summarize_source(name: str, points: list[Point], source_kind: str, error: str | None = None) -> dict[str, Any]:
    latest = points[-8:] if points else []
    return {
        "name": name,
        "source_kind": source_kind,
        "status": "OK" if points else ("ERROR" if error else "NO_VALUE"),
        "error": error,
        "latest_points": [asdict(point) for point in latest],
        "latest_period": latest[-1].period if latest else None,
        "latest_value": latest[-1].value if latest else None,
        "has_2026_q2": any(point.period == "2026-Q2" for point in points),
        "q2_value": next((point.value for point in points if point.period == "2026-Q2"), None),
        "q2_json_date": quarter_to_json_date("2026-Q2"),
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    database, database_path = load_json_database()
    report: dict[str, Any] = {
        "script_version": VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "database_path": database_path,
        "quarter_mapping_test": {
            "2026-Q1": quarter_to_json_date("2026-Q1"),
            "2026-Q2": quarter_to_json_date("2026-Q2"),
            "2026-Q3": quarter_to_json_date("2026-Q3"),
            "2026-Q4": quarter_to_json_date("2026-Q4"),
        },
        "countries": {},
    }

    tests = [
        ("germany", "de_gdp_yoy"),
        ("spain", "es_gdp_yoy"),
        ("france", "fr_gdp_yoy"),
        ("euro_area", "ea_gdp_yoy"),
    ]
    for country, series_id in tests:
        report["countries"][country] = {
            "series_id": series_id,
            "json": json_series_latest(database, series_id),
            "sources": [],
        }

    # Germany complete history.
    try:
        points, diagnostics, _ = germany_gdp_csv()
        report["countries"]["germany"]["sources"].append(summarize_source(
            "Destatis 81000-0002 CSV", points, "complete_history"
        ))
        report["countries"]["germany"]["destatis_diagnostics"] = diagnostics
    except Exception as error:
        report["countries"]["germany"]["sources"].append(summarize_source(
            "Destatis 81000-0002 CSV", [], "complete_history", f"{type(error).__name__}: {error}"
        ))
        report["countries"]["germany"]["traceback"] = traceback.format_exc(limit=8)

    # Eurostat complete-history source for ES, FR, and EA. Test EA21, then EA20.
    for country, geo, raw_name in [
        ("spain", "ES", "spain_namq_10_gdp_raw.json"),
        ("france", "FR", "france_namq_10_gdp_raw.json"),
    ]:
        try:
            points, diagnostics, _ = eurostat_gdp(geo, raw_name)
            report["countries"][country]["sources"].append(summarize_source(
                f"Eurostat namq_10_gdp {geo}", points, "complete_history"
            ))
            report["countries"][country]["eurostat_diagnostics"] = diagnostics
        except Exception as error:
            report["countries"][country]["sources"].append(summarize_source(
                f"Eurostat namq_10_gdp {geo}", [], "complete_history", f"{type(error).__name__}: {error}"
            ))
            report["countries"][country]["traceback"] = traceback.format_exc(limit=8)

    ea_errors: list[str] = []
    for geo in ("EA21", "EA20", "EA"):
        try:
            points, diagnostics, _ = eurostat_gdp(geo, f"euro_area_{geo}_namq_10_gdp_raw.json")
            report["countries"]["euro_area"]["sources"].append(summarize_source(
                f"Eurostat namq_10_gdp {geo}", points, "complete_history"
            ))
            report["countries"]["euro_area"][f"eurostat_diagnostics_{geo}"] = diagnostics
            if points:
                break
        except Exception as error:
            ea_errors.append(f"{geo}: {type(error).__name__}: {error}")
    if not report["countries"]["euro_area"]["sources"]:
        report["countries"]["euro_area"]["sources"].append(summarize_source(
            "Eurostat namq_10_gdp EA21/EA20/EA", [], "complete_history", " | ".join(ea_errors)
        ))

    # National flash releases. These diagnose publication-lag versus parser failure.
    for country, fetcher, label in [
        ("germany", germany_flash, "Destatis Q2 flash release"),
        ("spain", spain_flash, "INE Q2 advance estimate"),
    ]:
        try:
            points = fetcher()
            report["countries"][country]["sources"].append(summarize_source(label, points, "latest_flash"))
        except Exception as error:
            report["countries"][country]["sources"].append(summarize_source(
                label, [], "latest_flash", f"{type(error).__name__}: {error}"
            ))

    try:
        points, diagnostics = france_release_probe()
        report["countries"]["france"]["sources"].append(summarize_source(
            "INSEE Q2 first estimate release", points, "latest_flash"
        ))
        report["countries"]["france"]["insee_release_diagnostics"] = diagnostics
    except Exception as error:
        report["countries"]["france"]["sources"].append(summarize_source(
            "INSEE Q2 first estimate release", [], "latest_flash", f"{type(error).__name__}: {error}"
        ))

    # Final diagnosis per country.
    for country, item in report["countries"].items():
        complete = next((source for source in item["sources"] if source["source_kind"] == "complete_history" and source["status"] == "OK"), None)
        flash = next((source for source in item["sources"] if source["source_kind"] == "latest_flash" and source["status"] == "OK"), None)
        json_has_q2 = item["json"].get("has_2026_q2_date", False)
        if complete and complete["has_2026_q2"] and not json_has_q2:
            diagnosis = "SOURCE_HAS_Q2_BUT_JSON_DOES_NOT: inspect production merge/series ID/quarter date conversion."
        elif complete and not complete["has_2026_q2"] and flash and flash["has_2026_q2"]:
            diagnosis = "PUBLICATION_LAG: complete historical source is still at Q1, but official flash release has Q2. Add latest-flash overlay."
        elif complete and not complete["has_2026_q2"]:
            diagnosis = "COMPLETE_SOURCE_NOT_UPDATED: Q2 absent from the current structured source response."
        elif not complete:
            diagnosis = "STRUCTURED_FETCH_OR_PARSER_ERROR: inspect raw response and traceback."
        else:
            diagnosis = "Q2 state is consistent."
        item["diagnosis"] = diagnosis

    report_path = OUT / "gdp_debug_summary.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    md_lines = [
        "# EU GDP Source Debug Summary",
        "",
        f"Generated: `{report['generated_at']}`",
        "",
        "| Country | JSON has 2026-Q2 | Complete source latest | Complete has Q2 | Flash has Q2 | Diagnosis |",
        "|---|---:|---|---:|---:|---|",
    ]
    for country, item in report["countries"].items():
        complete = next((source for source in item["sources"] if source["source_kind"] == "complete_history"), {})
        flash = next((source for source in item["sources"] if source["source_kind"] == "latest_flash"), {})
        md_lines.append(
            f"| {country} | {item['json'].get('has_2026_q2_date', False)} | "
            f"{complete.get('latest_period', '')} | {complete.get('has_2026_q2', False)} | "
            f"{flash.get('has_2026_q2', False)} | {item['diagnosis']} |"
        )
    md_lines.extend(["", "## Parsed source points", ""])
    for country, item in report["countries"].items():
        md_lines.append(f"### {country}")
        md_lines.append("")
        for source in item["sources"]:
            md_lines.append(f"- **{source['name']}**: `{source['status']}`, latest=`{source.get('latest_period')}`, Q2=`{source.get('q2_value')}`")
            if source.get("error"):
                md_lines.append(f"  - Error: `{source['error']}`")
        md_lines.append("")
    OUT.joinpath("gdp_debug_summary.md").write_text("\n".join(md_lines), encoding="utf-8")

    log("\n=== GDP DEBUG SUMMARY ===")
    for country, item in report["countries"].items():
        log(f"{country}: {item['diagnosis']}")
    log(f"JSON: {report_path}")
    log(f"MD  : {OUT / 'gdp_debug_summary.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
