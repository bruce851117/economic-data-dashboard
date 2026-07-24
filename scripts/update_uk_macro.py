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
 'ukawmwho':('LMS','KAC3','employmentandlabourmarket/peoplenotinwork/unemployment',False),
 'ukawxprm':('LMS','KAJ4','employmentandlabourmarket/peoplenotinwork/unemployment',False),
 'ukvaap2y':('UNEM','AP2Y','employmentandlabourmarket/peoplenotinwork/outofworkbenefits',True),
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
def merge(db,id,pts,release_type=None):
 s=by_id(db,id)
 if not s:raise KeyError(id)
 old={p['date']:p for p in s.get('data',[])}; add=rev=0
 for p in pts:
  p={**p};
  if release_type:p['release_type']=release_type
  cur=old.get(p['date'])
  if cur is None:old[p['date']]=p;add+=1
  elif cur.get('release_type')=='final' and p.get('release_type')=='flash':continue
  elif cur.get('value')!=p.get('value') or (p.get('release_type')=='final' and cur.get('release_type')!='final'):
   old[p['date']]={**cur,**p};rev+=1
 s['data']=sorted(old.values(),key=lambda x:x['date']);return add,rev

def latest_missing_start(s):
 dates=[p['date'] for p in s.get('data',[])]; return max(dates) if dates else '2020-01-01'

def parse_te_calendar(url, label_regex):
 text=BeautifulSoup(get(url).text,'html.parser').get_text(' ',strip=True)
 pts=[]
 for m in re.finditer(r'(20\d{2})-(\d{2})-\d{2}\s+\d{1,2}:\d{2}\s+(?:AM|PM)\s+'+label_regex+r'\s+([+-]?\d+(?:\.\d+)?)',text,re.I):
  pts.append({'date':f'{m[1]}-{m[2]}-01','value':float(m[3]),'source_url':url})
 return pts

def update_gfk(db):
 url='https://tradingeconomics.com/united-kingdom/consumer-confidence'
 pts=parse_te_calendar(url,r'GfK Consumer Confidence(?:\s+[A-Z][a-z]{2})?')
 if not pts:
  text=BeautifulSoup(get(url).text,'html.parser').get_text(' ',strip=True)
  m=re.search(r'increased to\s+(-?\d+(?:\.\d+)?)\s+points in\s+([A-Za-z]+)\s+from\s+(-?\d+(?:\.\d+)?)\s+points in\s+([A-Za-z]+)\s+of\s+(20\d{2})',text,re.I)
  if m:pts=[{'date':f'{m[5]}-{MONTHS[m[2].lower()]:02d}-01','value':float(m[1]),'source_url':url},{'date':f'{m[5]}-{MONTHS[m[4].lower()]:02d}-01','value':float(m[3]),'source_url':url}]
 return merge(db,'ukcci',pts)

def update_te_pmi(db,id,url,kind):
 text=BeautifulSoup(get(url).text,'html.parser').get_text(' ',strip=True); pts=[]
 # Final/current value and previous month from the official-source summary mirrored by TE.
 pats=[
  rf'{kind} PMI (?:posted|was revised[^.]*?to)\s+([0-9]+(?:\.[0-9]+)?)\s+in\s+([A-Za-z]+)\s+(20\d{{2}})',
  rf'{kind} PMI[^.]*?\s(?:increased|decreased) to\s+([0-9]+(?:\.[0-9]+)?)\s+points in\s+([A-Za-z]+)\s+from\s+([0-9]+(?:\.[0-9]+)?)\s+points in\s+([A-Za-z]+)\s+of\s+(20\d{{2}})'
 ]
 m=re.search(pats[1],text,re.I)
 if m:
  pts=[{'date':f'{m[5]}-{MONTHS[m[2].lower()]:02d}-01','value':float(m[1]),'source_url':url},{'date':f'{m[5]}-{MONTHS[m[4].lower()]:02d}-01','value':float(m[3]),'source_url':url}]
 else:
  m=re.search(pats[0],text,re.I)
  if m:pts=[{'date':f'{m[3]}-{MONTHS[m[2].lower()]:02d}-01','value':float(m[1]),'source_url':url}]
 return merge(db,id,pts,'final')

def update_retail(db):
 # ONS Beta API full CSV. Labels are used rather than unstable option IDs.
 meta_url='https://api.beta.ons.gov.uk/v1/datasets/retail-sales-index/editions/time-series/versions/latest'
 meta=get(meta_url).json(); links=meta.get('downloads',{})
 csv_url=(links.get('csv') or {}).get('href')
 if not csv_url:raise RuntimeError('ONS Retail API did not return CSV download')
 raw=get(csv_url).content.decode('utf-8-sig','replace'); rows=list(csv.DictReader(io.StringIO(raw)))
 pts=[]
 for row in rows:
  norm={re.sub(r'[^a-z0-9]','',k.lower()):str(v).strip() for k,v in row.items() if k}
  joined=' | '.join(norm.values()).lower()
  if 'all retailing excluding automotive fuel' not in joined:continue
  if 'chained volume' not in joined or 'same month a year earlier' not in joined or 'seasonally adjusted' not in joined:continue
  val=next((v for k,v in norm.items() if k in ('observation','value') and re.fullmatch(r'-?\d+(?:\.\d+)?',v)),None)
  t=next((v for k,v in norm.items() if k in ('time','month','dates') or k.startswith('time')),None)
  if val and t:
   m=re.search(r'(20\d{2})[- ](?:M)?(\d{1,2})',t)
   if m:pts.append({'date':f'{m[1]}-{int(m[2]):02d}-01','value':float(val),'source_url':csv_url})
 if not pts:raise RuntimeError('Retail CSV filter returned no observations')
 return merge(db,'ukrvayoy',pts)

def main():
 db=json.loads(DATA_FILE.read_text(encoding='utf-8')); logs=[]
 for id,(dataset,cdid,path,rolling) in ONS.items():
  try:
   pts=ons_series(dataset,cdid,path)
   if rolling:pts=[{**p,'date':shift_month(p['date'])} for p in pts]
   logs.append((id,*merge(db,id,pts)))
  except Exception as e:logs.append((id,'ERROR',str(e)))
 for id,(dataset,cdid,path) in LEVELS.items():
  try:logs.append((id,*merge(db,id,yoy(ons_series(dataset,cdid,path)))))
  except Exception as e:logs.append((id,'ERROR',str(e)))
 for name,fn in [
  ('ukrvayoy',lambda:update_retail(db)),
  ('ukcci',lambda:update_gfk(db)),
  ('mpmigbma',lambda:update_te_pmi(db,'mpmigbma','https://tradingeconomics.com/united-kingdom/manufacturing-pmi','Manufacturing')),
  ('mpmigbsa',lambda:update_te_pmi(db,'mpmigbsa','https://tradingeconomics.com/united-kingdom/services-pmi','Services')),
 ]:
  try:logs.append((name,*fn()))
  except Exception as e:logs.append((name,'ERROR',str(e)))
 db['generated_at']=datetime.now(timezone.utc).isoformat(); DATA_FILE.write_text(json.dumps(db,ensure_ascii=False,indent=2),encoding='utf-8')
 for x in logs:print(*x)
if __name__=='__main__':main()
