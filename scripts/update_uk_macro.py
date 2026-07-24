from __future__ import annotations

import csv
import io
from io import BytesIO
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup, NavigableString
from pypdf import PdfReader

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


SP_RELEASES_URL = "https://www.pmi.spglobal.com/Public/Release/PressReleases"


def response_to_text(response: requests.Response) -> str:
    content_type = (response.headers.get("content-type") or "").lower()
    if response.content.startswith(b"%PDF") or "application/pdf" in content_type:
        reader = PdfReader(BytesIO(response.content))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    return BeautifulSoup(response.text, "html.parser").get_text("\n", strip=True)


def preceding_release_context(anchor: Any) -> str:
    parts = []
    for element in anchor.previous_elements:
        if isinstance(element, NavigableString):
            text = clean_cell(str(element))
            if text:
                parts.append(text)
        if len(" ".join(parts)) >= 280:
            break
    return " ".join(reversed(parts[-20:]))


def discover_sp_pmi_releases() -> list[dict[str, str]]:
    response = get(SP_RELEASES_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    candidates = []
    seen = set()

    for anchor in soup.find_all("a", href=True):
        href = anchor.get("href", "")
        if "/Public/Home/PressRelease/" not in href:
            continue
        url = requests.compat.urljoin(SP_RELEASES_URL, href)
        if url in seen:
            continue
        context = preceding_release_context(anchor)
        title_match = re.search(
            r"(S&P Global (?:Flash )?UK (?:Manufacturing|Services)?\s*PMI)",
            context,
            re.I,
        )
        if not title_match:
            continue
        title = clean_cell(title_match.group(1))
        release_date_match = re.search(
            r"([A-Za-z]+\s+\d{1,2}\s+20\d{2})\s+\d{2}:\d{2}\s+UTC",
            context,
            re.I,
        )
        candidates.append({
            "title": title,
            "url": url,
            "release_date": release_date_match.group(1) if release_date_match else "",
            "index_context": context,
        })
        seen.add(url)

    save_debug("sp_global_release_index_raw.html", response.text)
    save_debug("sp_global_release_candidates.json", candidates)
    debug_print("sp_global_release_candidates", candidates)
    return candidates


def extract_reference_month(text: str) -> str | None:
    head = clean_cell(text[:5000])
    matches = list(re.finditer(
        r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(20\d{2})\b",
        head,
        re.I,
    ))
    if not matches:
        return None
    # The report heading normally contains the reference month near the start.
    match = matches[0]
    month = MONTHS[match.group(1).lower()]
    return f"{int(match.group(2)):04d}-{month:02d}"


def extract_pmi_value(text: str, sector: str, release_type: str) -> float | None:
    compact = clean_cell(text)
    if sector == "manufacturing":
        patterns = [
            r"Manufacturing PMI(?:®|™)?\s+(?:at|posted|rose to|fell to)\s*([0-9]+(?:\.[0-9]+)?)",
            r"Manufacturing Purchasing Managers(?:’|') Index[^.]{0,180}?posted\s+([0-9]+(?:\.[0-9]+)?)",
            r"Manufacturing PMI[^.]{0,120}?([0-9]+(?:\.[0-9]+)?)\s+in\s+[A-Za-z]+",
        ]
    else:
        patterns = [
            r"Services PMI(?:®|™)?(?: Business Activity Index)?\s+(?:at|posted|rose to|fell to)\s*([0-9]+(?:\.[0-9]+)?)",
            r"UK Services PMI Business Activity Index[^.]{0,180}?posted\s+([0-9]+(?:\.[0-9]+)?)",
            r"Services Business Activity Index[^.]{0,180}?(?:at|posted)\s+([0-9]+(?:\.[0-9]+)?)",
        ]

    # Flash releases sometimes show a compact key-metrics line.
    if release_type == "flash":
        if sector == "manufacturing":
            patterns.insert(0, r"Flash UK Manufacturing PMI[^0-9]{0,80}([0-9]+(?:\.[0-9]+)?)")
        else:
            patterns.insert(0, r"Flash UK Services PMI[^0-9]{0,80}([0-9]+(?:\.[0-9]+)?)")

    for pattern in patterns:
        match = re.search(pattern, compact, re.I)
        if match:
            return float(match.group(1))
    return None


def update_sp_global_pmi(database: dict[str, Any]) -> dict[str, tuple[int, int]]:
    candidates = discover_sp_pmi_releases()
    observations = {"manufacturing": [], "services": []}
    release_debug = []

    for candidate in candidates:
        title_lower = candidate["title"].lower()
        release_type = "flash" if "flash" in title_lower else "final"
        sectors = []
        if "manufacturing" in title_lower:
            sectors.append("manufacturing")
        elif "services" in title_lower:
            sectors.append("services")
        elif "flash uk" in title_lower:
            sectors.extend(["manufacturing", "services"])
        else:
            continue

        try:
            response = get(candidate["url"])
            text = response_to_text(response)
        except Exception as error:
            release_debug.append({**candidate, "error": str(error)})
            continue

        reference_month = extract_reference_month(text)
        parsed = {
            **candidate,
            "release_type": release_type,
            "reference_month": reference_month,
            "content_type": response.headers.get("content-type"),
            "content_bytes": len(response.content),
            "values": {},
        }

        safe_name = candidate["url"].rstrip("/").split("/")[-1]
        save_debug(f"sp_release_{safe_name}.txt", text)

        if reference_month:
            for sector in sectors:
                value = extract_pmi_value(text, sector, release_type)
                parsed["values"][sector] = value
                if value is not None:
                    observations[sector].append({
                        "date": reference_month + "-01",
                        "value": value,
                        "release_type": release_type,
                        "source_url": candidate["url"],
                    })
        release_debug.append(parsed)

    selected = {}
    for sector, rows in observations.items():
        by_month: dict[str, list[dict[str, Any]]] = {}
        for row in rows:
            by_month.setdefault(month_key(row["date"]), []).append(row)
        selected[sector] = []
        for month, month_rows in by_month.items():
            month_rows.sort(
                key=lambda row: 1 if row["release_type"] == "final" else 0,
                reverse=True,
            )
            selected[sector].append(month_rows[0])
        selected[sector].sort(key=lambda row: row["date"])

    save_debug("sp_global_release_parsed.json", release_debug)
    save_debug("sp_global_pmi_selected.json", selected)
    debug_print("sp_global_release_parsed", release_debug)
    debug_print("sp_global_pmi_selected", selected)

    results = {}
    mapping = {
        "manufacturing": "mpmigbma",
        "services": "mpmigbsa",
    }
    for sector, series_id in mapping.items():
        if not selected[sector]:
            raise RuntimeError(f"No official S&P Global {sector} PMI observation found")
        added = revised = 0
        for row in selected[sector]:
            release_type = row["release_type"]
            point = {key: value for key, value in row.items() if key != "release_type"}
            a, r = merge(database, series_id, [point], release_type)
            added += a
            revised += r
        results[series_id] = (added, revised)
    return results


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

    try:
        pmi_results = update_sp_global_pmi(database)
        for pmi_id, result in pmi_results.items():
            logs.append((pmi_id, *result))
    except Exception as error:
        logs.append(("sp_global_pmi", "ERROR", str(error)))

    updates = [
        ("ukrvayoy", lambda: update_retail(database)),
        ("ukcci", lambda: update_gfk(database)),
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
