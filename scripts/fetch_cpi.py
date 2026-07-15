import json
import re
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup


# 顯示於輸出 JSON 的官方原始資料網址
BLS_URL = "https://www.bls.gov/news.release/cpi.t02.htm"

# GitHub Actions 執行後的 JSON 輸出位置
OUTPUT_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "cpi_table2.json"
)


def clean_text(value):
    """
    清除換行、Tab 與多餘空白。
    """
    if value is None:
        return ""

    text = str(value)

    if text.lower() == "nan":
        return ""

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def flatten_column(column):
    """
    BLS 表格使用多層表頭。
    將多層表頭合併成單一欄位名稱。
    """
    if isinstance(column, tuple):
        parts = []

        for part in column:
            part = clean_text(part)

            if not part:
                continue

            if part.lower().startswith("unnamed"):
                continue

            if part not in parts:
                parts.append(part)

        return " | ".join(parts)

    return clean_text(column)


def make_unique_columns(columns):
    """
    防止合併多層表頭後產生重複欄位名稱。
    """
    result = []
    counter = {}

    for column in columns:
        base_name = column or "column"

        if base_name not in counter:
            counter[base_name] = 1
            result.append(base_name)
        else:
            counter[base_name] += 1
            result.append(
                f"{base_name}_{counter[base_name]}"
            )

    return result


def get_release_title(html):
    """
    從 BLS 頁面擷取標題。
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
    從頁面內容擷取資料所屬月份，例如 June 2026。
    """
    soup = BeautifulSoup(html, "html.parser")

    page_text = clean_text(
        soup.get_text(" ", strip=True)
    )

    month_pattern = (
        r"\b(?:"
        r"January|February|March|April|May|June|"
        r"July|August|September|October|November|December"
        r")\s+\d{4}\b"
    )

    date_match = re.search(
        month_pattern,
        page_text,
        flags=re.IGNORECASE,
    )

    if date_match:
        return date_match.group(0)

    return ""


def fetch_bls_html():
    """
    向 BLS 下載 CPI Table 2。

    GitHub Actions 的資料中心 IP 可能被 www.bls.gov 阻擋，
    因此優先嘗試 BLS 官方列印版網址，再嘗試一般網址。
    """
    candidate_urls = [
        (
            "https://data.bls.gov/cgi-bin/print.pl/"
            "news.release/cpi.t02.htm"
        ),
        "https://www.bls.gov/news.release/cpi.t02.htm",
    ]

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,"
            "application/xml;q=0.9,"
            "image/avif,image/webp,*/*;q=0.8"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Referer": "https://www.bls.gov/",
    }

    session = requests.Session()
    session.headers.update(headers)

    errors = []

    for url in candidate_urls:
        try:
            print("=" * 60)
            print(f"Trying BLS URL: {url}")

            response = session.get(
                url,
                timeout=45,
                allow_redirects=True,
            )

            print(
                f"HTTP status: {response.status_code}"
            )
            print(f"Final URL: {response.url}")
            print(
                "Response length:",
                len(response.content),
                "bytes",
            )

            if response.status_code == 403:
                errors.append(
                    f"{url}: HTTP 403 Forbidden"
                )
                continue

            response.raise_for_status()

            html = response.text

            if len(html) < 1000:
                errors.append(
                    f"{url}: response was unexpectedly short "
                    f"({len(html)} characters)"
                )
                continue

            if "All items" not in html:
                errors.append(
                    f"{url}: downloaded HTML did not contain "
                    "'All items'"
                )
                continue

            print(
                "Successfully downloaded BLS CPI data."
            )
            print("=" * 60)

            return html

        except requests.RequestException as error:
            errors.append(
                f"{url}: {type(error).__name__}: {error}"
            )

    error_details = "\n".join(
        f"- {error}"
        for error in errors
    )

    raise RuntimeError(
        "Unable to download CPI Table 2 from all "
        "available BLS URLs.\n"
        f"{error_details}"
    )


def select_cpi_table(tables):
    """
    從網頁內所有 HTML 表格中找出 CPI Table 2。
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
            score += 4

        if "Food" in table_text:
            score += 2

        if "Energy" in table_text:
            score += 2

        if "All items less food and energy" in table_text:
            score += 4

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
            "No usable HTML tables were found "
            "on the BLS page."
        )

    candidates.sort(
        key=lambda item: (
            item["score"],
            item["rows"],
        ),
        reverse=True,
    )

    selected = candidates[0]

    print(
        "Selected HTML table:",
        selected["index"],
    )
    print(
        "Selected table score:",
        selected["score"],
    )
    print(
        "Selected table rows:",
        selected["rows"],
    )

    if selected["score"] < 4:
        raise RuntimeError(
            "HTML tables were found, but none appeared "
            "to be CPI Table 2."
        )

    return selected["table"]


def parse_cpi_table(html):
    """
    將 BLS CPI Table 2 轉成可輸出至 JSON 的資料。
    """
    try:
        tables = pd.read_html(
            StringIO(html)
        )
    except ValueError as error:
        raise RuntimeError(
            "BLS HTML was downloaded, but no table "
            "could be parsed."
        ) from error

    if not tables:
        raise RuntimeError(
            "BLS page did not contain any HTML tables."
        )

    print(
        f"Found {len(tables)} HTML table(s)."
    )

    selected_table = select_cpi_table(tables)

    selected_table.columns = make_unique_columns(
        [
            flatten_column(column)
            for column in selected_table.columns
        ]
    )

    selected_table = selected_table.fillna("")

    columns = [
        clean_text(column)
        for column in selected_table.columns
    ]

    rows = []

    for _, row in selected_table.iterrows():
        record = {}

        for column, value in row.items():
            column_name = clean_text(column)
            cleaned_value = clean_text(value)

            record[column_name] = cleaned_value

        first_value = next(
            iter(record.values()),
            "",
        )

        if not first_value:
            continue

        # 移除表頭被 pandas 重複解析成資料列的情況
        if first_value.lower() in {
            "expenditure category",
            "item",
        }:
            continue

        rows.append(record)

    if not rows:
        raise RuntimeError(
            "CPI table was found, but no data rows "
            "were successfully parsed."
        )

    row_text = " ".join(
        str(record)
        for record in rows
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
        if item not in row_text
    ]

    if missing_items:
        raise RuntimeError(
            "Parsed table is missing required CPI items: "
            + ", ".join(missing_items)
        )

    return columns, rows


def save_json(
    title,
    reference_period,
    columns,
    rows,
):
    """
    將結果儲存成 data/cpi_table2.json。
    """
    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    payload = {
        "source": (
            "U.S. Bureau of Labor Statistics"
        ),
        "source_url": BLS_URL,
        "title": title,
        "reference_period": reference_period,
        "updated_at_utc": (
            datetime.now(timezone.utc).isoformat()
        ),
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

    print("=" * 60)
    print(
        f"Saved {len(rows)} rows to:"
    )
    print(OUTPUT_PATH)
    print(
        "Reference period:",
        reference_period or "Not detected",
    )
    print("=" * 60)


def main():
    print(
        f"Fetching BLS CPI data from: {BLS_URL}"
    )

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
