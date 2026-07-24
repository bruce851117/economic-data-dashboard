from __future__ import annotations

import csv
import io
import json
import math
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DATA_FILE = Path("data/uk_macro.json")
USER_AGENT = "Mozilla/5.0 (compatible; economic-data-dashboard/1.0)"
TIMEOUT = 60
MAX_RETRIES = 4

# Official ONS series with definitions matched against the user's Bloomberg references.
ONS_SERIES = {
    "core_cpi_yoy": {"dataset": "MM23", "cdid": "DKO8", "frequency": "monthly", "ticker": "UKHCA9IQ Index"},
    "cpi_services_yoy": {"dataset": "MM23", "cdid": "D7NN", "frequency": "monthly", "ticker": "UKHPSERY Index"},
    "unemployment_rate": {"dataset": "LMS", "cdid": "MGSX", "frequency": "rolling_3m", "ticker": "UKUEILOR Index"},
    "claimant_count_rate": {"dataset": "UNEM", "cdid": "BCJE", "frequency": "monthly", "ticker": "UKUER Index"},
    "awe_total_pay_3m_yoy": {"dataset": "LMS", "cdid": "KAC3", "frequency": "monthly", "ticker": "UKAWMWHO Index"},
    "awe_private_regular_3m_yoy": {"dataset": "LMS", "cdid": "KAJ4", "frequency": "monthly", "ticker": "UKAWXPRM Index"},
    "vacancies": {"dataset": "UNEM", "cdid": "AP2Y", "frequency": "rolling_3m", "ticker": "UKVAAP2Y Index"},
    "unemployed_per_vacancy": {"dataset": "UNEM", "cdid": "JPC5", "frequency": "rolling_3m", "ticker": "UKLFJPC5 Index"},
    "monthly_gdp_mom": {"dataset": "MGDP", "cdid": "ECYX", "frequency": "monthly", "ticker": "UKGDM3M Index"},
}

# Quarterly level series. The updater derives year-on-year growth from official real SA levels.
QUARTERLY_LEVEL_SERIES = {
    "quarterly_gdp_yoy": {"dataset": "QNA", "cdid": "ABMI", "ticker": "UKGRABIY Index"},
    "hfce_yoy": {"dataset": "PN2", "cdid": "ABJR", "ticker": "UKGEABRY Index"},
    "gfcf_yoy": {"dataset": "UKEA", "cdid": "NPQT", "ticker": "UKGVNPQY Index"},
}

ONS_PATHS = {
    "MM23": "economy/inflationandpriceindices",
    "LMS": "employmentandlabourmarket/peoplenotinwork/unemployment",
    "UNEM": "employmentandlabourmarket/peoplenotinwork/outofworkbenefits",
    "MGDP": "economy/grossdomesticproductgdp",
    "QNA": "economy/grossdomesticproductgdp",
    "PN2": "economy/nationalaccounts/satelliteaccounts",
    "UKEA": "economy/grossdomesticproductgdp",
}


def fetch_bytes(url: str) -> bytes:
    last_error: Exception | None = None
    for attempt in range(MAX_RETRIES):
        try:
            req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
            with urlopen(req, timeout=TIMEOUT) as response:
                return response.read()
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            last_error = exc
            if isinstance(exc, HTTPError) and exc.code not in {429, 500, 502, 503, 504}:
                break
            time.sleep(3 * (2 ** attempt))
    raise RuntimeError(f"GET failed: {url}: {last_error}")


def ons_url(dataset: str, cdid: str) -> str:
    path = ONS_PATHS[dataset]
    edition = dataset.lower()
    if cdid == "ABJR":
        edition = "pn2"
    return (
        "https://www.ons.gov.uk/generator?format=csv&uri=/"
        f"{path}/timeseries/{cdid.lower()}/{edition}"
    )


def normalise_period(raw: str) -> str | None:
    value = " ".join(raw.strip().upper().split())
    months = {
        "JAN": "01", "FEB": "02", "MAR": "03", "APR": "04", "MAY": "05", "JUN": "06",
        "JUL": "07", "AUG": "08", "SEP": "09", "OCT": "10", "NOV": "11", "DEC": "12",
    }
    match = re.fullmatch(r"(\d{4}) (JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)", value)
    if match:
        return f"{match.group(1)}-{months[match.group(2)]}"
    match = re.fullmatch(r"(\d{4}) Q([1-4])", value)
    if match:
        return f"{match.group(1)}-Q{match.group(2)}"
    return None


def shift_month(period: str, months: int) -> str:
    year, month = map(int, period.split("-"))
    index = year * 12 + month - 1 + months
    return f"{index // 12:04d}-{index % 12 + 1:02d}"


def parse_ons_series(dataset: str, cdid: str) -> tuple[str, list[dict[str, Any]]]:
    url = ons_url(dataset, cdid)
    text = fetch_bytes(url).decode("utf-8-sig", errors="replace")
    rows = list(csv.reader(io.StringIO(text)))
    title = ""
    observations: list[dict[str, Any]] = []
    for row in rows:
        if len(row) < 2:
            continue
        if row[0].strip().lower() == "title":
            title = row[1].strip()
        period = normalise_period(row[0])
        raw_value = row[1].replace(",", "").strip()
        if period and re.fullmatch(r"-?\d+(?:\.\d+)?", raw_value):
            observations.append({"period": period, "value": float(raw_value)})
    if not observations:
        raise RuntimeError(f"No observations returned for {cdid}: {url}")
    return title, observations


def derive_quarterly_yoy(levels: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_period = {row["period"]: row["value"] for row in levels}
    output: list[dict[str, Any]] = []
    for period, value in by_period.items():
        match = re.fullmatch(r"(\d{4})-Q([1-4])", period)
        if not match:
            continue
        previous_period = f"{int(match.group(1)) - 1}-Q{match.group(2)}"
        previous = by_period.get(previous_period)
        if previous not in {None, 0}:
            output.append({"period": period, "value": (value / previous - 1) * 100})
    return sorted(output, key=lambda row: row["period"])


def load_database() -> dict[str, Any]:
    if not DATA_FILE.exists():
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        return {"updated_at": None, "series": {}}
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    if not isinstance(data.get("series"), dict):
        raise ValueError("data/uk_macro.json must contain a top-level 'series' object")
    return data


def merge_observations(
    database: dict[str, Any],
    key: str,
    metadata: dict[str, Any],
    incoming: list[dict[str, Any]],
) -> tuple[int, int]:
    series = database["series"].setdefault(key, {**metadata, "observations": []})
    for field, value in metadata.items():
        series[field] = value

    existing = {row["date"]: row for row in series.get("observations", []) if row.get("date")}
    added = 0
    revised = 0
    for row in incoming:
        date = row["date"]
        old = existing.get(date)
        new_row = {**row, "retrieved_at": datetime.now(timezone.utc).isoformat()}
        if old is None:
            existing[date] = new_row
            added += 1
        elif old.get("value") != row.get("value") or old.get("release_type") != row.get("release_type"):
            # Final data always beats flash. Flash must never overwrite final.
            if old.get("release_type") == "final" and row.get("release_type") == "flash":
                continue
            existing[date] = {**old, **new_row}
            revised += 1

    series["observations"] = sorted(existing.values(), key=lambda row: row["date"])
    return added, revised


def update_ons(database: dict[str, Any]) -> list[str]:
    logs: list[str] = []
    for key, config in ONS_SERIES.items():
        try:
            title, observations = parse_ons_series(config["dataset"], config["cdid"])
            incoming = []
            for row in observations:
                period = row["period"]
                display_period = shift_month(period, 1) if config["frequency"] == "rolling_3m" else period
                incoming.append({
                    "date": display_period,
                    "source_period": period,
                    "value": row["value"],
                    "source": "ONS",
                    "source_url": ons_url(config["dataset"], config["cdid"]),
                })
            added, revised = merge_observations(database, key, {
                "ticker": config["ticker"], "title": title, "frequency": config["frequency"],
                "source": "ONS", "cdid": config["cdid"],
            }, incoming)
            logs.append(f"{key}: +{added}, revised {revised}")
        except Exception as exc:
            logs.append(f"WARNING {key}: {exc}")

    for key, config in QUARTERLY_LEVEL_SERIES.items():
        try:
            title, levels = parse_ons_series(config["dataset"], config["cdid"])
            yoy = derive_quarterly_yoy(levels)
            incoming = [{
                "date": row["period"], "value": row["value"], "source": "ONS",
                "source_url": ons_url(config["dataset"], config["cdid"]),
                "calculation": "(current_quarter / same_quarter_previous_year - 1) * 100",
            } for row in yoy]
            added, revised = merge_observations(database, key, {
                "ticker": config["ticker"], "title": title + " - YoY", "frequency": "quarterly",
                "source": "ONS", "cdid": config["cdid"],
            }, incoming)
            logs.append(f"{key}: +{added}, revised {revised}")
        except Exception as exc:
            logs.append(f"WARNING {key}: {exc}")
    return logs


def ensure_manual_placeholders(database: dict[str, Any]) -> None:
    # These are kept in the same file so the user's existing history can be pasted once.
    placeholders = {
        "inflation_expectations_1y": {
            "ticker": "UKBFFTIN Index", "title": "1Y Inflation Expectations",
            "frequency": "monthly", "source": "manual", "status": "source_unverified",
        },
        "gfk_consumer_confidence": {
            "ticker": "UKCCI Index", "title": "GfK Consumer Confidence",
            "frequency": "monthly", "source": "NIQ/GfK", "status": "manual_history_then_incremental",
        },
        "manufacturing_pmi": {
            "ticker": "MPMIGBMA Index", "title": "S&P Global UK Manufacturing PMI",
            "frequency": "monthly", "source": "S&P Global", "selection_rule": "final_else_flash",
        },
        "services_pmi": {
            "ticker": "MPMIGBSA Index", "title": "S&P Global UK Services PMI",
            "frequency": "monthly", "source": "S&P Global", "selection_rule": "final_else_flash",
        },
        "retail_sales_ex_fuel_yoy": {
            "ticker": "UKRVAYOY Index", "title": "Retail Sales ex Automotive Fuel YoY",
            "frequency": "monthly", "source": "ONS Retail Sales Index", "status": "pending_api_filter",
        },
    }
    for key, metadata in placeholders.items():
        database["series"].setdefault(key, {**metadata, "observations": []})


def main() -> None:
    database = load_database()
    ensure_manual_placeholders(database)
    logs = update_ons(database)
    database["updated_at"] = datetime.now(timezone.utc).isoformat()
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(database, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n".join(logs))
    print(f"Saved: {DATA_FILE}")


if __name__ == "__main__":
    main()
