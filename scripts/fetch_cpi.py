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


# level：
# 0 = 最上層主要分類
# 1 = 第一層子分類
# 2 = 第二層子分類
# 3 = 第三層子分類
# 4 = 第四層子分類
#
# display_code：
# 顯示使用者提供的 Bloomberg／資料終端代碼。
#
# bls_series_id：
# BLS Public Data API 實際使用的季調 CPI Series ID。
CPI_SERIES = [
    {
        "name": "All Items",
        "display_code": "CPI INDX",
        "bls_series_id": "CUSR0000SA0",
        "level": 0,
    },
    {
        "name": "Food",
        "display_code": "CPSFFOOD",
        "bls_series_id": "CUSR0000SAF1",
        "level": 0,
    },
    {
        "name": "Energy",
        "display_code": "CPUPENER",
        "bls_series_id": "CUSR0000SA0E",
        "level": 0,
    },
    {
        "name": "All Items Less Food and Energy",
        "display_code": "CPUPAXFE",
        "bls_series_id": "CUSR0000SA0L1E",
        "level": 0,
    },
    {
        "name": (
            "Commodities Excluding Food "
            "and Energy Commodities"
        ),
        "display_code": "CPUPCXFE",
        "bls_series_id": "CUSR0000SACL1E",
        "level": 1,
    },
    {
        "name": "Household Furnishings and Supplies",
        "display_code": "CPIQHFAS",
        "bls_series_id": "CUSR0000SAH3",
        "level": 2,
    },
    {
        "name": "Apparel",
        "display_code": "CPSCTOT",
        "bls_series_id": "CUSR0000SAA",
        "level": 2,
    },
    {
        "name": (
            "Transportation Commodities "
            "Less Motor Fuel"
        ),
        "display_code": "CPIQTCMS",
        "bls_series_id": "CUSR0000SAT1",
        "level": 2,
    },
    {
        "name": "New Vehicles",
        "display_code": "CPSTNV",
        "bls_series_id": "CUSR0000SETA01",
        "level": 3,
    },
    {
        "name": "Used Cars and Trucks",
        "display_code": "CPSTUCTR",
        "bls_series_id": "CUSR0000SETA02",
        "level": 3,
    },
    {
        "name": "Medical Care Commodities",
        "display_code": "CPUMCMDY",
        "bls_series_id": "CUSR0000SAM1",
        "level": 2,
    },
    {
        "name": "Recreation Commodities",
        "display_code": "CPIQRECS",
        "bls_series_id": "CUSR0000SARC",
        "level": 2,
    },
    {
        "name": (
            "Education and Communication Commodities"
        ),
        "display_code": "CPIQECCS",
        "bls_series_id": "CUSR0000SAE2",
        "level": 2,
    },
    {
        "name": "Alcoholic Beverages",
        "display_code": "CPSFAB",
        "bls_series_id": "CUSR0000SAB",
        "level": 2,
    },
    {
        "name": "Other Goods",
        "display_code": "CPIQOTGS",
        "bls_series_id": "CUSR0000SAG",
        "level": 2,
    },
    {
        "name": "Services Excluding Energy Services",
        "display_code": "CPUPSXEN",
        "bls_series_id": "CUSR0000SASLE",
        "level": 1,
    },
    {
        "name": "Shelter",
        "display_code": "CPSHSHLT",
        "bls_series_id": "CUSR0000SAH1",
        "level": 2,
    },
    {
        "name": "Rent of Primary Residence",
        "display_code": "CPSHRPR",
        "bls_series_id": "CUSR0000SEHA",
        "level": 4,
    },
    {
        "name": "Lodging Away from Home",
        "display_code": "CPSHLODG",
        "bls_series_id": "CUSR0000SEHB",
        "level": 4,
    },
    {
        "name": (
            "Owners' Equivalent Rent of Residences"
        ),
        "display_code": "CPSHOEQR",
        "bls_series_id": "CUSR0000SEHC",
        "level": 4,
    },
    {
        "name": (
            "Water, Sewer and Trash Collection Services"
        ),
        "display_code": "CPSHWSTC",
        "bls_series_id": "CUSR0000SEHG01",
        "level": 2,
    },
    {
        "name": "Medical Care Services",
        "display_code": "CPUMSERV",
        "bls_series_id": "CUSR0000SAM2",
        "level": 2,
    },
    {
        "name": "Professional Services",
        "display_code": "CPUMPROF Index",
        "bls_series_id": "CUSR0000SEMC",
        "level": 3,
    },
    {
        "name": "Hospital and Related Services",
        "display_code": "CPUMHOSP Index",
        "bls_series_id": "CUSR0000SEMD",
        "level": 3,
    },
    {
        "name": "Health Insurance",
        "display_code": "CPRMHEUS",
        "bls_series_id": "CUSR0000SEME",
        "level": 3,
    },
    {
        "name": "Transportation Services",
        "display_code": "CPSSTRAN",
        "bls_series_id": "CUSR0000SAS4",
        "level": 2,
    },
    {
        "name": "Car and Truck Rental",
        "display_code": "CPIQCTRS Index",
        "bls_series_id": "CUSR0000SETD03",
        "level": 3,
    },
    {
        "name": (
            "Motor Vehicle Maintenance and Repair"
        ),
        "display_code": "CPSTMVMR",
        "bls_series_id": "CUSR0000SETD",
        "level": 3,
    },
    {
        "name": "Motor Vehicle Insurance",
        "display_code": "CPSTMVSA",
        "bls_series_id": "CUSR0000SETE",
        "level": 3,
    },
    {
        "name": "Public Transportation",
        "display_code": "CPSTPUBL",
        "bls_series_id": "CUSR0000SETG",
        "level": 3,
    },
    {
        "name": "Airline Fare",
        "display_code": "CPSTAIRF",
        "bls_series_id": "CUSR0000SETG01",
        "level": 4,
    },
    {
        "name": "Recreation Services",
        "display_code": "CPIQRESS",
        "bls_series_id": "CUSR0000SERA",
        "level": 2,
    },
    {
        "name": (
            "Education and Communication Services"
        ),
        "display_code": "CPIQECSS",
        "bls_series_id": "CUSR0000SAE1",
        "level": 2,
    },
]


def get_registration_key():
    """
    從 GitHub Actions Environment 取得 BLS API Key。
    """
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
    """
    使用註冊版 BLS Public Data API 抓取 CPI Series。

    需要至少13個月的指數，才能計算最近12個月月增率；
    這裡抓目前年份與前一年度，以涵蓋跨年情況。
    """
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
        f"Requested years: "
        f"{payload['startyear']} to {payload['endyear']}"
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


def parse_monthly_observations(series):
    """
    將 BLS Series 轉成按日期排序的月資料。

    排除 M13 年度平均，只保留 M01 至 M12。
    """
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
                "footnotes": [
                    footnote.get("text", "")
                    for footnote in observation.get(
                        "footnotes",
                        []
                    )
                    if footnote
                    and footnote.get("text")
                ],
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
    """
    由季調 CPI 指數計算月增率。
    """
    if previous_value == 0:
        return None

    result = (
        (current_value / previous_value)
        - 1
    ) * 100

    # JSON 儲存4位小數，網頁顯示2位小數。
    return round(result, 4)


def calculate_monthly_changes(observations):
    """
    計算每個月相對上月的季調月增率。
    """
    changes = []

    for index in range(1, len(observations)):
        current = observations[index]
        previous = observations[index - 1]

        monthly_change = calculate_percent_change(
            current["index_value"],
            previous["index_value"],
        )

        changes.append(
            {
                "year": current["year"],
                "month": current["month"],
                "period": current["period"],
                "period_name": current["period_name"],
                "value": monthly_change,
                "index_value": current["index_value"],
                "latest": current["latest"],
            }
        )

    # 只保存最近12個月的月增率
    return changes[-12:]


def build_cpi_rows(api_series):
    """
    依使用者指定順序建立33個 CPI 顯示項目。
    """
    api_lookup = {
        series.get("seriesID", ""): series
        for series in api_series
    }

    rows = []
    missing_series = []

    for order, config in enumerate(CPI_SERIES):
        series_id = config["bls_series_id"]
        series = api_lookup.get(series_id)

        if not series:
            missing_series.append(
                {
                    "name": config["name"],
                    "series_id": series_id,
                    "reason": (
                        "Series was not returned by BLS API"
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
                    "available": False,
                    "series_title": "",
                    "months": [],
                }
            )

            continue

        observations = parse_monthly_observations(
            series
        )

        monthly_changes = calculate_monthly_changes(
            observations
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

        catalog = series.get("catalog", {}) or {}

        rows.append(
            {
                "order": order,
                "name": config["name"],
                "display_code": (
                    config["display_code"]
                ),
                "bls_series_id": series_id,
                "level": config["level"],
                "available": bool(monthly_changes),
                "series_title": catalog.get(
                    "series_title",
                    "",
                ),
                "survey_name": catalog.get(
                    "survey_name",
                    "",
                ),
                "seasonality": (
                    "Seasonally Adjusted"
                ),
                "unit": (
                    "Percent change from previous month"
                ),
                "months": monthly_changes,
            }
        )

    return rows, missing_series


def collect_available_periods(rows):
    """
    建立整張 CPI 表格共用的月份清單。
    """
    periods = {}

    for row in rows:
        for month in row.get("months", []):
            period = month["period"]

            periods[period] = {
                "year": month["year"],
                "month": month["month"],
                "period": period,
                "period_name": month["period_name"],
                "label": (
                    f"{str(month['year'])[2:]} "
                    f"{month['period_name'][:3]}"
                ),
            }

    result = list(periods.values())

    result.sort(
        key=lambda item: (
            item["year"],
            item["month"],
        )
    )

    return result[-12:]


def align_rows_to_periods(rows, periods):
    """
    讓所有列都遵循相同的12個月份順序。

    若個別 Series 某月沒有數值，就填入 None。
    """
    period_keys = [
        period["period"]
        for period in periods
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
    """
    讀取目前的 data/cpi.json。
    """
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
    """
    儲存 CPI JSON。

    若 CPI 資料與既有資料完全相同，
    保留原更新時間，避免無意義 Commit。
    """
    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    aligned_rows = align_rows_to_periods(
        rows,
        periods,
    )

    existing = load_existing_payload()

    data_changed = True
    updated_at_utc = (
        datetime.now(timezone.utc).isoformat()
    )

    if existing:
        old_periods = existing.get(
            "periods",
            [],
        )
        old_rows = existing.get(
            "rows",
            [],
        )
        old_missing = existing.get(
            "missing_series",
            [],
        )

        if (
            old_periods == periods
            and old_rows == aligned_rows
            and old_missing == missing_series
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
            "Seasonally Adjusted Monthly Change"
        ),
        "description": (
            "Seasonally adjusted month-over-month "
            "percent changes calculated from BLS "
            "CPI index levels."
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

    rows, missing_series = build_cpi_rows(
        api_series
    )

    periods = collect_available_periods(rows)

    if len(periods) < 6:
        raise RuntimeError(
            "Fewer than 6 CPI periods were generated. "
            "The output is not sufficient for the dashboard."
        )

    save_json(
        periods=periods,
        rows=rows,
        missing_series=missing_series,
    )


if __name__ == "__main__":
    main()