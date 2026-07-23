from __future__ import annotations

import json
import math
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
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
        'benchmark': {'2026-04': 4.9},
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
        'benchmark': {'2026-04': 710.0, '2026-05': 712.0},
    },
    'unemployed_per_vacancy': {
        'dataset': 'UNEM', 'frequency': 'M', 'cdid': 'JPC5',
        'include': ['number of unemployed people per vacancy'],
        'benchmark': {'2026-04': 2.5},
    },
    'monthly_gdp_mom': {
        'dataset': 'MGDP', 'frequency': 'M', 'cdid': 'ECYX',
        'include': ['gross domestic product', 'month on month', 'growth'],
        'exclude': ['three months', 'year on year'],
        'benchmark': {'2026-05': 0.1},
    },
    'quarterly_gdp_yoy': {
        'dataset': 'QNA', 'frequency': 'Q', 'level_cdid': 'ABMI',
        'include': ['gross domestic product', 'year on year growth', 'cvm sa'],
        'benchmark': {'2025-Q4': 0.9, '2026-Q1': 0.9},
        'derive_yoy_from_level': True,
    },
    'hfce_yoy': {
        'dataset': 'PN2', 'frequency': 'Q',
        'level_cdid': 'ABJR',
        'include': ['household final consumption expenditure', 'cvm sa'],
        'benchmark': {'2025-Q4': 0.5, '2026-Q1': 0.9},
        'derive_yoy_from_level': True,
    },
    'gfcf_yoy': {
        'dataset': 'UKEA', 'frequency': 'Q', 'level_cdid': 'NPQT',
        'include': ['total fixed capital formation', 'annual growth rate', 'yoy', 'cvm sa'],
        'benchmark': {'2025-Q4': 3.86, '2026-Q1': 1.61},
        'derive_yoy_from_level': True,
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


def get_dataset_series(dataset: str, query: str = '') -> list[dict[str, Any]]:
    # DBnomics caps result sizes; use a focused query instead of requesting 20,000 rows.
    params = {'limit': 1000, 'observations': 0}
    if query:
        params['q'] = query
    url = f'https://api.db.nomics.world/v22/series/ONS/{quote(dataset)}?' + urlencode(params)
    data = fetch_json(url)
    docs = data.get('dataset', {}).get('series', {}).get('docs', [])
    if not docs:
        docs = data.get('series', {}).get('docs', [])
    return docs if isinstance(docs, list) else []


def find_candidate(dataset: str, include: list[str], exclude: list[str] | None, frequency: str) -> dict[str, Any] | None:
    candidates = []
    for row in get_dataset_series(dataset, ' '.join(include)):
        code = str(row.get('series_code') or row.get('code') or '')
        title = str(row.get('series_name') or row.get('name') or row.get('title') or '')
        if frequency and not code.upper().endswith('.' + frequency.upper()):
            continue
        score = score_title(title, include, exclude)
        if score > 0:
            candidates.append({'code': code, 'title': title, 'score': score})
    candidates.sort(key=lambda x: (-x['score'], len(x['title'])))
    return candidates[0] if candidates else None


ONS_PATHS = {
    'MM23': 'economy/inflationandpriceindices',
    'LMS': 'employmentandlabourmarket/peoplenotinwork/unemployment',
    'UNEM': 'employmentandlabourmarket/peoplenotinwork/outofworkbenefits',
    'MGDP': 'economy/grossdomesticproductgdp',
    'PN2': 'economy/grossdomesticproductgdp',
    'QNA': 'economy/grossdomesticproductgdp',
    'UKEA': 'economy/grossdomesticproductgdp',
}


def normalize_period(period: str) -> str:
    p = ' '.join(str(period).strip().upper().split())
    months = {'JAN':'01','FEB':'02','MAR':'03','APR':'04','MAY':'05','JUN':'06','JUL':'07','AUG':'08','SEP':'09','OCT':'10','NOV':'11','DEC':'12'}
    m = re.fullmatch(r'(\d{4}) (JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)', p)
    if m:
        return f'{m.group(1)}-{months[m.group(2)]}'
    q = re.fullmatch(r'(\d{4}) Q([1-4])', p)
    if q:
        return f'{q.group(1)}-Q{q.group(2)}'
    return period


def get_ons_direct_series(dataset: str, cdid: str) -> dict[str, Any]:
    path = ONS_PATHS[dataset]
    if cdid.upper() == 'ABJR':
        path = 'economy/nationalaccounts/satelliteaccounts'
    edition = dataset.lower()
    if cdid.upper() == 'NPQT':
        edition = 'ukea'
    elif cdid.upper() == 'ABMI':
        edition = 'qna'
    url = f'https://www.ons.gov.uk/generator?format=csv&uri=/{path}/timeseries/{cdid.lower()}/{edition}'
    text = fetch_text(url)
    import csv, io
    rows = list(csv.reader(io.StringIO(text)))
    title = ''
    obs = []
    for row in rows:
        if len(row) < 2:
            continue
        if row[0].strip().lower() == 'title':
            title = row[1].strip()
        period = normalize_period(row[0])
        value = row[1].replace(',', '').strip()
        if re.fullmatch(r'\d{4}-(?:\d{2}|Q[1-4])', period) and re.fullmatch(r'-?\d+(?:\.\d+)?', value):
            obs.append({'period': period, 'value': float(value)})
    if not obs:
        raise RuntimeError(f'ONS direct series returned no observations: {url}')
    return {'provider':'ONS direct','source_series':url,'title':title,'observations':obs}


def get_series(dataset: str, cdid: str, frequency: str) -> dict[str, Any]:
    code = f'{cdid.upper()}.{frequency.upper()}'
    url = f'https://api.db.nomics.world/v22/series/ONS/{dataset}/{code}?observations=1'
    data = fetch_json(url)
    docs = data.get('series', {}).get('docs', [])
    if not docs:
        docs = data.get('dataset', {}).get('series', {}).get('docs', [])
    if not docs:
        return get_ons_direct_series(dataset, cdid)
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
    if not obs:
        return get_ons_direct_series(dataset, cdid)
    return {
        'provider': 'ONS via DBnomics mirror',
        'source_series': f'ONS/{dataset}/{code}',
        'title': doc.get('series_name') or doc.get('name') or '',
        'observations': [{'period': normalize_period(x['period']), 'value': x['value']} for x in obs],
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


def fetch_bytes(url: str) -> bytes:
    req = Request(url, headers={'User-Agent': UA, 'Accept': 'application/pdf,text/html,*/*'})
    with urlopen(req, timeout=TIMEOUT) as r:
        return r.read()


def parse_sp_release(name: str, url: str) -> dict[str, Any]:
    raw = fetch_bytes(url)
    if raw.startswith(b'%PDF'):
        from io import BytesIO
        from pypdf import PdfReader
        text = ' '.join((page.extract_text() or '') for page in PdfReader(BytesIO(raw)).pages)
    else:
        text = strip_html(raw.decode('utf-8', 'replace'))
    if 'manufacturing' in name:
        patterns = [r'Manufacturing PMI at\s+(\d{2}\.\d)', r'posted\s+(\d{2}\.\d)\s+in June']
    else:
        patterns = [r'At\s+(\d{2}\.\d)\s+in June', r'Services PMI[^0-9]{0,80}(\d{2}\.\d)']
    value = None
    for pattern in patterns:
        m = re.search(pattern, text, re.I)
        if m:
            value = float(m.group(1)); break
    return {'url': url, 'value': value, 'is_flash': 'flash uk pmi' in text[:2000].lower(), 'preview': ' '.join(text.split())[:800]}


def find_core_cpi_from_mm23() -> dict[str, Any]:
    """Read official ONS monthly CPI bulletins and extract Core CPI YoY."""
    months = [
        ('2025-06','june2025'),('2025-07','july2025'),('2025-08','august2025'),
        ('2025-09','september2025'),('2025-10','october2025'),('2025-11','november2025'),
        ('2025-12','december2025'),('2026-01','january2026'),('2026-02','february2026'),
        ('2026-03','march2026'),('2026-04','april2026'),('2026-05','may2026'),('2026-06','june2026'),
    ]
    obs=[]
    urls=[]
    for period, slug in months:
        url=f'https://www.ons.gov.uk/economy/inflationandpriceindices/bulletins/consumerpriceinflation/{slug}'
        text=strip_html(fetch_text(url))
        m=re.search(r'Core CPI \(CPI excluding energy, food, alcohol,? and tobacco\) rose by\s+([0-9.]+)%', text, re.I)
        if not m:
            raise RuntimeError(f'Core CPI not found in ONS bulletin: {url}')
        obs.append({'period':period,'value':float(m.group(1))})
        urls.append(url)
    return {'provider':'ONS official bulletins','source_series':'ONS Consumer price inflation monthly bulletins','title':'Core CPI YoY','observations':obs,'urls':urls}


def choose_pmi(final_record: dict[str, Any] | None, flash_record: dict[str, Any] | None) -> dict[str, Any] | None:
    """Final always wins; flash is used only while final is unavailable."""
    if final_record and final_record.get('value') is not None:
        return {**final_record, 'release_type': 'final'}
    if flash_record and flash_record.get('value') is not None:
        return {**flash_record, 'release_type': 'flash'}
    return None

def main() -> None:
    report: dict[str, Any] = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'purpose': 'Validate UK macro sources against Bloomberg reference values supplied by user.',
        'indicators': {},
        'pmi': {'selection_rule': 'Use final when available; otherwise use flash. A later final release replaces flash for the same reference month.'},
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
    def cached(dataset: str, query: str = '') -> list[dict[str, Any]]:
        key = dataset + '|' + query
        if key not in dataset_cache:
            dataset_cache[key] = original_get(dataset, query)
        return dataset_cache[key]
    get_dataset_series = cached

    for key, spec in TARGETS.items():
        entry: dict[str, Any] = {'status': 'ERROR'}
        try:
            if key == 'core_cpi_yoy':
                series = find_core_cpi_from_mm23()
                entry.update({
                    'status': 'OK',
                    'resolved_cdid': series['source_series'].split('/timeseries/')[-1].split('/')[0].upper() if '/timeseries/' in series['source_series'] else '',
                    'title': series['title'],
                    'source_series': series['source_series'],
                    'latest': last_n(series, 13),
                    'benchmark_check': compare(series, spec['benchmark'], 0.06),
                })
                if any(x['status'] == 'MISMATCH' for x in entry['benchmark_check']):
                    entry['status'] = 'MISMATCH'
                report['indicators'][key] = entry
                continue
            cdid = spec.get('cdid')
            if not cdid and not spec.get('level_cdid'):
                candidate = find_candidate(spec['dataset'], spec['include'], spec.get('exclude'), spec['frequency'])
                entry['candidate'] = candidate
                if not candidate:
                    raise RuntimeError('No matching series candidate')
                cdid = candidate['code'].split('.')[0]
            if spec.get('level_cdid'):
                if key in {'quarterly_gdp_yoy', 'gfcf_yoy'}:
                    series = get_ons_direct_series(spec['dataset'], spec['level_cdid'])
                else:
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
