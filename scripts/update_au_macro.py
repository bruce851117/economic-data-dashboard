#!/usr/bin/env python3
"""Update Australian macro data using structured sources only.

Allowed sources: official/public CSV, JSON, XLS/XLSX and APIs.
No HTML or PDF text parsing is used. Unsupported survey series are intentionally skipped.
"""
from __future__ import annotations
import csv, io, json, math, re, time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import requests
from openpyxl import load_workbook

VERSION = "2026-08-31-au-structured-v1"
DATA_FILE = Path("data/au_macro.json")
MD_FILE = Path("au_macro_all_data.md")
OUT = Path("debug/au_macro_sources")
ABS_API = "https://data.api.abs.gov.au/rest/data"
SESSION = requests.Session()
SESSION.headers.update({"User-Agent":"AUMacroStructuredUpdater/1.0","Accept-Language":"en-AU,en;q=0.9"})

@dataclass
class Point:
    period: str
    value: float
    source_url: str
    note: str = ""

@dataclass
class Target:
    id: str; name: str; ticker: str; block: str; frequency: str; unit: str
    source: str; handler: str; expected: dict[str,float]
    flow: str = ""; include: tuple[str,...] = (); exclude: tuple[str,...] = ()
    transform: str = "level"; series_id: str = ""; color: str = "#2563eb"

TARGETS = [
    Target("auempchg","就業新增","AULFEMPC Index","就業","monthly","千人","ABS","abs",{"2026-07":-15.8,"2026-06":80.2},"LF",("employed persons australia seasonally adjusted",),("rate","hours","state"),"mom_diff"),
    Target("auempfull","就業新增-全職","AULFEMFC Index","就業","monthly","千人","ABS","abs",{"2026-07":16.3,"2026-06":48.9},"LF",("full time employed persons australia seasonally adjusted",),("rate","state"),"mom_diff"),
    Target("auemppart","就業新增-兼職","AULFEMCP Index","就業","monthly","千人","ABS","abs",{"2026-07":-32.2,"2026-06":31.4},"LF",("part time employed persons australia seasonally adjusted",),("rate","state"),"mom_diff"),
    Target("auempratio","就業比率","AULFETPR Index","就業","monthly","%","ABS","abs",{"2026-07":63.8704455,"2026-06":64.0412664},"LF",("employment to population ratio australia persons seasonally adjusted",),("state","trend","original")),
    Target("auunemp","失業率","AULFUNEM Index","就業","monthly","%","ABS","abs",{"2026-07":4.4618247,"2026-06":4.4315479},"LF",("unemployment rate australia persons seasonally adjusted",),("underemployment","underutilisation","state","youth")),
    Target("auunderemp","就業不足率","AUUPAUE Index","就業","monthly","%","ABS","abs",{"2026-07":6.3612462,"2026-06":6.449338},"LF",("underemployment rate australia persons seasonally adjusted",),("hours based","state","trend","original")),
    Target("auunderutil","勞動力未充分利用率","AUNDUR Index","就業","monthly","%","ABS","abs",{"2026-07":10.8230708,"2026-06":10.8808859},"LF",("underutilisation rate australia persons seasonally adjusted",),("hours based","state","trend","original")),
    Target("auparticipation","勞參率","AULFPART Index","就業","monthly","%","ABS","abs",{"2026-07":66.8533236,"2026-06":67.0108859},"LF",("participation rate australia persons seasonally adjusted",),("state","trend","original")),
    Target("auhours","工時","AUHRAMTL Index","就業","monthly","千小時","ABS","abs",{"2026-07":1997868.82584,"2026-06":2010341.69766},"LF",("aggregate monthly hours worked all jobs australia seasonally adjusted",),("state","trend","original")),
    Target("auindeed","Indeed職缺","INDDAOIS Index","就業","daily","指數","Indeed Hiring Lab","indeed",{"2026-08":149.45,"2026-07":146.04,"2026-06":145.75}),
    Target("auvacancy","職缺","AUEMVAC Index","就業","quarterly","千人","ABS","abs",{"2026-05":329.5,"2026-02":336.6,"2025-11":328.7},"JV",("job vacancies australia private public seasonally adjusted",),("trend","original")),
    Target("auwageprivate","私人企業時薪ex bonus(季度)","AUWCPY Index","就業","quarterly","YoY %","ABS","abs",{"2026-Q2":3.2,"2026-Q1":3.3,"2025-Q4":3.3},"WPI",("private sector hourly rates of pay excluding bonuses through the year",),("public sector","including bonuses")),
    Target("auwagepublic","政府時薪ex bonus(季度)","AUWCGY Index","就業","quarterly","YoY %","ABS","abs",{"2026-Q2":3.3,"2026-Q1":3.4,"2025-Q4":3.9},"WPI",("public sector hourly rates of pay excluding bonuses through the year",),("private sector","including bonuses")),
    Target("auhsgoods","Goods","AUPDYSGD Index","家戶消費","monthly","YoY %","ABS","abs",{"2026-07":7.2,"2026-06":5.8,"2026-05":5.7},"HSI_M",("goods household spending australia seasonally adjusted through the year",),("services","total")),
    Target("auhsservices","Services","AUPDYSSV Index","家戶消費","monthly","YoY %","ABS","abs",{"2026-07":6.8,"2026-06":6.4,"2026-05":5.0},"HSI_M",("services household spending australia seasonally adjusted through the year",),("goods","total")),
    Target("aucapbuilding","資本支出_住房","AUCEBLDQ Index","投資 QoQ","quarterly","QoQ %","ABS","abs",{"2026-Q2":2.1031,"2026-Q1":-3.26577,"2025-Q4":2.79896},"CAPEX",("buildings structures chain volume seasonally adjusted percentage change",),("equipment","expected")),
    Target("aucapequipment","資本支出 設備廠房","AUCEEQPQ Index","投資 QoQ","quarterly","QoQ %","ABS","abs",{"2026-Q2":-8.91491,"2026-Q1":18.38705,"2025-Q4":-1.22101},"CAPEX",("equipment plant machinery chain volume seasonally adjusted percentage change",),("buildings","expected")),
    Target("aubuildapprovals","Building Approvals YoY","AUBABPNY Index","房市","monthly","YoY %","ABS","abs",{"2026-06":14.58006,"2026-05":1.35569},"BA",("total dwelling units approved australia original",),("seasonally adjusted","trend","private sector"),"yoy_pct_m"),
    Target("auownerhousing","房貸餘額(房屋持有)","AULBHLOC Index","房市","monthly","十億澳元","RBA","rba_rank",{"2026-07":1665.078,"2026-06":1659.954,"2026-05":1649.611},include=("bank household lending owner occupiers housing",),exclude=("investor",)),
    Target("auinvestorhousing","房貸餘額(投資人)","AULBHLIN Index","房市","monthly","十億澳元","RBA","rba_rank",{"2026-07":815.11,"2026-06":813.865,"2026-05":806.411},include=("bank household lending investors housing",),exclude=("owner occupier",)),
    Target("auownerhousingyoy","房貸餘額(房屋持有) YoY","Derived","房市","monthly","YoY %","Derived","derived_yoy",{}),
    Target("auinvestorhousingyoy","房貸餘額(投資人) YoY","Derived","房市","monthly","YoY %","Derived","derived_yoy",{}),
    Target("auhouserepay","房貸總還款","AUHLOOSR Index","房市","quarterly","百萬澳元","RBA","rba_exact",{"2026-Q2":33442.475,"2026-Q1":31956.004,"2025-Q4":31636.717},series_id="LPHOSP"),
    Target("auhouseinterest","房貸利息還款","AUHLOOCI Index","房市","quarterly","百萬澳元","RBA","rba_exact",{"2026-Q2":21334.45,"2026-Q1":19439.391,"2025-Q4":19127.986},series_id="LPHOIC"),
    Target("aurentrate","房租季增率","AUCPRENQ Index","房市","quarterly","QoQ %","ABS","abs",{"2026-Q2":0.8,"2026-Q1":0.9,"2025-Q4":0.8},"CPI",("rents weighted average eight capital cities quarterly percentage change",),("annual","monthly")),
    Target("auincome","Income","AUNATGI Index","家庭","quarterly","百萬澳元","ABS","abs",{"2026-Q1":622128,"2025-Q4":618019,"2025-Q3":604919},"ANA_AGG",("households use of gross income gross income seasonally adjusted current prices",),("percentage","per capita")),
    Target("aupropertypayable","利息支出等","AUNATLPO Index","家庭","quarterly","百萬澳元","ABS","abs",{"2026-Q1":38720,"2025-Q4":37041,"2025-Q3":37051},"ANA_AGG",("households property income payable seasonally adjusted current prices",),("percentage","receivable")),
    Target("ausecondarypayable","所得稅 保險","AUNATSIP Index","家庭","quarterly","百萬澳元","ABS","abs",{"2026-Q1":127153,"2025-Q4":126478,"2025-Q3":122566},"ANA_AGG",("households secondary income payable seasonally adjusted current prices",),("percentage","receivable")),
    Target("audpi","DPI","AUNAGDI Index","家庭","quarterly","百萬澳元","ABS","abs",{"2026-Q1":456254,"2025-Q4":454500,"2025-Q3":445302},"ANA_AGG",("households gross disposable income seasonally adjusted current prices",),("percentage","per capita")),
    Target("auhfce","支出","AUNAFCX Index","家庭","quarterly","百萬澳元","ABS","abs",{"2026-Q1":382863,"2025-Q4":378740,"2025-Q3":374133},"ANA_AGG",("households final consumption expenditure seasonally adjusted current prices",),("percentage","chain volume")),
    Target("aucofc","固定資本消耗","AUNACOFC Index","家庭","quarterly","百萬澳元","ABS","abs",{"2026-Q1":47895,"2025-Q4":47332,"2025-Q3":46752},"ANA_AGG",("households consumption of fixed capital seasonally adjusted current prices",),("percentage",)),
    Target("aunetsaving","Net Saving","AUNANSAV Index","家庭","quarterly","百萬澳元","ABS","abs",{"2026-Q1":25496,"2025-Q4":28428,"2025-Q3":24417},"ANA_AGG",("households net saving seasonally adjusted current prices",),("percentage","ratio")),
]

ABS_ALIASES={"LF":["LF"],"JV":["JV"],"WPI":["WPI"],"HSI_M":["HSI_M","MHSI","HSI"],"CAPEX":["CAPEX","PNCE"],"BA":["BA"],"CPI":["CPI","CPI_Q"],"ANA_AGG":["ANA_AGG"]}
RBA_STRUCTURED_URLS=[
 "https://www.rba.gov.au/statistics/tables/csv/b18-data.csv",
 "https://www.rba.gov.au/statistics/tables/csv/b19-data.csv",
 "https://www.rba.gov.au/statistics/tables/csv/d2-data.csv",
]

def clean(v): return re.sub(r"\s+"," ",str(v or "")).strip()
def norm(v): return re.sub(r"[^a-z0-9]+"," ",clean(v).lower()).strip()
def num(v):
    if v is None or isinstance(v,bool): return None
    try:
        x=float(str(v).replace(",","").replace("%","").replace("−","-"))
        return x if math.isfinite(x) else None
    except: return None

def get(url,**kwargs):
    last=None
    for attempt in range(2):
        last=SESSION.get(url,timeout=45,**kwargs)
        if last.status_code==200 and last.content: return last
        time.sleep(1.5*(attempt+1))
    last.raise_for_status(); return last

def period_key(v,quarter=False):
    text=clean(v)
    m=re.match(r"^(\d{4})-(\d{2})(?:-(\d{2}))?",text)
    if m:
        y,mo=int(m.group(1)),int(m.group(2)); return f"{y}-Q{(mo-1)//3+1}" if quarter else f"{y}-{mo:02d}"
    m=re.match(r"^(\d{1,2})[/-](\d{1,2})[/-](\d{4})",text)
    if m:
        mo,y=int(m.group(2)),int(m.group(3)); return f"{y}-Q{(mo-1)//3+1}" if quarter else f"{y}-{mo:02d}"
    m=re.match(r"^(Mar|Jun|Sep|Dec).*?(\d{4})",text,re.I)
    if m: return f"{m.group(2)}-Q{ {'mar':1,'jun':2,'sep':3,'dec':4}[m.group(1).lower()] }"
    return None

def abs_rows(flow,start="2015-01"):
    errors=[]
    for alias in ABS_ALIASES.get(flow,[flow]):
        url=f"{ABS_API}/ABS,{alias},1.0.0/all?startPeriod={start}&format=csvfilewithlabels&labels=both"
        try:
            r=get(url,headers={"Accept":"text/csv"}); text=r.content.decode("utf-8-sig")
            rows=list(csv.DictReader(io.StringIO(text)))
            if rows: return rows,r.url
        except Exception as e: errors.append(f"{alias}: {e}")
    raise RuntimeError("; ".join(errors))

def row_period(row):
    for k,v in row.items():
        if re.sub(r"[^A-Z0-9_]","",k.upper().split(":")[0])=="TIME_PERIOD": return clean(v)
    return ""
def row_value(row):
    for k,v in row.items():
        if re.sub(r"[^A-Z0-9_]","",k.upper().split(":")[0])=="OBS_VALUE": return num(v)
    return None
def identity(row):
    ignored={"TIME_PERIOD","OBS_VALUE","OBS_STATUS","OBS_COMMENT","UNIT_MULT","DECIMALS"}
    return "|".join(f"{k}={v}" for k,v in sorted(row.items()) if re.sub(r"[^A-Z0-9_]","",k.upper().split(":")[0]) not in ignored)

def transform_values(raw,kind):
    ordered=sorted(raw)
    if kind=="level": return raw
    if kind=="mom_diff": return {ordered[i]:raw[ordered[i]]-raw[ordered[i-1]] for i in range(1,len(ordered))}
    if kind=="yoy_pct_m": return {ordered[i]:(raw[ordered[i]]/raw[ordered[i-12]]-1)*100 for i in range(12,len(ordered)) if raw[ordered[i-12]]}
    return raw

def fetch_abs(t):
    rows,url=abs_rows(t.flow,"2014-01")
    groups={}
    for row in rows:
        p=row_period(row); v=row_value(row)
        if not p or v is None: continue
        q=t.frequency=="quarterly"
        pk=period_key(p,q)
        if pk: groups.setdefault(identity(row),{})[pk]=v
    inc=[norm(x) for x in t.include]; exc=[norm(x) for x in t.exclude]
    ranked=[]
    for key,raw in groups.items():
        txt=norm(key); vals=transform_values(raw,t.transform)
        meta=sum(1 for x in inc if all(tok in txt for tok in x.split()))*20-sum(1 for x in exc if all(tok in txt for tok in x.split()))*30
        common=set(vals)&set(t.expected)
        mae=sum(abs(vals[p]-t.expected[p]) for p in common)/len(common) if common else 1e9
        ranked.append((len(common),-mae,meta,key,vals))
    if not ranked: raise RuntimeError("No ABS candidate series")
    ranked.sort(reverse=True); matches,neg_mae,meta,key,vals=ranked[0]
    if t.expected and matches==0: raise RuntimeError("No same-period ABS candidate")
    # Numerical validation is primary, metadata prevents similarly-valued accidental matches.
    if t.expected and -neg_mae>max(.2,max(abs(x) for x in t.expected.values())*.002):
        raise RuntimeError(f"ABS value mismatch; best MAE={-neg_mae:.6g}")
    return [Point(p,v,url,"ABS SDMX CSV") for p,v in sorted(vals.items())],{"identity":key,"matches":matches,"mae":-neg_mae,"metadata_score":meta,"url":url}

def parse_rba_csv(url):
    r=get(url); rows=list(csv.reader(io.StringIO(r.content.decode("utf-8-sig"))))
    sid_row=next((i for i,row in enumerate(rows) if row and clean(row[0]).lower()=="series id"),None)
    if sid_row is None: raise RuntimeError("No Series ID row")
    ids=rows[sid_row]; titles=rows[0] if rows else []
    out=[]
    for c in range(1,len(ids)):
        vals={}
        for row in rows[sid_row+1:]:
            if len(row)<=c: continue
            p=period_key(row[0],False); v=num(row[c])
            if p and v is not None: vals[p]=v
        out.append({"id":clean(ids[c]),"title":clean(titles[c] if c<len(titles) else ""),"values":vals,"url":r.url})
    return out

def fetch_rba_exact(t):
    series=parse_rba_csv("https://www.rba.gov.au/statistics/tables/csv/e13-data.csv")
    s=next(x for x in series if x["id"].upper()==t.series_id.upper())
    vals={f"{p[:4]}-Q{(int(p[5:7])-1)//3+1}":v for p,v in s["values"].items()}
    return [Point(p,v,s["url"],f"RBA series {s['id']}") for p,v in sorted(vals.items())],s

def fetch_rba_rank(t):
    candidates=[]
    for url in RBA_STRUCTURED_URLS:
        try: candidates.extend(parse_rba_csv(url))
        except Exception: pass
    ranked=[]
    for s in candidates:
        txt=norm(s["title"]+" "+s["id"]); common=set(s["values"])&set(t.expected)
        mae=sum(abs(s["values"][p]-t.expected[p]) for p in common)/len(common) if common else 1e9
        meta=sum(20 for phrase in t.include if all(tok in txt for tok in norm(phrase).split()))-sum(30 for phrase in t.exclude if all(tok in txt for tok in norm(phrase).split()))
        ranked.append((len(common),-mae,meta,s))
    ranked.sort(reverse=True,key=lambda x:x[:3]); m,nmae,meta,s=ranked[0]
    if not m or -nmae>1.0: raise RuntimeError(f"RBA candidate mismatch MAE={-nmae}")
    return [Point(p,v,s["url"],f"RBA series {s['id']}") for p,v in sorted(s["values"].items())],s

def fetch_indeed(t):
    url="https://raw.githubusercontent.com/hiring-lab/job_postings_tracker/master/AU/aggregate_job_postings_AU.csv"
    r=get(url); rows=list(csv.DictReader(io.StringIO(r.content.decode("utf-8-sig"))))
    by_month={}
    for row in rows:
        if norm(row.get("variable"))!="total postings": continue
        p=clean(row.get("date"))[:7]; v=num(row.get("indeed_job_postings_index_SA"))
        if p and v is not None: by_month[p]=(clean(row.get("date")),v)
    vals={p:v for p,(d,v) in by_month.items()}
    return [Point(p,v,r.url,"Month-end/latest daily 7-day average") for p,v in sorted(vals.items())],{"url":r.url}

def yoy(points):
    m={p.period:p for p in points}; out=[]
    for p in sorted(m):
        y,mo=map(int,p.split("-")[:2]); prev=f"{y-1:04d}-{mo:02d}"
        if prev in m and m[prev].value:
            out.append(Point(p,(m[p].value/m[prev].value-1)*100,m[p].source_url,"Calculated YoY from official level"))
    return out

def point_date(p):
    m=re.fullmatch(r"(\d{4})-Q([1-4])",p)
    return f"{m.group(1)}-{int(m.group(2))*3:02d}-01" if m else p+"-01"

def definition(t):
    return {"id":t.id,"name":t.name,"ticker":t.ticker,"source":t.source,"frequency":t.frequency,"unit":t.unit,"color":t.color,"data":[]}

def main():
    OUT.mkdir(parents=True,exist_ok=True); DATA_FILE.parent.mkdir(parents=True,exist_ok=True)
    db=json.loads(DATA_FILE.read_text(encoding="utf-8")) if DATA_FILE.exists() else {"series":[]}
    old={x.get("id"):x for x in db.get("series",[])}; results={}; logs=[]
    for t in TARGETS:
        if t.handler=="derived_yoy": continue
        try:
            if t.handler=="abs": pts,diag=fetch_abs(t)
            elif t.handler=="indeed": pts,diag=fetch_indeed(t)
            elif t.handler=="rba_exact": pts,diag=fetch_rba_exact(t)
            elif t.handler=="rba_rank": pts,diag=fetch_rba_rank(t)
            else: raise RuntimeError("Unknown handler")
            results[t.id]=pts; (OUT/f"{t.id}_diagnostics.json").write_text(json.dumps(diag,ensure_ascii=False,indent=2,default=str),encoding="utf-8")
            logs.append({"id":t.id,"status":"OK","latest":asdict(pts[-1]) if pts else None})
        except Exception as e:
            logs.append({"id":t.id,"status":"ERROR","error":f"{type(e).__name__}: {e}"})
            # Keep historical series if a temporary upstream failure occurs.
            if t.id in old:
                results[t.id]=[Point(str(p["date"])[:7],float(p["value"]),p.get("source_url","") or "",p.get("note","") or "") for p in old[t.id].get("data",[]) if p.get("date") and p.get("value") is not None]
    results["auownerhousingyoy"]=yoy(results.get("auownerhousing",[]))
    results["auinvestorhousingyoy"]=yoy(results.get("auinvestorhousing",[]))
    new=[]
    for t in TARGETS:
        item=definition(t); prior=old.get(t.id,{}); merged={str(p.get("date"))[:7]:dict(p) for p in prior.get("data",[]) if p.get("date")}
        for p in results.get(t.id,[]): merged[point_date(p.period)[:7]]={"date":point_date(p.period),"value":float(p.value),"source_url":p.source_url,"note":p.note}
        item["data"]=[merged[k] for k in sorted(merged)]; new.append(item)
    blocks=[]
    for title,color in [("就業","#0f766e"),("家戶消費","#2563eb"),("投資 QoQ","#ea580c"),("房市","#7c3aed"),("家庭","#a21caf")]:
        blocks.append({"title":title,"color":color,"series":[t.id for t in TARGETS if t.block==title]})
    db={"generated_at":datetime.now(timezone.utc).isoformat(),"script_version":VERSION,"blocks":blocks,"series":new}
    DATA_FILE.write_text(json.dumps(db,ensure_ascii=False,indent=2),encoding="utf-8")
    (OUT/"update_summary.json").write_text(json.dumps(logs,ensure_ascii=False,indent=2),encoding="utf-8")
    MD_FILE.write_text("# 澳洲總體資料更新\n\n"+"\n".join(f"- {x['id']}: {x['status']}" for x in logs)+"\n",encoding="utf-8")
    print(json.dumps(logs,ensure_ascii=False,indent=2)); return 0 if any(x["status"]=="OK" for x in logs) else 1
if __name__=="__main__": raise SystemExit(main())
