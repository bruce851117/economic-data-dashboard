from __future__ import annotations

import json
import math
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

OUT = Path('uk_validation_output')
OUT.mkdir(exist_ok=True)
UA = 'Mozilla/5.0 (compatible; economic-data-dashboard/2.0; +https://github.com/bruce851117/economic-data-dashboard)'
TIMEOUT = 60

TARGETS = {
    'core_cpi_yoy': {
        'dataset': 'MM23',
        'frequency': 'M',
        'include': ['cpi', 'annual rate', 'excluding', 'energy', 'food', 'alcohol', 'tobacco'],
        'exclude': ['cpih'],
        'benchmark': {'2026-05': 2.6, '2026-06': 2.6},
    },
    'cpi_services_yoy': {
        'dataset': 'MM23', 'frequency': 'M', 'cdid': 'D7NN',
        'include': ['cpi annual rate', 'services'], 'exclude': ['cpih'],
        'benchmark': {'2026-05': 3.7, '2026-06': 3.6},
    },
    'unemployment_rate': {
        'dataset': 'LMS', 'frequency': 'M', 'cdid': 'MGSX',
        'include': ['unemployment rate', 'aged 16 and over', 'seasonally adjusted'],
        'benchmark': {'2026-05': 4.9},
    },
    'claimant_count_rate': {
        'dataset': 'UNEM', 'frequency': 'M', 'cdid': 'BCJE',
        'include': ['claimant count', 'seasonally adjusted', 'percentage'],
        'benchmark': {'2026-05': 4.4, '2026-06': 4.4},
    },
    'awe_total_pay_3m_yoy': {
        'dataset': 'LMS', 'frequency': 'M', 'cdid': 'KAC3',
        'include': ['whole economy', 'year on year', 'three month average growth', 'total pay'],
        'benchmark': {'2026-05': 4.3},
    },
    'awe_private_regular_3m_yoy': {
        'dataset': 'LMS', 'frequency': 'M', 'cdid': 'KAJ4',
        'include': ['private sector', 'year on year', 'three month average growth', 'regular pay'],
        'benchmark': {'2026-05': 2.9},
    },
    'vacancies': {
        'dataset': 'UNEM', 'frequency': 'M', 'cdid': 'AP2Y',
        'include': ['vacancies', 'thousands', 'total'],
        'benchmark': {'2026-05': 710.0, '2026-06': 712.0},
    },
    'monthly_gdp_mom': {
        'dataset': 'MGDP', 'frequency': 'M',
        'include': ['gross domestic product', 'month on month', 'growth'],
        'exclude': ['three months', 'year on year'],
        'benchmark': {'2026-05': 0.1},
    },
    'quarterly_gdp_yoy': {
        'dataset': 'PN2', 'frequency': 'Q', 'cdid': 'IHYP',
        'include': ['gross domestic product', 'year on year growth', 'cvm sa'],
        'benchmark': {'2025-Q4': 0.9, '2026-Q1': 0.9},
    },
    'hfce_yoy': {
        'dataset': 'PN2', 'frequency': 'Q',
        'level_cdid': 'ABJR',
        'include': ['household final consumption expenditure', 'cvm sa'],
        'benchmark': {'2025-Q4': 0.5, '2026-Q1': 0.9},
        'derive_yoy_from_level': True,
    },
    'gfcf_yoy': {
        'dataset': 'PN2', 'frequency': 'Q', 'cdid': 'KG7N',
        'include': ['total fixed capital formation', 'annual growth rate', 'yoy', 'cvm sa'],
        'benchmark': {'2025-Q4': 3.86, '2026-Q1': 1.61},
    },
}

SP_RELEASES = {
    'uk_manufacturing_pmi_final_2026_06': 'https://www.pmi.spglobal.com/Public/Home/PressRelease/f1f57e739ff54287b52097b490d1522d',
    'uk_services_pmi_final_2026_06': 'https://www.pmi.spglobal.com/Public/Home/PressRelease/48614ce701c74b2facc9abf435f3a00b',
}


def fetch_json(url: str, retries: int = 3) -> dict[str, Any]:
    last = None
    for attempt in range(retries):
        try:
            req = Request(url, headers={'User-Agent': UA, 'Accept': 'application/json'})
            with urlopen(req, timeout=TIMEOUT) as r:
                return json.loads(r.read().decode('utf-8'))
        except (HTTPError, URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
            last = exc
            time.sleep(2 ** attempt)
    raise RuntimeError(f'GET failed: {url}: {last}')


def fetch_text(url: str, retries: int = 3) -> str:
    last = None
    for attempt in range(retries):
        try:
            req = Request(url, headers={'User-Agent': UA, 'Accept': 'text/html,*/*'})
            with urlopen(req, timeout=TIMEOUT) as r:
                return r.read().decode(r.headers.get_content_charset() or 'utf-8', 'replace')
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            last = exc
            time.sleep(2 ** attempt)
    raise RuntimeError(f'GET failed: {url}: {last}')


def norm(s: Any) -> str:
    return ' '.join(str(s or '').lower().split())


def score_title(title: str, include: list[str], exclude: list[str] | None = None) -> int:
    t = norm(title)
    if any(norm(x) in t for x in (exclude or [])):
        return -999
    return sum(1 for x in include if norm(x) in t)


def get_dataset_series(dataset: str) -> list[dict[str, Any]]:
    # DBnomics is used as a machine-readable mirror of ONS datasets.
    url = f'https://api.db.nomics.world/v22/series/ONS/{quote(dataset)}?limit=20000&observations=0'
    data = fetch_json(url)
    docs = data.get('dataset', {}).get('series', {}).get('docs', [])
    if not docs:
        docs = data.get('series', {}).get('docs', [])
    return docs if isinstance(docs, list) else []


def find_candidate(dataset: str, include: list[str], exclude: list[str] | None, frequency: str) -> dict[str, Any] | None:
    candidates = []
    for row in get_dataset_series(dataset):
        code = str(row.get('series_code') or row.get('code') or '')
        title = str(row.get('series_name') or row.get('name') or row.get('title') or '')
        if frequency and not code.upper().endswith('.' + frequency.upper()):
            continue
        score = score_title(title, include, exclude)
        if score > 0:
            candidates.append({'code': code, 'title': title, 'score': score})
    candidates.sort(key=lambda x: (-x['score'], len(x['title'])))
    return candidates[0] if candidates else None


def get_series(dataset: str, cdid: str, frequency: str) -> dict[str, Any]:
    code = f'{cdid.upper()}.{frequency.upper()}'
    url = f'https://api.db.nomics.world/v22/series/ONS/{dataset}/{code}?observations=1'
    data = fetch_json(url)
    docs = data.get('series', {}).get('docs', [])
    if not docs:
        docs = data.get('dataset', {}).get('series', {}).get('docs', [])
    if not docs:
        raise RuntimeError(f'No observations for ONS/{dataset}/{code}')
    doc = docs[0]
    periods = doc.get('period', [])
    values = doc.get('value', [])
    obs = []
    for p, v in zip(periods, values):
        if v is None:
            continue
        try:
            f = float(v)
        except (TypeError, ValueError):
            continue
        if math.isfinite(f):
            obs.append({'period': str(p), 'value': f})
    return {
        'provider': 'ONS via DBnomics mirror',
        'source_series': f'ONS/{dataset}/{code}',
        'title': doc.get('series_name') or doc.get('name') or '',
        'observations': obs,
    }


def last_n(series: dict[str, Any], n: int) -> list[dict[str, Any]]:
    return series.get('observations', [])[-n:][::-1]


def derive_yoy(level_series: dict[str, Any], lag: int = 4) -> dict[str, Any]:
    rows = level_series.get('observations', [])
    out = []
    for i in range(lag, len(rows)):
        cur, prev = rows[i], rows[i-lag]
        if prev['value'] == 0:
            continue
        out.append({'period': cur['period'], 'value': (cur['value'] / prev['value'] - 1) * 100})
    return {
        'provider': level_series['provider'],
        'source_series': level_series['source_series'] + ' (derived YoY)',
        'title': level_series['title'] + ' - derived YoY',
        'observations': out,
    }


def compare(series: dict[str, Any], benchmark: dict[str, float], tolerance: float = 0.06) -> list[dict[str, Any]]:
    by_period = {x['period']: x['value'] for x in series.get('observations', [])}
    result = []
    for period, expected in benchmark.items():
        actual = by_period.get(period)
        if actual is None:
            status = 'MISSING'
            diff = None
        else:
            diff = actual - expected
            status = 'MATCH' if abs(diff) <= tolerance else 'MISMATCH'
        result.append({'period': period, 'expected': expected, 'actual': actual, 'difference': diff, 'status': status})
    return result


def strip_html(text: str) -> str:
    return ' '.join(re.sub(r'(?s)<[^>]+>', ' ', text).split())


def parse_sp_release(name: str, url: str) -> dict[str, Any]:
    html = fetch_text(url)
    text = strip_html(html)
    if 'manufacturing' in name:
        match = re.search(r'(?:posted|at)\s+(\d{2}\.\d)\s+in\s+June|Manufacturing PMI at\s+(\d{2}\.\d)', text, re.I)
    else:
        match = re.search(r'At\s+(\d{2}\.\d)\s+in\s+June', text, re.I)
    vals = [float(v) for v in match.groups() if v] if match else []
    return {'url': url, 'value': vals[0] if vals else None, 'is_flash': 'flash' in text[:1200].lower(), 'preview': text[:800]}


def main() -> None:
    report: dict[str, Any] = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'purpose': 'Validate UK macro sources against Bloomberg reference values supplied by user.',
        'indicators': {},
        'pmi': {},
        'unverified': {
            'one_year_inflation_expectations': {
                'bloomberg_ticker': 'UKBFFTIN Index',
                'benchmark': {'2026-05': 3.96},
                'status': 'UNVERIFIED',
                'reason': 'Public BoE DMP value for May 2026 is 3.7, so DMP is not an exact match. Do not substitute until Bloomberg field definition is confirmed.',
            },
            'gfk_consumer_confidence_history': {
                'status': 'PARTIAL',
                'reason': 'Latest official NIQ/GfK releases are public, but no stable free historical API was confirmed. Formal script should accumulate monthly releases or use licensed data.',
            },
        },
    }

    dataset_cache: dict[str, list[dict[str, Any]]] = {}
    global get_dataset_series
    original_get = get_dataset_series
    def cached(dataset: str) -> list[dict[str, Any]]:
        if dataset not in dataset_cache:
            dataset_cache[dataset] = original_get(dataset)
        return dataset_cache[dataset]
    get_dataset_series = cached

    for key, spec in TARGETS.items():
        entry: dict[str, Any] = {'status': 'ERROR'}
        try:
            cdid = spec.get('cdid')
            if not cdid and not spec.get('level_cdid'):
                candidate = find_candidate(spec['dataset'], spec['include'], spec.get('exclude'), spec['frequency'])
                entry['candidate'] = candidate
                if not candidate:
                    raise RuntimeError('No matching series candidate')
                cdid = candidate['code'].split('.')[0]
            if spec.get('level_cdid'):
                series = get_series(spec['dataset'], spec['level_cdid'], spec['frequency'])
            else:
                series = get_series(spec['dataset'], cdid, spec['frequency'])
            if spec.get('derive_yoy_from_level'):
                series = derive_yoy(series)
            entry.update({
                'status': 'OK',
                'resolved_cdid': spec.get('level_cdid') or cdid,
                'title': series['title'],
                'source_series': series['source_series'],
                'latest': last_n(series, 13 if spec['frequency'] == 'M' else 5),
                'benchmark_check': compare(series, spec['benchmark'], 2.1 if key == 'vacancies' else 0.06),
            })
            if any(x['status'] == 'MISMATCH' for x in entry['benchmark_check']):
                entry['status'] = 'MISMATCH'
        except Exception as exc:
            entry['error'] = f'{type(exc).__name__}: {exc}'
        report['indicators'][key] = entry

    for name, url in SP_RELEASES.items():
        try:
            report['pmi'][name] = parse_sp_release(name, url)
        except Exception as exc:
            report['pmi'][name] = {'url': url, 'error': f'{type(exc).__name__}: {exc}'}

    out = OUT / 'uk_macro_validation.json'
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
