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
        "bls_series_id": "CUSR0000SA0",
        "level": 0,
    },
    {
        "name": "Food",
        "bls_series_id": "CUSR0000SAF1",
        "level": 0,
    },
    {
        "name": "Energy",
        "bls_series_id": "CUSR0000SA0E",
        "level": 0,
    },
    {
        "name": "All Items Less Food and Energy",
        "bls_series_id": "CUSR0000SA0L1E",
        "level": 0,
    },
    {
        "name": (
            "Commodities Excluding Food "
            "and Energy Commodities"
        ),
        "bls_series_id": "CUSR0000SACL1E",
        "level": 1,
    },
    {
        "name": "Household Furnishings and Supplies",
        "bls_series_id": "CUSR0000SAH31",
        "level": 2,
    },
    {
        "name": "Apparel",
        "bls_series_id": "CUSR0000SAA",
        "level": 2,
    },
    {
        "name": (
            "Transportation Commodities "
            "Less Motor Fuel"
        ),
        "bls_series_id": "CUSR0000SATCLTB",
        "level": 2,
    },
    {
        "name": "New Vehicles",
        "bls_series_id": "CUSR0000SETA01",
        "level": 3,
    },
    {
        "name": "Used Cars and Trucks",
        "bls_series_id": "CUSR0000SETA02",
        "level": 3,
    },
    {
        "name": "Medical Care Commodities",
        "bls_series_id": "CUSR0000SAM1",
        "level": 2,
    },
    {
        "name": "Recreation Commodities",
        "bls_series_id": "CUSR0000SARC",
        "level": 2,
    },
    {
        "name": (
            "Education and Communication Commodities"
        ),
        "bls_series_id": "CUSR0000SAEC",
        "level": 2,
    },
    {
        "name": "Alcoholic Beverages",
        "bls_series_id": "CUSR0000SAF116",
        "level": 2,
    },
    {
        "name": "Other Goods",
        "bls_series_id": "CUSR0000SAGC",
        "level": 2,
    },
    {
        "name": "Services Excluding Energy Services",
        "bls_series_id": "CUSR0000SASLE",
        "level": 1,
    },
    {
        "name": "Shelter",
        "bls_series_id": "CUSR0000SAH1",
        "level": 2,
    },
    {
        "name": "Rent of Primary Residence",
        "bls_series_id": "CUSR0000SEHA",
        "level": 4,
    },
    {
        "name": "Lodging Away from Home",
        "bls_series_id": "CUSR0000SEHB",
        "level": 4,
    },
    {
        "name": (
            "Owners' Equivalent Rent of Residences"
        ),
        "bls_series_id": "CUSR0000SEHC",
        "level": 4,
    },
    {
        "name": (
            "Water, Sewer and Trash Collection Services"
        ),
        "bls_series_id": "CUSR0000SEHG",
        "level": 2,
    },
    {
        "name": "Medical Care Services",
        "bls_series_id": "CUSR0000SAM2",
        "level": 2,
    },
    {
        "name": "Professional Services",
        "bls_series_id": "CUSR0000SEMC",
        "level": 3,
    },
    {
        "name": "Hospital and Related Services",
        "bls_series_id": "CUSR0000SEMD",
        "level": 3,
    },
    {
        "name": "Transportation Services",
        "bls_series_id": "CUSR0000SAS4",
        "level": 2,
    },
    {
        "name": "Car and Truck Rental",
        "bls_series_id": "CUSR0000SETA04",
        "level": 3,
    },
    {
        "name": (
            "Motor Vehicle Maintenance and Repair"
        ),
        "bls_series_id": "CUSR0000SETD",
        "level": 3,
    },
    {
        "name": "Motor Vehicle Insurance",
        "bls_series_id": "CUSR0000SETE",
        "level": 3,
    },
    {
        "name": "Public Transportation",
        "bls_series_id": "CUSR0000SETG",
        "level": 3,
    },
    {
        "name": "Airline Fare",
        "bls_series_id": "CUSR0000SETG01",
        "level": 4,
    },
    {
        "name": "Recreation Services",
        "bls_series_id": "CUSR0000SARS",
        "level": 2,
    },
    {
        "name": (
            "Education and Communication Services"
        ),
        "bls_series_id": "CUSR0000SAES",
        "level": 2,
    },
]


DERIVED_SERIES = [
    {
        "name": "Core Services Less Shelter",
        "base": "Services Excluding Energy Services",
        "exclude": [
            "Shelter",
        ],
    },
    {
        "name": "Core Services Less Rent & OER",
        "base": "Services Excluding Energy Services",
        "exclude": [
            "Rent of Primary Residence",
            "Owners' Equivalent Rent of Residences",
        ],
    },
    {
        "name": (
            "Core Services Less Shelter & "
            "Public Transportation"
        ),
        "base": "Services Excluding Energy Services",
        "exclude": [
            "Shelter",
            "Public Transportation",
        ],
    },
    {
        "name": "Core Less Shelter & Used Cars",
        "base": "All Items Less Food and Energy",
        "exclude": [
            "Shelter",
            "Used Cars and Trucks",
        ],
    },
    {
        "name": "Core Goods Less Used Cars",
        "base": (
            "Commodities Excluding Food "
            "and Energy Commodities"
        ),
        "exclude": [
            "Used Cars and Trucks",
        ],
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


def get_current_year():
    return datetime.now(timezone.utc).year


def fetch_cpi_series():
    registration_key = get_registration_key()

    series_ids = [
        item["bls_series_id"]
        for item in CPI_SERIES
    ]

    payload = {
        "seriesid": series_ids,
        "startyear": str(get_current_year() - 2),
        "endyear": str(get_current_year()),
        "calculations": False,
        "annualaverage": False,
        "catalog": True,

        # 要求 BLS 回傳 CPI Aspect metadata。
        # Relative Importance 的 aspect code 是 I。
        "aspects": True,

        "registrationkey": registration_key,
    }

    print("=" * 72)
    print("Calling registered BLS Public Data API.")
    print(f"API URL: {BLS_API_URL}")
    print(f"Requested CPI series: {len(series_ids)}")
    print("Aspects requested: True")
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


def to_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def normalize_aspect_code(value):
    if value is None:
        return ""

    return (
        str(value)
        .strip()
        .upper()
        .replace(" ", "")
        .replace("_", "")
        .replace("-", "")
    )


def extract_relative_importance_from_node(node):
    """
    BLS API 的 aspect 結構可能隨 API 回傳形式略有不同。

    此函數會遞迴搜尋：
    - aspectType
    - aspect_type
    - aspectCode
    - aspect_code
    - code
    - name / aspectName

    若識別到 code I 或文字 Relative Importance，
    就嘗試讀取該物件中的 value。
    """
    if isinstance(node, list):
        for item in node:
            result = extract_relative_importance_from_node(
                item
            )

            if result is not None:
                return result

        return None

    if not isinstance(node, dict):
        return None

    possible_code_keys = [
        "aspectType",
        "aspect_type",
        "aspectCode",
        "aspect_code",
        "code",
        "type",
    ]

    possible_name_keys = [
        "aspectName",
        "aspect_name",
        "name",
        "description",
        "variableName",
        "variable_name",
    ]

    code_values = [
        normalize_aspect_code(node.get(key))
        for key in possible_code_keys
        if key in node
    ]

    name_values = [
        str(node.get(key, "")).strip().lower()
        for key in possible_name_keys
        if key in node
    ]

    is_relative_importance = (
        "I" in code_values
        or any(
            "relative importance" in value
            for value in name_values
        )
    )

    if is_relative_importance:
        possible_value_keys = [
            "value",
            "aspectValue",
            "aspect_value",
            "dataValue",
            "data_value",
        ]

        for key in possible_value_keys:
            if key not in node:
                continue

            number = to_float(node.get(key))

            if number is not None:
                return number

    for value in node.values():
        if isinstance(value, (dict, list)):
            result = extract_relative_importance_from_node(
                value
            )

            if result is not None:
                return result

    return None


def extract_relative_importance(observation):
    """
    從單月 observation 的 aspect metadata 中讀取：
    I = Relative Importance。
    """
    possible_containers = [
        observation.get("aspects"),
        observation.get("aspect"),
        observation.get("metadata"),
    ]

    for container in possible_containers:
        result = extract_relative_importance_from_node(
            container
        )

        if result is not None:
            return result

    return None


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
            index_value = float(
                observation["value"]
            )
        except (KeyError, TypeError, ValueError):
            continue

        if not 1 <= month <= 12:
            continue

        relative_importance = (
            extract_relative_importance(
                observation
            )
        )

        observations.append(
            {
                "year": year,
                "month": month,
                "period": f"{year}-{month:02d}",
                "period_name": observation.get(
                    "periodName",
                    "",
                ),
                "index_value": index_value,
                "relative_importance": (
                    relative_importance
                ),
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

    return round(result, 6)


def build_monthly_changes(observations):
    """
    計算月增率。

    對於 t 月月增率，會優先使用 t 月 observation
    隨附的 Relative Importance。

    BLS 每月新聞稿的 Relative Importance 通常代表
    計算當月價格相對變化所搭配的前一期權重。
    """
    changes = []

    for index in range(1, len(observations)):
        current = observations[index]
        previous = observations[index - 1]

        value = calculate_percent_change(
            current["index_value"],
            previous["index_value"],
        )

        relative_importance = (
            current.get("relative_importance")
        )

        if relative_importance is None:
            relative_importance = (
                previous.get("relative_importance")
            )

        changes.append(
            {
                "year": current["year"],
                "month": current["month"],
                "period": current["period"],
                "period_name": current["period_name"],
                "value": value,
                "index_value": current["index_value"],
                "relative_importance": (
                    relative_importance
                ),
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
                "bls_series_id": series_id,
                "level": config["level"],
                "seasonality": "SA",
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
        relative_importance = []

        for period in period_keys:
            month = month_lookup.get(period)

            values.append(
                month.get("value")
                if month
                else None
            )

            relative_importance.append(
                month.get("relative_importance")
                if month
                else None
            )

        aligned_row = dict(row)
        aligned_row["values"] = values
        aligned_row["relative_importance"] = (
            relative_importance
        )
        aligned_row.pop("months", None)

        aligned_rows.append(aligned_row)

    return aligned_rows


def calculate_exclusion_aggregate(
    base_change,
    base_weight,
    excluded_components,
):
    """
    近似排除式加權月增率：

    (
        母項目權重 × 母項目月增率
        -
        Σ 排除項目權重 × 排除項目月增率
    )
    ÷
    (
        母項目權重
        -
        Σ 排除項目權重
    )
    """
    if (
        base_change is None
        or base_weight is None
    ):
        return None

    excluded_weight = 0.0
    excluded_contribution = 0.0

    for component in excluded_components:
        component_change = component.get("change")
        component_weight = component.get("weight")

        if (
            component_change is None
            or component_weight is None
        ):
            return None

        excluded_weight += component_weight

        excluded_contribution += (
            component_weight
            * component_change
        )

    effective_weight = (
        base_weight - excluded_weight
    )

    if effective_weight <= 0:
        return None

    base_contribution = (
        base_weight * base_change
    )

    result = (
        base_contribution
        - excluded_contribution
    ) / effective_weight

    return round(result, 6)


def build_derived_rows(aligned_rows, periods):
    rows_by_name = {
        row["name"]: row
        for row in aligned_rows
    }

    derived_rows = []

    for order, definition in enumerate(
        DERIVED_SERIES
    ):
        base_row = rows_by_name.get(
            definition["base"]
        )

        excluded_rows = [
            rows_by_name.get(name)
            for name in definition["exclude"]
        ]

        values = []
        calculation_details = []

        for index, period in enumerate(periods):
            base_change = None
            base_weight = None

            if base_row:
                base_change = base_row["values"][index]
                base_weight = (
                    base_row["relative_importance"][index]
                )

            excluded_components = []

            for excluded_name, excluded_row in zip(
                definition["exclude"],
                excluded_rows,
            ):
                excluded_change = None
                excluded_weight = None

                if excluded_row:
                    excluded_change = (
                        excluded_row["values"][index]
                    )

                    excluded_weight = (
                        excluded_row[
                            "relative_importance"
                        ][index]
                    )

                excluded_components.append(
                    {
                        "name": excluded_name,
                        "change": excluded_change,
                        "weight": excluded_weight,
                    }
                )

            value = calculate_exclusion_aggregate(
                base_change=base_change,
                base_weight=base_weight,
                excluded_components=(
                    excluded_components
                ),
            )

            excluded_weight_total = None
            effective_weight = None

            valid_excluded_weights = [
                item["weight"]
                for item in excluded_components
                if item["weight"] is not None
            ]

            if (
                base_weight is not None
                and len(valid_excluded_weights)
                == len(excluded_components)
            ):
                excluded_weight_total = sum(
                    valid_excluded_weights
                )

                effective_weight = (
                    base_weight
                    - excluded_weight_total
                )

            values.append(value)

            calculation_details.append(
                {
                    "period": period["period"],
                    "base_name": definition["base"],
                    "base_change": base_change,
                    "base_relative_importance": (
                        base_weight
                    ),
                    "excluded_components": (
                        excluded_components
                    ),
                    "excluded_relative_importance": (
                        excluded_weight_total
                    ),
                    "effective_relative_importance": (
                        effective_weight
                    ),
                    "result": value,
                    "status": (
                        "calculated"
                        if value is not None
                        else "missing_relative_importance"
                    ),
                }
            )

        derived_rows.append(
            {
                "order": order,
                "name": definition["name"],
                "type": "derived",
                "badge": "Derived",
                "level": 0,
                "base_series": definition["base"],
                "excluded_series": (
                    definition["exclude"]
                ),
                "values": values,
                "calculation_details": (
                    calculation_details
                ),
                "method": (
                    "Relative-importance-weighted "
                    "exclusion formula"
                ),
            }
        )

    return derived_rows


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

    derived_rows = build_derived_rows(
        aligned_rows,
        periods,
    )

    existing = load_existing_payload()

    data_changed = True
    updated_at_utc = (
        datetime.now(timezone.utc).isoformat()
    )

    if existing:
        same_data = (
            existing.get("periods", []) == periods
            and existing.get("rows", [])
            == aligned_rows
            and existing.get("derived_rows", [])
            == derived_rows
            and existing.get("missing_series", [])
            == missing_series
        )

        if same_data:
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
        "derived_row_count": len(derived_rows),
        "missing_series_count": len(
            missing_series
        ),
        "periods": periods,
        "rows": aligned_rows,
        "derived_rows": derived_rows,
        "missing_series": missing_series,
        "derived_methodology": {
            "method": (
                "Relative-importance-weighted "
                "exclusion formula"
            ),
            "formula": (
                "(base weight × base change "
                "- excluded weighted changes) "
                "÷ effective remaining weight"
            ),
            "official_bls_series": False,
            "caveat": (
                "Derived dashboard measures are "
                "approximations and may differ from "
                "official BLS special aggregate indexes."
            ),
        },
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
    print(f"Saved derived rows: {len(derived_rows)}")
    print(f"Saved periods: {len(periods)}")
    print(
        f"Missing source series: "
        f"{len(missing_series)}"
    )
    print(f"Data changed: {data_changed}")
    print(f"Output path: {OUTPUT_PATH}")

    missing_weight_count = 0

    for row in aligned_rows:
        available_weights = sum(
            value is not None
            for value in row[
                "relative_importance"
            ]
        )

        if available_weights < len(periods):
            missing_weight_count += 1

            print(
                "Relative Importance coverage:",
                row["name"],
                f"{available_weights}/{len(periods)}",
            )

    print(
        "Rows with incomplete Relative Importance:",
        missing_weight_count,
    )

    for row in derived_rows:
        calculated_count = sum(
            value is not None
            for value in row["values"]
        )

        print(
            "Derived coverage:",
            row["name"],
            f"{calculated_count}/{len(periods)}",
        )

    print("=" * 72)


def main():
    print(
        "Starting registered BLS CPI data update "
        "with Relative Importance."
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

    if len(rows) != 32:
        raise RuntimeError(
            "Expected 32 CPI rows, but generated "
            f"{len(rows)} rows."
        )

    save_json(
        periods=periods,
        rows=rows,
        missing_series=missing_series,
    )


if __name__ == "__main__":
    main()