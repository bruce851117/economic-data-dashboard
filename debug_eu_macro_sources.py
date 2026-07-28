from __future__ import annotations

import csv
import io
import json
import re
import time
from html.parser import HTMLParser
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

OUTPUT_DIR = Path("debug/eu_macro_sources")
OUTPUT_JSON = OUTPUT_DIR / "eu_last_6_periods.json"
TIMEOUT = 40
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,application/json;q=0.8,*/*;q=0.7",
    "Accept-Language": "en-GB,en;q=0.9",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1",
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
        "dataset": "prc_hicp_minr",
        "params": {"geo": "EA21", "coicop18": "TOT_X_NRG_FOOD", "unit": "RCH_A"},
        "frequency": "monthly",
        "expected_name": "Eurostat Eurozone Core MUICP YoY",
        "discovery_filters": {"geo": "EA21", "unit": "RCH_A"},
        "preferred": {"freq": "M", "unit": "RCH_A"},
        "dimension_label_keywords": {"coicop18": ["excluding energy", "food", "alcohol", "tobacco"]},
    },
    "euro_real_retail_yoy": {
        "label": "歐元區實質零售 YoY",
        "dataset": "sts_trtu_m",
        "params": {"geo": "EA21", "nace_r2": "G47", "indic_bt": "VOL_SLS", "s_adj": "CA", "unit": "PCH_SM"},
        "frequency": "monthly",
        "expected_name": "Eurostat Retail Sales Eurozone YoY",
        "discovery_filters": {"geo": "EA21", "nace_r2": "G47"},
        "preferred": {"freq": "M", "indic_bt": "VOL_SLS", "nace_r2": "G47", "s_adj": "CA", "unit": "PCH_SM"},
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
ALL_REMAINING = {
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



SOURCE_GROUPS = {
    "ine": {
        "url": "https://servicios.ine.es/wstempus/js/EN/OPERACIONES_DISPONIBLES",
        "series": {
            "spain_core_cpi_yoy": ["ipc", "subyacente"],
            "spain_unemployment_rate": ["encuesta de poblacion activa"],
            "spain_real_retail_yoy": ["comercio minorista"],
            "spain_gdp_yoy": ["contabilidad nacional trimestral"],
        },
    },
    "insee": {
        "url": "https://api.insee.fr/melodi/catalog/all",
        "accept_json": True,
        "series": {
            "france_cpi_ex_energy_yoy": ["prix a la consommation"],
            "france_unemployment_rate_ilo": ["chomage"],
            "france_consumer_confidence": ["confiance des menages"],
            "france_manufacturing_confidence": ["climat des affaires"],
            "france_business_confidence": ["climat des affaires"],
            "france_gdp_yoy": ["produit interieur brut"],
        },
    },
    "destatis": {
        "url": "https://www-genesis.destatis.de/genesisWS/rest/2020/find/find",
        "method": "POST",
        "base_params": {"username": "GAST", "password": "GAST", "language": "de", "category": "all", "pagelength": 100},
        "series": {
            "germany_core_cpi_yoy": ["verbraucherpreisindex", "ohne"],
            "germany_real_retail_mom": ["einzelhandel", "preisbereinigt"],
            "germany_industrial_production_yoy": ["produktionsindex", "industrie"],
            "germany_gdp_yoy": ["bruttoinlandsprodukt", "preisbereinigt"],
        },
    },
    "bundesbank_catalogue": {
        "url": "https://api.statistiken.bundesbank.de/rest/metadata/dataflow/BBK/BBDL1?references=all",
        "series": {
            "germany_unemployment_change_swda": ["unemployment", "change"],
        },
    },
    "spain_social_security": {
        "url": "https://www.seg-social.es/wps/portal/wss/internet/EstadisticasPresupuestosEstudios/Estadisticas",
        "series": {
            "spain_registered_employed_total_change": ["affiliation"],
        },
    },
    "nim_gfk": {
        "url": "https://www.nim.org/en/consumer-climate/all-releases",
        "series": {"germany_gfk_consumer_confidence": ["consumer climate"]},
    },
    "zew": {
        "url": "https://www.zew.de/en/publications/zew-expertises-research-reports/research-reports/business-cycle/zew-financial-market-survey",
        "series": {
            "germany_zew_current": ["current situation", "germany"],
            "germany_zew_expectations": ["economic sentiment", "germany"],
        },
    },
    "ifo": {
        "url": "https://www.ifo.de/en/ifo-time-series",
        "series": {"germany_ifo_business_climate": ["business climate"]},
    },
    "sp_global_pmi": {
        "url": "https://www.pmi.spglobal.com/Public/Release/PressReleases?language=en",
        "series": {
            "germany_manufacturing_pmi": ["germany", "manufacturing"],
            "france_manufacturing_pmi": ["france", "manufacturing"],
            "spain_manufacturing_pmi": ["spain", "manufacturing"],
            "germany_services_pmi": ["germany", "services"],
            "france_services_pmi": ["france", "services"],
            "spain_services_pmi": ["spain", "services"],
        },
    },
}


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.links: list[dict[str, str]] = []
        self._current_href = ""
        self._current_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "a":
            self._current_href = dict(attrs).get("href") or ""
            self._current_text = []

    def handle_data(self, data: str) -> None:
        clean = " ".join(data.split())
        if clean:
            self.parts.append(clean)
            if self._current_href:
                self._current_text.append(clean)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a" and self._current_href:
            self.links.append({
                "href": self._current_href,
                "text": " ".join(self._current_text),
            })
            self._current_href = ""
            self._current_text = []


def html_text(text: str) -> str:
    parser = _TextExtractor()
    parser.feed(text)
    return " ".join(parser.parts)


def _flatten_strings(value: Any) -> list[str]:
    output: list[str] = []
    if isinstance(value, dict):
        for child in value.values():
            output.extend(_flatten_strings(child))
    elif isinstance(value, list):
        for child in value:
            output.extend(_flatten_strings(child))
    elif isinstance(value, (str, int, float)):
        output.append(str(value))
    return output


def fetch_source_group(group_id: str, config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    params = dict(config.get("base_params", {}))
    if group_id == "sp_global_pmi":
        # Use the same browser-style session warm-up as the working UK pipeline.
        # Directly calling the release index with the debug bot UA was returning 403.
        request("https://www.pmi.spglobal.com/Public?language=en")
        time.sleep(1.0)
    request_headers = {"Accept": "application/json"} if config.get("accept_json") else None
    if config.get("method") == "POST":
        response = SESSION.post(
            config["url"], data=params or None, headers=request_headers, timeout=TIMEOUT
        )
        response.raise_for_status()
    else:
        response = request(config["url"], params=params or None, headers=request_headers)
    content_type = response.headers.get("Content-Type", "")
    is_json = "json" in content_type.lower() or response.text.lstrip().startswith(("{", "["))
    if is_json:
        payload: Any = response.json()
        searchable = " ".join(_flatten_strings(payload)).lower()
        raw_path = OUTPUT_DIR / f"raw_source_{group_id}.json"
        raw_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        payload = None
        parser = _TextExtractor()
        parser.feed(response.text)
        searchable = " ".join(parser.parts).lower()
        records = parser.links
        raw_path = OUTPUT_DIR / f"raw_source_{group_id}.html"
        raw_path.write_text(response.text, encoding="utf-8")

    results: dict[str, dict[str, Any]] = {}
    if is_json:
        records = payload if isinstance(payload, list) else []
    elif group_id == "sp_global_pmi":
        contextual_records: list[dict[str, str]] = []
        for match in re.finditer(
            r'href=["\']([^"\']*/Public/Home/PressRelease/[^"\']+)["\']',
            response.text,
            re.I,
        ):
            context_start = max(0, match.start() - 900)
            context_end = min(len(response.text), match.end() + 220)
            context_html = response.text[context_start:context_end]
            context_parser = _TextExtractor()
            context_parser.feed(context_html)
            context_text = " ".join(context_parser.parts)
            contextual_records.append({
                "href": requests.compat.urljoin(response.url, match.group(1)),
                "text": context_text,
            })
        records = contextual_records
        (OUTPUT_DIR / "raw_sp_global_contextual_links.json").write_text(
            json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    for series_id, keywords in config["series"].items():
        hits = [keyword for keyword in keywords if keyword.lower() in searchable]
        candidate_records = []
        for record in records:
            record_text = " ".join(_flatten_strings(record)).lower()
            if group_id == "sp_global_pmi":
                href = str(record.get("href", "")) if isinstance(record, dict) else ""
                same_record_match = all(keyword.lower() in record_text for keyword in keywords)
                if same_record_match and "/Public/Home/PressRelease/" in href:
                    candidate = dict(record)
                    candidate["match_score"] = sum(
                        record_text.rfind(keyword.lower()) for keyword in keywords
                    )
                    candidate_records.append(candidate)
            elif any(token.lower() in record_text for keyword in keywords for token in keyword.split()):
                candidate_records.append(record)
            if len(candidate_records) >= 15:
                break
        if group_id == "sp_global_pmi" and candidate_records:
            deduped: dict[str, dict[str, Any]] = {}
            for candidate in sorted(
                candidate_records,
                key=lambda item: item.get("match_score", -1),
                reverse=True,
            ):
                deduped.setdefault(candidate.get("href", ""), candidate)
            candidate_records = list(deduped.values())[:15]
        numbers = re.findall(r"(?<!\d)-?\d+(?:[.,]\d+)?(?!\d)", searchable)
        results[series_id] = {
            "status": (
                "candidate_links_found" if candidate_records else
                ("source_reachable" if hits else "source_reachable_no_keyword_match")
            ),
            "source_group": group_id,
            "source_url": response.url,
            "http_status": response.status_code,
            "matched_keywords": hits,
            "required_keywords": keywords,
            "candidate_records": candidate_records,
            "candidate_numbers_tail": numbers[-20:],
            "raw_file": str(raw_path),
            "data": [],
            "diagnostic": (
                "Official source reached; exact series/table and observation parser still required"
                if hits else
                "Official source reached, but expected keywords were not found in this response"
            ),
        }
    return results

def request(
    url: str,
    *,
    params: dict[str, str] | None = None,
    headers: dict[str, str] | None = None,
) -> requests.Response:
    for attempt in range(1, 4):
        print(f"[HTTP] {attempt}/3 {url} params={params}", flush=True)
        response = SESSION.get(url, params=params, headers=headers, timeout=TIMEOUT)
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



def write_all_series_summary(result: dict[str, Any]) -> None:
    rows: list[dict[str, Any]] = []
    for series_id, item in result.get("series", {}).items():
        data = item.get("data") or []
        latest = data[-1] if data else {}
        rows.append({
            "series_id": series_id,
            "definition": item.get("definition") or item.get("label") or "",
            "status": item.get("status", "unknown"),
            "source": item.get("source") or item.get("source_group") or "",
            "observation_count": len(data),
            "latest_period": latest.get("period"),
            "latest_value": latest.get("value"),
            "error": item.get("error", ""),
            "diagnostic": item.get("diagnostic", ""),
            "candidate_record_count": len(item.get("candidate_records") or []),
        })

    expected = set(EUROSTAT_SERIES) | set(BUNDESBANK_SERIES) | set(ALL_REMAINING)
    actual = {row["series_id"] for row in rows}
    missing = sorted(expected - actual)
    if missing:
        raise RuntimeError(f"Series missing from debug output: {missing}")

    (OUTPUT_DIR / "eu_all_series_debug_summary.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    with (OUTPUT_DIR / "eu_all_series_debug_summary.csv").open(
        "w", encoding="utf-8-sig", newline=""
    ) as handle:
        fieldnames = list(rows[0]) if rows else []
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("\n[ALL SERIES DEBUG SUMMARY]", flush=True)
    for row in rows:
        print(
            f"{row['series_id']} | {row['status']} | obs={row['observation_count']} | "
            f"latest={row['latest_period']} {row['latest_value']} | source={row['source']}",
            flush=True,
        )
    print(f"[ALL SERIES DEBUG SUMMARY] total={len(rows)} missing=0", flush=True)

def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    result: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scope": "official-source diagnostic; latest 6 available periods",
        "important_note": "Spain, France and Germany CPI must use national CPI, not HICP. Euro-area latest data use geo=EA21 from 2026; fallback queries also test EA and EA20 for continuity. All 31 series are actively diagnosed; national CPI definitions are not substituted with HICP.",
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

    probed_ids: set[str] = set()
    for group_id, config in SOURCE_GROUPS.items():
        print(f"[SOURCE PROBE] {group_id}", flush=True)
        try:
            group_results = fetch_source_group(group_id, config)
            for series_id, item in group_results.items():
                result["series"][series_id] = {
                    "definition": ALL_REMAINING[series_id],
                    **item,
                }
                probed_ids.add(series_id)
        except Exception as error:
            for series_id in config["series"]:
                result["series"][series_id] = {
                    "definition": ALL_REMAINING[series_id],
                    "status": "source_error",
                    "source_group": group_id,
                    "source_url": config["url"],
                    "error": str(error),
                    "data": [],
                }
                probed_ids.add(series_id)

    for series_id, definition in ALL_REMAINING.items():
        if series_id not in probed_ids:
            result["series"][series_id] = {
                "status": "source_not_configured",
                "definition": definition,
                "data": [],
            }

    write_all_series_summary(result)

    OUTPUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\n[SUMMARY]", flush=True)
    for series_id, item in result["series"].items():
        print(series_id, item["status"], len(item.get("data", [])), flush=True)
    print(f"\nSaved: {OUTPUT_JSON}", flush=True)


if __name__ == "__main__":
    main()
