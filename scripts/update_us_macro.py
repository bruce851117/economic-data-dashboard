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

# Individual series (section|name) to leave untouched. Core Services less
# Shelter's BLS series (CUUR0000SASL2RS) does not match the reference concept,
# so it is skipped until a correct series is chosen.
SKIP_KEYS = {"物價|Core Services less Shelter"}

# Dashboard only shows 2015 onward; drop everything older on every write.
HISTORY_START = "2015-01"


# ---------------------------------------------------------------------------
# New series added from the 2026-09 design sheet. Sourced from stable public
# endpoints only: BLS public API and FRED's public CSV endpoint (no key). Each
# entry: (block, name) -> dict(method, id, kind, ticker, source).
#   method: bls | fredcsv     kind: level | yoy
# Derived JOLTS Goods/Services sums are computed after fetching, below.
NEW_SERIES = {
 ("就業-失業","失業率16~24"):("bls","LNS14024887","level","USURT162 Index","Bureau of Labor Statistics"),
 ("就業-失業","失業率25~54"):("bls","LNS14000060","level","USURT254 Index","Bureau of Labor Statistics"),
 ("就業-失業","失業率55+"):("bls","LNS14024230","level","USURT55+ Index","Bureau of Labor Statistics"),
 ("就業-失業","失業率高中以下"):("bls","LNS14027659","level","USAELURT Index","Bureau of Labor Statistics"),
 ("就業-失業","失業率高中"):("bls","LNS14027660","level","USAEHURT Index","Bureau of Labor Statistics"),
 ("就業-失業","失業率大學肄業 / 副學士"):("bls","LNS14027689","level","USAESURT Index","Bureau of Labor Statistics"),
 ("就業-失業","失業率大學學位以上"):("bls","LNS14027662","level","USAECURT Index","Bureau of Labor Statistics"),
 ("就業-失業","勞參率"):("bls","LNS11300000","level","PRUSTOT Index","Bureau of Labor Statistics"),
 ("就業-失業","勞參率16~24"):("bls","LNS11324887","level","PRUSQNMS Index","Bureau of Labor Statistics"),
 ("就業-失業","勞參率25~54"):("bls","LNS11300060","level","PRUSQNTS Index","Bureau of Labor Statistics"),
 ("就業-失業","勞參率55+"):("bls","LNS11324230","level","PRUSQNGS Index","Bureau of Labor Statistics"),
 ("就業-失業","5週以下"):("bls","LNS13008396","level","USDULSFV Index","Bureau of Labor Statistics"),
 ("就業-失業","5~14"):("bls","LNS13008756","level","USDUFVFR Index","Bureau of Labor Statistics"),
 ("就業-失業","15~26"):("bls","LNS13008876","level","USDUFITS Index","Bureau of Labor Statistics"),
 ("就業-失業","27+"):("bls","LNS13008636","level","USDUTWSV Index","Bureau of Labor Statistics"),
 ("就業-失業金人數","初領失業"):("fredcsv","ICSA","claims_k","INJCJC Index","Department of Labor"),
 ("就業-失業金人數","續領失業"):("fredcsv","CCNSA","claims_k","INJCSPNS Index","Department of Labor"),
 ("就業-職缺","Indeed職缺"):("fredcsv","IHLIDXUS","level","INDDUOIS Index","Indeed"),
 ("就業-職缺","Mining and Logging"):("bls","JTS110099000000000JOL","level","JOLTMILS Index","Bureau of Labor Statistics"),
 ("就業-職缺","Construction"):("bls","JTS230000000000000JOL","level","JOLTCONS Index","Bureau of Labor Statistics"),
 ("就業-職缺","Manufacturing"):("bls","JTS300000000000000JOL","level","JOLTMANU Index","Bureau of Labor Statistics"),
 ("就業-職缺","Trade, Transportation, and Utilities"):("bls","JTS400000000000000JOL","level","JOLTTRAD Index","Bureau of Labor Statistics"),
 ("就業-職缺","Information"):("bls","JTS510000000000000JOL","level","JOLTINLS Index","Bureau of Labor Statistics"),
 ("就業-職缺","Financial Activities"):("bls","JTS510099000000000JOL","level","JOLTFALS Index","Bureau of Labor Statistics"),
 ("就業-職缺","Professional and Business Services"):("bls","JTS540099000000000JOL","level","JOLTPROF Index","Bureau of Labor Statistics"),
 ("就業-職缺","Education and Health Services"):("bls","JTS600000000000000JOL","level","JOLTEDUC Index","Bureau of Labor Statistics"),
 ("就業-職缺","Leisure and Hospitality"):("bls","JTS700000000000000JOL","level","JOLTLEIS Index","Bureau of Labor Statistics"),
 ("就業-薪水","時薪YoY"):("bls","CES0500000003","yoy","AHE YOY% Index","Bureau of Labor Statistics"),
 ("就業-薪水","時薪YoY-Goods-producing Sector"):("bls","CES0600000003","yoy","","Bureau of Labor Statistics"),
 ("就業-薪水","時薪YoY-Trade, Transportation, and Utilities"):("bls","CES4000000003","yoy","","Bureau of Labor Statistics"),
 ("就業-薪水","時薪YoY-Information"):("bls","CES5000000003","yoy","","Bureau of Labor Statistics"),
 ("就業-薪水","時薪YoY-Financial Activities"):("bls","CES5500000003","yoy","","Bureau of Labor Statistics"),
 ("就業-薪水","時薪YoY-Professional and Business Services"):("bls","CES6000000003","yoy","","Bureau of Labor Statistics"),
 ("就業-薪水","時薪YoY-Education and Health Services"):("bls","CES6500000003","yoy","","Bureau of Labor Statistics"),
 ("就業-薪水","時薪YoY-Leisure and Hospitality"):("bls","CES7000000003","yoy","","Bureau of Labor Statistics"),
 ("就業-調查","Income Higher - Lower"):("seed","CONCIDDF","level","CONCIDDF Index","Conference Board"),
 ("企業調查","達拉斯製造業"):("fredcsv","BACTSAMFRBDAL","level","DFEDGBA Index","Federal Reserve Bank of Dallas"),
 ("企業調查","帝國製造業"):("fredcsv","GACDISA066MSFRBNY","level","EMPRGBCI Index","Federal Reserve Bank of New York"),
 ("企業調查","費城製造業"):("fredcsv","GACDFSA066MSFRBPHI","level","OUTFGAF Index","Philadelphia Federal Reserve"),
 ("企業調查","DALLAS 服務業"):("fredcsv","TSSOSBACTSAMFRBDAL","level","DSERGBCC Index","Federal Reserve Bank of Dallas"),
 ("企業調查","NY FED 服務業"):("fredcsv","BACDINA066MNFRBNY","level","NYBLCNBA Index","Federal Reserve Bank of New York"),
 ("企業調查","S&P製造業"):("sp","manufacturing","level","MPMIUSMA Index","S&P Global"),
 ("企業調查","S&P服務業"):("sp","services","level","MPMIUSSA Index","S&P Global"),
 ("企業調查","Kansas 製造業"):("kc","KCLSSACI","level","KCLSSACI Index","Federal Reserve Bank of Kansas City"),
 ("企業調查","Richmond製造業"):("richmond","RCHSINDX","level","RCHSINDX Index","Richmond Fed"),
 ("企業調查","PHILI 服務業"):("fredcsv","GARBNDIF066MSFRBPHI","level","PNMARADI Index","Philadelphia Federal Reserve"),
}
# JOLTS industries whose openings sum to the "Goods" table row / chart line.
JOLTS_GOODS = ["Mining and Logging","Construction","Manufacturing"]
JOLTS_SERVICES = ["Trade, Transportation, and Utilities","Information","Financial Activities",
                  "Professional and Business Services","Education and Health Services","Leisure and Hospitality"]


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
        if s.provider in SKIP_PROVIDERS or key in SKIP_KEYS:
            continue
        try:
            if s.provider == "bls":
                # The 月增減 block uses the same level ticker as the 人數 block but
                # must store the real month-over-month change (level[t]-level[t-1]),
                # which is exactly what the spec's "change" transform computes.
                vals = fus.transform(bls.get(s.source_id, {}), s.transform)
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


def fetch_new_series() -> tuple[dict[str, dict[str, float]], list[str]]:
    """Fetch the 2026-09 additions from BLS API + FRED public CSV.

    Returns {'block|name' -> {YYYY-MM: value}} plus derived JOLTS Goods/Services
    opening sums. 'seed' method entries are not fetched (kept as seeded, marked
    non-updating on the dashboard)."""
    out: dict[str, dict[str, float]] = {}
    errors: list[str] = []
    bls_ids = sorted({v[1] for v in NEW_SERIES.values() if v[0] == "bls"})
    try:
        bls = fus.fetch_bls(bls_ids)
    except Exception as e:
        bls = {}; errors.append(f"BLS(new): {e}")
    sp_data = {}
    if any(v[0] == "sp" for v in NEW_SERIES.values()):
        try:
            sp_data = fus.fetch_sp_us_pmi()
        except Exception as e:
            errors.append(f"S&P US PMI: {e}")
    for (block, name), (method, fid, kind, _tk, _src) in NEW_SERIES.items():
        try:
            if method == "bls":
                raw = bls.get(fid, {})
                vals = fus.transform(raw, "yoy_pct") if kind == "yoy" else raw
            elif method == "fredcsv":
                raw = fus.fetch_fred_csv(fid)
                vals = {k: round(v / 1000, 3) for k, v in raw.items()} if kind == "claims_k" else raw
            elif method == "richmond":
                vals = fus.fetch_richmond_mfg()
            elif method == "kc":
                vals = fus.fetch_kc_mfg()
            elif method == "sp":
                vals = sp_data.get(fid, {})  # fid is 'manufacturing' | 'services'
            else:
                vals = {}  # seed-only: keep existing seeded values
            if vals:
                out[f"{block}|{name}"] = dict(vals)
        except Exception as e:
            errors.append(f"{name}(new): {e}")
    # Derived JOLTS openings sums (Goods = mining+construction+manufacturing).
    def grp(names):
        maps = [out.get(f"就業-職缺|{n}", {}) for n in names]
        keys = set.intersection(*[set(m) for m in maps]) if all(maps) else set()
        return {k: round(sum(m[k] for m in maps), 3) for k in keys}
    g = grp(JOLTS_GOODS); sv = grp(JOLTS_SERVICES)
    if g: out["就業-職缺|職缺Goods"] = g
    if sv: out["就業-職缺|職缺Services"] = sv
    return out, errors


def _slug(text: str) -> str:
    t = re.sub(r"\s+index$", "", str(text).strip(), flags=re.I)
    t = re.sub(r"[^A-Za-z0-9]+", "_", t).strip("_").lower()
    return t or "series"


def ensure_new_shells(database: dict, index: dict) -> None:
    """Create empty series shells (with ticker/source) for every new series so
    the full-history fetch can populate them; existing ones are left as-is."""
    used = {s["id"] for s in database["series"]}
    def add(block, name, ticker, source):
        key = f"{block}|{name}"
        if key in index:
            s = index[key]
            if ticker and not s.get("ticker"): s["ticker"] = ticker
            if source: s["source"] = source
            return
        base = _slug(ticker or name); sid = base; n = 2
        while sid in used: sid = f"{base}_{n}"; n += 1
        used.add(sid)
        s = {"id": sid, "block": block, "name": name, "ticker": ticker,
             "source": source, "frequency": "monthly", "new": True, "data": []}
        database["series"].append(s); index[key] = s
    for (block, name), (_m, _id, _k, tk, src) in NEW_SERIES.items():
        add(block, name, tk, src)
    add("就業-職缺", "職缺Goods", "", "Bureau of Labor Statistics")
    add("就業-職缺", "職缺Services", "", "Bureau of Labor Statistics")


def main() -> None:
    if not DATA_FILE.exists():
        raise SystemExit(f"{DATA_FILE} not found; build it from US_ECON.xlsx first.")
    database = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    index = {f"{s['block']}|{s['name']}": s for s in database.get("series", [])}
    ensure_new_shells(database, index)

    current, errors = fetch_current()

    # New series: authoritative full-history replace (they are freshly sourced).
    new_current, new_errors = fetch_new_series()
    errors += new_errors
    # Scraped sources return only the latest month, so merge (keep history);
    # full-history sources (BLS/FRED/Richmond) authoritatively replace.
    merge_only = {f"{b}|{n}" for (b, n), v in NEW_SERIES.items() if v[0] == "sp"}
    for key, vals in new_current.items():
        s = index.get(key)
        if not s:
            continue
        if key in merge_only:
            merge_series(s, vals)
            continue
        pts = []
        for k, v in vals.items():
            mk = month_key(k)
            if mk:
                pts.append((mk, normalize_value(v)))
        pts.sort()
        s["data"] = [{"date": mk + "-01", "value": v} for mk, v in pts]

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

    # Series that now have a live auto-updating source must not carry a stale
    # "static" flag from the original seed (Kansas/Income stay static).
    live_keys = {f"{b}|{n}" for (b, n), v in NEW_SERIES.items() if v[0] != "seed"}
    for s in database.get("series", []):
        if f"{s['block']}|{s['name']}" in live_keys:
            s.pop("static", None)

    # Drop any point dated beyond the current month: real observations never
    # lead the calendar, so a future date signals a mis-attributed month.
    this_month = datetime.now(timezone.utc).strftime("%Y-%m")
    # Keep only 2015 onward across every series (dashboard history floor).
    for s in database.get("series", []):
        s["data"] = [
            p for p in s.get("data", [])
            if HISTORY_START <= str(p.get("date", ""))[:7] <= this_month
        ]

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
