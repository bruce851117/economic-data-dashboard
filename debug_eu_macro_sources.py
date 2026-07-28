from __future__ import annotations

import csv
import io
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

OUTPUT_DIR = Path("debug/eu_macro_sources")
OUTPUT_JSON = OUTPUT_DIR / "eu_last_6_periods.json"
TIMEOUT = 40
USER_AGENT = "EU-Macro-Dashboard-Debug/0.1 (+https://github.com/bruce851117/economic-data-dashboard)"

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": USER_AGENT,
    "Accept-Language": "en,en-GB;q=0.9",
})

EUROSTAT_BASE = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"

# 第一階段只納入已能明確對應官方資料集、單位及調整方式的序列。
# CPI：西、法、德仍採國內 CPI；在找到各國官方精確序列 ID 前不以 HICP 代替。
EUROSTAT_SERIES = {
    "euro_unemployment_rate": {
        "label": "歐元區失業率",
        "dataset": "une_rt_m",
        "params": {"geo": "EA20", "sex": "T", "age": "Y15-74", "unit": "PC_ACT", "s_adj": "SA"},
        "frequency": "monthly",
        "expected_name": "Eurostat Unemployment Eurozone",
    },
    "euro_core_hicp_yoy": {
        "label": "歐元區 Core HICP YoY",
        "dataset": "prc_hicp_manr",
        "params": {"geo": "EA20", "coicop": "TOT_X_NRG_FOOD", "unit": "RCH_A"},
        "frequency": "monthly",
        "expected_name": "Eurostat Eurozone Core MUICP YoY",
    },
    "euro_real_retail_yoy": {
        "label": "歐元區實質零售 YoY",
        "dataset": "sts_trtu_m",
        "params": {"geo": "EA20", "nace_r2": "G47", "indic_bt": "VOL_SLS", "s_adj": "SCA", "unit": "PCH_SM"},
        "frequency": "monthly",
        "expected_name": "Eurostat Retail Sales Eurozone YoY",
    },
    "euro_gdp_yoy": {
        "label": "歐元區 GDP YoY",
        "dataset": "namq_10_gdp",
        "params": {"geo": "EA20", "na_item": "B1GQ", "unit": "CLV_PCH_SM", "s_adj": "SCA"},
        "frequency": "quarterly",
        "expected_name": "Euro Area Gross Domestic Product YoY",
    },
}

BUNDESBANK_SERIES = {
    "germany_unemployment_rate_swda": {
        "label": "德國失業率 SWDA",
        "flow": "BBDL1",
        "key": "M.DE.Y.UNE.UBA000.A0000.A01.D00.0.R00.A",
        "frequency": "monthly",
        "expected_name": "Germany Unemployment Rate SWDA",
    },
}

# 尚待精確確認官方序列 ID 的項目。程式會把這些項目列入結果，避免誤用近似指標。
PENDING = {
    "spain_core_cpi_yoy": "INE 國內 CPI：Underlying inflation（排除未加工食品及能源）",
    "france_cpi_ex_energy_yoy": "INSEE 國內 CPI：All items excluding energy YoY",
    "germany_core_cpi_yoy": "Destatis 國內 CPI：Overall index excluding specified components YoY",
    "france_unemployment_rate_ilo": "INSEE France Unemployment Rate ILO",
    "spain_unemployment_rate": "INE Spain Unemployment Rate",
    "spain_registered_employed_total_change": "Spanish Labour Ministry Registered Employed Total change",
    "germany_unemployment_change_swda": "Bundesbank Germany Unemployment Change SWDA",
    "spain_real_retail_yoy": "INE Spain Retail Sales Constant Prices Working Day Adjusted YoY",
    "germany_real_retail_mom": "Destatis Germany Retail Sales Constant Prices SA MoM",
    "germany_industrial_production_yoy": "Destatis/BMWK Germany Industrial Production YoY",
    "france_consumer_confidence": "INSEE France Consumer Confidence Overall",
    "germany_gfk_consumer_confidence": "NIM Consumer Climate powered by GfK",
    "germany_zew_current": "ZEW Germany Assessment of Current Situation",
    "germany_zew_expectations": "ZEW Germany Economic Expectations",
    "germany_manufacturing_pmi": "S&P Global/HCOB Germany Manufacturing PMI",
    "france_manufacturing_pmi": "S&P Global/HCOB France Manufacturing PMI",
    "spain_manufacturing_pmi": "S&P Global/HCOB Spain Manufacturing PMI",
    "germany_services_pmi": "S&P Global/HCOB Germany Services PMI Business Activity Index",
    "france_services_pmi": "S&P Global/HCOB France Services PMI Business Activity Index",
    "spain_services_pmi": "S&P Global/HCOB Spain Services PMI Business Activity Index",
    "france_manufacturing_confidence": "INSEE France Manufacturing Business Confidence",
    "france_business_confidence": "INSEE France Composite Business Confidence",
    "germany_ifo_business_climate": "ifo Pan Germany Business Climate Index",
    "germany_gdp_yoy": "Destatis Germany real GDP YoY",
    "spain_gdp_yoy": "INE Spain real GDP SA YoY",
    "france_gdp_yoy": "INSEE France real GDP YoY",
}


def request(url: str, *, params: dict[str, str] | None = None) -> requests.Response:
    for attempt in range(1, 4):
        print(f"[HTTP] {attempt}/3 {url} params={params}", flush=True)
        response = SESSION.get(url, params=params, timeout=TIMEOUT)
        print(f"[HTTP] status={response.status_code} bytes={len(response.content)}", flush=True)
        if response.ok:
            return response
        if response.status_code not in {429, 500, 502, 503, 504}:
            response.raise_for_status()
        wait = int(response.headers.get("Retry-After", "0") or 0) or (5 * attempt)
        time.sleep(wait)
    response.raise_for_status()
    return response


def jsonstat_points(payload: dict[str, Any]) -> list[dict[str, Any]]:
    ids = payload.get("id") or []
    sizes = payload.get("size") or []
    dimensions = payload.get("dimension") or {}
    values = payload.get("value") or {}
    if "time" not in ids:
        raise RuntimeError(f"Eurostat response has no time dimension: {ids}")

    categories: list[list[str]] = []
    for dim_id in ids:
        index = dimensions[dim_id]["category"]["index"]
        if isinstance(index, dict):
            ordered = [k for k, _ in sorted(index.items(), key=lambda item: item[1])]
        else:
            ordered = list(index)
        categories.append(ordered)

    points: list[dict[str, Any]] = []
    total = 1
    for size in sizes:
        total *= size
    for flat_index in range(total):
        raw_value = values.get(str(flat_index), values.get(flat_index))
        if raw_value is None:
            continue
        remainder = flat_index
        coordinates = [0] * len(sizes)
        for i in range(len(sizes) - 1, -1, -1):
            coordinates[i] = remainder % sizes[i]
            remainder //= sizes[i]
        labels = {ids[i]: categories[i][coordinates[i]] for i in range(len(ids))}
        points.append({"period": labels["time"], "value": float(raw_value), "dimensions": labels})
    points.sort(key=lambda point: point["period"])
    return points


def fetch_eurostat(config: dict[str, Any]) -> dict[str, Any]:
    url = f"{EUROSTAT_BASE}/{config['dataset']}"
    response = request(url, params={**config["params"], "lang": "EN"})
    payload = response.json()
    raw_name = f"raw_eurostat_{config['dataset']}.json"
    (OUTPUT_DIR / raw_name).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    if payload.get("error"):
        raise RuntimeError(str(payload["error"]))
    points = jsonstat_points(payload)[-6:]
    return {
        "status": "ok",
        "source": "Eurostat Statistics API",
        "source_url": response.url,
        "dataset": config["dataset"],
        "filters": config["params"],
        "data": points,
    }


def parse_bundesbank_csv(text: str) -> list[dict[str, Any]]:
    # Bundesbank下載檔是metadata列加上period/value列；分隔符可能是逗號或分號。
    delimiter = ";" if text.count(";") > text.count(",") else ","
    rows = csv.reader(io.StringIO(text.lstrip("\ufeff")), delimiter=delimiter)
    points = []
    for row in rows:
        if len(row) < 2:
            continue
        period = row[0].strip().strip('"')
        value = row[1].strip().strip('"').replace(",", ".")
        if re.fullmatch(r"\d{4}-\d{2}", period) and re.fullmatch(r"-?\d+(?:\.\d+)?", value):
            points.append({"period": period, "value": float(value)})
    return points


def fetch_bundesbank(config: dict[str, Any]) -> dict[str, Any]:
    url = f"https://api.statistiken.bundesbank.de/rest/download/{config['flow']}/{config['key']}"
    response = request(url, params={"format": "csv", "lang": "en"})
    raw_name = f"raw_bundesbank_{config['flow']}.csv"
    (OUTPUT_DIR / raw_name).write_text(response.text, encoding="utf-8")
    points = parse_bundesbank_csv(response.text)[-6:]
    if not points:
        raise RuntimeError("Bundesbank CSV contained no monthly observations")
    return {
        "status": "ok",
        "source": "Deutsche Bundesbank SDMX download API",
        "source_url": response.url,
        "flow": config["flow"],
        "key": config["key"],
        "data": points,
    }


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    result: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scope": "official-source diagnostic; latest 6 available periods",
        "important_note": "Spain, France and Germany CPI must use national CPI, not HICP. Pending series are intentionally not substituted.",
        "series": {},
    }

    for series_id, config in EUROSTAT_SERIES.items():
        print(f"[EUROSTAT] {series_id}", flush=True)
        try:
            result["series"][series_id] = {**config, **fetch_eurostat(config)}
        except Exception as error:
            result["series"][series_id] = {**config, "status": "error", "error": str(error)}

    for series_id, config in BUNDESBANK_SERIES.items():
        print(f"[BUNDESBANK] {series_id}", flush=True)
        try:
            result["series"][series_id] = {**config, **fetch_bundesbank(config)}
        except Exception as error:
            result["series"][series_id] = {**config, "status": "error", "error": str(error)}

    for series_id, definition in PENDING.items():
        result["series"][series_id] = {
            "status": "pending_exact_official_series_id",
            "definition": definition,
            "data": [],
        }

    OUTPUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\n[SUMMARY]", flush=True)
    for series_id, item in result["series"].items():
        print(series_id, item["status"], len(item.get("data", [])), flush=True)
    print(f"\nSaved: {OUTPUT_JSON}", flush=True)


if __name__ == "__main__":
    main()
