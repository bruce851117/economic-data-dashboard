import json
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
    / "cpi_table2.json"
)


CPI_SERIES = [
    {
        "name_en": "All items",
        "name_zh": "整體 CPI",
        "unadjusted": "CUUR0000SA0",
        "adjusted": "CUSR0000SA0",
    },
    {
        "name_en": "All items less food and energy",
        "name_zh": "核心 CPI",
        "unadjusted": "CUUR0000SA0L1E",
        "adjusted": "CUSR0000SA0L1E",
    },
    {
        "name_en": "Food",
        "name_zh": "食品",
        "unadjusted": "CUUR0000SAF1",
        "adjusted": "CUSR0000SAF1",
    },
    {
        "name_en": "Energy",
        "name_zh": "能源",
        "unadjusted": "CUUR0000SA0E",
        "adjusted": "CUSR0000SA0E",
    },
    {
        "name_en": "Shelter",
        "name_zh": "居住成本",
        "unadjusted": "CUUR0000SAH1",
        "adjusted": "CUSR0000SAH1",
    },
    {
        "name_en": "Commodities less food and energy",
        "name_zh": "核心商品",
        "unadjusted": "CUUR0000SA0L1",
        "adjusted": "CUSR0000SA0L1",
    },
    {
        "name_en": "New vehicles",
        "name_zh": "新車",
        "unadjusted": "CUUR0000SETA01",
        "adjusted": "CUSR0000SETA01",
    },
    {
        "name_en": "Used cars and trucks",
        "name_zh": "二手車與卡車",
        "unadjusted": "CUUR0000SETA02",
        "adjusted": "CUSR0000SETA02",
    },
    {
        "name_en": "Medical care services",
        "name_zh": "醫療照護服務",
        "unadjusted": "CUUR0000SAM2",
        "adjusted": "CUSR0000SAM2",
    },
    {
        "name_en": "Transportation services",
        "name_zh": "運輸服務",
        "unadjusted": "CUUR0000SAS4",
        "adjusted": "CUSR0000SAS4",
    },
]


def current_year():
    return datetime.now(timezone.utc).year


def build_series_lookup():
    lookup = {}

    for item in CPI_SERIES:
        lookup[item["unadjusted"]] = {
            "item": item,
            "adjustment": "unadjusted",
        }

        lookup[item["adjusted"]] = {
            "item": item,
            "adjustment": "adjusted",
        }

    return lookup


def fetch_bls_api():
    """
    呼叫 BLS 官方 Public Data API。

    不再抓取 BLS HTML，也不透過 Cloudflare Worker
    代理 BLS 資料。
    """
    series_ids = []

    for item in CPI_SERIES:
        series_ids.append(item["unadjusted"])
        series_ids.append(item["adjusted"])

    payload = {
        "seriesid": series_ids,
        "startyear": str(current_year() - 2),
        "endyear": str(current_year()),
        "calculations": True,
        "annualaverage": False,
        "aspects": True,
    }

    print("=" * 70)
    print("Calling BLS Public Data API.")
    print(f"API URL: {BLS_API_URL}")
    print(f"Series requested: {len(series_ids)}")

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
        timeout=60,
    )

    print(f"HTTP status: {response.status_code}")
    print(
        f"Response length: {len(response.content)} bytes"
    )

    if response.status_code != 200:
        raise RuntimeError(
            "BLS API request failed.\n"
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

    if status != "REQUEST_SUCCEEDED":
        raise RuntimeError(
            "BLS API request was not successful.\n"
            f"Status: {status}\n"
            f"Messages: {result.get('message', [])}"
        )

    series = (
        result
        .get("Results", {})
        .get("series", [])
    )

    if not series:
        raise RuntimeError(
            "BLS API returned no CPI series."
        )

    print(f"Series returned: {len(series)}")
    print("=" * 70)

    return series


def valid_monthly_observations(series):
    """
    保留正式月份 M01 至 M12，排除年度平均 M13。
    """
    observations = []

    for item in series.get("data", []):
        period = item.get("period", "")

        if not period.startswith("M"):
            continue

        if period == "M13":
            continue

        try:
            month = int(period[1:])
        except ValueError:
            continue

        if not 1 <= month <= 12:
            continue

        try:
            value = float(item["value"])
        except (KeyError, TypeError, ValueError):
            continue

        observations.append(
            {
                "year": int(item["year"]),
                "month": month,
                "period": period,
                "period_name": item.get(
                    "periodName",
                    "",
                ),
                "value": value,
                "latest": item.get(
                    "latest",
                    False,
                ),
                "footnotes": [
                    footnote.get("text", "")
                    for footnote in item.get(
                        "footnotes",
                        [],
                    )
                    if footnote
                    and footnote.get("text")
                ],
                "aspects": item.get(
                    "aspects",
                    [],
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


def percent_change(new_value, old_value):
    if old_value == 0:
        return None

    return round(
        (
            (new_value / old_value)
            - 1
        ) * 100,
        3,
    )


def find_observation(
    observations,
    year,
    month,
):
    for observation in observations:
        if (
            observation["year"] == year
            and observation["month"] == month
        ):
            return observation

    return None


def previous_month(year, month):
    if month == 1:
        return year - 1, 12

    return year, month - 1


def extract_relative_importance(observation):
    """
    嘗試從 API aspect metadata 擷取相對重要性。

    若該 series 或月份沒有提供，就回傳 None。
    """
    if not observation:
        return None

    aspects = observation.get("aspects", [])

    if isinstance(aspects, dict):
        aspects = [aspects]

    for aspect in aspects:
        if not isinstance(aspect, dict):
            continue

        aspect_type = str(
            aspect.get(
                "aspectType",
                aspect.get(
                    "aspect_type",
                    aspect.get("code", ""),
                ),
            )
        ).upper()

        aspect_name = str(
            aspect.get(
                "aspectName",
                aspect.get(
                    "name",
                    aspect.get("description", ""),
                ),
            )
        ).lower()

        if (
            aspect_type == "I"
            or "relative importance" in aspect_name
        ):
            raw_value = aspect.get(
                "value",
                aspect.get("aspectValue"),
            )

            try:
                return float(raw_value)
            except (TypeError, ValueError):
                return raw_value

    return None


def build_output_rows(api_series):
    lookup = build_series_lookup()
    observations_by_series = {}

    for series in api_series:
        series_id = series.get("seriesID", "")

        observations_by_series[series_id] = (
            valid_monthly_observations(series)
        )

    rows = []

    for item in CPI_SERIES:
        unadjusted_id = item["unadjusted"]
        adjusted_id = item["adjusted"]

        unadjusted = observations_by_series.get(
            unadjusted_id,
            [],
        )

        adjusted = observations_by_series.get(
            adjusted_id,
            [],
        )

        if not unadjusted:
            print(
                f"WARNING: No unadjusted data: "
                f"{unadjusted_id}"
            )
            continue

        if not adjusted:
            print(
                f"WARNING: No adjusted data: "
                f"{adjusted_id}"
            )
            continue

        latest_unadjusted = unadjusted[-1]
        latest_adjusted = adjusted[-1]

        reference_year = latest_unadjusted["year"]
        reference_month = latest_unadjusted["month"]

        year_ago = find_observation(
            unadjusted,
            reference_year - 1,
            reference_month,
        )

        previous_year, previous_month_number = (
            previous_month(
                reference_year,
                reference_month,
            )
        )

        previous_unadjusted = find_observation(
            unadjusted,
            previous_year,
            previous_month_number,
        )

        adjusted_changes = []

        for index in range(
            max(1, len(adjusted) - 3),
            len(adjusted),
        ):
            current = adjusted[index]
            previous = adjusted[index - 1]

            adjusted_changes.append(
                {
                    "year": current["year"],
                    "month": current["month"],
                    "period_name": current[
                        "period_name"
                    ],
                    "percent_change": (
                        percent_change(
                            current["value"],
                            previous["value"],
                        )
                    ),
                }
            )

        row = {
            "name_en": item["name_en"],
            "name_zh": item["name_zh"],
            "unadjusted_series_id": unadjusted_id,
            "adjusted_series_id": adjusted_id,
            "reference_year": reference_year,
            "reference_month": reference_month,
            "reference_period": (
                f"{latest_unadjusted['period_name']} "
                f"{reference_year}"
            ),
            "relative_importance": (
                extract_relative_importance(
                    latest_unadjusted
                )
            ),
            "unadjusted_index": (
                latest_unadjusted["value"]
            ),
            "year_over_year_percent_change": (
                percent_change(
                    latest_unadjusted["value"],
                    year_ago["value"],
                )
                if year_ago
                else None
            ),
            "unadjusted_month_over_month_change": (
                percent_change(
                    latest_unadjusted["value"],
                    previous_unadjusted["value"],
                )
                if previous_unadjusted
                else None
            ),
            "seasonally_adjusted_index": (
                latest_adjusted["value"]
            ),
            "seasonally_adjusted_changes": (
                adjusted_changes
            ),
        }

        rows.append(row)

    if not rows:
        raise RuntimeError(
            "No CPI output rows could be created."
        )

    names = {
        row["name_en"]
        for row in rows
    }

    required_names = {
        "All items",
        "All items less food and energy",
        "Food",
        "Energy",
    }

    missing_names = required_names - names

    if missing_names:
        raise RuntimeError(
            "Required CPI categories are missing: "
            + ", ".join(sorted(missing_names))
        )

    return rows


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


def save_json(rows):
    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    latest_row = max(
        rows,
        key=lambda row: (
            row["reference_year"],
            row["reference_month"],
        ),
    )

    reference_period = latest_row[
        "reference_period"
    ]

    existing = load_existing_payload()

    data_changed = True
    updated_at_utc = (
        datetime.now(timezone.utc).isoformat()
    )

    if existing:
        old_data = existing.get("data", [])

        if old_data == rows:
            data_changed = False

            updated_at_utc = existing.get(
                "updated_at_utc",
                updated_at_utc,
            )

    payload = {
        "source": (
            "U.S. Bureau of Labor Statistics"
        ),
        "source_type": "BLS Public Data API",
        "api_url": BLS_API_URL,
        "source_url": BLS_SOURCE_URL,
        "title": (
            "Consumer Price Index for "
            "All Urban Consumers"
        ),
        "reference_period": reference_period,
        "updated_at_utc": updated_at_utc,
        "data_changed": data_changed,
        "row_count": len(rows),
        "data": rows,
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

    print("=" * 70)
    print(f"Saved {len(rows)} CPI categories.")
    print(f"Reference period: {reference_period}")
    print(f"Data changed: {data_changed}")
    print(f"Output path: {OUTPUT_PATH}")
    print("=" * 70)


def main():
    print("Starting CPI update through BLS Public Data API.")

    api_series = fetch_bls_api()

    rows = build_output_rows(api_series)

    save_json(rows)


if __name__ == "__main__":
    main()
