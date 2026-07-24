from __future__ import annotations
import csv, io, json, re, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader

DATA_FILE=Path('data/uk_macro.json')
UA='Mozilla/5.0 (compatible; UKMacroDashboard/1.0)'
S=requests.Session(); S.headers.update({'User-Agent':UA,'Accept-Language':'en-GB,en;q=0.9'})

ONS={
 'ukhca9iq':('MM23','DKO8','economy/inflationandpriceindices',False),
 'ukhpsery':('MM23','D7NN','economy/inflationandpriceindices',False),
 'ukueilor':('LMS','MGSX','employmentandlabourmarket/peoplenotinwork/unemployment',True),
 'ukuer':('UNEM','BCJE','employmentandlabourmarket/peoplenotinwork/outofworkbenefits',False),
 'ukawmwho':('LMS','KAC3','employmentandlabourmarket/peopleinwork/earningsandworkinghours',False),
 'ukawxprm':('LMS','KAJ4','employmentandlabourmarket/peopleinwork/earningsandworkinghours',False),
 'ukvaap2y':('UNEM','AP2Y','employmentandlabourmarket/peopleinwork/employmentandemployeetypes',True),
 'uklfjpc5':('UNEM','JPC5','employmentandlabourmarket/peoplenotinwork/unemployment',True),
 'ukgdm3m':('MGDP','ECYX','economy/grossdomesticproductgdp',False),
}
LEVELS={
 'ukgrabiy':('QNA','ABMI','economy/grossdomesticproductgdp'),
 'ukgeabry':('PN2','ABJR','economy/nationalaccounts/satelliteaccounts'),
 'ukgvnpqy':('UKEA','NPQT','economy/grossdomesticproductgdp'),
}
MONTHS={m:i for i,m in enumerate(['january','february','march','april','may','june','july','august','september','october','november','december'],1)}

def get(url,**kw):
 for n in range(4):
  r=S.get(url,timeout=60,**kw)
  if r.status_code<400:return r
  if r.status_code not in (429,500,502,503,504):r.raise_for_status()
  time.sleep(3*(2**n))
 r.raise_for_status()

def period(s):
 s=' '.join(str(s).upper().split()); ms={'JAN':'01','FEB':'02','MAR':'03','APR':'04','MAY':'05','JUN':'06','JUL':'07','AUG':'08','SEP':'09','OCT':'10','NOV':'11','DEC':'12'}
 m=re.fullmatch(r'(\d{4}) ('+'|'.join(ms)+r')',s)
 if m:return f'{m[1]}-{ms[m[2]]}-01'
 q=re.fullmatch(r'(\d{4}) Q([1-4])',s)
 if q:return f'{q[1]}-{int(q[2])*3:02d}-01'

def shift_month(d,n=1):
 y,m=map(int,d[:7].split('-')); z=y*12+m-1+n
 return f'{z//12:04d}-{z%12+1:02d}-01'

def ons_series(dataset,cdid,path):
 edition={'ABJR':'pn2','ABMI':'qna','NPQT':'ukea'}.get(cdid,dataset.lower())
 url=f'https://www.ons.gov.uk/generator?format=csv&uri=/{path}/timeseries/{cdid.lower()}/{edition}'
 rows=csv.reader(io.StringIO(get(url).content.decode('utf-8-sig','replace'))); out=[]
 for row in rows:
  if len(row)<2:continue
  d=period(row[0]); v=row[1].replace(',','').strip()
  if d and re.fullmatch(r'-?\d+(?:\.\d+)?',v):out.append({'date':d,'value':float(v),'source_url':url})
 if not out:raise RuntimeError(f'ONS {cdid} returned no data')
 return out

def yoy(levels):
 d={p['date']:p for p in levels}; out=[]
 for dt,p in d.items():
  prev=f'{int(dt[:4])-1}{dt[4:]}'
  if prev in d and d[prev]['value']:
   out.append({'date':dt,'value':(p['value']/d[prev]['value']-1)*100,'source_url':p['source_url']})
 return out

def by_id(db,id):return next((x for x in db['series'] if x['id']==id),None)
def month_key(value):
 value=str(value or '').strip()
 m=re.match(r'^(\d{4})-(\d{2})',value)
 return f'{m.group(1)}-{m.group(2)}' if m else value

def merge(db,id,pts,release_type=None):
 s=by_id(db,id)
 if not s:raise KeyError(id)
 # Compare by YYYY-MM, regardless of whether old JSON used month-end or day 01.
 old={month_key(p.get('date')):{**p,'date':month_key(p.get('date'))+'-01'} for p in s.get('data',[]) if month_key(p.get('date'))}
 add=rev=0
 if old:
  latest_existing=max(old)
  pts=[p for p in pts if month_key(p.get('date'))>=latest_existing]
 for p in pts:
  key=month_key(p.get('date'))
  if not key:continue
  p={**p,'date':key+'-01'}
  if release_type:p['release_type']=release_type
  cur=old.get(key)
  if cur is None:old[key]=p;add+=1
  elif cur.get('release_type')=='final' and p.get('release_type')=='flash':continue
  elif cur.get('value')!=p.get('value') or (p.get('release_type')=='final' and cur.get('release_type')!='final'):
   old[key]={**cur,**p};rev+=1
 s['data']=sorted(old.values(),key=lambda x:x['date'])
 return add,rev


def latest_missing_start(s):
 dates=[p['date'] for p in s.get('data',[])]; return max(dates) if dates else '2020-01-01'

def point(year, month_name, value, url):
    month = MONTHS[month_name.lower()]
    return {
        'date': f'{int(year):04d}-{month:02d}-01',
        'value': float(value),
        'source_url': url,
    }


def previous_month_point(year, month_name, value, url):
    month = MONTHS[month_name.lower()]
    serial = int(year) * 12 + month - 2
    return {
        'date': f'{serial // 12:04d}-{serial % 12 + 1:02d}-01',
        'value': float(value),
        'source_url': url,
    }


def reject_future_points(points):
    """Do not treat scheduled releases or forecasts as actual observations."""
    current_month = datetime.now(timezone.utc).strftime('%Y-%m')
    return [p for p in points if month_key(p.get('date')) <= current_month]


def update_gfk(db):
    url = 'https://tradingeconomics.com/united-kingdom/consumer-confidence'
    text = BeautifulSoup(get(url).text, 'html.parser').get_text(' ', strip=True)

    # Only accept the page summary where current value, current reference month,
    # previous value and previous reference month appear in the same sentence.
    # Do not parse the calendar table: future rows contain forecasts/previous values.
    patterns = [
        r'Consumer Confidence in the United Kingdom (?:increased|decreased|rose|fell|was unchanged) to\s+'
        r'(-?\d+(?:\.\d+)?)\s+points in\s+([A-Za-z]+)\s+from\s+'
        r'(-?\d+(?:\.\d+)?)\s+points in\s+([A-Za-z]+)\s+of\s+(20\d{2})',
        r'GfK Consumer Confidence Index (?:increased|decreased|rose|fell|held steady|was unchanged)'
        r'(?:\s+at|\s+to)?\s+(-?\d+(?:\.\d+)?)\s+in\s+([A-Za-z]+)\s+(20\d{2})'
        r'.{0,180}?(?:from|unchanged from)\s+(-?\d+(?:\.\d+)?)\s+in\s+([A-Za-z]+)',
    ]

    pts = []
    m = re.search(patterns[0], text, re.I)
    if m:
        pts = [
            point(m[5], m[2], m[1], url),
            point(m[5], m[4], m[3], url),
        ]
    else:
        m = re.search(patterns[1], text, re.I)
        if m:
            pts = [
                point(m[3], m[2], m[1], url),
                point(m[3], m[5], m[4], url),
            ]

    pts = reject_future_points(pts)
    if not pts:
        raise RuntimeError('GfK current and previous actual values not found')
    return merge(db, 'ukcci', pts)


def update_te_pmi(db, id, url, kind):
    text = BeautifulSoup(get(url).text, 'html.parser').get_text(' ', strip=True)

    # Only accept an explicit current/previous summary sentence.
    # Never read the economic-calendar rows, because a future row may show the
    # previous value even though the new actual has not been released.
    patterns = [
        rf'{kind} PMI[^.]*?(?:increased|decreased|rose|fell|was unchanged|held steady) to\s+'
        r'([0-9]+(?:\.[0-9]+)?)\s+points in\s+([A-Za-z]+)\s+from\s+'
        r'([0-9]+(?:\.[0-9]+)?)\s+points in\s+([A-Za-z]+)\s+of\s+(20\d{2})',
        rf'{kind} PMI[^.]*?(?:posted|was revised to|came in at)\s+'
        r'([0-9]+(?:\.[0-9]+)?)\s+in\s+([A-Za-z]+)\s+(20\d{2})',
    ]

    pts = []
    m = re.search(patterns[0], text, re.I)
    if m:
        pts = [
            point(m[5], m[2], m[1], url),
            point(m[5], m[4], m[3], url),
        ]
    else:
        m = re.search(patterns[1], text, re.I)
        if m:
            pts = [point(m[3], m[2], m[1], url)]

    pts = reject_future_points(pts)
    if not pts:
        raise RuntimeError(f'{kind} PMI current actual value not found')

    # Trading Economics page summary is treated as the currently reported value.
    # Existing final values still cannot be overwritten by flash in merge().
    return merge(db, id, pts, 'final')


def update_retail(db):
    url = 'https://tradingeconomics.com/united-kingdom/retail-sales-ex-fuel'
    text = BeautifulSoup(get(url).text, 'html.parser').get_text(' ', strip=True)

    # The month/year must be in the same sentence as both the current and previous
    # actual values. The old code searched the entire page for any "in Month Year"
    # and could attach the value to an unrelated or future month.
    patterns = [
        r'(?:Retail Sales Ex Fuel YoY|retail sales excluding fuel)[^.]*?'
        r'(?:increased|decreased|accelerated|slowed|rose|fell|declined|was unchanged)'
        r'(?:\s+to|\s+at)?\s+([+-]?\d+(?:\.\d+)?)%\s+in\s+([A-Za-z]+)\s+(20\d{2})'
        r'[^.]*?from\s+([+-]?\d+(?:\.\d+)?)%\s+in\s+([A-Za-z]+)',
        r'On an annual basis, retail sales excluding fuel '
        r'(?:accelerated|rose|increased|fell|declined|was unchanged) to\s+'
        r'([+-]?\d+(?:\.\d+)?)%\s+from\s+([+-]?\d+(?:\.\d+)?)%[^.]*?'
        r'in\s+([A-Za-z]+)\s+(20\d{2})',
    ]

    pts = []
    m = re.search(patterns[0], text, re.I)
    if m:
        pts = [
            point(m[3], m[2], m[1], url),
            point(m[3], m[5], m[4], url),
        ]
    else:
        m = re.search(patterns[1], text, re.I)
        if m:
            pts = [
                point(m[4], m[3], m[1], url),
                previous_month_point(m[4], m[3], m[2], url),
            ]

    pts = reject_future_points(pts)
    if not pts:
        raise RuntimeError('Retail Sales ex Fuel YoY current and previous actual values not found')
    return merge(db, 'ukrvayoy', pts)

def main():
    db = json.loads(
        DATA_FILE.read_text(encoding="utf-8")
    )
    logs = []

    for id, (dataset, cdid, path, rolling) in ONS.items():
        try:
            pts = ons_series(dataset, cdid, path)

            if id == "ukvaap2y":
                # AP2Y原始月份是滾動三個月期間的中間月。
                #
                # 例如：
                # ONS Raw 2026-05
                # = 統計期間2026年4月至6月
                # = 2026年7月發布
                #
                # Dashboard使用發布月份，因此往後移兩個月。
                pts = [
                    {
                        **p,
                        "date": shift_month(
                            p["date"],
                            2,
                        ),
               **   }
                    for p in**ts
                ]

           **lif rolling:
                # 其他**三個月資料維持往後移一個月。
                #
**              # 例如失業率：
          **    # ONS Raw 2026-04
           **   # = 統計期間2026年3月至5月
           **   # = Dashboard顯示2026年5月。
      **        pts = [
                    {
                        **p,
                        "date": shift_month(
                            p["date"],
                            1,
                        ),
                    }
                    for p in pts
                ]

            logs.append(
                (
                    id,
                    *merge(
                        db,
                        id,
                        pts,
                    ),
                )
            )

        except Exception as e:
            logs.append(
                (
                    id,
                    "ERROR",
                    str(e),
                )
            )

    for id, (dataset, cdid, path) in LEVELS.items():
        try:
            pts = ons_series(
                dataset,
                cdid,
                path,
            )

            calculated_yoy = yoy(pts)

            logs.append(
                (
                    id,
                    *merge(
                        db,
                        id,
                        calculated_yoy,
                    ),
                )
            )

        except Exception as e:
            logs.append(
                (
                    id,
                    "ERROR",
                    str(e),
                )
            )

    additional_updates = [
        (
            "ukrvayoy",
            lambda: update_retail(db),
        ),
        (
            "ukcci",
            lambda: update_gfk(db),
        ),
        (
            "mpmigbma",
            lambda: update_te_pmi(
                db,
                "mpmigbma",
                "https://tradingeconomics.com/united-kingdom/manufacturing-pmi",
                "Manufacturing",
            ),
        ),
        (
            "mpmigbsa",
            lambda: update_te_pmi(
                db,
                "mpmigbsa",
                "https://tradingeconomics.com/united-kingdom/services-pmi",
                "Services",
            ),
        ),
    ]

    for name, update_function in additional_updates:
        try:
            logs.append(
                (
                    name,
                    *update_function(),
                )
            )

        except Exception as e:
            logs.append(
                (
                    name,
                    "ERROR",
                    str(e),
                )
            )

    db["generated_at"] = (
        datetime.now(timezone.utc).isoformat()
    )

    DATA_FILE.write_text(
        json.dumps(
            db,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    for log_entry in logs:
        print(*log_entry)


if __name__ == "__main__":
    main()
