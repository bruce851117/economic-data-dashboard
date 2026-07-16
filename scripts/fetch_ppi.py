import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests


BLS_API_URL = (
    "https://api.bls.gov/publicAPI/v2/timeseries/data/"
)

BLS_PPI_SOURCE_URL = (
    "https://www.bls.gov/ppi/"
)

OUTPUT_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "ppi.json"
)


PPI_SERIES = [
    {
        "name": "PPI for Hospitals",
        "short_name": "Hospitals",
        "bls_series_id": "PCU622---622---",
        "seasonality": "NSA",
        "pce_weight": 8.569,
    },
    {
        "name": "PPI for Offices of Physicians",
        "short_name": "Offices of Physicians",
        "bls_series_id": "PCU6211--6211--",
        "seasonality": "NSA",
        "pce_weight": 4.473,
    },
    {
        "name": "PPI for Portfolio Management",
        "short_name": "Portfolio Management",
        "bls_series_id": "WPU402",
        "seasonality": "NSA",
        "pce_weight": 0.890,
    },
    {
        "name": "PPI for Investment Advice",
        "short_name": "Investment Advice",
        "bls_series_id": "PCU523940523940P",
        "seasonality": "NSA",
        "pce_weight": 0.890,
    },
    {
        "name": "PPI for Nursing Care Facilities",
        "short_name": "Nursing Care Facilities",
        "bls_series_id": "PCU623110623110",
        "seasonality": "NSA",
        "pce_weight": 1.445,
    },
    {
        "name": (
            "PPI for Direct Health and Medical "
            "Insurance Carriers"
        ),
        "short_name": (
            "Direct Health and Medical "
            "Insurance Carriers"
        ),
        "bls_series_id": "PCU524114524114",
        "seasonality": "NSA",
        "pce_weight": 1.299,
    },
    {
        "name": "PPI for Home Health Care Services",
        "short_name": "Home Health Care Services",
        "bls_series_id": "PCU6216--6216--",
        "seasonality": "NSA",
        "pce_weight": 1.109,
    },
    {
        "name": (
            "PPI for Domestic Scheduled Passenger "
            "Air Transportation"
        ),
        "short_name": (
            "Domestic Scheduled Passenger "
            "Air Transportation"
        ),
        "bls_series_id": "PCU4811114811111",
        "seasonality": "NSA",
        "pce_weight": 1.023,
    },
    {
        "name": (
            "PPI for Private Passenger "
            "Auto Insurance"
        ),
        "short_name": (
            "Private Passenger Auto Insurance"
        ),
        "bls_series_id": "PCU5241265241261",
        "seasonality": "NSA",
        "pce_weight": 0.587,
    },
    {
        "name": "PPI for Medical Laboratories",
        "short_name": "Medical Laboratories",
        "bls_series_id": "PCU621511621511P",
        "seasonality": "NSA",
        "pce_weight": 0.145,
    },
    {
        "name": (
            "PPI for Diagnostic Imaging Centers"
        ),
        "short_name": (
            "Diagnostic Imaging Centers"
        ),
        "bls_series_id": "PCU6215126215124",
        "seasonality": "NSA",
        "pce_weight": 0.145,
    },
    {
        "name": "PPI for Brokerage Services",
        "short_name": "Brokerage Services",
        "bls_series_id": "WPU40110201",
        "seasonality": "NSA",
        "pce_weight": 0.098,
    },
    {
        "name": "PPI for Dealer Transactions",
        "short_name": "Dealer Transactions",
        "bls_series_id": "WPU40110101",
        "seasonality": "NSA",
        "pce_weight": 0.098,
    },
    {
        "name": (
            "PPI for Workers' Compensation "
            "Insurance"
        ),
        "short_name": (
            "Workers' Compensation Insurance"
        ),
        "bls_series_id": "PCU5241265241266",
        "seasonality": "NSA",
        "pce_weight": 0.192,
    },
    {
        "name": (
            "PPI for Commercial Bank "
            "Trust Services"
        ),
        "short_name": (
            "Commercial Bank Trust Services"
        ),
        "bls_series_id": "PCU5221105221103",
        "seasonality": "NSA",
        "pce_weight": 0.117,
    },
    {
        "name": "PPI for Homeowners' Insurance",
        "short_name": "Homeowners' Insurance",
        "bls_series_id": "PCU9241269241262",
        "seasonality": "NSA",
        "pce_weight": 0.104,
    },
    {
        "name": (
            "PPI for Employment "
            "Placement Agencies"
        ),
        "short_name": (
            "Employment Placement Agencies"
        ),
        "bls_series_id": "PCU5613--5613--",
        "seasonality": "NSA",
        "pce_weight": 0.009,
    },
    {
        "name": "PPI for Apparel",
        "short_name": (
            "Apparel, Jewelry, Footwear, "
            "and Accessories Retailing"
        ),
        "bls_series_id": "WPS5831",
        "seasonality": "SA",
        "pce_weight": 0.002,
    },
]


EXPECTED_WEIGHT_TOTAL = 21.195


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


def fetch_ppi_series():
    series_ids = [
        item["bls_series_id"]
        for item in PPI_SERIES
    ]

    payload = {
        "seriesid": series_ids,
        "startyear": str(
            get_current_year() - 2
        ),
        "endyear": str(
            get_current_year()
        ),
        "calculations": False,
        "annualaverage": False,
        "catalog": True,
        "aspects": False,
        "registrationkey": (
            get_registration_key()
        ),
    }

    print("=" * 72)
    print(
        "Calling registered BLS Public Data API."
    )
    print(f"API URL: {BLS_API_URL}")
    print(
        f"Requested PPI series: "
        f"{len(series_ids)}"
    )
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

    print(
        f"HTTP status: {response.status_code}"
    )
    print(
        f"Response length: "
        f"{len(response.content)} bytes"
    )

    if response.status_code != 200:
        raise RuntimeError(
            "BLS PPI API returned an HTTP error.\n"
            f"HTTP status: {response.status_code}\n"
            f"Response: {response.text[:3000]}"
        )

    try:
        result = response.json()
    except requests.JSONDecodeError as error:
        raise RuntimeError(
            "BLS PPI API did not return valid JSON."
        ) from error

    status = result.get(
        "status",
        "",
    )

    messages = result.get(
        "message",
        [],
    )

    print(
        f"BLS response status: {status}"
    )

    if messages:
        print("BLS response messages:")

        for message in messages:
            print(f"- {message}")

    if status != "REQUEST_SUCCEEDED":
        raise RuntimeError(
            "BLS PPI API request did not succeed.\n"
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
            "BLS API returned no PPI series."
        )

    print(
        f"Returned PPI series: "
        f"{len(returned_series)}"
    )
    print("=" * 72)

    return returned_series


def parse_observations(series):
    observations = []

    for observation in series.get(
        "data",
        [],
    ):
        period = str(
            observation.get(
                "period",
                "",
            )
        )

        if (
            not period.startswith("M")
            or period == "M13"
        ):
            continue

        try:
            year = int(
                observation["year"]
            )

            month = int(
                period[1:]
            )

            index_value = float(
                observation["value"]
            )

        except (
            KeyError,
            TypeError,
            ValueError,
        ):
            continue

        if not 1 <= month <= 12:
            continue

        observations.append(
            {
                "year": year,
                "month": month,
                "period": (
                    f"{year}-{month:02d}"
                ),
                "period_name": (
                    observation.get(
                        "periodName",
                        "",
                    )
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
            (
                current_value
                / previous_value
            )
            - 1
        )
        * 100,
        6,
    )


def build_monthly_changes(
    observations,
):
    changes = []

    for index in range(
        1,
        len(observations),
    ):
        current = observations[index]

        previous = observations[
            index - 1
        ]

        current_number = (
            current["year"] * 12
            + current["month"]
        )

        previous_number = (
            previous["year"] * 12
            + previous["month"]
        )

        # 只使用真正相鄰的兩個月份計算月增率。
        # 若中間缺少月份，不跨月計算。
        if (
            current_number
            - previous_number
            != 1
        ):
            continue

        changes.append(
            {
                "year": current["year"],
                "month": current["month"],
                "period": current["period"],
                "period_name": (
                    current["period_name"]
                ),
                "value": (
                    calculate_percent_change(
                        current[
                            "index_value"
                        ],
                        previous[
                            "index_value"
                        ],
                    )
                ),
                "index_value": (
                    current[
                        "index_value"
                    ]
                ),
                "previous_index_value": (
                    previous[
                        "index_value"
                    ]
                ),
                "latest": (
                    current["latest"]
                ),
            }
        )

    return changes


def build_source_rows(
    api_series,
):
    api_lookup = {
        series.get(
            "seriesID",
            "",
        ): series
        for series in api_series
    }

    rows = []
    missing_series = []

    for order, config in enumerate(
        PPI_SERIES
    ):
        series_id = config[
            "bls_series_id"
        ]

        series = api_lookup.get(
            series_id
        )

        monthly_changes = []
        series_title = ""

        if series:
            observations = (
                parse_observations(
                    series
                )
            )

            monthly_changes = (
                build_monthly_changes(
                    observations
                )
            )

            catalog = (
                series.get(
                    "catalog",
                    {},
                )
                or {}
            )

            series_title = catalog.get(
                "series_title",
                "",
            )

        if not monthly_changes:
            missing_series.append(
                {
                    "name": (
                        config["name"]
                    ),
                    "series_id": series_id,
                    "reason": (
                        "Series contained no usable "
                        "consecutive monthly "
                        "observations"
                    ),
                }
            )

        print(
            "PPI series:",
            series_id,
            "|",
            config["name"],
            "|",
            config["seasonality"],
            "|",
            series_title,
            "| observations:",
            len(monthly_changes),
        )

        rows.append(
            {
                "order": order,
                "name": config["name"],
                "short_name": (
                    config["short_name"]
                ),
                "bls_series_id": (
                    series_id
                ),
                "seasonality": (
                    config[
                        "seasonality"
                    ]
                ),
                "pce_weight": (
                    config["pce_weight"]
                ),
                "available": bool(
                    monthly_changes
                ),
                "series_title": (
                    series_title
                ),
                "months": monthly_changes,
            }
        )

    return rows, missing_series


def collect_common_periods(rows):
    """
    只選擇18個PPI項目都有月增率的月份。

    這能避免不同Series的最新月份不同，
    導致PCE影響列只包含部分項目。
    """

    period_sets = []

    for row in rows:
        available_periods = {
            month["period"]
            for month in row.get(
                "months",
                [],
            )
            if month.get("value")
            is not None
        }

        if not available_periods:
            raise RuntimeError(
                "No usable monthly PPI changes for "
                f"{row['name']} "
                f"({row['bls_series_id']})."
            )

        period_sets.append(
            available_periods
        )

    common_periods = set.intersection(
        *period_sets
    )

    if len(common_periods) < 12:
        raise RuntimeError(
            "Expected at least 12 common PPI "
            "months across all series, but found "
            f"{len(common_periods)}."
        )

    selected_periods = sorted(
        common_periods
    )[-12:]

    result = []

    for period_key in selected_periods:
        year_text, month_text = (
            period_key.split("-")
        )

        year = int(year_text)
        month = int(month_text)

        date_value = datetime(
            year,
            month,
            1,
        )

        result.append(
            {
                "year": year,
                "month": month,
                "period": period_key,
                "period_name": (
                    date_value.strftime(
                        "%B"
                    )
                ),
                "label": (
                    date_value.strftime(
                        "%y %b"
                    )
                ),
            }
        )

    return result


def align_rows(
    rows,
    periods,
):
    period_keys = [
        period["period"]
        for period in periods
    ]

    aligned_rows = []

    for row in rows:
        month_lookup = {
            month["period"]: month
            for month in row.get(
                "months",
                [],
            )
        }

        values = []
        index_values = []

        for period_key in period_keys:
            month = month_lookup.get(
                period_key
            )

            values.append(
                month.get("value")
                if month
                else None
            )

            index_values.append(
                month.get("index_value")
                if month
                else None
            )

        aligned_row = dict(row)

        aligned_row[
            "values"
        ] = values

        aligned_row[
            "index_values"
        ] = index_values

        aligned_row.pop(
            "months",
            None,
        )

        aligned_rows.append(
            aligned_row
        )

    return aligned_rows


def build_pce_impact_row(
    rows,
    periods,
):
    """
    對核心PCE的近似影響：

    Σ（PPI月增率 × PCE權重 ÷ 100）

    結果單位為百分點。
    """

    values = []
    calculation_details = []

    for index, period in enumerate(
        periods
    ):
        contribution = 0.0
        available_weight = 0.0
        complete = True
        components = []

        for row in rows:
            value = row[
                "values"
            ][index]

            weight = float(
                row["pce_weight"]
            )

            if value is None:
                complete = False

                component_contribution = (
                    None
                )

            else:
                component_contribution = (
                    float(value)
                    * weight
                    / 100
                )

                contribution += (
                    component_contribution
                )

                available_weight += weight

            components.append(
                {
                    "name": row["name"],
                    "series_id": (
                        row[
                            "bls_series_id"
                        ]
                    ),
                    "seasonality": (
                        row[
                            "seasonality"
                        ]
                    ),
                    "ppi_mom": value,
                    "pce_weight": weight,
                    "contribution": (
                        round(
                            component_contribution,
                            8,
                        )
                        if (
                            component_contribution
                            is not None
                        )
                        else None
                    ),
                }
            )

        result = (
            round(
                contribution,
                6,
            )
            if complete
            else None
        )

        values.append(result)

        calculation_details.append(
            {
                "period": (
                    period["period"]
                ),
                "result": result,
                "unit": (
                    "percentage_point"
                ),
                "complete": complete,
                "available_weight": round(
                    available_weight,
                    3,
                ),
                "total_weight": (
                    EXPECTED_WEIGHT_TOTAL
                ),
                "components": components,
            }
        )

    return {
        "order": len(rows),
        "name": (
            "Estimated Impact on Core PCE"
        ),
        "short_name": (
            "Estimated Impact on Core PCE"
        ),
        "type": "derived",
        "badge": "PCE Impact",
        "bls_series_id": None,
        "seasonality": "Mixed",
        "pce_weight": (
            EXPECTED_WEIGHT_TOTAL
        ),
        "available": any(
            value is not None
            for value in values
        ),
        "series_title": (
            "Weighted impact estimated from "
            "selected PPI components"
        ),
        "values": values,
        "unit": "percentage_point",
        "calculation_details": (
            calculation_details
        ),
    }


def load_existing_payload():
    if not OUTPUT_PATH.exists():
        return None

    try:
        with OUTPUT_PATH.open(
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)

    except (
        OSError,
        json.JSONDecodeError,
    ):
        return None


def save_json(
    periods,
    rows,
    pce_impact_row,
    missing_series,
):
    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    existing = load_existing_payload()

    data_changed = True

    updated_at_utc = (
        datetime.now(
            timezone.utc
        ).isoformat()
    )

    if existing:
        same_data = (
            existing.get(
                "periods",
                [],
            )
            == periods
            and existing.get(
                "rows",
                [],
            )
            == rows
            and existing.get(
                "pce_impact_row"
            )
            == pce_impact_row
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
        "source_url": (
            BLS_PPI_SOURCE_URL
        ),
        "title": (
            "Selected Producer Price Indexes"
        ),
        "description": (
            "Monthly percent changes calculated "
            "from selected BLS PPI index levels."
        ),
        "updated_at_utc": (
            updated_at_utc
        ),
        "data_changed": data_changed,
        "default_months": 6,
        "available_filter_options": [
            3,
            6,
            12,
        ],
        "period_count": len(periods),
        "row_count": len(rows),
        "pce_weight_total": round(
            sum(
                row["pce_weight"]
                for row in rows
            ),
            3,
        ),
        "pce_impact_method": {
            "formula": (
                "sum(PPI monthly percent change "
                "x PCE weight / 100)"
            ),
            "unit": "percentage_point",
            "coverage": (
                "Selected components represent "
                "21.195 percent of the supplied "
                "PCE weights."
            ),
            "official_bea_forecast": False,
            "caveat": (
                "This is a mechanical proxy based "
                "on selected PPI components, not "
                "an official BEA Core PCE estimate."
            ),
        },
        "periods": periods,
        "rows": rows,
        "pce_impact_row": (
            pce_impact_row
        ),
        "missing_series_count": len(
            missing_series
        ),
        "missing_series": missing_series,
    }

    temporary_path = (
        OUTPUT_PATH.with_suffix(
            ".json.tmp"
        )
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

    temporary_path.replace(
        OUTPUT_PATH
    )

    print("=" * 72)
    print(
        f"Saved PPI rows: {len(rows)}"
    )
    print(
        f"Saved periods: {len(periods)}"
    )
    print(
        "PCE weight total:",
        payload["pce_weight_total"],
    )
    print(
        "Missing PPI series:",
        len(missing_series),
    )
    print(
        f"Data changed: {data_changed}"
    )
    print(
        f"Output path: {OUTPUT_PATH}"
    )

    if periods:
        print(
            "PPI common period range:",
            periods[0]["period"],
            "to",
            periods[-1]["period"],
        )

    impact_coverage = sum(
        value is not None
        for value in pce_impact_row[
            "values"
        ]
    )

    print(
        "PCE impact coverage:",
        f"{impact_coverage}/"
        f"{len(periods)}",
    )

    for period, value in zip(
        periods,
        pce_impact_row["values"],
    ):
        print(
            "PCE impact:",
            period["period"],
            value,
        )

    print("=" * 72)


def main():
    print(
        "Starting registered BLS PPI "
        "data update."
    )

    weight_total = round(
        sum(
            row["pce_weight"]
            for row in PPI_SERIES
        ),
        3,
    )

    if (
        weight_total
        != EXPECTED_WEIGHT_TOTAL
    ):
        raise RuntimeError(
            "PCE weight total does not match "
            f"{EXPECTED_WEIGHT_TOTAL}. "
            f"Calculated total: {weight_total}"
        )

    api_series = fetch_ppi_series()

    rows, missing_series = (
        build_source_rows(
            api_series
        )
    )

    if len(rows) != 18:
        raise RuntimeError(
            "Expected 18 PPI rows, "
            f"but generated {len(rows)} rows."
        )

    if missing_series:
        missing_text = ", ".join(
            item["series_id"]
            for item in missing_series
        )

        raise RuntimeError(
            "One or more PPI series returned "
            "no usable data: "
            f"{missing_text}"
        )

    periods = collect_common_periods(
        rows
    )

    aligned_rows = align_rows(
        rows,
        periods,
    )

    pce_impact_row = (
        build_pce_impact_row(
            aligned_rows,
            periods,
        )
    )

    save_json(
        periods=periods,
        rows=aligned_rows,
        pce_impact_row=(
            pce_impact_row
        ),
        missing_series=(
            missing_series
        ),
    )


if __name__ == "__main__":
    main()