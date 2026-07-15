import json
import re
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup


BLS_URL = "https://www.bls.gov/news.release/cpi.t02.htm"

OUTPUT_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "cpi_table2.json"
)


def clean_text(value):
    """整理表格文字與多餘空白。"""
    if value is None:
        return ""

    text = str(value)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def flatten_column(column):
    """
    BLS 表格可能包含多層表頭。
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
    """避免合併表頭後出現重複欄位名稱。"""
    result = []
    counter = {}

    for column in columns:
        base_name = column or "column"

        if base_name not in counter:
            counter[base_name] = 1
            result.append(base_name)
        else:
            counter[base_name] += 1
            result.append(f"{base_name}_{counter[base_name]}")

    return result


def get_release_title(html):
    """讀取 BLS 頁面標題。"""
    soup = BeautifulSoup(html, "html.parser")

    heading = soup.find("h1")

    if heading:
        return clean_text(heading.get_text(" ", strip=True))

    if soup.title:
        return clean_text(soup.title.get_text(" ", strip=True))

    return "BLS CPI Table 2"


def get_reference_period(html):
    """
    從頁面文字中嘗試擷取資料月份，例如 June 2026。
    若擷取不到，回傳空字串。
    """
    soup = BeautifulSoup(html, "html.parser")
    page_text = clean_text(soup.get_text(" ", strip=True))

    month_pattern = (
        r"\b("
        r"January|February|March|April|May|June|"
        r"July|August|September|October|November|December"
        r")\s+\d{4}\b"
    )

    matches = re.findall(month_pattern, page_text)

    full_matches = re.findall(month_pattern.replace("(", "(?:"), page_text)

    if full_matches:
        return full_matches[0]

    date_match = re.search(
        r"\b(?:January|February|March|April|May|June|"
        r"July|August|September|October|November|December)"
        r"\s+\d{4}\b",
        page_text,
    )

    return date_match.group(0) if date_match else ""


def fetch_bls_html():
    """向 BLS 下載 CPI Table 2 HTML。"""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (compatible; EconomicDataDashboard/1.0; "
            "+https://github.com/bruce851117/economic-data-dashboard)"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }

    response = requests.get(
        BLS_URL,
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()

    return response.text


def parse_cpi_table(html):
    """解析 BLS CPI Table 2。"""
    tables = pd.read_html(StringIO(html))

    if not tables:
        raise RuntimeError("BLS 頁面中找不到任何 HTML 表格。")

    selected_table = None

    for table in tables:
        first_column_text = " ".join(
            clean_text(value)
            for value in table.iloc[:, 0].head(20).tolist()
        )

        if "All items" in first_column_text and "Food" in first_column_text:
            selected_table = table
            break

    if selected_table is None:
        selected_table = max(tables, key=lambda table: len(table.index))

    selected_table.columns = make_unique_columns(
        [flatten_column(column) for column in selected_table.columns]
    )

    selected_table = selected_table.fillna("")

    rows = []

    for _, row in selected_table.iterrows():
        record = {
            clean_text(column): clean_text(value)
            for column, value in row.items()
        }

        first_value = next(iter(record.values()), "")

        if not first_value:
            continue

        rows.append(record)

    if not rows:
        raise RuntimeError("成功找到 BLS 表格，但解析後沒有任何資料。")

    return list(selected_table.columns), rows


def save_json(title, reference_period, columns, rows):
    """將 CPI 資料儲存成 JSON。"""
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "source": "U.S. Bureau of Labor Statistics",
        "source_url": BLS_URL,
        "title": title,
        "reference_period": reference_period,
        "updated_at_utc": datetime.now(timezone.utc).isoformat(),
        "columns": columns,
        "row_count": len(rows),
        "data": rows,
    }

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(
            payload,
            file,
            ensure_ascii=False,
            indent=2,
        )

    print(f"Saved {len(rows)} rows to {OUTPUT_PATH}")
    print(f"Reference period: {reference_period or 'Not detected'}")


def main():
    print(f"Fetching BLS CPI data from: {BLS_URL}")

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
