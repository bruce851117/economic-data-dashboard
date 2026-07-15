import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests


BLS_API_URL = (
    "https://api.bls.gov/publicAPI/v2/timeseries/data/"
)

BLS_SOURCE_URL = (
    "https://www.bls.gov/news.release/cpi.t02.htm"
)

OUTPUT_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "cpi.json"
)


CPI_SERIES = [
    {
        "name": "All Items",
        "display_code": "CPI INDX",
        "bls_series_id": "CUSR0000SA0",
        "level": 0,
        "seasonality": "SA",
    },
    {
        "name": "Food",
        "display_code": "CPSFFOOD",
        "bls_series_id": "CUSR0000SAF1",
        "level": 0,
        "seasonality": "SA",
    },
    {
        "name": "Energy",
        "display_code": "CPUPENER",
        "bls_series_id": "CUSR0000SA0E",
        "level": 0,
        "seasonality": "SA",
    },
    {
        "name": "All Items Less Food and Energy",
        "display_code": "CPUPAXFE",
        "bls_series_id": "CUSR0000SA0L1E",
        "level": 0,
        "seasonality": "SA",
    },
    {
        "name": (
            "Commodities Excluding Food "
            "and Energy Commodities"
        ),
        "display_code": "CPUPCXFE",
        "bls_series_id": "CUSR0000SACL1E",
        "level": 1,
        "seasonality": "SA",
    },
    {
        "name": "Household Furnishings and Supplies",
        "display_code": "CPIQHFAS",
        "bls_series_id": "CUSR0000SAH3",
        "level": 2,
        "seasonality": "SA",
    },
    {
        "name": "Apparel",
        "display_code": "CPSCTOT",
        "bls_series_id": "CUSR0000SAA",
        "level": 2,
        "seasonality": "SA",
    },
    {
        "name": (
            "Transportation Commodities "
            "Less Motor Fuel"
        ),
        "display_code": "CPIQTCMS",
        "bls_series_id": "CUSR0000SAT1",
        "level": 2,
        "seasonality": "SA",
    },
    {
        "name": "New Vehicles",
        "display_code": "CPSTNV",
        "bls_series_id": "CUSR0000SETA01",
        "level": 3,
        "seasonality": "SA",
    },
    {
        "name": "Used Cars and Trucks",
        "display_code": "CPSTUCTR",
        "bls_series_id": "CUSR0000SETA02",
        "level": 3,
        "seasonality": "SA",
    },
    {
        "name": "Medical Care Commodities",
        "display_code": "CPUMCMDY",
        "bls_series_id": "CUSR0000SAM1",
        "level": 2,
        "seasonality": "SA",
    },
    {
        "name": "Recreation Commodities",
        "display_code": "CPIQRECS",
        "bls_series_id": "CUSR0000SARC",
        "level": 2,
        "seasonality": "SA",
    },
    {
        "name": (
            "Education and Communication Commodities"
        ),
        "display_code": "CPIQECCS",
        "bls_series_id": "CUSR0000SAE2",
        "level": 2,
        "seasonality": "SA",
    },
    {
        "name": "Alcoholic Beverages",
        "display_code": "CPSFAB",
        "bls_series_id": "CUSR0000SAF116",
        "level": 2,
        "seasonality": "SA",
    },
    {
        "name": "Other Goods",
        "display_code": "CPIQOTGS",
        "bls_series_id": "CUSR0000SAG",
        "level": 2,
        "seasonality": "SA",
    },
    {
        "name": "Services Excluding Energy Services",
        "display_code": "CPUPSXEN",
        "bls_series_id": "CUSR0000SASLE",
        "level": 1,
        "seasonality": "SA",
    },
    {
        "name": "Shelter",
        "display_code": "CPSHSHLT",
        "bls_series_id": "CUSR0000SAH1",
        "level": 2,
        "seasonality": "SA",
    },
    {
        "name": "Rent of Primary Residence",
        "display_code": "CPSHRPR",
        "bls_series_id": "CUSR0000SEHA",
        "level": 4,
        "seasonality": "SA",
    },
    {
        "name": "Lodging Away from Home",
        "display_code": "CPSHLODG",
        "bls_series_id": "CUSR0000SEHB",
        "level": 4,
        "seasonality": "SA",
    },
    {
        "name": (
            "Owners' Equivalent Rent of Residences"
        ),
        "display_code": "CPSHOEQR",
        "bls_series_id": "CUSR0000SEHC",
        "level": 4,
        "seasonality": "SA",
    },
    {
        "name": (
            "Water, Sewer and Trash Collection Services"
        ),
        "display_code": "CPSHWSTC",
        "bls_series_id": "CUSR0000SEHG01",
        "level": 2,
        "seasonality": "SA",
    },
    {
        "name": "Medical Care Services",
        "display_code": "CPUMSERV",
        "bls_series_id": "CUSR0000SAM2",
        "level": 2,
        "seasonality": "SA",
    },
    {
        "name": "Professional Services",
        "display_code": "CPUMPROF Index",
        "bls_series_id": "CUSR0000SEMC",
        "level": 3,
        "seasonality": "SA",
    },
    {
        "name": "Hospital and Related Services",
        "display_code": "CPUMHOSP Index",
        "bls_series_id": "CUSR0000SEMD",
        "level": 3,
        "seasonality": "SA",
    },
    {
        "name": "Health Insurance",
        "display_code": "CPRMHEUS",
        "bls_series_id": "CUUR0000SEME",
        "level": 3,
        "seasonality": "NSA",
    },
    {
        "name": "Transportation Services",
        "display_code": "CPSSTRAN",
        "bls_series_id": "CUSR0000SAS4",
        "level": 2,
        "seasonality": "SA",
    },
    {
        "name": "Car and Truck Rental",
        "display_code": "CPIQCTRS Index",
        "bls_series_id": "CUSR0000SETD03",
        "level": 3,
        "seasonality": "SA",
    },
    {
        "name": (
            "Motor Vehicle Maintenance and Repair"
        ),
        "display_code": "CPSTMVMR",
        "bls_series_id": "CUSR0000SETD",
        "level": 3,
        "seasonality": "SA",
    },
    {
        "name": "Motor Vehicle Insurance",
        "display_code": "CPSTMVSA",
        "bls_series_id": "CUSR0000SETE",
        "level": 3,
        "seasonality": "SA",
    },
    {
        "name": "Public Transportation",
        "display_code": "CPSTPUBL",
        "bls_series_id": "CUSR0000SETG",
        "level": 3,
        "seasonality": "SA",
    },
    {
        "name": "Airline Fare",
        "display_code": "CPSTAIRF",
        "bls_series_id": "CUSR0000SETG01",
        "level": 4,
        "seasonality": "SA",
    },
    {
        "name": "Recreation Services",
        "display_code": "CPIQRESS",
        "bls_series_id": "CUSR0000SERA",
        "level": 2,
        "seasonality": "SA",
    },
    {
        "name": (
            "Education and Communication Services"
        ),
        "display_code": "CPIQECSS",
        "bls_series_id": "CUSR0000SAE1",
        "level": 2,
        "seasonality": "SA",
    },
]


def get_registration_key():
    registration_key = os.environ.get(
        "BLS_API_KEY",
        "",
    ).strip()

    if not registration_key:
        raise RuntimeError(
            "Missing BLS_API_KEY environment variable."
        )

    return registration_key


def current_year():
    return datetime.now(timezone.utc).year


def fetch_cpi_series():
    registration_key = get_registration_key()

    series_ids = [
        item["bls_series_id"]
        for item in CPI_SERIES
    ]

    payload = {
        "seriesid": series_ids,
        "startyear": str(current_year() - 2),
        "endyear": str(current_year()),
        "calculations": False,
        "annualaverage": False,
        "catalog": True,
        "aspects": False,
        "registrationkey": registration_key,
    }

    print("=" * 72)
    print("Calling registered BLS Public Data API.")
    print(f"API URL: {BLS_API_URL}")
    print(f"Requested CPI series: {len(series_ids)}")
    print(
        "Requested years:",
        payload["startyear"],
        "to",
        payload["endyear"],
    )

    response = requests.post(
        BLS_API_URL,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": (
                "EconomicDataDashboard/1.0 "
                "GitHub-Actions"
            ),
        },
        json=payload,
        timeout=90,
    )

    print(f"HTTP status: {response.status_code}")
    print(
        f"Response length: {len(response.content)} bytes"
    )

    if response.status_code != 200:
        raise RuntimeError(
            "BLS API returned an HTTP error.\n"
            f"HTTP status: {response.status_code}\n"
            f"Response: {response.text[:3000]}"
        )

    try:
        result = response.json()
    except requests.JSONDecodeError as error:
        raise RuntimeError(
            "BLS API did not return valid JSON."
        ) from error

    status = result.get("status", "")
    messages = result.get("message", [])

    print(f"BLS response status: {status}")

    if messages:
        print("BLS response messages:")

        for message in messages:
            print(f"- {message}")

    if status != "REQUEST_SUCCEEDED":
        raise RuntimeError(
            "BLS API request did not succeed.\n"
            f"Status: {status}\n"
            f"Messages: {messages}"
        )

    returned_series = (
        result
        .get("Results", {})
        .get("series", [])
    )

    if not returned_series:
        raise RuntimeError(
            "BLS API returned no CPI series."
        )

    print(
        f"Returned CPI series: {len(returned_series)}"
    )
    print("=" * 72)

    return returned_series


def parse_observations(series):
    observations = []

    for observation in series.get("data", []):
        period = observation.get("period", "")

        if not period.startswith("M"):
            continue

        if period == "M13":
            continue

        try:
            month = int(period[1:])
            year = int(observation["year"])
            value = float(observation["value"])
        except (KeyError, TypeError, ValueError):
            continue

        if not 1 <= month <= 12:
            continue

        observations.append(
            {
                "year": year,
                "month": month,
                "period": f"{year}-{month:02d}",
                "period_name": observation.get(
                    "periodName",
                    "",
                ),
                "index_value": value,
                "latest": observation.get(
                    "latest",
                    False,
                ),
            }
        )

    observations.sort(
        key=lambda row: (
            row["year"],
            row["month"],
        )
    )

    return observations


def calculate_percent_change(
    current_value,
    previous_value,
):
    if previous_value == 0:
        return None

    result = (
        (current_value / previous_value)
        - 1
    ) * 100

    return round(result, 4)


def build_monthly_changes(observations):
    changes = []

    for index in range(1, len(observations)):
        current = observations[index]
        previous = observations[index - 1]

        value = calculate_percent_change(
            current["index_value"],
            previous["index_value"],
        )

        changes.append(
            {
                "year": current["year"],
                "month": current["month"],
                "period": current["period"],
                "period_name": current["period_name"],
                "value": value,
                "index_value": current["index_value"],
                "latest": current["latest"],
            }
        )

    return changes[-12:]


def build_rows(api_series):
    api_lookup = {
        series.get("seriesID", ""): series
        for series in api_series
    }

    rows = []
    missing_series = []

    for order, config in enumerate(CPI_SERIES):
        series_id = config["bls_series_id"]
        series = api_lookup.get(series_id)

        monthly_changes = []
        series_title = ""

        if series:
            observations = parse_observations(
                series
            )

            monthly_changes = build_monthly_changes(
                observations
            )

            catalog = series.get(
                "catalog",
                {},
            ) or {}

            series_title = catalog.get(
                "series_title",
                "",
            )

        if not monthly_changes:
            missing_series.append(
                {
                    "name": config["name"],
                    "series_id": series_id,
                    "reason": (
                        "Series contained no usable "
                        "monthly observations"
                    ),
                }
            )

        rows.append(
            {
                "order": order,
                "name": config["name"],
                "display_code": (
                    config["display_code"]
                ),
                "bls_series_id": series_id,
                "level": config["level"],
                "seasonality": (
                    config["seasonality"]
                ),
                "available": bool(monthly_changes),
                "series_title": series_title,
                "months": monthly_changes,
            }
        )

    return rows, missing_series


def collect_periods(rows):
    period_lookup = {}

    for row in rows:
        for month in row.get("months", []):
            period_lookup[month["period"]] = {
                "year": month["year"],
                "month": month["month"],
                "period": month["period"],
                "period_name": month["period_name"],
                "label": (
                    f"{str(month['year'])[2:]} "
                    f"{month['period_name'][:3]}"
                ),
            }

    periods = list(period_lookup.values())

    periods.sort(
        key=lambda item: (
            item["year"],
            item["month"],
        )
    )

    return periods[-12:]


def align_rows(rows, periods):
    period_keys = [
        item["period"]
        for item in periods
    ]

    aligned_rows = []

    for row in rows:
        month_lookup = {
            month["period"]: month
            for month in row.get("months", [])
        }

        values = []

        for period in period_keys:
            month = month_lookup.get(period)

            values.append(
                month.get("value")
                if month
                else None
            )

        aligned_row = dict(row)
        aligned_row["values"] = values
        aligned_row.pop("months", None)

        aligned_rows.append(aligned_row)

    return aligned_rows


def load_existing_payload():
    if not OUTPUT_PATH.exists():
        return None

    try:
        with OUTPUT_PATH.open(
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)

    except (OSError, json.JSONDecodeError):
        return None


def save_json(
    periods,
    rows,
    missing_series,
):
    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    aligned_rows = align_rows(
        rows,
        periods,
    )

    existing = load_existing_payload()

    data_changed = True
    updated_at_utc = (
        datetime.now(timezone.utc).isoformat()
    )

    if existing:
        if (
            existing.get("periods", []) == periods
            and existing.get("rows", []) == aligned_rows
            and existing.get(
                "missing_series",
                [],
            ) == missing_series
        ):
            data_changed = False

            updated_at_utc = existing.get(
                "updated_at_utc",
                updated_at_utc,
            )

    payload = {
        "source": (
            "U.S. Bureau of Labor Statistics"
        ),
        "source_type": (
            "BLS Public Data API Version 2"
        ),
        "api_url": BLS_API_URL,
        "source_url": BLS_SOURCE_URL,
        "title": (
            "Consumer Price Index - "
            "Monthly Percent Change"
        ),
        "description": (
            "Seasonally adjusted monthly percent "
            "changes calculated from BLS CPI index "
            "levels. Health Insurance uses the "
            "not seasonally adjusted BLS series."
        ),
        "updated_at_utc": updated_at_utc,
        "data_changed": data_changed,
        "default_months": 6,
        "available_filter_options": [
            3,
            6,
            12,
        ],
        "period_count": len(periods),
        "row_count": len(aligned_rows),
        "missing_series_count": len(
            missing_series
        ),
        "periods": periods,
        "rows": aligned_rows,
        "missing_series": missing_series,
    }

    temporary_path = OUTPUT_PATH.with_suffix(
        ".json.tmp"
    )

    with temporary_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            payload,
            file,
            ensure_ascii=False,
            indent=2,
        )

    temporary_path.replace(OUTPUT_PATH)

    print("=" * 72)
    print(f"Saved CPI rows: {len(aligned_rows)}")
    print(f"Saved periods: {len(periods)}")
    print(
        f"Missing series: {len(missing_series)}"
    )
    print(f"Data changed: {data_changed}")
    print(f"Output path: {OUTPUT_PATH}")

    if periods:
        print(
            "Period range:",
            periods[0]["period"],
            "to",
            periods[-1]["period"],
        )

    if missing_series:
        print("WARNING: Missing CPI series:")

        for item in missing_series:
            print(
                f"- {item['name']} "
                f"({item['series_id']}): "
                f"{item['reason']}"
            )

    print("=" * 72)


def main():
    print(
        "Starting registered BLS CPI data update."
    )

    api_series = fetch_cpi_series()

    rows, missing_series = build_rows(
        api_series
    )

    periods = collect_periods(rows)

    if len(periods) != 12:
        raise RuntimeError(
            "Expected 12 CPI periods, but generated "
            f"{len(periods)} periods."
        )

    save_json(
        periods=periods,
        rows=rows,
        missing_series=missing_series,
    )


if __name__ == "__main__":
    main()