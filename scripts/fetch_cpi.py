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


REQUIRED_WEIGHT_NAMES = {
    definition["base"]
    for definition in DERIVED_SERIES
}

for definition in DERIVED_SERIES:
    REQUIRED_WEIGHT_NAMES.update(
        definition["exclude"]
    )


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


def to_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def normalize_text(value):
    return (
        str(value or "")
        .strip()
        .upper()
        .replace(" ", "")
        .replace("_", "")
        .replace("-", "")
    )


def to_unadjusted_series_id(
    adjusted_series_id,
):
    """
    將季調 CPI-U Series 轉成同項目的未季調 Series。

    例如：
    CUSR0000SAH1
    -> CUUR0000SAH1
    """

    if adjusted_series_id.startswith("CUSR"):
        return (
            "CUUR"
            + adjusted_series_id[4:]
        )

    return adjusted_series_id


def request_bls_series(
    series_ids,
    include_aspects,
    request_name,
):
    payload = {
        "seriesid": series_ids,
        "startyear": str(get_current_year() - 2),
        "endyear": str(get_current_year()),
        "calculations": False,
        "annualaverage": False,
        "catalog": True,
        "aspects": include_aspects,
        "registrationkey": get_registration_key(),
    }

    print("=" * 72)
    print(f"BLS request: {request_name}")
    print(f"Requested series: {len(series_ids)}")
    print(f"Aspects requested: {include_aspects}")
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
            f"{request_name} returned HTTP error.\n"
            f"HTTP status: {response.status_code}\n"
            f"Response: {response.text[:3000]}"
        )

    try:
        result = response.json()
    except requests.JSONDecodeError as error:
        raise RuntimeError(
            f"{request_name} did not return valid JSON."
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
            f"{request_name} failed.\n"
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
            f"{request_name} returned no series."
        )

    print(
        f"Returned series: {len(returned_series)}"
    )
    print("=" * 72)

    return returned_series


def fetch_adjusted_cpi_data():
    """
    第一批請求：
    抓取全部32個季調 CPI 指數。

    這次不需要 Aspects。
    """

    series_ids = [
        item["bls_series_id"]
        for item in CPI_SERIES
    ]

    return request_bls_series(
        series_ids=series_ids,
        include_aspects=False,
        request_name=(
            "Seasonally adjusted CPI indexes"
        ),
    )


def fetch_required_weights():
    """
    第二批請求：

    只抓計算5個衍生指標需要的8個
    Relative Importance Series。

    不會替全部32個項目抓權重。
    """

    config_by_name = {
        item["name"]: item
        for item in CPI_SERIES
    }

    requested_series = []

    for name in sorted(REQUIRED_WEIGHT_NAMES):
        config = config_by_name.get(name)

        if not config:
            raise RuntimeError(
                "Missing CPI configuration for "
                f"required weight: {name}"
            )

        unadjusted_id = (
            to_unadjusted_series_id(
                config["bls_series_id"]
            )
        )

        if unadjusted_id not in requested_series:
            requested_series.append(
                unadjusted_id
            )

    print(
        "Required weight count:",
        len(requested_series),
    )

    print(
        "Relative Importance source series:",
        ", ".join(requested_series),
    )

    if len(requested_series) != 8:
        raise RuntimeError(
            "Expected 8 Relative Importance Series, "
            f"but generated {len(requested_series)}."
        )

    return request_bls_series(
        series_ids=requested_series,
        include_aspects=True,
        request_name=(
            "Required CPI Relative Importance"
        ),
    )


def is_relative_importance_name(value):
    normalized = normalize_text(value)

    return normalized in {
        "I",
        "RELATIVEIMPORTANCE",
    }


def extract_relative_importance(node):
    """
    從 observation["aspects"] 讀取：

    {
        "name": "Relative Importance",
        "value": "78.762"
    }
    """

    if node is None:
        return None

    if isinstance(node, list):
        for item in node:
            result = extract_relative_importance(
                item
            )

            if result is not None:
                return result

        return None

    if not isinstance(node, dict):
        return None

    aspect_name = node.get(
        "name",
        node.get(
            "aspectName",
            node.get(
                "aspect_type",
                node.get("code"),
            ),
        ),
    )

    if is_relative_importance_name(
        aspect_name
    ):
        value = to_float(
            node.get(
                "value",
                node.get("aspectValue"),
            )
        )

        if value is not None:
            return value

    for key, value in node.items():
        if is_relative_importance_name(key):
            direct_value = to_float(value)

            if direct_value is not None:
                return direct_value

    for child in node.values():
        if isinstance(child, (dict, list)):
            result = extract_relative_importance(
                child
            )

            if result is not None:
                return result

    return None


def print_weight_sample(weight_api_series):
    for series in weight_api_series:
        for observation in series.get("data", []):
            aspects = observation.get("aspects")

            relative_importance = (
                extract_relative_importance(
                    aspects
                )
            )

            if relative_importance is None:
                continue

            print(
                "Weight sample series:",
                series.get("seriesID", ""),
            )

            print(
                "Weight sample period:",
                observation.get("year", ""),
                observation.get("period", ""),
            )

            print(
                "Weight sample value:",
                relative_importance,
            )

            return

    print(
        "WARNING: No Relative Importance sample "
        "could be parsed."
    )


def build_weight_lookup(
    weight_api_series,
):
    """
    建立：

    {
        "CUUR0000SAH1": {
            "2026-06": 35.149
        }
    }

    這裡的2026-06代表：
    2026年6月API observation所附的
    Relative Importance。

    不再額外往前錯移一個月份。
    """

    lookup = {}

    for series in weight_api_series:
        series_id = series.get(
            "seriesID",
            "",
        )

        monthly_weights = {}

        for observation in series.get("data", []):
            period = str(
                observation.get("period", "")
            )

            if (
                not period.startswith("M")
                or period == "M13"
            ):
                continue

            try:
                year = int(observation["year"])
                month = int(period[1:])
            except (KeyError, TypeError, ValueError):
                continue

            if not 1 <= month <= 12:
                continue

            relative_importance = (
                extract_relative_importance(
                    observation.get("aspects")
                )
            )

            if relative_importance is None:
                continue

            period_key = (
                f"{year}-{month:02d}"
            )

            monthly_weights[period_key] = (
                relative_importance
            )

        lookup[series_id] = monthly_weights

    return lookup


def parse_monthly_indexes(series):
    observations = []

    for observation in series.get("data", []):
        period = str(
            observation.get("period", "")
        )

        if (
            not period.startswith("M")
            or period == "M13"
        ):
            continue

        try:
            year = int(observation["year"])
            month = int(period[1:])
            index_value = float(
                observation["value"]
            )
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
                "index_value": index_value,
                "latest": observation.get(
                    "latest",
                    False,
                ),
            }
        )

    observations.sort(
        key=lambda item: (
            item["year"],
            item["month"],
        )
    )

    return observations


def calculate_percent_change(
    current_value,
    previous_value,
):
    if previous_value == 0:
        return None

    return round(
        (
            (current_value / previous_value)
            - 1
        ) * 100,
        6,
    )


def build_monthly_changes(observations):
    changes = []

    for index in range(1, len(observations)):
        current = observations[index]
        previous = observations[index - 1]

        changes.append(
            {
                "year": current["year"],
                "month": current["month"],
                "period": current["period"],
                "period_name": (
                    current["period_name"]
                ),
                "value": calculate_percent_change(
                    current["index_value"],
                    previous["index_value"],
                ),
                "index_value": (
                    current["index_value"]
                ),
                "latest": current["latest"],
            }
        )

    return changes[-12:]


def build_source_rows(
    adjusted_api_series,
):
    api_lookup = {
        series.get("seriesID", ""): series
        for series in adjusted_api_series
    }

    rows = []
    missing_series = []

    for order, config in enumerate(CPI_SERIES):
        series_id = config["bls_series_id"]
        series = api_lookup.get(series_id)

        monthly_changes = []
        series_title = ""

        if series:
            observations = parse_monthly_indexes(
                series
            )

            monthly_changes = build_monthly_changes(
                observations
            )

            catalog = (
                series.get("catalog", {})
                or {}
            )

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
                "weight_series_id": (
                    to_unadjusted_series_id(
                        series_id
                    )
                ),
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
                "period_name": (
                    month["period_name"]
                ),
                "label": (
                    f"{str(month['year'])[2:]} "
                    f"{month['period_name'][:3]}"
                ),
            }

    periods = list(
        period_lookup.values()
    )

    periods.sort(
        key=lambda item: (
            item["year"],
            item["month"],
        )
    )

    return periods[-12:]


def align_source_rows(
    rows,
    periods,
    weight_lookup,
):
    aligned_rows = []

    for row in rows:
        month_lookup = {
            month["period"]: month
            for month in row.get("months", [])
        }

        values = []
        relative_importance = []

        weight_series = weight_lookup.get(
            row["weight_series_id"],
            {},
        )

        available_weights = {
            period_key: weight
            for period_key, weight
            in weight_series.items()
            if weight is not None
        }

        latest_weight = None

        if available_weights:
            latest_period = max(
                available_weights.keys()
            )

            latest_weight = available_weights[
                latest_period
            ]

        for period in periods:
            period_key = period["period"]

            month_data = month_lookup.get(
                period_key
            )

            values.append(
                month_data.get("value")
                if month_data
                else None
            )

            if row["name"] in REQUIRED_WEIGHT_NAMES:
                weight = latest_weight
            else:
                weight = None

            relative_importance.append(weight)

        aligned_row = dict(row)

        aligned_row["values"] = values

        aligned_row["relative_importance"] = (
            relative_importance
        )

        aligned_row.pop(
            "months",
            None,
        )

        aligned_rows.append(aligned_row)

    return aligned_rows


def calculate_exclusion_aggregate(
    base_change,
    base_weight,
    excluded_components,
):
    if (
        base_change is None
        or base_weight is None
    ):
        return None

    excluded_weight = 0.0
    excluded_contribution = 0.0

    for component in excluded_components:
        component_change = component.get(
            "change"
        )

        component_weight = component.get(
            "weight"
        )

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

    result = (
        (
            base_weight * base_change
        )
        - excluded_contribution
    ) / effective_weight

    return round(result, 6)


def build_derived_rows(
    aligned_rows,
    periods,
):
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
            base_change = (
                base_row["values"][index]
                if base_row
                else None
            )

            base_weight = (
                base_row[
                    "relative_importance"
                ][index]
                if base_row
                else None
            )

            excluded_components = []

            for (
                excluded_name,
                excluded_row,
            ) in zip(
                definition["exclude"],
                excluded_rows,
            ):
                excluded_components.append(
                    {
                        "name": excluded_name,
                        "change": (
                            excluded_row[
                                "values"
                            ][index]
                            if excluded_row
                            else None
                        ),
                        "weight": (
                            excluded_row[
                                "relative_importance"
                            ][index]
                            if excluded_row
                            else None
                        ),
                    }
                )

            result = calculate_exclusion_aggregate(
                base_change=base_change,
                base_weight=base_weight,
                excluded_components=(
                    excluded_components
                ),
            )

            excluded_weight_values = [
                component["weight"]
                for component in excluded_components
                if component["weight"] is not None
            ]

            excluded_weight_total = None
            effective_weight = None

            if (
                base_weight is not None
                and len(excluded_weight_values)
                == len(excluded_components)
            ):
                excluded_weight_total = sum(
                    excluded_weight_values
                )

                effective_weight = (
                    base_weight
                    - excluded_weight_total
                )

            values.append(result)

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
                    "result": result,
                    "status": (
                        "calculated"
                        if result is not None
                        else (
                            "missing_relative_importance"
                        )
                    ),
                }
            )

        derived_rows.append(
            {
                "order": order,
                "name": definition["name"],
                "type": "derived",
                "badge": "Derived",
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
    derived_rows,
    missing_series,
):
    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    existing = load_existing_payload()

    data_changed = True

    updated_at_utc = (
        datetime.now(timezone.utc).isoformat()
    )

    if existing:
        same_data = (
            existing.get("periods", [])
            == periods
            and existing.get("rows", [])
            == rows
            and existing.get("derived_rows", [])
            == derived_rows
            and existing.get(
                "missing_series",
                [],
            )
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
        "row_count": len(rows),
        "derived_row_count": len(
            derived_rows
        ),
        "missing_series_count": len(
            missing_series
        ),
        "relative_importance_series_count": (
            len(REQUIRED_WEIGHT_NAMES)
        ),
        "periods": periods,
        "rows": rows,
        "derived_rows": derived_rows,
        "missing_series": missing_series,
        "derived_methodology": {
            "official_bls_series": False,
            "weight_source": (
                "Eight required CPI-U unadjusted "
                "Relative Importance series"
            ),
            "weight_month_alignment": (
                "Relative Importance attached to the "
                "same API observation as the target "
                "monthly change"
            ),
            "method": (
                "Relative-importance-weighted "
                "exclusion formula"
            ),
            "formula": (
                "(base weight x base change "
                "- excluded weighted changes) "
                "/ effective remaining weight"
            ),
            "caveat": (
                "Dashboard-derived approximation. "
                "Results may differ from official BLS "
                "special aggregate indexes."
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
    print(f"Saved CPI rows: {len(rows)}")
    print(
        f"Saved derived rows: {len(derived_rows)}"
    )
    print(f"Saved periods: {len(periods)}")
    print(
        "Relative Importance source series:",
        len(REQUIRED_WEIGHT_NAMES),
    )
    print(
        "Missing source series:",
        len(missing_series),
    )
    print(f"Data changed: {data_changed}")
    print(f"Output path: {OUTPUT_PATH}")

    rows_by_name = {
        row["name"]: row
        for row in rows
    }

    for name in sorted(REQUIRED_WEIGHT_NAMES):
        row = rows_by_name[name]

        coverage = sum(
            value is not None
            for value in row[
                "relative_importance"
            ]
        )

        print(
            "Relative Importance coverage:",
            name,
            f"{coverage}/{len(periods)}",
        )

    incomplete_derived_rows = 0

    for row in derived_rows:
        coverage = sum(
            value is not None
            for value in row["values"]
        )

        missing_periods = [
            periods[index]["period"]
            for index, value in enumerate(
                row["values"]
            )
            if value is None
        ]

        if coverage < len(periods):
            incomplete_derived_rows += 1

        print(
            "Derived coverage:",
            row["name"],
            f"{coverage}/{len(periods)}",
        )

        if missing_periods:
            print(
                "Derived missing periods:",
                row["name"],
                ", ".join(missing_periods),
            )

            for detail in row.get(
                "calculation_details",
                [],
            ):
                if (
                    detail.get("period")
                    not in missing_periods
                ):
                    continue

                print(
                    "Derived missing detail:",
                    row["name"],
                    json.dumps(
                        detail,
                        ensure_ascii=False,
                    ),
                )

    print(
        "Derived rows with incomplete coverage:",
        incomplete_derived_rows,
    )

    print("=" * 72)


def main():
    print(
        "Starting registered BLS CPI data update "
        "with required Relative Importance only."
    )

    adjusted_api_series = (
        fetch_adjusted_cpi_data()
    )

    weight_api_series = (
        fetch_required_weights()
    )

    print_weight_sample(
        weight_api_series
    )

    source_rows, missing_series = (
        build_source_rows(
            adjusted_api_series
        )
    )

    periods = collect_periods(
        source_rows
    )

    if len(periods) != 12:
        raise RuntimeError(
            "Expected 12 CPI periods, but generated "
            f"{len(periods)} periods."
        )

    if len(source_rows) != 32:
        raise RuntimeError(
            "Expected 32 CPI rows, but generated "
            f"{len(source_rows)} rows."
        )

    weight_lookup = build_weight_lookup(
        weight_api_series
    )

    aligned_rows = align_source_rows(
        rows=source_rows,
        periods=periods,
        weight_lookup=weight_lookup,
    )

    derived_rows = build_derived_rows(
        aligned_rows=aligned_rows,
        periods=periods,
    )

    save_json(
        periods=periods,
        rows=aligned_rows,
        derived_rows=derived_rows,
        missing_series=missing_series,
    )


if __name__ == "__main__":
    main()
