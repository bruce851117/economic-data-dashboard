#!/usr/bin/env python3
"""Update data/us_macro.json in place from live official US sources.

Fetching logic is reused verbatim from ``fetch_us_macro_table.py`` (same SPECS,
same provider fetchers). The overwrite/merge philosophy follows the other
countries (see ``update_uk_macro.py``): official sources are authoritative, so
every overlapping month is overwritten and newer months are appended, while
history older than the first fetched month is preserved.

NFIB hiring plan (`就業-調查|中小企hiring plan`) is intentionally skipped: the
public SBET API only returns the unadjusted answer distribution, not the
seasonally adjusted net headline, so its existing value is left untouched.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import fetch_us_macro_table as fus

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "us_macro.json"

# Provider that must not overwrite the reference value (see module docstring).
SKIP_PROVIDERS = {"nfib"}


def month_key(date: str) -> str | None:
    """Return 'YYYY-MM' from a 'YYYY-MM' or 'YYYY-MM-DD' string."""
    if not date:
        return None
    m = re.match(r"(\d{4})-(\d{2})", str(date))
    return f"{m.group(1)}-{m.group(2)}" if m else None


def normalize_value(v):
    if v is None:
        return None
    if isinstance(v, float) and v == int(v):
        return int(v)
    return v


def fetch_current() -> tuple[dict[str, dict[str, float]], list[str]]:
    """Reproduce fetch_us_macro_table.main()'s data collection.

    Returns (current, errors) where current maps 'section|name' -> {YYYY-MM: value}.
    """
    current: dict[str, dict[str, float]] = {}
    errors: list[str] = []

    bls_ids = sorted({s.source_id for s in fus.SPECS if s.provider == "bls"})
    try:
        bls = fus.fetch_bls(bls_ids)
    except Exception as e:
        bls = {}; errors.append(f"BLS: {e}")
    try:
        atl = fus.fetch_atlanta()
    except Exception as e:
        atl = {}; errors.append(f"Atlanta Fed: {e}")
    try:
        adp = fus.fetch_adp()
    except Exception as e:
        adp = {}; errors.append(f"ADP: {e}")
    try:
        zori = fus.fetch_zillow()
    except Exception as e:
        zori = {}; errors.append(f"Zillow: {e}")
    try:
        pages = fus.fetch_page_latest()
    except Exception as e:
        pages = {}; errors.append(f"Official pages: {e}")
    try:
        nyfed_sce = fus.fetch_nyfed_sce()
    except Exception as e:
        nyfed_sce = {}; errors.append(f"NY Fed SCE: {e}")
    try:
        umich = fus.fetch_umichigan_csv()
    except Exception as e:
        umich = {}; errors.append(f"University of Michigan CSV: {e}")
    try:
        umich_financial = fus.fetch_umich_financial()
    except Exception as e:
        umich_financial = {}; errors.append(f"University of Michigan financial charts: {e}")
    try:
        retail_control, _raw = fus.fetch_census_retail_control()
    except Exception as e:
        retail_control = {}; errors.append(f"Census retail control: {e}")

    for s in fus.SPECS:
        key = f"{s.section}|{s.name}"
        if s.provider in SKIP_PROVIDERS:
            continue
        try:
            if s.provider == "bls":
                # The two employment blocks share the same Bloomberg level ticker;
                # the reference stores levels in both and the dashboard derives the
                # month change at render time, so never apply the "change" transform.
                tr = "level" if "月增減" in s.section else s.transform
                vals = fus.transform(bls.get(s.source_id, {}), tr)
            elif s.provider == "fred":
                vals = fus.transform(fus.fetch_fred(s.source_id), s.transform)
            elif s.provider == "atlanta":
                vals = atl.get(s.source_id, {})
            elif s.provider == "adp":
                vals = adp.get(s.source_id, {})
            elif s.provider == "umich_csv":
                vals = umich.get(s.source_id, {})
            elif s.provider == "umich":
                vals = umich_financial.get(s.source_id, {})
            elif s.provider == "zillow":
                vals = zori
            elif s.provider == "nyfed_xlsx":
                vals = nyfed_sce.get(s.source_id, {})
            elif s.provider == "census" and s.source_id == "retail_control":
                vals = retail_control
            elif s.provider in {"ism", "conference", "nyfed"}:
                vals = pages.get((s.provider, s.source_id), {})
            else:
                vals = {}
            if vals:
                current[key] = dict(vals)
        except Exception as e:
            errors.append(f"{s.name}: {e}")

    # Derived vacancy/unemployment ratio from freshly fetched levels.
    jolts = current.get("就業-職缺|JOLTS", {})
    unemployed = current.get("就業-失業|Unemployed", {})
    ratio = {
        k: round(jolts[k] / unemployed[k], 7)
        for k in jolts.keys() & unemployed.keys()
        if unemployed[k]
    }
    if ratio:
        current["就業-職缺|職缺/失業人口"] = ratio

    return current, errors


def merge_series(series: dict, fetched: dict[str, float]) -> tuple[int, int]:
    """Official-authoritative merge: overwrite overlapping months, append newer.

    History older than the first fetched month is preserved (mirrors the
    replace_source_range behaviour in update_uk_macro.py).
    """
    old = {
        month_key(p.get("date")): dict(p)
        for p in series.get("data", [])
        if month_key(p.get("date"))
    }
    new = {mk: v for mk, v in ((month_key(k), v) for k, v in fetched.items()) if mk}
    if not new:
        return 0, 0

    earliest_existing = min(old) if old else min(new)
    added = revised = 0
    for mk in sorted(new):
        if mk < earliest_existing:
            continue
        value = normalize_value(new[mk])
        if mk not in old:
            old[mk] = {"date": mk + "-01", "value": value}
            added += 1
        elif old[mk].get("value") != value:
            old[mk] = {**old[mk], "date": mk + "-01", "value": value}
            revised += 1
    series["data"] = sorted(old.values(), key=lambda p: p["date"])
    return added, revised


def main() -> None:
    if not DATA_FILE.exists():
        raise SystemExit(f"{DATA_FILE} not found; build it from US_ECON.xlsx first.")
    database = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    index = {f"{s['block']}|{s['name']}": s for s in database.get("series", [])}

    current, errors = fetch_current()

    total_added = total_revised = 0
    unmatched = []
    for key, vals in current.items():
        series = index.get(key)
        if not series:
            unmatched.append(key)
            continue
        a, r = merge_series(series, vals)
        total_added += a
        total_revised += r
        if a or r:
            print(f"[MERGE] {key}: +{a} added, {r} revised", flush=True)

    database["generated_at"] = datetime.now(timezone.utc).isoformat()
    DATA_FILE.write_text(
        json.dumps(database, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(
        f"Wrote {DATA_FILE}: {len(database['series'])} series, "
        f"+{total_added} added, {total_revised} revised, "
        f"{len(current)} fetched, warnings={len(errors)}"
    )
    if unmatched:
        print("Unmatched fetched keys:", ", ".join(unmatched))
    for e in errors:
        print("  WARN", e)


if __name__ == "__main__":
    sys.exit(main())
