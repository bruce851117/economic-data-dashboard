import calendar
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests

BLS_API_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "data" / "employment.json"
BATCH_SIZE = 10

# unit: thousand / percent / week
# transform: change = month-over-month level change; level = published level
SERIES = [
    # Establishment survey: payroll employment by industry
    ("CES0000000001", "Payroll Employment (Thousands)", "payroll", 0, "CES", "thousand", "change"),
    ("CES0500000001", "Private", "payroll", 1, "CES", "thousand", "change"),
    ("CES0600000001", "Goods-producing Sector", "payroll", 2, "CES", "thousand", "change"),
    ("CES1000000001", "Mining and Logging", "payroll", 3, "CES", "thousand", "change"),
    ("CES2000000001", "Construction", "payroll", 3, "CES", "thousand", "change"),
    ("CES3000000001", "Manufacturing", "payroll", 3, "CES", "thousand", "change"),
    ("CES0800000001", "Private Service-Providing", "payroll", 2, "CES", "thousand", "change"),
    ("CES4000000001", "Trade, Transportation, and Utilities", "payroll", 3, "CES", "thousand", "change"),
    ("CES4142000001", "Wholesale Trade", "payroll", 4, "CES", "thousand", "change"),
    ("CES4200000001", "Retail Trade", "payroll", 4, "CES", "thousand", "change"),
    ("CES4300000001", "Transportation and Warehousing", "payroll", 4, "CES", "thousand", "change"),
    ("CES4422000001", "Utilities", "payroll", 4, "CES", "thousand", "change"),
    ("CES5000000001", "Information", "payroll", 3, "CES", "thousand", "change"),
    ("CES5500000001", "Financial Activities", "payroll", 3, "CES", "thousand", "change"),
    ("CES6000000001", "Professional and Business Services", "payroll", 3, "CES", "thousand", "change"),
    ("CES6056132001", "Temporary Help Services", "payroll", 5, "CES", "thousand", "change"),
    ("CES6500000001", "Education and Health Services", "payroll", 3, "CES", "thousand", "change"),
    ("CES6562000001", "Health Care and Social Assistance", "payroll", 4, "CES", "thousand", "change"),
    ("CES6562000101", "Health Care", "payroll", 5, "CES", "thousand", "change"),
    ("CES6562100001", "Ambulatory Health Care Services", "payroll", 6, "CES", "thousand", "change"),
    ("CES6562200001", "Hospitals", "payroll", 6, "CES", "thousand", "change"),
    ("CES6562300001", "Nursing and Residential Care Facilities", "payroll", 6, "CES", "thousand", "change"),
    ("CES6562400001", "Social Assistance", "payroll", 5, "CES", "thousand", "change"),
    ("CES7000000001", "Leisure and Hospitality", "payroll", 3, "CES", "thousand", "change"),
    ("CES8000000001", "Other Services", "payroll", 3, "CES", "thousand", "change"),

    # Household survey levels
    ("LNS11000000", "Labor Force", "household", 0, "CPS", "thousand", "level"),
    ("LNS11300000", "Participation Rate", "household", 0, "CPS", "percent", "level"),
    ("LNS12000000", "Employed", "household", 0, "CPS", "thousand", "level"),
    ("LNS13000000", "Unemployed", "household", 0, "CPS", "thousand", "level"),
    ("LNS13000003", "White", "household", 1, "CPS", "thousand", "level"),
    ("LNS13000006", "Black or African American", "household", 1, "CPS", "thousand", "level"),
    ("LNS13000009", "Hispanic or Latino", "household", 1, "CPS", "thousand", "level"),
    ("LNS13032183", "Asian", "household", 1, "CPS", "thousand", "level"),

    # Gross flows into unemployment
    ("LNS17400000", "Employed to Unemployed", "flows", 0, "CPS", "thousand", "level"),
    ("LNS17500000", "Unemployed to Unemployed", "flows", 0, "CPS", "thousand", "level"),
    ("LNS17600000", "Not in Labor Force to Unemployed", "flows", 0, "CPS", "thousand", "level"),
    ("LNS17700000", "Other Inflows to Unemployment", "flows", 0, "CPS", "thousand", "level"),

    # Reasons for unemployment
    ("LNS13023653", "On Temporary Layoff", "reasons", 0, "CPS", "thousand", "level"),
    ("LNS13026638", "Permanent Job Losers", "reasons", 0, "CPS", "thousand", "level"),
    ("LNS13026637", "Completed Temp Job", "reasons", 0, "CPS", "thousand", "level"),
    ("LNS13023705", "Job Leavers", "reasons", 0, "CPS", "thousand", "level"),
    ("LNS13023557", "Reentrants", "reasons", 0, "CPS", "thousand", "level"),
    ("LNS13023569", "New Entrants", "reasons", 0, "CPS", "thousand", "level"),

    # Average duration
    ("LNS13008275", "平均失業 Duration", "duration", 0, "CPS", "week", "level"),
]


def registration_key():
    key = os.environ.get("BLS_API_KEY", "").strip()
    if not key:
        raise RuntimeError("Missing BLS_API_KEY environment variable.")
    return key


def request_batch(ids, number, total):
    current_year = datetime.now(timezone.utc).year
    payload = {
        "seriesid": ids,
        "startyear": str(current_year - 2),
        "endyear": str(current_year),
        "calculations": False,
        "annualaverage": False,
        "catalog": True,
        "aspects": False,
        "registrationkey": registration_key(),
    }
    print("=" * 72)
    print(f"BLS Employment batch: {number}/{total}")
    print("Requested series:", len(ids))
    print("Series IDs:", ", ".join(ids))
    response = requests.post(
        BLS_API_URL,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "EconomicDataDashboard/1.0 GitHub-Actions",
        },
        json=payload,
        timeout=90,
    )
    print("HTTP status:", response.status_code)
    print("Response length:", len(response.content), "bytes")
    response.raise_for_status()
    result = response.json()
    print("BLS response status:", result.get("status"))
    for message in result.get("message", []):
        print("-", message)
    if result.get("status") != "REQUEST_SUCCEEDED":
        raise RuntimeError(
            f"Employment batch {number}/{total} failed: {result.get('message', [])}; "
            f"series={ids}"
        )
    returned = result.get("Results", {}).get("series", [])
    print("Returned series:", len(returned))
    return returned


def fetch_all():
    ids = [item[0] for item in SERIES]
    batches = [ids[i:i + BATCH_SIZE] for i in range(0, len(ids), BATCH_SIZE)]
    print("Starting registered BLS employment data update.")
    print("Total employment series:", len(ids))
    print("Batch size:", BATCH_SIZE)
    print("Total batches:", len(batches))
    combined = []
    for number, batch in enumerate(batches, 1):
        combined.extend(request_batch(batch, number, len(batches)))
    return combined


def parse_series(series):
    observations = []
    for item in series.get("data", []):
        period = str(item.get("period", ""))
        if not period.startswith("M") or period == "M13":
            continue
        try:
            year = int(item["year"])
            month = int(period[1:])
            value = float(item["value"])
        except (KeyError, TypeError, ValueError):
            continue
        if 1 <= month <= 12:
            observations.append({
                "year": year,
                "month": month,
                "period": f"{year}-{month:02d}",
                "value": value,
            })
    observations.sort(key=lambda x: (x["year"], x["month"]))
    return observations


def transform(observations, mode):
    if mode == "level":
        return observations
    result = []
    for previous, current in zip(observations, observations[1:]):
        p = previous["year"] * 12 + previous["month"]
        c = current["year"] * 12 + current["month"]
        if c - p == 1:
            result.append({
                **current,
                "value": round(current["value"] - previous["value"], 3),
                "level": current["value"],
            })
    return result


def make_row(meta, api_lookup, order):
    series_id, name, section, level, source, unit, mode = meta
    api_series = api_lookup.get(series_id)
    observations = transform(parse_series(api_series), mode) if api_series else []
    title = ((api_series or {}).get("catalog") or {}).get("series_title", "")
    print(series_id, "|", name, "|", title, "| observations:", len(observations))
    return {
        "order": order,
        "name": name,
        "series_id": series_id,
        "section": section,
        "level": level,
        "source": source,
        "unit": unit,
        "transform": mode,
        "seasonality": "SA",
        "series_title": title,
        "months": observations,
    }


def period_list(rows):
    period_keys = set()
    for row in rows:
        period_keys.update(item["period"] for item in row["months"])
    selected = sorted(period_keys)[-12:]
    result = []
    for key in selected:
        year, month = map(int, key.split("-"))
        last_day = calendar.monthrange(year, month)[1]
        result.append({
            "year": year,
            "month": month,
            "period": key,
            "label": f"{year}/{month}/{last_day}",
        })
    return result


def align(row, periods):
    lookup = {item["period"]: item for item in row.pop("months")}
    row["values"] = [lookup.get(p["period"], {}).get("value") for p in periods]
    return row


def derived_row(name, section, source_rows, formula, unit="thousand", order=0):
    values = []
    for index in range(len(source_rows[0]["values"])):
        args = [row["values"][index] for row in source_rows]
        values.append(None if any(value is None for value in args) else round(formula(*args), 3))
    return {
        "order": order,
        "name": name,
        "series_id": None,
        "section": section,
        "level": 0,
        "source": "Derived",
        "unit": unit,
        "transform": "derived",
        "seasonality": "SA",
        "series_title": "Calculated from BLS CPS levels",
        "values": values,
    }


def main():
    returned = fetch_all()
    api_lookup = {item.get("seriesID", ""): item for item in returned}
    rows = [make_row(meta, api_lookup, order) for order, meta in enumerate(SERIES)]
    missing = [row["series_id"] for row in rows if not row["months"]]
    if missing:
        raise RuntimeError("Employment series returned no usable data: " + ", ".join(missing))

    periods = period_list(rows)
    rows = [align(row, periods) for row in rows]
    lookup = {row["series_id"]: row for row in rows}

    summary = [
        derived_row("Unemployment Rate", "summary", [lookup["LNS13000000"], lookup["LNS11000000"]], lambda u, lf: u / lf * 100, unit="percent", order=0),
        derived_row("勞動人口變化", "summary", [lookup["LNS11000000"]], lambda value: value, order=1),
        derived_row("Employed變化", "summary", [lookup["LNS12000000"]], lambda value: value, order=2),
        derived_row("Unemployed變化", "summary", [lookup["LNS13000000"]], lambda value: value, order=3),
    ]
    # Replace the three change rows with changes calculated from aligned levels.
    for target, source_id in zip(summary[1:], ["LNS11000000", "LNS12000000", "LNS13000000"]):
        levels = lookup[source_id]["values"]
        target["values"] = [None] + [None if levels[i] is None or levels[i - 1] is None else round(levels[i] - levels[i - 1], 3) for i in range(1, len(levels))]

    sections = {
        key: [row for row in rows if row["section"] == key]
        for key in ["payroll", "household", "flows", "reasons", "duration"]
    }
    sections["summary"] = summary

    payload = {
        "source": "U.S. Bureau of Labor Statistics",
        "api_url": BLS_API_URL,
        "updated_at_utc": datetime.now(timezone.utc).isoformat(),
        "default_months": 6,
        "available_filter_options": [3, 6, 12],
        "periods": periods,
        "sections": sections,
        "row_count": len(rows) + len(summary),
        "methodology": {
            "payroll": "CES seasonally adjusted all-employees levels converted to monthly changes",
            "household": "CPS seasonally adjusted published levels",
            "unemployment_rate": "Unemployed divided by labor force, displayed with two decimals",
        },
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print("=" * 72)
    print("Saved employment rows:", payload["row_count"])
    print("Saved periods:", len(periods))
    print("Output path:", OUTPUT_PATH)
    print("Employment period range:", periods[0]["period"], "to", periods[-1]["period"])


if __name__ == "__main__":
    main()
