#!/usr/bin/env python3
"""Build data/us_macro.json (the reference/standard answer) from US_ECON.xlsx.

Layout of US_ECON.xlsx (sheet "Sheet1"):
  row 0 : ["","","", <date>, <date>, ...]  dates descending from newest
  row N : [section, name, ticker, v_newest, ..., v_oldest]

Output schema matches the other countries (uk/eu/au):
  {generated_at, source, blocks:[{id,title,color,series:[ids]}], series:[{id,block,name,ticker,frequency,color,data:[{date,value}]}]}
"""
from __future__ import annotations
import json, re, sys, unicodedata
from datetime import datetime, timezone
from pathlib import Path
import openpyxl

ROOT = Path(__file__).resolve().parent.parent
XLSX = ROOT / "US_ECON.xlsx"
OUT = ROOT / "data" / "us_macro.json"

# xlsx display name -> canonical fetch name (must equal SPEC section|name in fetch_us_macro_table.py)
NAME_ALIASES = {
    ("消費", "CB (Consumer Confidence)"): "CB",
    ("消費", "密大 (sentiment)"): "密大",
}

BLOCK_COLORS = ["#2563eb", "#16a34a", "#7c3aed", "#ea580c", "#0891b2",
                "#dc2626", "#0d9488", "#9333ea", "#c026d3", "#65a30d"]


def num(x):
    if x is None:
        return None
    if isinstance(x, (int, float)):
        return x
    s = str(x).replace(",", "").replace("%", "").strip()
    if s == "" or s.upper() in {"N/A", "NA", "#N/A"}:
        return None
    try:
        f = float(s)
        return int(f) if f == int(f) else round(f, 6)
    except ValueError:
        return None


def slug(ticker: str) -> str:
    t = ticker.strip()
    t = re.sub(r"\s+index$", "", t, flags=re.I)
    t = unicodedata.normalize("NFKD", t)
    t = re.sub(r"[^A-Za-z0-9]+", "_", t).strip("_").lower()
    return t or "series"


def month_key(dt) -> str | None:
    if isinstance(dt, datetime):
        return f"{dt.year:04d}-{dt.month:02d}-01"
    m = re.search(r"(\d{4})-(\d{2})", str(dt))
    return f"{m.group(1)}-{m.group(2)}-01" if m else None


def main():
    wb = openpyxl.load_workbook(XLSX, data_only=True, read_only=True)
    ws = wb["Sheet1"]
    rows = list(ws.iter_rows(values_only=True))
    header = rows[0]
    date_cols = [(i, month_key(header[i])) for i in range(3, len(header)) if month_key(header[i])]

    # Per-series official source, taken from the fetcher's SPECS so the seed
    # matches what update_us_macro.py records. Keyed by "section|name".
    src_map: dict[str, str] = {}
    try:
        import importlib.util
        _spec = importlib.util.spec_from_file_location(
            "fetch_us_macro_table", str(Path(__file__).with_name("fetch_us_macro_table.py"))
        )
        _mod = importlib.util.module_from_spec(_spec)
        sys.modules["fetch_us_macro_table"] = _mod
        _spec.loader.exec_module(_mod)
        src_map = {f"{s.section}|{s.name}": s.source for s in _mod.SPECS}
    except Exception as exc:  # pragma: no cover - source is best-effort
        print(f"warning: could not load SPECS for source map: {exc}")

    blocks: list[dict] = []
    block_index: dict[str, dict] = {}
    series: list[dict] = []
    used_ids: set[str] = set()

    for r in rows[1:]:
        section = (r[0] or "").strip()
        raw_name = (r[1] or "").strip()
        ticker = (r[2] or "").strip()
        if not section or not raw_name:
            continue
        name = NAME_ALIASES.get((section, raw_name), raw_name)

        # unique id
        base = slug(ticker) if ticker and ticker.lower() != "derived" else slug(name)
        sid = base
        n = 2
        while sid in used_ids:
            sid = f"{base}_{n}"
            n += 1
        used_ids.add(sid)

        if section not in block_index:
            blk = {
                "id": section,
                "title": section,
                "color": BLOCK_COLORS[len(blocks) % len(BLOCK_COLORS)],
                "series": [],
            }
            blocks.append(blk)
            block_index[section] = blk
        block_index[section]["series"].append(sid)

        data = []
        for col, date in date_cols:
            v = num(r[col])
            if v is not None:
                data.append({"date": date, "value": v})
        data.sort(key=lambda d: d["date"])

        series.append({
            "id": sid,
            "block": section,
            "name": name,
            "ticker": ticker,
            "source": src_map.get(f"{section}|{name}",
                                  "Derived" if ticker.lower() == "derived" else "Bloomberg (US_ECON.xlsx)"),
            "frequency": "monthly",
            "color": block_index[section]["color"],
            "data": data,
        })

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": {"type": "excel_import", "file": "US_ECON.xlsx", "sheet": "Sheet1"},
        "blocks": blocks,
        "series": series,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}: {len(blocks)} blocks, {len(series)} series")
    for b in blocks:
        print(f"  block {b['id']}: {len(b['series'])} series")


if __name__ == "__main__":
    main()
