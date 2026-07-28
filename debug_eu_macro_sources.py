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
        "params": {"geo": "EA21", "sex": "T", "age": "TOTAL", "unit": "PC_ACT", "s_adj": "SA"},
        "frequency": "monthly",
        "expected_name": "Eurostat Unemployment Eurozone",
        "discovery_filters": {"geo": "EA21"},
        "preferred": {"freq": "M", "sex": "T", "age": "TOTAL", "unit": "PC_ACT", "s_adj": "SA"},
    },
    "euro_core_hicp_yoy": {
        "label": "歐元區 Core HICP YoY",
        "dataset": "prc_hicp_manr",
        "params": {"geo": "EA21", "coicop": "TOT_X_NRG_FOOD", "unit": "RCH_A"},
        "frequency": "monthly",
        "expected_name": "Eurostat Eurozone Core MUICP YoY",
        "discovery_filters": {"geo": "EA21", "unit": "RCH_A"},
        "preferred": {"freq": "M", "unit": "RCH_A"},
        "dimension_label_keywords": {"coicop": ["excluding energy", "food", "alcohol", "tobacco"]},
    },
    "euro_real_retail_yoy": {
        "label": "歐元區實質零售 YoY",
        "dataset": "sts_trtu_m",
        "params": {"geo": "EA21", "nace_r2": "G47", "indic_bt": "VOL_SLS", "s_adj": "SCA", "unit": "PCH_SM"},
        "frequency": "monthly",
        "expected_name": "Eurostat Retail Sales Eurozone YoY",
        "discovery_filters": {"geo": "EA21", "nace_r2": "G47"},
        "preferred": {"freq": "M", "indic_bt": "VOL_SLS", "nace_r2": "G47", "s_adj": "SCA", "unit": "PCH_SM"},
    },
    "euro_gdp_yoy": {
        "label": "歐元區 GDP YoY",
        "dataset": "namq_10_gdp",
        "params": {"geo": "EA21", "na_item": "B1GQ", "unit": "CLV_PCH_SM", "s_adj": "SCA"},
        "frequency": "quarterly",
        "expected_name": "Euro Area Gross Domestic Product YoY",
        "discovery_filters": {"geo": "EA21", "na_item": "B1GQ"},
        "preferred": {"freq": "Q", "na_item": "B1GQ", "unit": "CLV_PCH_SM", "s_adj": "SCA"},
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


def _ordered_codes(payload: dict[str, Any], dim_id: str) -> list[str]:
    index = payload["dimension"][dim_id]["category"]["index"]
    if isinstance(index, dict):
        return [key for key, _ in sorted(index.items(), key=lambda item: item[1])]
    return list(index)


def jsonstat_points(payload: dict[str, Any]) -> list[dict[str, Any]]:
    ids = payload.get("id") or []
    sizes = payload.get("size") or []
    dimensions = payload.get("dimension") or {}
    values = payload.get("value")
    if "time" not in ids:
        raise RuntimeError(f"Eurostat response has no time dimension: {ids}")

    categories = [_ordered_codes(payload, dim_id) for dim_id in ids]
    labels = {
        dim_id: dimensions[dim_id].get("category", {}).get("label", {})
        for dim_id in ids
    }
    total = 1
    for size in sizes:
        total *= size

    points: list[dict[str, Any]] = []
    for flat_index in range(total):
        if isinstance(values, list):
            raw_value = values[flat_index] if flat_index < len(values) else None
        elif isinstance(values, dict):
            raw_value = values.get(str(flat_index), values.get(flat_index))
        else:
            raw_value = None
        if raw_value is None:
            continue
        remainder = flat_index
        coordinates = [0] * len(sizes)
        for i in range(len(sizes) - 1, -1, -1):
            coordinates[i] = remainder % sizes[i]
            remainder //= sizes[i]
        codes = {ids[i]: categories[i][coordinates[i]] for i in range(len(ids))}
        point_labels = {
            dim_id: labels[dim_id].get(code, code)
            for dim_id, code in codes.items()
        }
        points.append({
            "period": codes["time"],
            "value": float(raw_value),
            "dimensions": codes,
            "dimension_labels": point_labels,
        })
    points.sort(key=lambda point: point["period"])
    return points


def dimension_options(payload: dict[str, Any]) -> dict[str, list[dict[str, str]]]:
    output: dict[str, list[dict[str, str]]] = {}
    for dim_id in payload.get("id") or []:
        codes = _ordered_codes(payload, dim_id)
        label_map = payload["dimension"][dim_id].get("category", {}).get("label", {})
        output[dim_id] = [{"code": code, "label": label_map.get(code, code)} for code in codes]
    return output


def _matches_preferred(point: dict[str, Any], preferred: dict[str, str]) -> bool:
    dimensions = point.get("dimensions", {})
    return all(dimensions.get(key) == value for key, value in preferred.items())


def _matches_keywords(point: dict[str, Any], rules: dict[str, list[str]]) -> bool:
    labels = point.get("dimension_labels", {})
    for dim_id, keywords in rules.items():
        text = str(labels.get(dim_id, "")).lower()
        if not all(keyword.lower() in text for keyword in keywords):
            return False
    return True

def fetch_eurostat(config: dict[str, Any]) -> dict[str, Any]:
    url = f"{EUROSTAT_BASE}/{config['dataset']}"
    current_year = datetime.now(timezone.utc).year
    geo_candidates = ["EA21", "EA", "EA20"]
    query_attempts: list[dict[str, Any]] = []
    combined_points: list[dict[str, Any]] = []
    payloads: list[dict[str, Any]] = []

    # Query each official euro-area composition separately. Eurostat does not
    # expose geo=EA consistently across all datasets, while 2026 observations
    # are published under EA21 and older observations may remain under EA20.
    for geo in geo_candidates:
        params = {**config["params"], "geo": geo, "lang": "EN", "lastTimePeriod": "18"}
        response = request(url, params=params)
        payload = response.json()
        raw_name = f"raw_eurostat_{config['dataset']}_{geo}_exact.json"
        (OUTPUT_DIR / raw_name).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        has_empty_dimension = any(size == 0 for size in payload.get("size", []))
        points = (
            jsonstat_points(payload)
            if not payload.get("error") and not has_empty_dimension
            else []
        )
        query_attempts.append({
            "geo": geo,
            "url": response.url,
            "observation_count": len(points),
            "newest_period": max((point["period"] for point in points), default=None),
            "empty_dimension": has_empty_dimension,
        })
        if points:
            combined_points.extend(points)
            payloads.append(payload)

    preferred_without_geo = {
        key: value for key, value in config.get("preferred", {}).items()
        if key != "geo"
    }
    candidates = [
        point for point in combined_points
        if _matches_preferred(point, preferred_without_geo)
    ]
    keyword_rules = config.get("dimension_label_keywords", {})
    if keyword_rules:
        candidates = [point for point in candidates if _matches_keywords(point, keyword_rules)]

    # If the exact slices still fail, run one broader EA21 discovery request.
    selection_mode = "geo_composition_fallback"
    if not candidates:
        discovery_filters = {
            **config.get("discovery_filters", {}),
            "geo": "EA21",
            "lang": "EN",
            "lastTimePeriod": "18",
        }
        response = request(url, params=discovery_filters)
        payload = response.json()
        (OUTPUT_DIR / f"raw_eurostat_{config['dataset']}_EA21_discovery.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        has_empty_dimension = any(size == 0 for size in payload.get("size", []))
        all_points = (
            jsonstat_points(payload)
            if not payload.get("error") and not has_empty_dimension
            else []
        )
        candidates = [
            point for point in all_points
            if _matches_preferred(point, preferred_without_geo)
        ]
        if keyword_rules:
            candidates = [point for point in candidates if _matches_keywords(point, keyword_rules)]
        query_attempts.append({
            "geo": "EA21-discovery",
            "url": response.url,
            "observation_count": len(all_points),
            "matched_count": len(candidates),
            "empty_dimension": has_empty_dimension,
        })
        payloads.append(payload)
        selection_mode = "EA21_dimension_discovery"

    # For duplicate periods, prefer the composition applicable to that year:
    # EA21 from 2026, EA20 before 2026, then changing-composition EA.
    geo_priority = {"EA21": 3, "EA20": 2, "EA": 1}
    by_period: dict[str, dict[str, Any]] = {}
    for point in candidates:
        period = point["period"]
        point_geo = point.get("dimensions", {}).get("geo", "")
        preferred_geo = "EA21" if period.startswith(str(current_year)) else "EA20"
        score = 10 if point_geo == preferred_geo else geo_priority.get(point_geo, 0)
        current = by_period.get(period)
        if current is None or score > current["_score"]:
            by_period[period] = {**point, "_score": score}
    points = []
    for period in sorted(by_period)[-6:]:
        clean = {key: value for key, value in by_period[period].items() if key != "_score"}
        points.append(clean)

    options = dimension_options(payloads[-1]) if payloads else {}
    return {
        "status": "ok" if points else "no_data",
        "source": "Eurostat Statistics API",
        "source_url": query_attempts[-1]["url"] if query_attempts else url,
        "dataset": config["dataset"],
        "filters": config["params"],
        "selection_mode": selection_mode,
        "query_attempts": query_attempts,
        "selected_dimensions": points[-1]["dimensions"] if points else None,
        "available_dimension_options": options,
        "data": points,
        **({"diagnostic": "No observations matched across EA21, EA and EA20"} if not points else {}),
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
        "important_note": "Spain, France and Germany CPI must use national CPI, not HICP. Euro-area latest data use geo=EA21 from 2026; fallback queries also test EA and EA20 for continuity. Pending series are intentionally not substituted.",
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
