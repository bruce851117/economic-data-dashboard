from __future__ import annotations

import csv
import io
import json
import re
import sys
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

OUTPUT_DIR = Path("uk_macro_test_output")
RAW_DIR = OUTPUT_DIR / "raw"
PARSED_DIR = OUTPUT_DIR / "parsed"
REPORT_FILE = OUTPUT_DIR / "report.json"
TAIPEI_TZ = timezone(timedelta(hours=8))
USER_AGENT = "Mozilla/5.0 (compatible; economic-data-dashboard-test/1.0)"
TIMEOUT = 60

# 先抓完整官方資料集，再以關鍵字尋找候選序列；測試階段避免因猜錯CDID而漏資料。
ONS_DATASETS = {
    "inflation_mm23": {
        "url": "https://www.ons.gov.uk/file?uri=/economy/inflationandpriceindices/datasets/consumerpriceindices/current/mm23.csv",
        "keywords": [
            ["CPI", "excluding", "energy", "food", "alcohol", "tobacco", "annual"],
            ["CPI", "services", "annual"],
        ],
    },
    "labour_a01": {
        "url": "https://www.ons.gov.uk/file?uri=/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/datasets/summaryoflabourmarketstatistics/current/a01jun2026.xls",
        "keywords": [["unemployment rate"], ["vacancies"], ["average weekly earnings"]],
    },
    "labour_unem": {
        "url": "https://www.ons.gov.uk/file?uri=/employmentandlabourmarket/peoplenotinwork/unemployment/datasets/claimantcountandvacanciesdataset/current/unem.csv",
        "keywords": [["claimant count rate"], ["vacancies"]],
    },
    "earnings_earn01": {
        "url": "https://www.ons.gov.uk/file?uri=/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/averageweeklyearningsearn01/current/earn01.csv",
        "keywords": [
            ["average weekly earnings", "regular pay"],
            ["private sector", "regular pay"],
            ["private sector", "total pay"],
        ],
    },
    "monthly_gdp_mgdp": {
        "url": "https://www.ons.gov.uk/file?uri=/economy/grossdomesticproductgdp/datasets/gdpmonthlyestimateuktimeseriesdataset/current/mgdp.csv",
        "keywords": [["GDP", "month on month"], ["GDP", "three months"], ["GDP", "year on year"]],
    },
    "quarterly_gdp_qna": {
        "url": "https://www.ons.gov.uk/file?uri=/economy/grossdomesticproductgdp/datasets/quarterlynationalaccounts/current/qna.csv",
        "keywords": [
            ["gross domestic product", "quarter on quarter"],
            ["household final consumption expenditure", "quarter on quarter"],
            ["gross fixed capital formation", "quarter on quarter"],
            ["business investment", "quarter on quarter"],
            ["domestic demand"],
        ],
    },
}

# 已知可直接測試的ONS單一時間序列。若其中某一代碼失效，報告會保留錯誤，不中止。
ONS_SERIES = {
    "headline_cpi_yoy": ("d7g7", "mm23"),
    "unemployment_rate_3m": ("mgsx", "lms"),
    "household_consumption_level": ("abjr", "pn2"),
    "household_consumption_qoq": ("zz5m", "qna"),
    "quarterly_gdp_qoq": ("ihyq", "pn2"),
    "quarterly_gdp_yoy": ("ihyp", "pn2"),
}

DBNOMICS_SEARCHES = {
    "uk_pmi_exact_search": "United Kingdom S&P Global manufacturing PMI services PMI",
    "uk_oecd_bci_proxy": "United Kingdom OECD business confidence index",
    "uk_business_survey_proxy": "United Kingdom business confidence survey",
}

BOE_PAGES = {
    "inflation_attitudes": "https://www.bankofengland.co.uk/statistics/research-datasets",
    "dmp_latest": "https://www.bankofengland.co.uk/decision-maker-panel",
}

PRIVATE_SURVEY_PAGES = {
    "gfk_consumer_confidence": "https://nielseniq.com/global/en/landing-page/consumer-confidence-barometer/",
    "sp_global_pmi_home": "https://www.pmi.spglobal.com/",
}


def now_iso() -> str:
    return datetime.now(TAIPEI_TZ).isoformat()


def request(url: str, accept: str = "*/*") -> dict[str, Any]:
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": accept, "Accept-Language": "en-GB,en;q=0.9"})
    started = time.time()
    try:
        with urlopen(req, timeout=TIMEOUT) as response:
            body = response.read()
            charset = response.headers.get_content_charset() or "utf-8"
            return {
                "ok": True,
                "url": url,
                "final_url": response.geturl(),
                "status": response.status,
                "content_type": response.headers.get("Content-Type", ""),
                "bytes": len(body),
                "elapsed": round(time.time() - started, 3),
                "body": body,
                "text": body.decode(charset, errors="replace"),
            }
    except (HTTPError, URLError, TimeoutError, OSError) as exc:
        return {"ok": False, "url": url, "status": getattr(exc, "code", None), "error": f"{type(exc).__name__}: {exc}", "bytes": 0, "body": b"", "text": ""}


def save_response(name: str, response: dict[str, Any]) -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    suffix = ".json" if "json" in response.get("content_type", "").lower() else ".txt"
    if "spreadsheet" in response.get("content_type", "").lower() or response.get("body", b"")[:2] == b"PK":
        suffix = ".xlsx"
    elif response.get("body", b"")[:8] == bytes.fromhex("D0CF11E0A1B11AE1"):
        suffix = ".xls"
    (RAW_DIR / f"{name}{suffix}").write_bytes(response.get("body", b""))


def response_meta(response: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in response.items() if k not in {"body", "text"}}


def normalize(value: Any) -> str:
    return " ".join(str(value or "").replace("\ufeff", "").split()).strip()


def ons_series_csv(cdid: str, dataset: str) -> str:
    return f"https://www.ons.gov.uk/generator?format=csv&uri=/economy/{'inflationandpriceindices' if dataset == 'mm23' else 'grossdomesticproductgdp'}/timeseries/{cdid}/{dataset}"


def parse_ons_generator_csv(text: str, months: int = 13) -> dict[str, Any]:
    rows = list(csv.reader(io.StringIO(text)))
    metadata: dict[str, str] = {}
    observations: list[dict[str, Any]] = []
    for row in rows:
        if len(row) >= 2 and row[0] and row[1] and not re.match(r"^(\d{4}|[A-Z]{3}|Q[1-4])", row[0].strip()):
            metadata[normalize(row[0])] = normalize(row[1])
        if len(row) >= 2:
            period = normalize(row[0])
            value = normalize(row[1]).replace(",", "")
            if re.search(r"\d{4}", period) and re.fullmatch(r"-?\d+(?:\.\d+)?", value):
                observations.append({"period": period, "value": float(value)})
    return {"metadata": metadata, "observations_last": observations[-months:]}


def keyword_score(text: str, keywords: list[str]) -> int:
    low = text.lower()
    return sum(1 for keyword in keywords if keyword.lower() in low)


def scan_text_dataset(text: str, keyword_groups: list[list[str]]) -> list[dict[str, Any]]:
    lines = [normalize(line) for line in text.splitlines() if normalize(line)]
    matches: list[dict[str, Any]] = []
    for group in keyword_groups:
        candidates = []
        for idx, line in enumerate(lines):
            score = keyword_score(line, group)
            if score:
                context = " | ".join(lines[max(0, idx - 1): min(len(lines), idx + 2)])[:1200]
                candidates.append({"score": score, "keywords": group, "line": line[:700], "context": context})
        candidates.sort(key=lambda row: (-row["score"], len(row["line"])))
        matches.extend(candidates[:12])
    return matches


def test_ons_series(report: dict[str, Any]) -> None:
    report["ons_series"] = {}
    for name, (cdid, dataset) in ONS_SERIES.items():
        if dataset == "lms":
            url = f"https://www.ons.gov.uk/generator?format=csv&uri=/employmentandlabourmarket/peoplenotinwork/unemployment/timeseries/{cdid}/lms"
        else:
            url = ons_series_csv(cdid, dataset)
        response = request(url, "text/csv,*/*")
        save_response(f"ons_series_{name}", response)
        entry = response_meta(response)
        if response["ok"]:
            try:
                parsed = parse_ons_generator_csv(response["text"])
                entry["parsed"] = parsed
                PARSED_DIR.mkdir(parents=True, exist_ok=True)
                (PARSED_DIR / f"ons_series_{name}.json").write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8")
            except Exception as exc:
                entry["parse_error"] = f"{type(exc).__name__}: {exc}"
        report["ons_series"][name] = entry


def test_ons_datasets(report: dict[str, Any]) -> None:
    report["ons_datasets"] = {}
    for name, config in ONS_DATASETS.items():
        response = request(config["url"])
        save_response(f"ons_dataset_{name}", response)
        entry = response_meta(response)
        if response["ok"]:
            if response.get("content_type", "").lower().find("text") >= 0 or response["body"][:2] not in {b"PK"}:
                entry["keyword_candidates"] = scan_text_dataset(response["text"], config["keywords"])
            else:
                entry["note"] = "Binary spreadsheet downloaded; inspect artifact or add openpyxl/xlrd parser after confirming workbook layout."
        report["ons_datasets"][name] = entry


def test_ons_retail_api(report: dict[str, Any]) -> None:
    # 先探勘最新版metadata；正式版再依据回传dimensions构造精确observation/filter请求。
    urls = [
        "https://api.beta.ons.gov.uk/v1/datasets/retail-sales-index",
        "https://api.beta.ons.gov.uk/v1/datasets/retail-sales-index/editions/time-series/versions/latest",
    ]
    report["ons_retail_api"] = []
    for idx, url in enumerate(urls, 1):
        response = request(url, "application/json")
        save_response(f"ons_retail_api_{idx}", response)
        entry = response_meta(response)
        if response["ok"]:
            try:
                entry["json"] = json.loads(response["text"])
            except json.JSONDecodeError as exc:
                entry["parse_error"] = str(exc)
        report["ons_retail_api"].append(entry)


def test_boe_pages(report: dict[str, Any]) -> None:
    report["boe"] = {}
    for name, url in BOE_PAGES.items():
        response = request(url, "text/html,*/*")
        save_response(f"boe_{name}", response)
        entry = response_meta(response)
        if response["ok"]:
            links = re.findall(r'href=["\']([^"\']+\.(?:xlsx|xls|csv)(?:\?[^"\']*)?)["\']', response["text"], flags=re.I)
            entry["data_links"] = links[:30]
            entry["one_year_inflation_mentions"] = re.findall(r'.{0,120}(?:year.ahead|coming year|12 months).{0,220}', normalize(response["text"]), flags=re.I)[:10]
        report["boe"][name] = entry


def test_private_surveys(report: dict[str, Any]) -> None:
    report["private_surveys"] = {}
    for name, url in PRIVATE_SURVEY_PAGES.items():
        response = request(url, "text/html,*/*")
        save_response(name, response)
        entry = response_meta(response)
        if response["ok"]:
            visible = normalize(re.sub(r"(?s)<[^>]+>", " ", response["text"]))
            entry["value_candidates"] = re.findall(r'.{0,100}(?:PMI|Consumer Confidence|Overall Index).{0,180}', visible, flags=re.I)[:30]
        report["private_surveys"][name] = entry


def test_dbnomics(report: dict[str, Any]) -> None:
    report["dbnomics"] = {}
    for name, query_text in DBNOMICS_SEARCHES.items():
        url = "https://api.db.nomics.world/v22/series/" + "?" + urlencode({"q": query_text, "limit": 50})
        # Search endpoint compatibility fallback is recorded if this endpoint changes.
        response = request(url, "application/json")
        if not response["ok"]:
            url = "https://api.db.nomics.world/v22/series/" + "?" + urlencode({"q": query_text})
            response = request(url, "application/json")
        save_response(f"dbnomics_{name}", response)
        entry = response_meta(response)
        if response["ok"]:
            try:
                payload = json.loads(response["text"])
                entry["top_level_keys"] = list(payload) if isinstance(payload, dict) else []
                entry["preview"] = json.dumps(payload, ensure_ascii=False)[:5000]
            except json.JSONDecodeError as exc:
                entry["parse_error"] = str(exc)
        report["dbnomics"][name] = entry


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    report: dict[str, Any] = {
        "generated_at": now_iso(),
        "purpose": "Explore free UK macro sources and retrieve/identify approximately the latest year of data.",
        "notes": [
            "This is a discovery test, not the production updater.",
            "ONS and BoE are authoritative. GfK and S&P Global are private datasets; public pages may expose only current releases.",
            "PMI proxies are not identical to S&P Global PMI and must not be labelled as PMI.",
        ],
    }
    tests = [test_ons_series, test_ons_datasets, test_ons_retail_api, test_boe_pages, test_private_surveys, test_dbnomics]
    for test in tests:
        print(f"Running {test.__name__}...")
        try:
            test(report)
        except Exception as exc:
            report.setdefault("test_errors", []).append({"test": test.__name__, "error": f"{type(exc).__name__}: {exc}"})
    REPORT_FILE.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {REPORT_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
