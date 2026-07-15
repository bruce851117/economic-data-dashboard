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

