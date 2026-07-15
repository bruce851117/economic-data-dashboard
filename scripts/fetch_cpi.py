import json
import os
import re
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup


BLS_SOURCE_URL = (
    "https://www.bls.gov/news.release/cpi.t02.htm"
)

OUTPUT_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "cpi_table2.json"
)


def clean_text(value):
    """
    清除換行、Tab、多餘空白與 pandas NaN。
    """
    if value is None:
        return ""

    text = str(value)

    if text.lower() == "nan":
        return ""

    return re.sub(r"\s+", " ", text).strip()


def flatten_column(column):
    """
    將 BLS 的多層表頭合併為單一欄位名稱。
    """
    if not isinstance(column, tuple):
        return clean_text(column)

    parts = []

    for part in column:
        cleaned_part = clean_text(part)

        if not cleaned_part:
            continue

        if cleaned_part.lower().startswith("unnamed"):
            continue

        if cleaned_part not in parts:
            parts.append(cleaned_part)

    return " | ".join(parts)


def make_unique_columns(columns):
    """
    避免欄位名稱重複。
    """
    result = []
    counts = {}

    for column in columns:
        base_name = clean_text(column) or "column"

        counts[base_name] = counts.get(base_name, 0) + 1

        if counts[base_name] == 1:
            result.append(base_name)
        else:
            result.append(
                f"{base_name}_{counts[base_name]}"
            )

    return result


def fetch_bls_html():
    """
    透過 Cloudflare Worker 代理取得 BLS CPI HTML。

    GitHub Actions 不直接連線 BLS。
    """
    proxy_url = os.environ.get(
        "BLS_PROXY_URL",
        "",
    ).strip()

    proxy_key = os.environ.get(
        "BLS_PROXY_KEY",
        "",
    ).strip()

    if not proxy_url:
        raise RuntimeError(
            "Missing GitHub Secret: BLS_PROXY_URL"
        )

    if not proxy_key:
        raise RuntimeError(
            "Missing GitHub Secret: BLS_PROXY_KEY"
        )

    print("=" * 70)
    print("Using Cloudflare Worker proxy.")
    print(f"Fetching CPI through proxy: {proxy_url}")

    response = requests.get(
        proxy_url,
        headers={
            "X-Proxy-Key": proxy_key,
            "Accept": "text/html",
            "User-Agent": (
                "EconomicDataDashboard/1.0 "
                "GitHub-Actions"
            ),
        },
        timeout=60,
    )

    print(f"Proxy HTTP status: {response.status_code}")
    print(
        f"Response length: {len(response.content)} bytes"
    )

    if response.status_code != 200:
        response_preview = response.text[:3000]

        raise RuntimeError(
            "Cloudflare Worker request failed.\n"
            f"HTTP status: {response.status_code}\n"
            f"Response:\n{response_preview}"
        )

    html = response.text

    if len(html) < 1000:
        raise RuntimeError(
            "Cloudflare Worker response was too short: "
            f"{len(html)} characters."
        )

    required_phrases = [
        "All items",
        "Food",
        "Energy",
    ]

    missing_phrases = [
        phrase
        for phrase in required_phrases
        if phrase.lower() not in html.lower()
    ]

    if missing_phrases:
        raise RuntimeError(
            "Cloudflare Worker returned HTML, but "
            "the expected CPI content was missing: "
            + ", ".join(missing_phrases)
        )

    print("BLS CPI HTML downloaded through Worker.")
    print("=" * 70)

    return html


def get_release_title(html):
    """
    從 BLS HTML 擷取標題。
    """
    soup = BeautifulSoup(html, "html.parser")

    heading = soup.find("h1")

    if heading:
        return clean_text(
            heading.get_text(" ", strip=True)
        )

    if soup.title:
        return clean_text(
            soup.title.get_text(" ", strip=True)
        )

    return "BLS CPI Table 2"


def get_reference_period(html):
    """
    擷取資料月份，例如 June 2026。
    """
    soup = BeautifulSoup(html, "html.parser")

    page_text = clean_text(
        soup.get_text(" ", strip=True)
    )

    pattern = (
        r"\b(?:"
        r"January|February|March|April|May|June|"
        r"July|August|September|October|November|December"
        r")\s+\d{4}\b"
    )

    match = re.search(
        pattern,
        page_text,
        flags=re.IGNORECASE,
    )

    if not match:
        return ""

    return match.group(0)


def select_cpi_table(tables):
    """
    從所有 HTML 表格中找出 CPI Table 2。
    """
    candidates = []

    for index, table in enumerate(tables):
        if table.empty:
            continue

        table_text = " ".join(
            clean_text(value)
            for value in table.astype(str).values.flatten()
        )

        score = 0

        if "All items" in table_text:
            score += 5

        if "Food" in table_text:
            score += 2

        if "Energy" in table_text:
            score += 2

        if "All items less food and energy" in table_text:
            score += 5

        if len(table.index) >= 50:
            score += 2

        candidates.append(
            {
                "index": index,
                "score": score,
                "rows": len(table.index),
                "table": table,
            }
        )

    if not candidates:
        raise RuntimeError(
            "No usable HTML tables were found."
        )

    candidates.sort(
        key=lambda item: (
            item["score"],
            item["rows"],
        ),
        reverse=True,
    )

    selected = candidates[0]

    print(f"Selected table index: {selected['index']}")
    print(f"Selected table score: {selected['score']}")
    print(f"Selected table rows: {selected['rows']}")

    if selected["score"] < 5:
        raise RuntimeError(
            "HTML tables were found, but none matched "
            "the expected CPI Table 2 structure."
        )

    return selected["table"]


def parse_cpi_table(html):
    """
    將 BLS CPI Table 2 解析成 JSON 資料。
    """
    try:
        tables = pd.read_html(
            StringIO(html)
        )
    except ValueError as error:
        raise RuntimeError(
            "BLS HTML was downloaded, but no HTML "
            "tables could be parsed."
        ) from error

    if not tables:
        raise RuntimeError(
            "The BLS HTML contains no tables."
        )

    print(f"Found {len(tables)} HTML table(s).")

    table = select_cpi_table(tables)

    table.columns = make_unique_columns(
        [
            flatten_column(column)
            for column in table.columns
        ]
    )

    table = table.fillna("")

    columns = [
        clean_text(column)
        for column in table.columns
    ]

    rows = []

    for _, row in table.iterrows():
        record = {
            clean_text(column): clean_text(value)
            for column, value in row.items()
        }

        first_value = next(
            iter(record.values()),
            "",
        )

        if not first_value:
            continue

        if first_value.lower() in {
            "expenditure category",
            "item",
        }:
            continue

        rows.append(record)

    if not rows:
        raise RuntimeError(
            "The CPI table was found, but no rows "
            "were parsed."
        )

    all_rows_text = json.dumps(
        rows,
        ensure_ascii=False,
    )

    required_items = [
        "All items",
        "Food",
        "Energy",
        "All items less food and energy",
    ]

    missing_items = [
        item
        for item in required_items
        if item not in all_rows_text
    ]

    if missing_items:
        raise RuntimeError(
            "Parsed CPI data is missing required items: "
            + ", ".join(missing_items)
        )

    return columns, rows


def load_existing_payload():
    """
    讀取現有的 CPI JSON。
    """
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
    title,
    reference_period,
    columns,
    rows,
):
    """
    儲存 CPI JSON。

    如果 CPI 欄位和資料內容沒有改變，
    保留原本更新時間，避免無意義 Commit。
    """
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
        old_columns = existing.get(
            "columns",
            [],
        )
        old_rows = existing.get(
            "data",
            [],
        )

        if old_columns == columns and old_rows == rows:
            data_changed = False
            updated_at_utc = existing.get(
                "updated_at_utc",
                updated_at_utc,
            )

    payload = {
        "source": "U.S. Bureau of Labor Statistics",
        "source_url": BLS_SOURCE_URL,
        "title": title,
        "reference_period": reference_period,
        "updated_at_utc": updated_at_utc,
        "data_changed": data_changed,
        "columns": columns,
        "row_count": len(rows),
        "data": rows,
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

    print("=" * 70)
    print(f"Saved {len(rows)} CPI rows.")
    print(f"Output path: {OUTPUT_PATH}")
    print(
        "Reference period:",
        reference_period or "Not detected",
    )
    print(f"Data changed: {data_changed}")
    print("=" * 70)


def main():
    print("Starting BLS CPI update through Cloudflare Worker.")
    print(f"Official source: {BLS_SOURCE_URL}")

    html = fetch_bls_html()

    title = get_release_title(html)

    reference_period = get_reference_period(html)

    columns, rows = parse_cpi_table(html)

    save_json(
        title=title,
        reference_period=reference_period,
        columns=columns,
        rows=rows,
    )


if __name__ == "__main__":
    main()
