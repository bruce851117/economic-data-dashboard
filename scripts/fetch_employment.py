import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests


BLS_API_URL = (
    "https://api.bls.gov/publicAPI/v2/timeseries/data/"
)

BLS_EMPLOYMENT_SOURCE_URL = (
    "https://www.bls.gov/news.release/"
    "empsit.toc.htm"
)

OUTPUT_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "employment.json"
)

BLS_BATCH_SIZE = 10


EMPLOYMENT_SERIES = [
    {
        "name": "Total Nonfarm Payrolls",
        "display_name": "非農就業",
        "series_id": "CES0000000001",
        "section": "overview",
        "source": "CES",
        "unit": "thousand",
        "transform": "change",
        "seasonality": "SA",
    },
    {
        "name": "Household Employment",
        "display_name": "家庭調查就業",
        "series_id": "LNS12000000",
        "section": "overview",
        "source": "CPS",
        "unit": "thousand",
        "transform": "change",
        "seasonality": "SA",
    },
    {
        "name": "Civilian Labor Force",
        "display_name": "勞動力",
        "series_id": "LNS11000000",
        "section": "overview",
        "source": "CPS",
        "unit": "thousand",
        "transform": "change",
        "seasonality": "SA",
    },
    {
        "name": "Unemployment Level",
        "display_name": "失業人數",
        "series_id": "LNS13000000",
        "section": "overview",
        "source": "CPS",
        "unit": "thousand",
        "transform": "change",
        "seasonality": "SA",
    },
    {
        "name": "Unemployment Rate",
        "display_name": "失業率",
        "series_id": "LNS14000000",
        "section": "overview",
        "source": "CPS",
        "unit": "percent",
        "transform": "level",
        "seasonality": "SA",
    },
    {
        "name": "Labor Force Participation Rate",
        "display_name": "勞動參與率",
        "series_id": "LNS11300000",
        "section": "overview",
        "source": "CPS",
        "unit": "percent",
        "transform": "level",
        "seasonality": "SA",
    },
    {
        "name": "Employment-Population Ratio",
        "display_name": "就業人口比",
        "series_id": "LNS12300000",
        "section": "overview",
        "source": "CPS",
        "unit": "percent",
        "transform": "level",
        "seasonality": "SA",
    },
    {
        "name": "Average Weeks Unemployed",
        "display_name": "平均失業期間",
        "series_id": "LNS13008275",
        "section": "overview",
        "source": "CPS",
        "unit": "week",
        "transform": "level",
        "seasonality": "SA",
    },
    {
        "name": "Employed to Unemployed",
        "display_name": "就業 → 失業",
        "series_id": "LNS17400000",
        "section": "flows",
        "source": "CPS",
        "unit": "thousand",
        "transform": "level",
        "seasonality": "SA",
    },
    {
        "name": "Unemployed to Employed",
        "display_name": "失業 → 就業",
        "series_id": "LNS17100000",
        "section": "flows",
        "source": "CPS",
        "unit": "thousand",
        "transform": "level",
        "seasonality": "SA",
    },
    {
        "name": "Employed to Not in Labor Force",
        "display_name": "就業 → 退出勞動力",
        "series_id": "LNS17800000",
        "section": "flows",
        "source": "CPS",
        "unit": "thousand",
        "transform": "level",
        "seasonality": "SA",
    },
    {
        "name": "Not in Labor Force to Employed",
        "display_name": "退出勞動力 → 就業",
        "series_id": "LNS17200000",
        "section": "flows",
        "source": "CPS",
        "unit": "thousand",
        "transform": "level",
        "seasonality": "SA",
    },
    {
        "name": "Unemployed to Not in Labor Force",
        "display_name": "失業 → 退出勞動力",
        "series_id": "LNS17900000",
        "section": "flows",
        "source": "CPS",
        "unit": "thousand",
        "transform": "level",
        "seasonality": "SA",
    },
    {
        "name": "Not in Labor Force to Unemployed",
        "display_name": "退出勞動力 → 失業",
        "series_id": "LNS17600000",
        "section": "flows",
        "source": "CPS",
        "unit": "thousand",
        "transform": "level",
        "seasonality": "SA",
    },
    {
        "name": "Job Losers on Layoff",
        "display_name": "暫時性裁員",
        "series_id": "LNS13023653",
        "section": "reasons",
        "source": "CPS",
        "unit": "thousand",
        "transform": "level",
        "seasonality": "SA",
    },
    {
        "name": "Permanent Job Losers",
        "display_name": "永久失業",
        "series_id": "LNS13026638",
        "section": "reasons",
        "source": "CPS",
        "unit": "thousand",
        "transform": "level",
        "seasonality": "SA",
    },
    {
        "name": "Completed Temporary Jobs",
        "display_name": "臨時工作結束",
        "series_id": "LNS13026637",
        "section": "reasons",
        "source": "CPS",
        "unit": "thousand",
        "transform": "level",
        "seasonality": "SA",
    },
    {
        "name": "Job Leavers",
        "display_name": "主動離職",
        "series_id": "LNS13023705",
        "section": "reasons",
        "source": "CPS",
        "unit": "thousand",
        "transform": "level",
        "seasonality": "SA",
    },
    {
        "name": "Reentrants to Labor Force",
        "display_name": "重返勞動市場",
        "series_id": "LNS13023557",
        "section": "reasons",
        "source": "CPS",
        "unit": "thousand",
        "transform": "level",
        "seasonality": "SA",
    },
    {
        "name": "New Entrants",
        "display_name": "初次進入勞動市場",
        "series_id": "LNS13023569",
        "section": "reasons",
        "source": "CPS",
        "unit": "thousand",
        "transform": "level",
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


def get_current_year():
    return datetime.now(
        timezone.utc
    ).year


def split_into_batches(
    items,
    batch_size,
):
    return [
        items[
            index:
            index + batch_size
        ]
        for index in range(
            0,
            len(items),
            batch_size,
        )
    ]


def request_employment_batch(
    series_ids,
    batch_number,
    total_batches,
):
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
        "BLS Employment batch:",
        f"{batch_number}/{total_batches}",
    )
    print(
        "Requested series:",
        len(series_ids),
    )
    print(
        "Series IDs:",
        ", ".join(series_ids),
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
            "Content-Type": (
                "application/json"
            ),
            "Accept": (
                "application/json"
            ),
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
            "BLS Employment API returned "
            "an HTTP error.\n"
            f"Batch: {batch_number}/"
            f"{total_batches}\n"
            f"Series IDs: {series_ids}\n"
            f"HTTP status: "
            f"{response.status_code}\n"
            f"Response: "
            f"{response.text[:3000]}"
        )

    try:
        result = response.json()
    except requests.JSONDecodeError as error:
        raise RuntimeError(
            "BLS Employment API did not "
            "return valid JSON.\n"
            f"Batch: {batch_number}/"
            f"{total_batches}\n"
            f"Series IDs: {series_ids}"
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
        print(
            "BLS response messages:"
        )

        for message in messages:
            print(f"- {message}")

    if status != "REQUEST_SUCCEEDED":
        raise RuntimeError(
            "BLS Employment API batch "
            "did not succeed.\n"
            f"Batch: {batch_number}/"
            f"{total_batches}\n"
            f"Series IDs: "
            f"{', '.join(series_ids)}\n"
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
            "BLS Employment API batch "
            "returned no series.\n"
            f"Batch: {batch_number}/"
            f"{total_batches}\n"
            f"Series IDs: "
            f"{', '.join(series_ids)}"
        )

    print(
        "Returned series:",
        len(returned_series),
    )
    print("=" * 72)

    return returned_series


def fetch_employment_series():
    series_ids = [
        item["series_id"]
        for item in EMPLOYMENT_SERIES
    ]

    batches = split_into_batches(
        series_ids,
        BLS_BATCH_SIZE,
    )

    print(
        "Starting BLS employment "
        "batch requests."
    )
    print(
        "Total employment series:",
        len(series_ids),
    )
    print(
        "Batch size:",
        BLS_BATCH_SIZE,
    )
    print(
        "Total batches:",
        len(batches),
    )

    all_series = []

    for batch_index, batch in enumerate(
        batches,
        start=1,
    ):
        batch_series = (
            request_employment_batch(
                series_ids=batch,
                batch_number=batch_index,
                total_batches=len(batches),
            )
        )

        all_series.extend(
            batch_series
        )

    returned_ids = {
        series.get(
            "seriesID",
            "",
        )
        for series in all_series
    }

    missing_returned_ids = [
        series_id
        for series_id in series_ids
        if series_id not in returned_ids
    ]

    print("=" * 72)
    print(
        "Combined returned series:",
        len(all_series),
    )

    if missing_returned_ids:
        print(
            "Series not returned by API:",
            ", ".join(
                missing_returned_ids
            ),
        )

    print("=" * 72)

    return all_series


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

            value = float(
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
                "value": value,
                "latest": (
                    observation.get(
                        "latest",
                        False,
                    )
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


def transform_observations(
    observations,
    transform,
):
    if transform == "level":
        return observations

    if transform != "change":
        raise RuntimeError(
            "Unknown employment transform: "
            f"{transform}"
        )

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

        changes.append(
            {
                "year": current["year"],
                "month": current["month"],
                "period": current["period"],
                "period_name": (
                    current["period_name"]
                ),
                "value": round(
                    current["value"]
                    - previous["value"],
                    3,
                ),
                "level": (
                    current["value"]
                ),
                "previous_level": (
                    previous["value"]
                ),
                "latest": (
                    current["latest"]
                ),
            }
        )

    return changes


def build_rows(api_series):
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
        EMPLOYMENT_SERIES
    ):
        series_id = config[
            "series_id"
        ]

        series = api_lookup.get(
            series_id
        )

        transformed_data = []
        series_title = ""

        if series:
            observations = (
                parse_observations(
                    series
                )
            )

            transformed_data = (
                transform_observations(
                    observations,
                    config["transform"],
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

        if not transformed_data:
            missing_series.append(
                {
                    "name": (
                        config["name"]
                    ),
                    "series_id": series_id,
                    "reason": (
                        "Series contained no "
                        "usable monthly data"
                    ),
                }
            )

        print(
            "Employment series:",
            series_id,
            "|",
            config["display_name"],
            "|",
            config["section"],
            "|",
            series_title,
            "| observations:",
            len(transformed_data),
        )

        rows.append(
            {
                "order": order,
                "name": config["name"],
                "display_name": (
                    config[
                        "display_name"
                    ]
                ),
                "series_id": series_id,
                "section": (
                    config["section"]
                ),
                "source": (
                    config["source"]
                ),
                "unit": config["unit"],
                "transform": (
                    config["transform"]
                ),
                "seasonality": (
                    config[
                        "seasonality"
                    ]
                ),
                "series_title": (
                    series_title
                ),
                "available": bool(
                    transformed_data
                ),
                "months": (
                    transformed_data
                ),
            }
        )

    return rows, missing_series


def collect_periods(rows):
    period_lookup = {}

    for row in rows:
        for month in row.get(
            "months",
            [],
        ):
            period_lookup[
                month["period"]
            ] = {
                "year": (
                    month["year"]
                ),
                "month": (
                    month["month"]
                ),
                "period": (
                    month["period"]
                ),
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
        levels = []

        for period in periods:
            month = month_lookup.get(
                period["period"]
            )

            values.append(
                month.get("value")
                if month
                else None
            )

            if month:
                levels.append(
                    month.get(
                        "level",
                        month.get("value"),
                    )
                )

            else:
                levels.append(None)

        aligned_row = dict(row)

        aligned_row[
            "values"
        ] = values

        aligned_row[
            "levels"
        ] = levels

        aligned_row.pop(
            "months",
            None,
        )

        aligned_rows.append(
            aligned_row
        )

    return aligned_rows


def split_sections(rows):
    return {
        "overview": [
            row
            for row in rows
            if row["section"]
            == "overview"
        ],
        "flows": [
            row
            for row in rows
            if row["section"]
            == "flows"
        ],
        "reasons": [
            row
            for row in rows
            if row["section"]
            == "reasons"
        ],
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
    missing_series,
):
    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    sections = split_sections(
        rows
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

    payload = {
        "source": (
            "U.S. Bureau of Labor Statistics"
        ),
        "source_type": (
            "BLS Public Data API Version 2"
        ),
        "api_url": BLS_API_URL,
        "source_url": (
            BLS_EMPLOYMENT_SOURCE_URL
        ),
        "title": (
            "U.S. Employment Situation "
            "Dashboard"
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
        "section_counts": {
            "overview": len(
                sections["overview"]
            ),
            "flows": len(
                sections["flows"]
            ),
            "reasons": len(
                sections["reasons"]
            ),
        },
        "periods": periods,
        "rows": rows,
        "sections": sections,
        "missing_series_count": len(
            missing_series
        ),
        "missing_series": (
            missing_series
        ),
        "methodology": {
            "ces": (
                "Current Employment Statistics "
                "establishment survey"
            ),
            "cps": (
                "Current Population Survey "
                "household survey"
            ),
            "change_rows": (
                "Current month level minus "
                "previous month level"
            ),
            "flow_definition": (
                "Movement between employed, "
                "unemployed, and not in labor "
                "force states"
            ),
        },
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
        "Saved employment rows:",
        len(rows),
    )
    print(
        "Saved periods:",
        len(periods),
    )
    print(
        "Overview rows:",
        len(sections["overview"]),
    )
    print(
        "Flow rows:",
        len(sections["flows"]),
    )
    print(
        "Reason rows:",
        len(sections["reasons"]),
    )
    print(
        "Missing employment series:",
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
            "Employment period range:",
            periods[0]["period"],
            "to",
            periods[-1]["period"],
        )

    print("=" * 72)


def main():
    print(
        "Starting registered BLS "
        "employment data update."
    )

    api_series = (
        fetch_employment_series()
    )

    rows, missing_series = (
        build_rows(
            api_series
        )
    )

    if len(rows) != len(
        EMPLOYMENT_SERIES
    ):
        raise RuntimeError(
            "Expected "
            f"{len(EMPLOYMENT_SERIES)} "
            "employment rows, but generated "
            f"{len(rows)} rows."
        )

    if missing_series:
        missing_text = ", ".join(
            item["series_id"]
            for item in missing_series
        )

        raise RuntimeError(
            "One or more employment series "
            "returned no usable data: "
            f"{missing_text}"
        )

    periods = collect_periods(
        rows
    )

    if len(periods) != 12:
        raise RuntimeError(
            "Expected 12 employment periods, "
            f"but generated {len(periods)}."
        )

    aligned_rows = align_rows(
        rows,
        periods,
    )

    save_json(
        periods=periods,
        rows=aligned_rows,
        missing_series=(
            missing_series
        ),
    )


if __name__ == "__main__":
    main()