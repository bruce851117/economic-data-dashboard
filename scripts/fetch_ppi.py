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

EXPECTED_WEIGHT_TOTAL = 22.946

PPI_SERIES = [
    {"category": '醫療', "name": 'PPI for hospitals.', "short_name": 'Hospitals', "bls_series_id": 'PCU622---622---', "seasonality": "NSA", "pce_weight": 8.602},
    {"category": '醫療', "name": 'PPI for nursing care facilities.', "short_name": 'Nursing Care Facilities', "bls_series_id": 'PCU623110623110', "seasonality": "NSA", "pce_weight": 1.445},
    {"category": '醫療', "name": 'PPI for offices of physicians.', "short_name": 'Offices of Physicians', "bls_series_id": 'PCU6211--6211--', "seasonality": "NSA", "pce_weight": 4.493},
    {"category": '醫療', "name": 'PPI for home health care services.', "short_name": 'Home Health Care Services', "bls_series_id": 'PCU62161-62161-', "seasonality": "NSA", "pce_weight": 1.132},
    {"category": '醫療', "name": 'PPI for medical laboratories', "short_name": 'Medical Laboratories', "bls_series_id": 'PCU6215116215112', "seasonality": "NSA", "pce_weight": 0.1425},
    {"category": '醫療', "name": 'PPI for diagnostic imaging centers.', "short_name": 'Diagnostic Imaging Centers', "bls_series_id": 'PCU6215126215124', "seasonality": "NSA", "pce_weight": 0.1425},
    {"category": '投管', "name": 'PPI for Portfolio management & investment advice.', "short_name": 'Portfolio Management & Investment Advice', "bls_series_id": 'PCU523940523940', "seasonality": "NSA", "pce_weight": 1.794},
    {"category": '金融', "name": 'PPI for brokerage services, equities, and ETFs.', "short_name": 'Brokerage Services, Equities & ETFs', "bls_series_id": 'PCU5231505231501011', "seasonality": "NSA", "pce_weight": 0.042},
    {"category": '金融', "name": 'PPI for brokerage services, all other securities.', "short_name": 'Brokerage Services, All Other Securities', "bls_series_id": 'PCU5231505231501012', "seasonality": "NSA", "pce_weight": 0.042},
    {"category": '金融', "name": 'PPI for dealer transactions, debt securities and all other trading.', "short_name": 'Dealer Transactions, Debt & Other Trading', "bls_series_id": 'PCU5231505231502012', "seasonality": "NSA", "pce_weight": 0.05},
    {"category": '金融', "name": 'PPI for dealer transactions, equity securities.', "short_name": 'Dealer Transactions, Equity Securities', "bls_series_id": 'PCU5231505231502011', "seasonality": "NSA", "pce_weight": 0.024},
    {"category": '金融', "name": 'PPI for other securities related services including margin lending and mutual fund sales.', "short_name": 'Other Securities Related Services', "bls_series_id": 'PCU523150523150102', "seasonality": "NSA", "pce_weight": 0.052},
    {"category": '金融', "name": 'PPI for commercial bank trust services.', "short_name": 'Commercial Bank Trust Services', "bls_series_id": 'PCU5221105221103', "seasonality": "NSA", "pce_weight": 0.116},
    {"category": '保險', "name": 'PPI for direct health and medical insurance carriers.', "short_name": 'Direct Health & Medical Insurance Carriers', "bls_series_id": 'PCU524114524114', "seasonality": "NSA", "pce_weight": 1.295},
    {"category": '保險', "name": 'PPI for workers’ compensation insurance.', "short_name": 'Workers Compensation Insurance', "bls_series_id": 'PCU5241265241266', "seasonality": "NSA", "pce_weight": 0.19},
    {"category": '保險', "name": 'PPI for private passenger auto insurance.', "short_name": 'Private Passenger Auto Insurance', "bls_series_id": 'PCU5241265241261', "seasonality": "NSA", "pce_weight": 0.581},
    {"category": '保險', "name": 'PPI for homeowners’ insurance.', "short_name": 'Premiums for Homeowners Insurance', "bls_series_id": 'PCU5241265241262', "seasonality": "NSA", "pce_weight": 0.104},
    {"category": '運輸', "name": 'PPI for domestic scheduled passenger air transportation.', "short_name": 'Domestic Scheduled Passenger Air Transportation', "bls_series_id": 'PCU4811114811111', "seasonality": "NSA", "pce_weight": 1.04},
    {"category": '法律', "name": 'PPI for legal services.', "short_name": 'Legal Services', "bls_series_id": 'WPU451101', "seasonality": "NSA", "pce_weight": 0.848},
    {"category": '其他', "name": 'PPI for employment placement agencies - primary services.', "short_name": 'Employment Placement Services', "bls_series_id": 'PCU5613805613802', "seasonality": "NSA", "pce_weight": 0.009},
    {"category": '其他', "name": 'PPI for apparel', "short_name": 'Apparel', "bls_series_id": 'WPU0381', "seasonality": "NSA", "pce_weight": 0.002},
    {"category": '軟體', "name": 'PPI for game software publishing', "short_name": 'Game Software Publishing', "bls_series_id": 'WPU342104', "seasonality": "NSA", "pce_weight": 0.4},
    {"category": '軟體', "name": 'PPI for hosting, ASP (active server pages); and other IT (information technology) infrastructure provisioning services', "short_name": 'Hosting, ASP & Other IT Infrastructure', "bls_series_id": 'WPU381101', "seasonality": "NSA", "pce_weight": 0.4},
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
    return datetime.now(
        timezone.utc
    ).year


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
        "Requested PPI series:",
        len(series_ids),
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
        "HTTP status:",
        response.status_code,
    )
    print(
        "Response length:",
        len(response.content),
        "bytes",
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
        "BLS response status:",
        status,
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
        "Returned PPI series:",
        len(returned_series),
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


def is_consecutive_month(
    current,
    previous,
):
    current_number = (
        current["year"] * 12
        + current["month"]
    )

    previous_number = (
        previous["year"] * 12
        + previous["month"]
    )

    return (
        current_number
        - previous_number
        == 1
    )


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

        if not is_consecutive_month(
            current,
            previous,
        ):
            continue

        change_value = (
            calculate_percent_change(
                current["index_value"],
                previous["index_value"],
            )
        )

        changes.append(
            {
                "year": current["year"],
                "month": current["month"],
                "period": current["period"],
                "period_name": (
                    current["period_name"]
                ),
                "value": change_value,
                "index_value": (
                    current["index_value"]
                ),
                "previous_index_value": (
                    previous["index_value"]
                ),
                "latest": current["latest"],
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
                    "name": config["name"],
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
                "category": config["category"],
                "name": config["name"],
                "short_name": (
                    config["short_name"]
                ),
                "bls_series_id": (
                    series_id
                ),
                "seasonality": (
                    config["seasonality"]
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

    common_periods = (
        set.intersection(
            *period_sets
        )
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

        for period in periods:
            month = month_lookup.get(
                period["period"]
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

        aligned_row["values"] = (
            values
        )

        aligned_row["index_values"] = (
            index_values
        )

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
    values = []
    calculation_details = []

    for index, period in enumerate(
        periods
    ):
        total_contribution = 0.0
        available_weight = 0.0
        complete = True
        components = []

        for row in rows:
            ppi_mom = row[
                "values"
            ][index]

            pce_weight = float(
                row["pce_weight"]
            )

            if ppi_mom is None:
                complete = False

                component_contribution = (
                    None
                )

            else:
                component_contribution = (
                    float(ppi_mom)
                    * pce_weight
                    / 100
                )

                total_contribution += (
                    component_contribution
                )

                available_weight += (
                    pce_weight
                )

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
                    "ppi_mom": ppi_mom,
                    "pce_weight": (
                        pce_weight
                    ),
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
                total_contribution,
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


def build_category_impact_rows(rows, periods):
    category_order = ["醫療", "投管", "金融", "保險", "運輸", "法律", "其他", "軟體"]
    result = []
    for order, category in enumerate(category_order):
        members = [row for row in rows if row["category"] == category]
        values = []
        for index, _period in enumerate(periods):
            parts = [float(row["values"][index]) * float(row["pce_weight"]) / 100 for row in members if row["values"][index] is not None]
            values.append(round(sum(parts), 6) if len(parts) == len(members) else None)
        result.append({"order": order, "category": category, "name": "金融（不含投管）" if category == "金融" else category, "pce_weight": round(sum(float(row["pce_weight"]) for row in members), 4), "values": values, "unit": "percentage_point"})
    return result

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
    category_impact_rows,
    missing_series,
):
    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    existing = (
        load_existing_payload()
    )

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

            updated_at_utc = (
                existing.get(
                    "updated_at_utc",
                    updated_at_utc,
                )
            )

    pce_weight_total = round(
        sum(
            row["pce_weight"]
            for row in rows
        ),
        3,
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
        "data_changed": (
            data_changed
        ),
        "default_months": 6,
        "available_filter_options": [
            3,
            6,
            12,
        ],
        "period_count": len(periods),
        "row_count": len(rows),
        "pce_weight_total": (
            pce_weight_total
        ),
        "pce_impact_method": {
            "formula": (
                "sum(PPI monthly percent change "
                "x PCE weight / 100)"
            ),
            "unit": (
                "percentage_point"
            ),
            "coverage": (
                "Selected components represent "
                f"{EXPECTED_WEIGHT_TOTAL:.3f} percent of the supplied "
                "PCE weights."
            ),
            "official_bea_forecast": False,
            "caveat": (
                "This is a mechanical proxy "
                "based on selected PPI "
                "components, not an official "
                "BEA Core PCE estimate."
            ),
        },
        "periods": periods,
        "rows": rows,
        "pce_impact_row": (
            pce_impact_row
        ),
        "category_impact_rows": category_impact_rows,
        "missing_series_count": len(
            missing_series
        ),
        "missing_series": (
            missing_series
        ),
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
        "Saved PPI rows:",
        len(rows),
    )
    print(
        "Saved periods:",
        len(periods),
    )
    print(
        "PCE weight total:",
        pce_weight_total,
    )
    print(
        "Missing PPI series:",
        len(missing_series),
    )
    print(
        "Data changed:",
        data_changed,
    )
    print(
        "Output path:",
        OUTPUT_PATH,
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
            item["pce_weight"]
            for item in PPI_SERIES
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

    if len(rows) != len(PPI_SERIES):
        raise RuntimeError(
            "Expected configured PPI rows, "
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
    category_impact_rows = build_category_impact_rows(aligned_rows, periods)

    save_json(
        periods=periods,
        rows=aligned_rows,
        pce_impact_row=(
            pce_impact_row
        ),
        category_impact_rows=category_impact_rows,
        missing_series=(
            missing_series
        ),
    )


if __name__ == "__main__":
    main()