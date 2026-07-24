from __future__ import annotations

import csv
import io
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup

OUT = Path("uk_raw_source_debug")
OUT.mkdir(parents=True, exist_ok=True)

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (compatible; UKMacroSourceDebugger/1.0)",
    "Accept-Language": "en-GB,en;q=0.9",
})

SOURCES = {
    "vacancies_ap2y": "https://www.ons.gov.uk/generator?format=csv&uri=/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/timeseries/ap2y/unem",
    "retail_ex_fuel": "https://tradingeconomics.com/united-kingdom/retail-sales-ex-fuel",
    "gfk_consumer_confidence": "https://tradingeconomics.com/united-kingdom/consumer-confidence",
}

MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4,
    "may": 5, "june": 6, "july": 7, "august": 8,
    "september": 9, "october": 10, "november": 11, "december": 12,
}


def fetch(url: str) -> requests.Response:
    last: Exception | None = None
    for attempt in range(4):
        try:
            response = SESSION.get(url, timeout=90, allow_redirects=True)
            if response.status_code < 400:
                return response
            if response.status_code not in {429, 500, 502, 503, 504}:
                response.raise_for_status()
        except Exception as exc:
            last = exc
        time.sleep(3 * (2 ** attempt))
    if last:
        raise last
    response.raise_for_status()
    return response


def save_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def save_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def shift_month(month: str, offset: int) -> str:
    year, mon = map(int, month.split("-"))
    serial = year * 12 + mon - 1 + offset
    return f"{serial // 12:04d}-{serial % 12 + 1:02d}"


def parse_ons_period(value: str) -> str | None:
    value = normalize_space(value).upper()
    match = re.fullmatch(r"(\d{4})\s+([A-Z]{3})", value)
    if not match:
        return None
    aliases = {
        "JAN": 1, "FEB": 2, "MAR": 3, "APR": 4, "MAY": 5, "JUN": 6,
        "JUL": 7, "AUG": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12,
    }
    mon = aliases.get(match.group(2))
    return f"{match.group(1)}-{mon:02d}" if mon else None


def debug_vacancies(report: dict[str, Any]) -> None:
    name = "vacancies_ap2y"
    url = SOURCES[name]
    response = fetch(url)
    raw = response.content.decode("utf-8-sig", "replace")
    save_text(OUT / "01_vacancies_ap2y_raw.csv", raw)

    all_rows = list(csv.reader(io.StringIO(raw)))
    save_json(OUT / "01_vacancies_ap2y_first_80_rows.json", all_rows[:80])

    observations = []
    for row_no, row in enumerate(all_rows, start=1):
        if len(row) < 2:
            continue
        ons_month = parse_ons_period(row[0])
        raw_value = row[1].replace(",", "").strip()
        if not ons_month or not re.fullmatch(r"-?\d+(?:\.\d+)?", raw_value):
            continue
        observations.append({
            "csv_row": row_no,
            "raw_period": row[0],
            "ons_label_month": ons_month,
            "dashboard_end_month_if_shifted_plus_1": shift_month(ons_month, 1),
            "value": float(raw_value),
            "raw_row": row,
        })

    observations.sort(key=lambda x: x["ons_label_month"], reverse=True)
    save_json(OUT / "01_vacancies_ap2y_latest_36.json", observations[:36])
    report[name] = {
        "url": url,
        "status": response.status_code,
        "content_type": response.headers.get("content-type"),
        "bytes": len(response.content),
        "observation_count": len(observations),
        "latest_12": observations[:12],
        "note": "ONS AP2Y is a three-month moving average. File shows the ONS label month; the debug output also shows the dashboard month after +1 month conversion.",
    }


def extract_contexts(text: str, patterns: list[str], radius: int = 350) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    seen: set[str] = set()
    for pattern in patterns:
        for match in re.finditer(pattern, text, re.I):
            start = max(0, match.start() - radius)
            end = min(len(text), match.end() + radius)
            context = normalize_space(text[start:end])
            key = context.lower()
            if key in seen:
                continue
            seen.add(key)
            output.append({
                "pattern": pattern,
                "match": match.group(0),
                "start": match.start(),
                "context": context,
            })
            if len(output) >= 80:
                return output
    return output


def extract_tables(soup: BeautifulSoup) -> list[dict[str, Any]]:
    tables = []
    for table_no, table in enumerate(soup.find_all("table"), start=1):
        rows = []
        for tr in table.find_all("tr"):
            cells = [normalize_space(cell.get_text(" ", strip=True)) for cell in tr.find_all(["th", "td"])]
            if cells:
                rows.append(cells)
        if rows:
            tables.append({"table_no": table_no, "rows": rows[:100]})
    return tables


def debug_web_page(name: str, url: str, patterns: list[str], prefix: str, report: dict[str, Any]) -> None:
    response = fetch(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    visible = normalize_space(soup.get_text(" ", strip=True))

    save_text(OUT / f"{prefix}_{name}_raw.html", html)
    save_text(OUT / f"{prefix}_{name}_visible_text.txt", visible)
    save_json(OUT / f"{prefix}_{name}_keyword_contexts.json", extract_contexts(visible, patterns))
    save_json(OUT / f"{prefix}_{name}_tables.json", extract_tables(soup))

    scripts = []
    for index, script in enumerate(soup.find_all("script"), start=1):
        body = script.string or script.get_text("", strip=False)
        if not body or len(body) < 50:
            continue
        if any(re.search(pattern, body, re.I) for pattern in patterns):
            scripts.append({
                "script_no": index,
                "type": script.get("type", ""),
                "length": len(body),
                "preview": body[:3000],
            })
    save_json(OUT / f"{prefix}_{name}_matching_scripts.json", scripts[:40])

    report[name] = {
        "url": url,
        "final_url": response.url,
        "status": response.status_code,
        "content_type": response.headers.get("content-type"),
        "bytes": len(response.content),
        "visible_text_chars": len(visible),
        "table_count": len(soup.find_all("table")),
        "matching_script_count": len(scripts),
        "files": [
            f"{prefix}_{name}_raw.html",
            f"{prefix}_{name}_visible_text.txt",
            f"{prefix}_{name}_keyword_contexts.json",
            f"{prefix}_{name}_tables.json",
            f"{prefix}_{name}_matching_scripts.json",
        ],
    }


def main() -> int:
    report: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "purpose": "Inspect raw source responses only. This script does not modify data/uk_macro.json.",
        "sources": {},
    }

    jobs = [
        ("vacancies", lambda: debug_vacancies(report["sources"])),
        ("retail", lambda: debug_web_page(
            "retail_ex_fuel",
            SOURCES["retail_ex_fuel"],
            [
                r"Retail Sales ex Fuel YoY",
                r"retail sales excluding fuel",
                r"annual basis",
                r"calendar",
                r"forecast",
                r"previous",
            ],
            "02",
            report["sources"],
        )),
        ("gfk", lambda: debug_web_page(
            "gfk_consumer_confidence",
            SOURCES["gfk_consumer_confidence"],
            [
                r"GfK Consumer Confidence",
                r"Consumer Confidence in the United Kingdom",
                r"consumer confidence",
                r"calendar",
                r"forecast",
                r"previous",
            ],
            "03",
            report["sources"],
        )),
    ]

    had_error = False
    for label, function in jobs:
        try:
            print(f"[START] {label}")
            function()
            print(f"[OK] {label}")
        except Exception as exc:
            had_error = True
            report["sources"][label] = {
                "status": "ERROR",
                "error": f"{type(exc).__name__}: {exc}",
            }
            print(f"[ERROR] {label}: {type(exc).__name__}: {exc}")

    save_json(OUT / "00_report.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"Output directory: {OUT}")

    # Keep workflow successful so artifacts are always uploaded for inspection.
    return 0


if __name__ == "__main__":
    sys.exit(main())
