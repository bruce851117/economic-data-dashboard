from __future__ import annotations

import csv
import io
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup

DATA_FILE = Path("data/uk_macro.json")
DEBUG_DIR = Path("debug/uk_macro_sources")
USER_AGENT = "Mozilla/5.0 (compatible; UKMacroDashboard/1.0)"

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": USER_AGENT,
    "Accept-Language": "en-GB,en;q=0.9",
})

ONS = {
    "ukhca9iq": ("MM23", "DKO8", "economy/inflationandpriceindices", 0),
    "ukhpsery": ("MM23", "D7NN", "economy/inflationandpriceindices", 0),
    "ukueilor": ("LMS", "MGSX", "employmentandlabourmarket/peoplenotinwork/unemployment", 1),
    "ukuer": ("UNEM", "BCJE", "employmentandlabourmarket/peoplenotinwork/outofworkbenefits", 0),
    "ukawmwho": ("LMS", "KAC3", "employmentandlabourmarket/peopleinwork/earningsandworkinghours", 0),
    "ukawxprm": ("LMS", "KAJ4", "employmentandlabourmarket/peopleinwork/earningsandworkinghours", 0),
    # AP2Y Raw月份是3個月統計期間的中間月；Dashboard採發布月份，所以+2個月。
    "ukvaap2y": ("UNEM", "AP2Y", "employmentandlabourmarket/peopleinwork/employmentandemployeetypes", 2),
    "uklfjpc5": ("UNEM", "JPC5", "employmentandlabourmarket/peoplenotinwork/unemployment", 1),
    "ukgdm3m": ("MGDP", "ECYX", "economy/grossdomesticproductgdp", 0),
}

LEVELS = {
    "ukgrabiy": ("QNA", "ABMI", "economy/grossdomesticproductgdp"),
    "ukgeabry": ("PN2", "ABJR", "economy/nationalaccounts/satelliteaccounts"),
    "ukgvnpqy": ("UKEA", "NPQT", "economy/grossdomesticproductgdp"),
}

MONTHS = {
    name: index
    for index, name in enumerate(
        [
            "january", "february", "march", "april", "may", "june",
            "july", "august", "september", "october", "november", "december",
        ],
        1,
    )
}
MONTH_ABBR = {name[:3]: number for name, number in MONTHS.items()}

RETAIL_URL = "https://tradingeconomics.com/united-kingdom/retail-sales-ex-fuel"
GFK_URL = "https://tradingeconomics.com/united-kingdom/consumer-confidence"
MANUFACTURING_PMI_URL = (
    "https://www.investing.com/economic-calendar/"
    "united-kingdom-manufacturing-purchasing-managers-index-(pmi)-204"
)
SERVICES_PMI_URL = (
    "https://www.investing.com/economic-calendar/"
    "united-kingdom-services-purchasing-managers-index-(pmi)-274"
)


def get(url: str, **kwargs: Any) -> requests.Response:
    last_response: requests.Response | None = None
    for attempt in range(4):
        response = SESSION.get(url, timeout=60, **kwargs)
        last_response = response
        if response.status_code < 400:
            return response
        if response.status_code not in {429, 500, 502, 503, 504}:
            response.raise_for_status()
        time.sleep(3 * (2**attempt))
    assert last_response is not None
    last_response.raise_for_status()
    return last_response


def save_debug(name: str, payload: Any) -> None:
    DEBUG_DIR.mkdir(parents=True, exist_ok=True)
    path = DEBUG_DIR / name
    if isinstance(payload, str):
        path.write_text(payload, encoding="utf-8")
    else:
        path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


def debug_print(label: str, payload: Any) -> None:
    print(f"\n[DEBUG {label}]")
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def period(value: str) -> str | None:
    value = " ".join(str(value).upper().split())
    aliases = {
        "JAN": "01", "FEB": "02", "MAR": "03", "APR": "04",
        "MAY": "05", "JUN": "06", "JUL": "07", "AUG": "08",
        "SEP": "09", "OCT": "10", "NOV": "11", "DEC": "12",
    }
    month_match = re.fullmatch(r"(\d{4}) (" + "|".join(aliases) + r")", value)
    if month_match:
        return f"{month_match[1]}-{aliases[month_match[2]]}-01"
    quarter_match = re.fullmatch(r"(\d{4}) Q([1-4])", value)
    if quarter_match:
        return f"{quarter_match[1]}-{int(quarter_match[2]) * 3:02d}-01"
    return None


def shift_month(date_value: str, offset: int = 1) -> str:
    year, month = map(int, date_value[:7].split("-"))
    serial = year * 12 + month - 1 + offset
    return f"{serial // 12:04d}-{serial % 12 + 1:02d}-01"


def ons_series(dataset: str, cdid: str, path: str) -> list[dict[str, Any]]:
    edition = {"ABJR": "pn2", "ABMI": "qna", "NPQT": "ukea"}.get(
        cdid,
        dataset.lower(),
    )
    url = (
        "https://www.ons.gov.uk/generator?format=csv&uri=/"
        f"{path}/timeseries/{cdid.lower()}/{edition}"
    )
    raw = get(url).content.decode("utf-8-sig", "replace")
    rows = csv.reader(io.StringIO(raw))
    output = []
    for row in rows:
        if len(row) < 2:
            continue
        date_value = period(row[0])
        raw_value = row[1].replace(",", "").strip()
        if date_value and re.fullmatch(r"-?\d+(?:\.\d+)?", raw_value):
            output.append({
                "date": date_value,
                "value": float(raw_value),
                "source_url": url,
            })
    if not output:
        raise RuntimeError(f"ONS {cdid} returned no data")
    return output


def year_over_year(levels: list[dict[str, Any]]) -> list[dict[str, Any]]:
    indexed = {point["date"]: point for point in levels}
    output = []
    for date_value, point in indexed.items():
        previous_date = f"{int(date_value[:4]) - 1}{date_value[4:]}"
        previous = indexed.get(previous_date)
        if previous and previous["value"]:
            output.append({
                "date": date_value,
                "value": (point["value"] / previous["value"] - 1) * 100,
                "source_url": point["source_url"],
            })
    return output


def by_id(database: dict[str, Any], series_id: str) -> dict[str, Any] | None:
    return next(
        (item for item in database["series"] if item["id"] == series_id),
        None,
    )


def month_key(value: Any) -> str:
    match = re.match(r"^(\d{4})-(\d{2})", str(value or "").strip())
    return f"{match.group(1)}-{match.group(2)}" if match else ""


def merge(
    database: dict[str, Any],
    series_id: str,
    points: list[dict[str, Any]],
    release_type: str | None = None,
) -> tuple[int, int]:
    series = by_id(database, series_id)
    if not series:
        raise KeyError(series_id)

    old = {
        month_key(point.get("date")): {
            **point,
            "date": month_key(point.get("date")) + "-01",
        }
        for point in series.get("data", [])
        if month_key(point.get("date"))
    }

    added = revised = 0
    if old:
        latest_existing = max(old)
        points = [
            point
            for point in points
            if month_key(point.get("date")) >= latest_existing
        ]

    for point in points:
        key = month_key(point.get("date"))
        if not key:
            continue
        candidate = {**point, "date": key + "-01"}
        if release_type:
            candidate["release_type"] = release_type

        current = old.get(key)
        if current is None:
            old[key] = candidate
            added += 1
        elif (
            current.get("release_type") == "final"
            and candidate.get("release_type") == "flash"
        ):
            continue
        elif (
            current.get("value") != candidate.get("value")
            or (
                candidate.get("release_type") == "final"
                and current.get("release_type") != "final"
            )
        ):
            old[key] = {**current, **candidate}
            revised += 1

    series["data"] = sorted(old.values(), key=lambda item: item["date"])
    return added, revised


def clean_cell(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def extract_tables(html: str) -> list[list[list[str]]]:
    soup = BeautifulSoup(html, "html.parser")
    tables = []
    for table in soup.find_all("table"):
        rows = []
        for row in table.find_all("tr"):
            cells = [
                clean_cell(cell.get_text(" ", strip=True))
                for cell in row.find_all(["th", "td"])
            ]
            if cells:
                rows.append(cells)
        if rows:
            tables.append(rows)
    return tables


def number_or_none(value: str) -> float | None:
    cleaned = value.replace(",", "").replace("%", "").strip()
    if not cleaned or cleaned in {"-", "N/A", "n/a"}:
        return None
    match = re.fullmatch(r"[+-]?\d+(?:\.\d+)?", cleaned)
    return float(cleaned) if match else None


def te_reference_month(release_date: str, reference: str) -> str | None:
    date_match = re.match(r"(20\d{2})-(\d{2})-(\d{2})", release_date)
    if not date_match:
        return None
    reference_no = MONTH_ABBR.get(reference.strip().lower()[:3])
    if not reference_no:
        return None
    year = int(date_match.group(1))
    release_month = int(date_match.group(2))
    if reference_no > release_month + 1:
        year -= 1
    return f"{year:04d}-{reference_no:02d}-01"


def update_te_table(
    database: dict[str, Any],
    series_id: str,
    url: str,
    indicator_name: str,
    debug_name: str,
) -> tuple[int, int]:
    response = get(url)
    tables = extract_tables(response.text)
    matched_rows = []
    points = []

    for table_no, table in enumerate(tables, 1):
        for row_no, cells in enumerate(table, 1):
            if len(cells) < 6 or indicator_name.lower() not in cells[2].lower():
                continue
            release_date, release_time, indicator, reference, actual = cells[:5]
            matched_rows.append({
                "table_no": table_no,
                "row_no": row_no,
                "cells": cells,
                "release_date": release_date,
                "reference": reference,
                "actual_raw": actual,
            })
            actual_value = number_or_none(actual)
            date_value = te_reference_month(release_date, reference)
            if actual_value is None or not date_value:
                continue
            points.append({
                "date": date_value,
                "value": actual_value,
                "source_url": url,
            })

    save_debug(f"{debug_name}_raw.html", response.text)
    save_debug(f"{debug_name}_tables.json", tables)
    save_debug(f"{debug_name}_matched_rows.json", matched_rows)
    debug_print(debug_name, matched_rows)

    if not points:
        raise RuntimeError(f"No actual rows found for {indicator_name}")
    return merge(database, series_id, points)


def update_retail(database: dict[str, Any]) -> tuple[int, int]:
    return update_te_table(
        database,
        "ukrvayoy",
        RETAIL_URL,
        "Retail Sales ex Fuel YoY",
        "retail_ex_fuel",
    )


def update_gfk(database: dict[str, Any]) -> tuple[int, int]:
    return update_te_table(
        database,
        "ukcci",
        GFK_URL,
        "GfK Consumer Confidence",
        "gfk_consumer_confidence",
    )


def parse_investing_release_date(value: str) -> tuple[datetime, int] | None:
    match = re.search(
        r"([A-Za-z]{3})\s+(\d{1,2}),\s*(20\d{2})\s*\(([A-Za-z]{3})\)",
        value,
    )
    if not match:
        return None
    release_date = datetime.strptime(
        f"{match.group(1)} {match.group(2)} {match.group(3)}",
        "%b %d %Y",
    )
    reference_month = MONTH_ABBR.get(match.group(4).lower())
    if not reference_month:
        return None
    return release_date, reference_month


def update_investing_pmi(
    database: dict[str, Any],
    series_id: str,
    url: str,
    debug_name: str,
) -> tuple[int, int]:
    response = get(url)
    tables = extract_tables(response.text)
    parsed_rows = []
    candidates: dict[str, list[dict[str, Any]]] = {}

    for table_no, table in enumerate(tables, 1):
        for row_no, cells in enumerate(table, 1):
            if len(cells) < 5:
                continue
            parsed_date = parse_investing_release_date(cells[0])
            if not parsed_date:
                continue
            release_date, reference_month = parsed_date
            actual_value = number_or_none(cells[2])
            row_debug = {
                "table_no": table_no,
                "row_no": row_no,
                "cells": cells,
                "release_date": release_date.date().isoformat(),
                "reference_month": reference_month,
                "actual": actual_value,
            }
            parsed_rows.append(row_debug)
            if actual_value is None:
                continue

            reference_year = release_date.year
            if reference_month > release_date.month + 1:
                reference_year -= 1
            key = f"{reference_year:04d}-{reference_month:02d}"

            # 同一參考月份：參考月內發布的是Flash；次月發布的是Final。
            release_type = (
                "final"
                if (release_date.year, release_date.month)
                > (reference_year, reference_month)
                else "flash"
            )
            candidates.setdefault(key, []).append({
                "date": key + "-01",
                "value": actual_value,
                "release_type": release_type,
                "release_date": release_date.date().isoformat(),
                "source_url": url,
            })

    selected = []
    for key, rows in candidates.items():
        rows.sort(
            key=lambda row: (
                1 if row["release_type"] == "final" else 0,
                row["release_date"],
            ),
            reverse=True,
        )
        selected.append(rows[0])

    save_debug(f"{debug_name}_raw.html", response.text)
    save_debug(f"{debug_name}_tables.json", tables)
    save_debug(f"{debug_name}_parsed_rows.json", parsed_rows)
    save_debug(f"{debug_name}_selected.json", selected)
    debug_print(debug_name + "_parsed_rows", parsed_rows)
    debug_print(debug_name + "_selected", selected)

    if not selected:
        raise RuntimeError(f"No PMI actual rows found from {url}")

    # Process months in chronological order. This matters when the newest month
    # is Flash but the preceding month has a Final: adding the Flash first would
    # otherwise make the older Final look older than the latest stored month.
    added = revised = 0
    for row in sorted(selected, key=lambda item: item["date"]):
        release_type = row["release_type"]
        point = {
            key: value
            for key, value in row.items()
            if key != "release_type"
        }
        result = merge(database, series_id, [point], release_type)
        added += result[0]
        revised += result[1]
    return added, revised


def dmp_page_candidates() -> list[tuple[str, str]]:
    now = datetime.now(timezone.utc)
    output = []
    for offset in range(0, 6):
        serial = now.year * 12 + now.month - 1 - offset
        year = serial // 12
        month = serial % 12 + 1
        month_name = list(MONTHS)[month - 1]
        output.append((
            f"{year:04d}-{month:02d}",
            f"https://www.bankofengland.co.uk/decision-maker-panel/{year}/{month_name}-{year}",
        ))
    return output


def update_dmp_inflation(database: dict[str, Any]) -> tuple[int, int]:
    debug_pages = []
    for reference_month, url in dmp_page_candidates():
        try:
            response = get(url)
        except Exception as error:
            debug_pages.append({"url": url, "error": str(error)})
            continue

        text = clean_cell(BeautifulSoup(response.text, "html.parser").get_text(" ", strip=True))
        contexts = []
        for match in re.finditer(r"year-ahead CPI inflation", text, re.I):
            contexts.append(text[max(0, match.start() - 180): match.end() + 300])

        value = None
        # Prefer the single-month DMP value. Example:
        # "In the single-month data year-ahead CPI inflation expectations
        # fell from 3.7% to 3.3%."  The required value is the final 3.3%,
        # not the three-month average of 3.7% mentioned earlier.
        patterns = [
            r"single-month data[^.]{0,220}?year-ahead CPI inflation expectations[^.]{0,160}?"
            r"(?:fell|rose|increased|decreased|moved|changed)\s+from\s+\d+(?:\.\d+)?%\s+to\s+"
            r"(\d+(?:\.\d+)?)%",
            r"single-month data[^.]{0,220}?year-ahead CPI inflation expectations[^.]{0,160}?"
            r"(?:were|was|stood at|remained at)\s+(\d+(?:\.\d+)?)%",
            r"single-month[^.]{0,220}?year-ahead CPI inflation expectations[^.]{0,160}?"
            r"(?:to|at)\s+(\d+(?:\.\d+)?)%",
        ]
        for pattern_value in patterns:
            match = re.search(pattern_value, text, re.I)
            if match:
                value = float(match.group(1))
                break

        debug_pages.append({
            "url": url,
            "reference_month": reference_month,
            "status": response.status_code,
            "contexts": contexts,
            "parsed_value": value,
        })
        save_debug("boe_dmp_latest_page.html", response.text)

        if value is not None:
            save_debug("boe_dmp_debug.json", debug_pages)
            debug_print("boe_dmp", debug_pages)
            return merge(database, "ukbfftin", [{
                "date": reference_month + "-01",
                "value": value,
                "source_url": url,
                "measure": "DMP year-ahead CPI inflation expectations",
            }])

    save_debug("boe_dmp_debug.json", debug_pages)
    debug_print("boe_dmp", debug_pages)
    raise RuntimeError("BoE DMP year-ahead CPI expectation not found")


def main() -> None:
    database = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    logs = []

    for series_id, (dataset, cdid, path, month_shift) in ONS.items():
        try:
            points = ons_series(dataset, cdid, path)
            if month_shift:
                points = [
                    {**point, "date": shift_month(point["date"], month_shift)}
                    for point in points
                ]
            logs.append((series_id, *merge(database, series_id, points)))
        except Exception as error:
            logs.append((series_id, "ERROR", str(error)))

    for series_id, (dataset, cdid, path) in LEVELS.items():
        try:
            points = year_over_year(ons_series(dataset, cdid, path))
            logs.append((series_id, *merge(database, series_id, points)))
        except Exception as error:
            logs.append((series_id, "ERROR", str(error)))

    updates = [
        ("ukrvayoy", lambda: update_retail(database)),
        ("ukcci", lambda: update_gfk(database)),
        (
            "mpmigbma",
            lambda: update_investing_pmi(
                database,
                "mpmigbma",
                MANUFACTURING_PMI_URL,
                "manufacturing_pmi_investing",
            ),
        ),
        (
            "mpmigbsa",
            lambda: update_investing_pmi(
                database,
                "mpmigbsa",
                SERVICES_PMI_URL,
                "services_pmi_investing",
            ),
        ),
        ("ukbfftin", lambda: update_dmp_inflation(database)),
    ]

    for name, update_function in updates:
        try:
            logs.append((name, *update_function()))
        except Exception as error:
            logs.append((name, "ERROR", str(error)))

    database["generated_at"] = datetime.now(timezone.utc).isoformat()
    DATA_FILE.write_text(
        json.dumps(database, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("\n[UPDATE SUMMARY]")
    for entry in logs:
        print(*entry)
    print(f"\nDebug files saved under: {DEBUG_DIR}")


if __name__ == "__main__":
    main()
