#!/usr/bin/env python3
"""Build data/us_macro_table.md from stable US macro sources.

Priority: official machine-readable source > official downloadable file > FRED API.
Required secrets: BLS_API_KEY. Optional: FRED_API_KEY.
Prior successful observations are retained in data/us_macro_cache.json when a source fails.
"""
from __future__ import annotations

import calendar, io, json, os, re, time, zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "us_macro_table.md"
CACHE = ROOT / "data" / "us_macro_cache.json"
MONTHS = 5
BLS_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
FRED_URL = "https://api.stlouisfed.org/fred/series/observations"
UA = "USMacroDashboard/1.0 GitHub-Actions"
SESSION = requests.Session(); SESSION.headers.update({"User-Agent": UA})

@dataclass(frozen=True)
class Spec:
    section: str; name: str; ticker: str; source: str; series: str
    provider: str; source_id: str = ""; transform: str = "level"; level: int = 0

CES = [
("非農","NFP T Index","CES0000000001",0),("Private","NFP P Index","CES0500000001",1),
("Goods-producing Sector","NFP GP Index","CES0600000001",2),("Mining and Logging","USMMNATR Index","CES1000000001",3),
("Construction","USECTOT Index","CES2000000001",3),("Manufacturing","USMMMANU Index","CES3000000001",3),
("Durable goods","USEDTOT Index","CES3100000001",4),("Nondurable goods","USENTOT Index","CES3200000001",4),
("Private Service-Providing","USESPRIV Index","CES0800000001",2),("Trade, Transportation, and Utilities","NFP TTUT Index","CES4000000001",3),
("Wholesale Trade","USEWTOT Index","CES4142000001",4),("Retail Trade","USRTTOT Index","CES4200000001",4),
("Transportation and warehousing","USETTOT Index","CES4300000001",4),("Utilities","NFP UTLS Index","CES4422000001",4),
("Information","USEITOTS Index","CES5000000001",3),("Financial Activities","USEFTOT Index","CES5500000001",3),
("Professional and Business Services","USESTOT Index","CES6000000001",3),("Temporary Help Services","USESTEMP Index","CES6056132001",5),
("Education and Health Services","USEETOTS Index","CES6500000001",3),("Health care and social assistance","USEEHEAL Index","CES6562000001",4),
("Health Care","USEEHLCR Index","CES6562000101",5),("Ambulatory health care services","USEEAMBU Index","CES6562100001",6),
("Hospitals","USEEHOSP Index","CES6562200001",6),("Nursing and residential care facilities","USEENURS Index","CES6562300001",6),
("Social assistance","USEESOCA Index","CES6562400001",5),("Leisure and Hospitality","USEHTOTS Index","CES7000000001",3),
("Other Services","USEOTOTS Index","CES8000000001",3),]

SPECS = []
for name,ticker,sid,level in CES:
    SPECS.append(Spec("就業-就業（人數，千人）",name,ticker,"Bureau of Labor Statistics",sid,"bls",sid,"level",level))
for name,ticker,sid,level in CES:
    SPECS.append(Spec("就業-就業（月增減，千人）",name,ticker,"Bureau of Labor Statistics",sid,"bls",sid,"change",level))

for x in [
("Multiple Jobholder","USMJTMJS Index","LNS12026619"),("失業率","USURTOT Index","LNS14000000"),
("Labor Force","USLFTOT Index","LNS11000000"),("Employed","USEMTOT Index","LNS12000000"),
("Unemployed","USUETOT Index","LNS13000000"),("Employed to Unemployed","BLSFE2UN Index","LNS17400000"),
("Unemployed to Unemployed","BLSFU2U Index","LNS17500000"),("Not in Labor Force to Unemployed","BLSFN2UN Index","LNS17600000"),
("On temporary layoff","USJLTEMP Index","LNS13023653"),("Permanent Job Losers","USJLPJLS Index","LNS13026638"),
("Completed Temp Job","USJLPTJS Index","LNS13026637"),("Job leavers","USJLJOBL Index","LNS13023705"),
("Reentrants","USJLREEN Index","LNS13023557"),("New entrants","USJLNENT Index","LNS13023569"),
("平均失業Duration","USDUMEAN Index","LNS13008275")]:
    SPECS.append(Spec("就業-失業",x[0],x[1],"Bureau of Labor Statistics",x[2],"bls",x[2]))
for name,ticker,sid in [("JOLTS","JOLTTOTL Index","JTS000000000000000JOL"),("Quit Rate","JOLTQUIS Index","JTS000000000000000QUR"),("Layoff Rate","JOLTLAYS Index","JTS000000000000000LDR")]:
    SPECS.append(Spec("就業-職缺",name,ticker,"Bureau of Labor Statistics",sid,"bls",sid))
SPECS.append(Spec("就業-職缺","職缺/失業人口","Derived","Derived","JOLTS / Unemployed","derived","vacancy_ratio"))
SPECS += [
Spec("就業-薪水","時薪 MoM%","AHE MOM% Index","Bureau of Labor Statistics","CES0500000003","bls","CES0500000003","mom_pct"),
Spec("就業-薪水","Atlanta Fed Job Switcher薪資","WGTRJBSW Index","Federal Reserve Bank of Atlanta","Job switcher","atlanta","switcher"),
Spec("就業-薪水","Atlanta Fed Job Stayer薪資","WGTRJBSY Index","Federal Reserve Bank of Atlanta","Job stayer","atlanta","stayer"),
Spec("就業-薪水","Atlanta Fed最低25%薪資","WGTRQUA1 Index","Federal Reserve Bank of Atlanta","1st wage quartile","atlanta","q1"),
Spec("就業-薪水","Atlanta Fed 50%薪資","WGTRQUA2 Index","Federal Reserve Bank of Atlanta","2nd wage quartile","atlanta","q2"),
Spec("就業-薪水","Atlanta Fed 75%薪資","WGTRQUA3 Index","Federal Reserve Bank of Atlanta","3rd wage quartile","atlanta","q3"),
Spec("就業-薪水","Atlanta Fed最高25%薪資","WGTRQUA4 Index","Federal Reserve Bank of Atlanta","4th wage quartile","atlanta","q4"),
Spec("就業-薪水","ADP Pay Job Changers薪資","ADPUJCPG Index","ADP Research","Median YoY job changers","adp","changer"),
Spec("就業-薪水","ADP Pay Job Stayers薪資","ADPUJSPG Index","ADP Research","Median YoY job stayers","adp","stayer"),]

# BLS price series. YoY uses official unadjusted indexes; PPI uses SA index and YoY.
for name,ticker,sid,transform in [
("Core CPI","CPI XYOY Index","CUUR0000SA0L1E","yoy_pct"),("Core Goods","CPRPCXYY Index","CUUR0000SACL1E","yoy_pct"),
("Core Services","CPRPSXYY Index","CUUR0000SASLE","yoy_pct"),("SuperCore","CPUPNFEY Index","CUUR0000SASL2RS","yoy_pct"),
("Core PPI","FDIUSGYO Index","WPSFD49116","yoy_pct")]:
    SPECS.append(Spec("物價",name,ticker,"Bureau of Labor Statistics",sid,"bls",sid,transform))
SPECS.append(Spec("物價","US Zillow Rent Index All Homes MoM Smoothed SA","ZRIOAMOM Index","Zillow Research","National ZORI SA MoM","zillow","zori_mom"))

# FRED is used only where the primary publisher has no stable open API used here.
for section,name,ticker,source,fred_id,transform in [
("物價","密大1y通膨預期","CONSPXMD Index","University of Michigan","MICH","level"),
("物價","密大5~10y通膨預期","CONSP5MD Index","University of Michigan","MICH5E","level"),
("消費","Real Personal Spending","PCE CHY% Index","Bureau of Economic Analysis","PCEC96","yoy_pct"),
("消費","disposable personal income","PIDSDI Index","Bureau of Economic Analysis","DSPI","level"),
("消費","Personal Outlays","PIDSSO Index","Bureau of Economic Analysis","A068RC1M027SBEA","level"),
("消費","Personal Saving","PIDSS Index","Bureau of Economic Analysis","PSAVE","level"),
("消費","Interest Paid","PIDSINT Index","Bureau of Economic Analysis","B069RC1M027SBEA","level"),
("消費","密大","CONSSENT Index","University of Michigan","UMCSENT","level")]:
    SPECS.append(Spec(section,name,ticker,source,fred_id,"fred",fred_id,transform))

# Official downloadable/page sources. These parsers report unavailable rather than silently substituting a different concept.
for name,ticker,key in [("NY FED 1y通膨預期","NYCNM1IR Index","one_year"),("NY FED 5y通膨預期","NYCN5IMD Index","five_year")]:
    SPECS.append(Spec("物價",name,ticker,"Federal Reserve Bank of New York","Survey of Consumer Expectations","nyfed",key))
for section,name,ticker,key in [
("就業-調查","ISM服務就業","NAPMNEMP Index","services_employment"),("就業-調查","ISM製造就業","NAPMEMPL Index","manufacturing_employment"),
("物價","ISM製造價格","NAPMPRIC Index","manufacturing_prices"),("物價","ISM服務價格","NAPMNPRC Index","services_prices"),
("企業調查","ISM製造","NAPMPMI Index","manufacturing_pmi"),("企業調查","ISM服務","NAPMNMI Index","services_pmi")]:
    SPECS.append(Spec(section,name,ticker,"Institute for Supply Management","Official monthly report","ism",key))
SPECS += [
Spec("就業-調查","中小企hiring plan","SBOIHIRE Index","NFIB","Plans to Increase Employment","nfib","hiring_plan"),
Spec("就業-調查","自願離職調查","NYCNJSJV Index","Federal Reserve Bank of New York","Job Separation Leaving a Job","nyfed","job_separation"),
Spec("就業-調查","Job Plentiful","CONCJOBP Index","The Conference Board","Jobs plentiful","conference","plentiful"),
Spec("就業-調查","Job Hard to get","CONCJOBH Index","The Conference Board","Jobs hard to get","conference","hard"),
Spec("消費","家戶金融狀況vs一年前","CONSPAGI Index","University of Michigan","PAGO_R_ALL","umich","pago"),
Spec("消費","預計未來一年金融狀況","CONSEXFI Index","University of Michigan","PEXP_R_ALL","umich","pexp"),
Spec("消費","CB","CONCCONF Index","The Conference Board","Consumer Confidence Index","conference","confidence"),
Spec("消費","零售控制 MoM%","RSTAXAGM Index","U.S. Census Bureau","MRTS control group","census","retail_control"),]

def month_key(year:int, month:int)->str: return f"{year:04d}-{month:02d}"
def month_end(period:str)->str:
    y,m=map(int,period.split("-")); return f"{y:04d}/{m:02d}/{calendar.monthrange(y,m)[1]:02d}"
def num(x):
    try: return float(str(x).replace(",", "").replace("%", "").strip())
    except: return None

def request_json(url, **kwargs):
    for attempt in range(3):
        try:
            r=SESSION.get(url,timeout=60,**kwargs); r.raise_for_status(); return r.json()
        except Exception:
            if attempt==2: raise
            time.sleep(2**attempt)

def fetch_bls(ids:list[str])->dict[str,dict[str,float]]:
    out={}; key=os.getenv("BLS_API_KEY","").strip(); batch=50 if key else 25
    now=datetime.now(timezone.utc).year
    for i in range(0,len(ids),batch):
        payload={"seriesid":ids[i:i+batch],"startyear":str(now-3),"endyear":str(now),"calculations":False,"annualaverage":False,"catalog":True}
        if key: payload["registrationkey"]=key
        r=SESSION.post(BLS_URL,json=payload,timeout=90); r.raise_for_status(); data=r.json()
        if data.get("status")!="REQUEST_SUCCEEDED": raise RuntimeError(data.get("message"))
        for s in data["Results"]["series"]:
            vals={}
            for d in s.get("data",[]):
                p=str(d.get("period",""))
                if p.startswith("M") and p != "M13":
                    v=num(d.get("value"));
                    if v is not None: vals[month_key(int(d["year"]),int(p[1:]))]=v
            out[s["seriesID"]]=vals
    return out

def transform(vals:dict[str,float], mode:str)->dict[str,float]:
    keys=sorted(vals); result={}
    if mode=="level": return vals
    for i,k in enumerate(keys):
        if i==0: continue
        y,m=map(int,k.split("-")); py,pm=(y-1,12) if m==1 else (y,m-1); prev=month_key(py,pm)
        if mode=="change" and prev in vals: result[k]=round(vals[k]-vals[prev],3)
        if mode=="mom_pct" and prev in vals and vals[prev]: result[k]=round((vals[k]/vals[prev]-1)*100,3)
        yoy=month_key(y-1,m)
        if mode=="yoy_pct" and yoy in vals and vals[yoy]: result[k]=round((vals[k]/vals[yoy]-1)*100,3)
    return result

def fetch_fred(series_id:str)->dict[str,float]:
    key=os.getenv("FRED_API_KEY","").strip()
    if not key: raise RuntimeError("Missing FRED_API_KEY")
    params={"series_id":series_id,"api_key":key,"file_type":"json","observation_start":f"{datetime.now().year-3}-01-01"}
    data=request_json(FRED_URL,params=params); out={}
    for d in data.get("observations",[]):
        v=num(d.get("value"));
        if v is not None: out[d["date"][:7]]=v
    return out

def fetch_atlanta()->dict[str,dict[str,float]]:
    url="https://www.atlantafed.org/-/media/Project/Atlanta/FRBA/Documents/datafiles/chcs/wage-growth-tracker/wage-growth-data.xlsx"
    r=SESSION.get(url,timeout=90); r.raise_for_status(); book=pd.ExcelFile(io.BytesIO(r.content))
    aliases={"switcher":["job switcher"],"stayer":["job stayer"],"q1":["1st quartile","first quartile"],"q2":["2nd quartile","second quartile"],"q3":["3rd quartile","third quartile"],"q4":["4th quartile","fourth quartile"]}
    result={k:{} for k in aliases}
    for sheet in book.sheet_names:
        raw=pd.read_excel(book,sheet_name=sheet,header=None)
        for header in range(min(12,len(raw))):
            df=pd.read_excel(book,sheet_name=sheet,header=header)
            date_col=next((c for c in df.columns if "date" in str(c).lower()),None)
            if date_col is None: continue
            dates=pd.to_datetime(df[date_col],errors="coerce")
            if dates.notna().sum()<3: continue
            for key,words in aliases.items():
                col=next((c for c in df.columns if any(w in str(c).lower() for w in words)),None)
                if col is not None:
                    for d,v in zip(dates,df[col]):
                        n=num(v)
                        if pd.notna(d) and n is not None: result[key][d.strftime("%Y-%m")]=n
    return result

def fetch_zillow()->dict[str,float]:
    url="https://files.zillowstatic.com/research/public_csvs/zori/Metro_zori_uc_sfrcondomfr_sm_sa_month.csv"
    df=pd.read_csv(url); row=df[df["RegionName"].astype(str).str.lower().isin(["united states","united states of america"])]
    if row.empty: row=df.iloc[[0]]
    vals={}
    for c in df.columns:
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}",str(c)):
            v=num(row.iloc[0][c]);
            if v is not None: vals[c[:7]]=v
    return transform(vals,"mom_pct")

def fetch_adp()->dict[str,dict[str,float]]:
    html=SESSION.get("https://adpemploymentreport.com/",timeout=60).text
    m=re.search(r'https://adpemploymentreport\.com/artifacts/us_ner/\d+/ADP_NER_history\.zip',html)
    if not m: raise RuntimeError("ADP history link not found")
    r=SESSION.get(m.group(0),timeout=90); r.raise_for_status(); z=zipfile.ZipFile(io.BytesIO(r.content))
    result={"changer":{},"stayer":{}}
    for name in z.namelist():
        if not name.lower().endswith(".csv"): continue
        df=pd.read_csv(z.open(name))
        cols={str(c).lower():c for c in df.columns}; date=next((c for c in df.columns if "date" in str(c).lower()),None)
        if date is None: continue
        for key,needles in {"changer":["changer","job changer"],"stayer":["stayer","job stayer"]}.items():
            col=next((c for c in df.columns if any(n in str(c).lower() for n in needles) and "pay" in str(c).lower()),None)
            if col is None: continue
            for d,v in zip(pd.to_datetime(df[date],errors="coerce"),df[col]):
                n=num(v)
                if pd.notna(d) and n is not None: result[key][d.strftime("%Y-%m")]=n
    return result

def fetch_page_latest()->dict[tuple[str,str],dict[str,float]]:
    """Official-page latest values. Full history remains in cache when publisher offers no open history API."""
    out={}; now=datetime.now(); period=f"{now.year:04d}-{now.month:02d}"
    pages={
      "nfib":SESSION.get("https://nfib-sbet.org/MainPage.html",timeout=60).text,
      "conference":SESSION.get("https://www.conference-board.org/topics/consumer-confidence/index.cfm",timeout=60).text,
      "ism":SESSION.get("https://www.ismworld.org/",timeout=60).text,
      "nyfed":SESSION.get("https://www.newyorkfed.org/microeconomics/sce",timeout=60).text,
    }
    patterns=[
      (("nfib","hiring_plan"),r"Plans to Increase Employment\D{0,80}(-?\d+(?:\.\d+)?)"),
      (("conference","confidence"),r"Consumer Confidence Index[^\d]{0,100}(?:decreased|increased).*?to\s+(\d+(?:\.\d+)?)"),
      (("conference","hard"),r"jobs[^\n]{0,40}hard to get[^\d]{0,80}(\d+(?:\.\d+)?)"),
      (("nyfed","one_year"),r"one-year ahead[^\d]{0,100}(\d+(?:\.\d+)?)\s*percent"),
      (("nyfed","five_year"),r"five-year-ahead[^\d]{0,100}(\d+(?:\.\d+)?)\s*percent"),
      (("ism","services_pmi"),r"Services PMI[^\d]{0,100}(\d+(?:\.\d+)?)%"),]
    for (provider,key),pat in patterns:
        m=re.search(pat,pages[provider],re.I|re.S)
        if m: out[(provider,key)]={period:float(m.group(1))}
    return out

def merge(old,new):
    x=dict(old or {}); x.update(new or {}); return dict(sorted(x.items()))
def fmt(v):
    if v is None: return "N/A"
    if abs(v-round(v))<1e-9: return str(int(round(v)))
    return f"{v:.3f}".rstrip("0").rstrip(".")

def main():
    OUT.parent.mkdir(parents=True,exist_ok=True)
    cache=json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {"series":{}}
    old=cache.get("series",{}); current={}; errors=[]
    bls_ids=sorted({s.source_id for s in SPECS if s.provider=="bls"})
    try: bls=fetch_bls(bls_ids)
    except Exception as e: bls={}; errors.append(f"BLS: {e}")
    try: atl=fetch_atlanta()
    except Exception as e: atl={}; errors.append(f"Atlanta Fed: {e}")
    try: adp=fetch_adp()
    except Exception as e: adp={}; errors.append(f"ADP: {e}")
    try: zori=fetch_zillow()
    except Exception as e: zori={}; errors.append(f"Zillow: {e}")
    try: pages=fetch_page_latest()
    except Exception as e: pages={}; errors.append(f"Official pages: {e}")
    for s in SPECS:
        key=f"{s.section}|{s.name}"
        try:
            if s.provider=="bls": vals=transform(bls.get(s.source_id,{}),s.transform)
            elif s.provider=="fred": vals=transform(fetch_fred(s.source_id),s.transform)
            elif s.provider=="atlanta": vals=atl.get(s.source_id,{})
            elif s.provider=="adp": vals=adp.get(s.source_id,{})
            elif s.provider=="zillow": vals=zori
            elif s.provider in {"ism","nfib","conference","nyfed"}: vals=pages.get((s.provider,s.source_id),{})
            else: vals={}
            current[key]=merge(old.get(key,{}),vals)
        except Exception as e:
            current[key]=old.get(key,{})
            errors.append(f"{s.name}: {e}")
    # Derived vacancy/unemployment ratio from levels.
    jolts=current.get("就業-職缺|JOLTS",{}); unemployed=current.get("就業-失業|Unemployed",{})
    current["就業-職缺|職缺/失業人口"]=merge(old.get("就業-職缺|職缺/失業人口",{}),{k:round(jolts[k]/unemployed[k],7) for k in jolts.keys()&unemployed.keys() if unemployed[k]})
    cache={"updated_at_utc":datetime.now(timezone.utc).isoformat(),"series":current,"errors":errors}
    CACHE.write_text(json.dumps(cache,ensure_ascii=False,indent=2),encoding="utf-8")
    all_periods=sorted({p for values in current.values() for p in values})[-MONTHS:]
    lines=["# 美國總體經濟數據", "", f"> 更新時間：{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}  ", "> 日期為資料所屬月份月底。N/A 代表該月份尚未發布，或官方來源未提供可穩定自動下載的歷史值。", ""]
    for section in dict.fromkeys(s.section for s in SPECS):
        rows=[s for s in SPECS if s.section==section]
        lines += [f"## {section}","", "| 指標 | Bloomberg | 最新資料月份 | 來源 | 官方序列 / 定義 | " + " | ".join(month_end(p) for p in reversed(all_periods)) + " |", "|---|---|---:|---|---|"+"---:|"*len(all_periods)]
        for s in rows:
            vals=current.get(f"{s.section}|{s.name}",{}); latest=max(vals) if vals else None
            display="&nbsp;"*(s.level*4)+s.name
            lines.append("| " + " | ".join([display,s.ticker,month_end(latest) if latest else "N/A",s.source,s.series]+[fmt(vals.get(p)) for p in reversed(all_periods)]) + " |")
        lines.append("")
    if errors:
        lines += ["## 更新警告","", *[f"- {e}" for e in errors],""]
    lines += ["## 來源策略","", "- BLS：Public Data API v2，涵蓋 CES、CPS、JOLTS、CPI、PPI。", "- Atlanta Fed、ADP、Zillow：優先使用官方 XLSX、ZIP/CSV。", "- BEA 與密大公開序列：使用 FRED API，需設定 `FRED_API_KEY`。", "- ISM、NFIB、紐約聯準銀行與 Conference Board：只補官方頁面可穩定辨識的最新值；未提供開放歷史 API 的月份不臆造，並保留先前成功資料。", ""]
    OUT.write_text("\n".join(lines),encoding="utf-8")
    print(f"Wrote {OUT} with {len(SPECS)} rows; warnings={len(errors)}")

if __name__=="__main__": main()
