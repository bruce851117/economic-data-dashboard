#!/usr/bin/env python3
"""Build data/us_macro_table.md from stable US macro sources.

Priority: official machine-readable source > official downloadable file > FRED API.
Required secrets: BLS_API_KEY. Optional: FRED_API_KEY.
Prior successful observations are retained in data/us_macro_cache.json when a source fails.
"""
from __future__ import annotations

import calendar, io, json, os, re, time, zipfile
from urllib.parse import urljoin
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
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
CENSUS_MARTS_URL = "https://api.census.gov/data/timeseries/eits/marts"
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

# BLS price series. YoY uses official unadjusted indexes. Core PPI is final demand less foods and energy.
for name,ticker,sid,transform in [
("Core CPI","CPI XYOY Index","CUUR0000SA0L1E","yoy_pct"),("Core Goods","CPRPCXYY Index","CUUR0000SACL1E","yoy_pct"),
("Core Services","CPRPSXYY Index","CUUR0000SASLE","yoy_pct"),("Core Services less Shelter","CPUPNFEY Index","CUUR0000SASL2RS","yoy_pct"),
("Core PPI","FDIUSGYO Index","WPUFD49104","yoy_pct")]:
    SPECS.append(Spec("物價",name,ticker,"Bureau of Labor Statistics",sid,"bls",sid,transform))
SPECS.append(Spec("物價","US Zillow Rent Index All Homes MoM Smoothed SA","ZRIOAMOM Index","Zillow Research","National ZORI SA MoM","zillow","zori_mom"))

# University of Michigan public CSV files are the primary source for sentiment and inflation expectations.
SPECS += [
    Spec("物價", "密大1y通膨預期", "CONSPXMD Index", "University of Michigan", "PX_MD", "umich_csv", "px1"),
    Spec("物價", "密大5~10y通膨預期", "CONSP5MD Index", "University of Michigan", "PX5_MD", "umich_csv", "px5"),
    Spec("消費", "密大", "CONSSENT Index", "University of Michigan", "ICS_ALL", "umich_csv", "sentiment"),
]

# FRED is retained for BEA series where it is already working.
for section,name,ticker,source,fred_id,transform in [
("消費","Real Personal Spending","PCE CHY% Index","Bureau of Economic Analysis","PCEC96","yoy_pct"),
("消費","disposable personal income","PIDSDI Index","Bureau of Economic Analysis","DSPI","level"),
("消費","Personal Outlays","PIDSSO Index","Bureau of Economic Analysis","A068RC1","level"),
("消費","Personal Saving","PIDSS Index","Bureau of Economic Analysis","PSAVE","level"),
("消費","Interest Paid","PIDSINT Index","Bureau of Economic Analysis","B069RC1","level"),
]:
    SPECS.append(Spec(section,name,ticker,source,fred_id,"fred",fred_id,transform))

# Official downloadable/page sources. These parsers report unavailable rather than silently substituting a different concept.
for name,ticker,key,series_name in [
    ("NY FED 1y通膨預期","NYCNM1IR Index","one_year","Median one-year ahead expected inflation rate"),
    ("NY FED 5y通膨預期","NYCN5IMD Index","five_year","Median five-year ahead expected inflation rate"),
]:
    SPECS.append(Spec("物價",name,ticker,"Federal Reserve Bank of New York",series_name,"nyfed_xlsx",key))
for section,name,ticker,key in [
("就業-調查","ISM服務就業","NAPMNEMP Index","services_employment"),("就業-調查","ISM製造就業","NAPMEMPL Index","manufacturing_employment"),
("物價","ISM製造價格","NAPMPRIC Index","manufacturing_prices"),("物價","ISM服務價格","NAPMNPRC Index","services_prices"),
("企業調查","ISM製造","NAPMPMI Index","manufacturing_pmi"),("企業調查","ISM服務","NAPMNMI Index","services_pmi")]:
    SPECS.append(Spec(section,name,ticker,"Institute for Supply Management","Official monthly report","ism",key))
SPECS += [
Spec("就業-調查","中小企hiring plan","SBOIHIRE Index","NFIB","Plans to Increase Employment","nfib","hiring_plan"),
Spec("就業-調查","失去工作機率調查","NYCNJSLJ Index","Federal Reserve Bank of New York","Mean probability of losing a job","nyfed_xlsx","job_loss"),
Spec("就業-調查","自願離職調查","NYCNJSJV Index","Federal Reserve Bank of New York","Mean probability of leaving a job voluntarily","nyfed_xlsx","job_separation"),
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

def _period_value_map(frame, date_column, value_column):
    result = {}
    dates = pd.to_datetime(frame[date_column], errors="coerce")
    values = pd.to_numeric(frame[value_column], errors="coerce")
    for date, value in zip(dates, values):
        if pd.notna(date) and pd.notna(value):
            result[date.strftime("%Y-%m")] = float(value)
    return result


def _parse_atlanta_workbook(content):
    """Parse the current Atlanta Fed Wage Growth Tracker workbook."""
    workbook = pd.ExcelFile(io.BytesIO(content))
    required_sheets = {"data_overall", "Average Wage Quartile"}
    missing = required_sheets.difference(workbook.sheet_names)
    if missing:
        raise RuntimeError("Atlanta Fed workbook missing sheets: " + ", ".join(sorted(missing)))

    overall = pd.read_excel(workbook, sheet_name="data_overall", header=1)
    overall_date = overall.columns[0]
    for column in ("Job Stayer", "Job Switcher"):
        if column not in overall.columns:
            raise RuntimeError(f"Atlanta Fed data_overall missing column: {column}")

    quartiles = pd.read_excel(workbook, sheet_name="Average Wage Quartile", header=2)
    quartile_date = quartiles.columns[0]
    quartile_columns = {
        "q1": "Lowest quartile of wage distribution",
        "q2": "2nd quartile of wage distribution",
        "q3": "3rd quartile of wage distribution",
        "q4": "Highest quartile of wage distribution",
    }
    for column in quartile_columns.values():
        if column not in quartiles.columns:
            raise RuntimeError(f"Atlanta Fed quartile sheet missing column: {column}")

    result = {
        "switcher": _period_value_map(overall, overall_date, "Job Switcher"),
        "stayer": _period_value_map(overall, overall_date, "Job Stayer"),
    }
    for key, column in quartile_columns.items():
        result[key] = _period_value_map(quartiles, quartile_date, column)
    empty = [key for key, values in result.items() if not values]
    if empty:
        raise RuntimeError("Atlanta Fed returned no usable data for: " + ", ".join(empty))
    return result


def fetch_atlanta():
    url = (
        "https://www.atlantafed.org/-/media/Project/Atlanta/FRBA/Documents/"
        "datafiles/chcs/wage-growth-tracker/wage-growth-data.xlsx"
    )
    response = SESSION.get(url, timeout=90)
    response.raise_for_status()
    return _parse_atlanta_workbook(response.content)

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

def _parse_adp_pay_history(content):
    frame = pd.read_csv(io.BytesIO(content))
    required = {"timestep", "agg", "category", "date", "median pay change"}
    missing = required.difference(frame.columns)
    if missing:
        raise RuntimeError("ADP history missing columns: " + ", ".join(sorted(missing)))

    selected = frame[
        frame["timestep"].astype(str).str.upper().eq("M")
        & frame["agg"].astype(str).str.strip().str.casefold().eq("worker type")
    ].copy()
    selected["date"] = pd.to_datetime(selected["date"], errors="coerce")
    selected["median pay change"] = pd.to_numeric(selected["median pay change"], errors="coerce")
    result = {"changer": {}, "stayer": {}}
    for category, key in (("job changer", "changer"), ("job stayer", "stayer")):
        rows = selected[selected["category"].astype(str).str.strip().str.casefold().eq(category)]
        for date, value in zip(rows["date"], rows["median pay change"]):
            if pd.notna(date) and pd.notna(value):
                result[key][date.strftime("%Y-%m")] = float(value)
    empty = [key for key, values in result.items() if not values]
    if empty:
        raise RuntimeError("ADP Pay Insights returned no usable data for: " + ", ".join(empty))
    return result


def _adp_history_links(html, page_url):
    """Discover ADP_PAY_history.zip without assuming the dated directory name."""
    decoded = html.replace("\\/", "/").replace("&amp;", "&")
    patterns = [
        r'''href\s*=\s*["']([^"']*ADP_PAY_history\.zip(?:\?[^"']*)?)["']''',
        r'''((?:https?:)?//[^\s"']+/artifacts/us_wage/\d{8}/ADP_PAY_history\.zip)''',
        r'''(/artifacts/us_wage/\d{8}/ADP_PAY_history\.zip)''',
    ]
    links = []
    for pattern in patterns:
        for href in re.findall(pattern, decoded, flags=re.IGNORECASE):
            absolute = urljoin(page_url, href)
            if absolute not in links:
                links.append(absolute)

    # Prefer the newest official dated directory when more than one link is embedded.
    def release_date(url):
        match = re.search(r"/us_wage/(\d{8})/ADP_PAY_history\.zip", url, flags=re.I)
        return match.group(1) if match else "00000000"
    return sorted(links, key=release_date, reverse=True)


def _adp_fallback_links(page_url):
    """Last-resort dated candidates. The date is discovered by probing recent calendar dates, not hard-coded."""
    today = datetime.now(timezone.utc).date()
    return [
        urljoin(page_url, f"/artifacts/us_wage/{(today - timedelta(days=offset)):%Y%m%d}/ADP_PAY_history.zip")
        for offset in range(0, 15)
    ]


def fetch_adp():
    page_url = "https://payinsights.adp.com/"
    browser_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": page_url,
    }
    page = SESSION.get(page_url, headers=browser_headers, timeout=60)
    page.raise_for_status()
    links = _adp_history_links(page.text, page_url)
    if not links:
        links = _adp_fallback_links(page_url)

    failures = []
    for link in links:
        try:
            response = SESSION.get(
                link,
                headers={
                    **browser_headers,
                    "Accept": "application/zip,application/octet-stream,*/*;q=0.8",
                    "Referer": page_url,
                },
                timeout=90,
            )
            response.raise_for_status()
            if not response.content.startswith(b"PK"):
                raise RuntimeError(f"response is not a ZIP file ({response.headers.get('content-type')})")
            with zipfile.ZipFile(io.BytesIO(response.content)) as archive:
                candidates = [
                    name for name in archive.namelist()
                    if Path(name).name.casefold() == "adp_pay_history.csv"
                ]
                if not candidates:
                    candidates = [
                        name for name in archive.namelist()
                        if name.lower().endswith(".csv")
                        and "pay" in Path(name).name.lower()
                        and "history" in Path(name).name.lower()
                    ]
                if not candidates:
                    raise RuntimeError("ADP_PAY_history.csv not found inside ZIP")
                return _parse_adp_pay_history(archive.read(candidates[0]))
        except Exception as error:
            failures.append(f"{link}: {error}")
    raise RuntimeError("ADP Pay Insights ZIP could not be parsed; " + " | ".join(failures))


def _parse_month_name_period(month_value, year_value):
    month_text = str(month_value).strip().title()
    if month_text not in calendar.month_name:
        return None
    return month_key(int(year_value), list(calendar.month_name).index(month_text))


def fetch_umichigan_csv():
    """Fetch official University of Michigan sentiment and inflation-expectation CSV files."""
    urls = {
        "sentiment": "https://www.sca.isr.umich.edu/files/tbmics.csv",
        "inflation": "https://www.sca.isr.umich.edu/files/tbmpx1px5.csv",
    }
    frames = {}
    for key, url in urls.items():
        response = SESSION.get(url, timeout=90)
        response.raise_for_status()
        frames[key] = pd.read_csv(io.BytesIO(response.content))

    result = {"sentiment": {}, "px1": {}, "px5": {}}
    sentiment = frames["sentiment"]
    inflation = frames["inflation"]
    required_sentiment = {"Month", "YYYY", "ICS_ALL"}
    required_inflation = {"Month", "YYYY", "PX_MD", "PX5_MD"}
    if not required_sentiment.issubset(sentiment.columns):
        raise RuntimeError(f"Michigan sentiment CSV missing columns: {sorted(required_sentiment - set(sentiment.columns))}")
    if not required_inflation.issubset(inflation.columns):
        raise RuntimeError(f"Michigan inflation CSV missing columns: {sorted(required_inflation - set(inflation.columns))}")

    for _, row in sentiment.iterrows():
        period = _parse_month_name_period(row["Month"], row["YYYY"])
        value = num(row["ICS_ALL"])
        if period and value is not None:
            result["sentiment"][period] = value

    for _, row in inflation.iterrows():
        period = _parse_month_name_period(row["Month"], row["YYYY"])
        if not period:
            continue
        one_year = num(row["PX_MD"])
        long_run = num(row["PX5_MD"])
        if one_year is not None:
            result["px1"][period] = one_year
        if long_run is not None:
            result["px5"][period] = long_run

    empty = [key for key, values in result.items() if not values]
    if empty:
        raise RuntimeError("Michigan CSV returned no usable data for: " + ", ".join(empty))
    return result


ISM_REPORT_BASE = "https://www.ismworld.org/supply-management-news-and-reports/reports/ism-pmi-reports"


def _month_candidates(count=8):
    today = datetime.now(timezone.utc).date().replace(day=1)
    candidates = []
    year, month = today.year, today.month
    for _ in range(count):
        candidates.append((year, month, calendar.month_name[month].lower()))
        month -= 1
        if month == 0:
            year -= 1
            month = 12
    return candidates


def _plain_html(html):
    text = re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.I | re.S)
    text = re.sub(r"<style[^>]*>.*?</style>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _ism_number(text, patterns, label):
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.I | re.S)
        if match:
            return float(match.group(1))
    raise RuntimeError(f"ISM {label} value not found")


def _parse_ism_report(html, sector, expected_year, expected_month):
    text = _plain_html(html)
    month_name = calendar.month_name[expected_month]
    if not re.search(rf"\b{month_name}\s+{expected_year}\b|\b{month_name}\b", text, flags=re.I):
        raise RuntimeError(f"ISM report does not identify {month_name} {expected_year}")

    if sector == "manufacturing":
        pmi = _ism_number(text, [
            r"Manufacturing PMI(?:®)?\s+(?:registered|at)\s+(\d+(?:\.\d+)?)\s*percent",
            r"Manufacturing PMI(?:®)?\s+at\s+(\d+(?:\.\d+)?)%",
        ], "Manufacturing PMI")
        employment = _ism_number(text, [
            r"Employment Index(?: reading)?(?: of)?\s+(\d+(?:\.\d+)?)\s*percent",
            r"Employment Index\s+(?:registered|at)\s+(\d+(?:\.\d+)?)\s*percent",
        ], "Manufacturing Employment")
        return {"manufacturing_pmi": pmi, "manufacturing_employment": employment}

    pmi = _ism_number(text, [
        r"Services PMI(?:®)?\s+(?:registered|at)\s+(\d+(?:\.\d+)?)\s*percent",
        r"Services PMI(?:®)?\s+at\s+(\d+(?:\.\d+)?)%",
    ], "Services PMI")
    employment = _ism_number(text, [
        r"Employment Index(?: returned[^.]{0,120}?with a reading of| registered| at)\s+(\d+(?:\.\d+)?)\s*percent",
        r"Employment Index[^.]{0,160}?reading of\s+(\d+(?:\.\d+)?)\s*percent",
    ], "Services Employment")
    return {"services_pmi": pmi, "services_employment": employment}


def fetch_ism_official():
    """Fetch recent Manufacturing and Services PMI/Employment values from ISM official monthly reports."""
    result = {
        "manufacturing_pmi": {},
        "manufacturing_employment": {},
        "services_pmi": {},
        "services_employment": {},
    }
    failures = []
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "text/html,application/xhtml+xml"}
    for year, month, slug in _month_candidates(8):
        period = month_key(year, month)
        for sector, path in (("manufacturing", "pmi"), ("services", "services")):
            url = f"{ISM_REPORT_BASE}/{path}/{slug}/"
            try:
                response = SESSION.get(url, headers=headers, timeout=60)
                response.raise_for_status()
                parsed = _parse_ism_report(response.text, sector, year, month)
                for key, value in parsed.items():
                    result[key][period] = value
            except Exception as error:
                failures.append(f"{sector} {period}: {error}")

    if not any(result.values()):
        raise RuntimeError("All ISM official monthly reports failed; " + " | ".join(failures))
    return result


CENSUS_CONTROL_CATEGORIES = {
    "total": "44X72",
    "motor_vehicles": "441",
    "gasoline": "447",
    "building_materials": "444",
    "food_services": "722",
}


def _parse_census_marts_rows(payload):
    if not isinstance(payload, list) or len(payload) < 2:
        raise RuntimeError("Census MARTS returned no data rows")
    headers = payload[0]
    required = {"cell_value", "category_code", "data_type_code", "seasonally_adj", "time"}
    missing = required.difference(headers)
    if missing:
        raise RuntimeError("Census MARTS missing fields: " + ", ".join(sorted(missing)))
    indexes = {name: headers.index(name) for name in required}
    values = {name: {} for name in CENSUS_CONTROL_CATEGORIES}
    reverse_codes = {code: name for name, code in CENSUS_CONTROL_CATEGORIES.items()}

    for row in payload[1:]:
        category = str(row[indexes["category_code"]]).strip()
        key = reverse_codes.get(category)
        if not key:
            continue
        if str(row[indexes["data_type_code"]]).strip().upper() != "SM":
            continue
        if str(row[indexes["seasonally_adj"]]).strip().lower() not in {"yes", "true", "1"}:
            continue
        period_match = re.search(r"(20\d{2})-(0[1-9]|1[0-2])", str(row[indexes["time"]]))
        value = num(row[indexes["cell_value"]])
        if period_match and value is not None:
            values[key][f"{period_match.group(1)}-{period_match.group(2)}"] = value
    return values


def fetch_census_retail_control():
    """Retail control group level and MoM%, calculated from Census MARTS seasonally adjusted monthly sales."""
    api_key = os.getenv("CENSUS_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("Missing CENSUS_API_KEY")
    start_year = datetime.now(timezone.utc).year - 3
    params = {
        "get": "cell_value,data_type_code,category_code,seasonally_adj,time",
        "time": f"from {start_year}-01",
        "data_type_code": "SM",
        "key": api_key,
    }
    payload = request_json(CENSUS_MARTS_URL, params=params)
    components = _parse_census_marts_rows(payload)
    missing = [name for name, values in components.items() if not values]
    if missing:
        raise RuntimeError("Census MARTS missing control-group components: " + ", ".join(missing))

    common_periods = set.intersection(*(set(values) for values in components.values()))
    levels = {}
    for period in common_periods:
        levels[period] = round(
            components["total"][period]
            - components["motor_vehicles"][period]
            - components["gasoline"][period]
            - components["building_materials"][period]
            - components["food_services"][period],
            3,
        )
    if not levels:
        raise RuntimeError("Census MARTS has no common months for control-group calculation")
    return transform(dict(sorted(levels.items())), "mom_pct")


NYFED_SCE_XLSX_URL = "https://www.newyorkfed.org/medialibrary/interactives/sce/sce/downloads/data/frbny-sce-data.xlsx"


def _nyfed_period(value):
    """Convert NY Fed YYYYMM values, including Excel numeric cells, to YYYY-MM."""
    if value is None or pd.isna(value):
        return None
    if isinstance(value, (datetime, pd.Timestamp)):
        return pd.Timestamp(value).strftime("%Y-%m")
    text = str(value).strip()
    if text.endswith(".0"):
        text = text[:-2]
    if re.fullmatch(r"20\d{4}", text):
        year, month = int(text[:4]), int(text[4:])
        if 1 <= month <= 12:
            return month_key(year, month)
    parsed = pd.to_datetime(value, errors="coerce")
    return parsed.strftime("%Y-%m") if pd.notna(parsed) else None


def _parse_nyfed_sheet(workbook, sheet_name, required_columns):
    """Read NY Fed sheets whose field names are on Excel row 4 and dates in column A."""
    frame = pd.read_excel(workbook, sheet_name=sheet_name, header=3)
    date_column = frame.columns[0]
    missing = [column for column in required_columns.values() if column not in frame.columns]
    if missing:
        raise RuntimeError(f"NY Fed sheet {sheet_name} missing columns: {', '.join(missing)}")
    result = {key: {} for key in required_columns}
    for _, row in frame.iterrows():
        period = _nyfed_period(row[date_column])
        if not period:
            continue
        for key, column in required_columns.items():
            value = num(row[column])
            if value is not None:
                result[key][period] = value
    return result


def _parse_nyfed_sce_workbook(content):
    workbook = pd.ExcelFile(io.BytesIO(content))
    required_sheets = {
        "Job separation expectation",
        "Inflation expectations",
        "Five-year ahead Infl Exp",
    }
    missing_sheets = required_sheets.difference(workbook.sheet_names)
    if missing_sheets:
        raise RuntimeError("NY Fed workbook missing sheets: " + ", ".join(sorted(missing_sheets)))

    result = {}
    result.update(_parse_nyfed_sheet(
        workbook,
        "Job separation expectation",
        {
            "job_loss": "Mean probability of losing a job",
            "job_separation": "Mean probability of leaving a job voluntarily",
        },
    ))
    result.update(_parse_nyfed_sheet(
        workbook,
        "Inflation expectations",
        {"one_year": "Median one-year ahead expected inflation rate"},
    ))
    result.update(_parse_nyfed_sheet(
        workbook,
        "Five-year ahead Infl Exp",
        {"five_year": "Median five-year ahead expected inflation rate"},
    ))
    empty = [key for key, values in result.items() if not values]
    if empty:
        raise RuntimeError("NY Fed workbook returned no usable data for: " + ", ".join(empty))
    return result


def fetch_nyfed_sce():
    response = SESSION.get(NYFED_SCE_XLSX_URL, timeout=120)
    response.raise_for_status()
    if not response.content.startswith(b"PK"):
        raise RuntimeError(f"NY Fed SCE response is not an XLSX file ({response.headers.get('content-type')})")
    return _parse_nyfed_sce_workbook(response.content)


def fetch_page_latest()->dict[tuple[str,str],dict[str,float]]:
    """Fetch the remaining publisher pages and official ISM monthly reports."""
    out={}; now=datetime.now(); period=f"{now.year:04d}-{now.month:02d}"
    pages={
      "nfib":SESSION.get("https://nfib-sbet.org/MainPage.html",timeout=60).text,
      "conference":SESSION.get("https://www.conference-board.org/topics/consumer-confidence/index.cfm",timeout=60).text,
    }
    patterns=[
      (("nfib","hiring_plan"),r"Plans to Increase Employment\D{0,80}(-?\d+(?:\.\d+)?)"),
      (("conference","confidence"),r"Consumer Confidence Index[^\d]{0,100}(?:decreased|increased).*?to\s+(\d+(?:\.\d+)?)"),
      (("conference","hard"),r"jobs[^\n]{0,40}hard to get[^\d]{0,80}(\d+(?:\.\d+)?)"),
    ]
    for (provider,key),pat in patterns:
        match=re.search(pat,pages[provider],re.I|re.S)
        if match:
            out[(provider,key)]={period:float(match.group(1))}

    for key, values in fetch_ism_official().items():
        out[("ism", key)] = values
    return out

def fetch_michigan_long_run_latest():
    """Fetch the latest official University of Michigan long-run inflation expectation."""
    url = "https://www.sca.isr.umich.edu/"
    response = SESSION.get(url, timeout=60)
    response.raise_for_status()
    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", response.text))

    period_match = re.search(
        r"(?:Final|Preliminary) Results for ([A-Za-z]+) (20\d{2})",
        text,
        flags=re.IGNORECASE,
    )
    if not period_match:
        raise RuntimeError("University of Michigan reference month not found")
    month_number = list(calendar.month_name).index(period_match.group(1).title())
    period = month_key(int(period_match.group(2)), month_number)

    patterns = [
        r"Long-run inflation expectations[^.]{0,180}?(\d+(?:\.\d+)?)%",
        r"long-run[^.]{0,120}?at\s+(\d+(?:\.\d+)?)%",
        r"five[- ]year inflation expectations[^.]{0,120}?(\d+(?:\.\d+)?)%",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return {period: float(match.group(1))}
    raise RuntimeError("University of Michigan long-run inflation value not found")

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
    try: nyfed_sce=fetch_nyfed_sce()
    except Exception as e: nyfed_sce={}; errors.append(f"NY Fed SCE: {e}")
    try: umich=fetch_umichigan_csv()
    except Exception as e: umich={}; errors.append(f"University of Michigan CSV: {e}")
    try: retail_control=fetch_census_retail_control()
    except Exception as e: retail_control={}; errors.append(f"Census retail control: {e}")
    for s in SPECS:
        key=f"{s.section}|{s.name}"
        try:
            if s.provider=="bls": vals=transform(bls.get(s.source_id,{}),s.transform)
            elif s.provider=="fred": vals=transform(fetch_fred(s.source_id),s.transform)
            elif s.provider=="atlanta": vals=atl.get(s.source_id,{})
            elif s.provider=="adp": vals=adp.get(s.source_id,{})
            elif s.provider=="umich_csv": vals=umich.get(s.source_id,{})
            elif s.provider=="zillow": vals=zori
            elif s.provider=="nyfed_xlsx": vals=nyfed_sce.get(s.source_id,{})
            elif s.provider=="census" and s.source_id=="retail_control": vals=retail_control
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
    # Markdown暫時列出程式內所有指標，依SPECS既有分類與順序顯示。
    # 已成功抓取的指標仍會持續更新，本區只控制Markdown呈現方式。
    method_labels = {
        "bls": "API（BLS Public Data API v2）",
        "atlanta": "XLSX（Atlanta Fed官方下載檔）",
        "adp": "ZIP／CSV（ADP Pay Insights動態下載連結）",
        "zillow": "CSV（Zillow Research官方下載檔）",
        "umich_csv": "CSV（University of Michigan官方下載檔）",
        "fred": "API（FRED API）",
        "nyfed_xlsx": "XLSX（New York Fed SCE官方下載檔）",
        "ism": "HTML（ISM官方月報）",
        "nfib": "HTML（NFIB官方頁面）",
        "conference": "HTML（Conference Board官方頁面）",
        "census": "API＋計算（Census MARTS API）",
        "derived": "計算（由其他已抓取序列推導）",
        "umich": "HTML（University of Michigan官方頁面）",
        "nyfed": "HTML（New York Fed官方頁面）",
    }

    all_periods = sorted({
        period
        for values in current.values()
        for period in values
    })[-MONTHS:]

    lines = [
        "# 美國總體經濟數據",
        "",
        f"> 更新時間：{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}  ",
        "> 日期為資料所屬月份月底。N/A代表該月份尚未發布，或來源暫時未成功取得。",
        "",
    ]

    for section in dict.fromkeys(spec.section for spec in SPECS):
        section_specs = [spec for spec in SPECS if spec.section == section]
        lines += [
            f"## {section}",
            "",
            "| 指標 | 最新資料月份 | 來源 | 抓取方式 | 官方序列／定義 | "
            + " | ".join(month_end(period) for period in reversed(all_periods))
            + " |",
            "|---|---:|---|---|---|" + "---:|" * len(all_periods),
        ]
        for spec in section_specs:
            key = f"{spec.section}|{spec.name}"
            values = current.get(key, {})
            latest = max(values) if values else None
            display_name = "&nbsp;" * (spec.level * 4) + spec.name
            method = method_labels.get(spec.provider, f"其他（{spec.provider}）")
            lines.append("| " + " | ".join(
                [
                    display_name,
                    month_end(latest) if latest else "N/A",
                    spec.source,
                    method,
                    spec.series,
                ]
                + [fmt(values.get(period)) for period in reversed(all_periods)]
            ) + " |")
        lines.append("")

    if errors:
        lines += ["## 更新警告", "", *[f"- {error}" for error in errors], ""]

    lines += [
        "## 抓取方式說明",
        "",
        "- API：直接呼叫官方或資料庫API並解析JSON。",
        "- CSV：下載官方CSV後依月份與欄位名稱解析。",
        "- XLSX：下載官方Excel後依工作表與欄位名稱解析。",
        "- ZIP／CSV：先從官方頁面動態取得ZIP連結，再解壓縮並解析CSV。",
        "- HTML：讀取官方月報或發布頁面中的文字與數值。",
        "- API＋計算：取得官方組成項目後，再依定義計算衍生指標。",
        "- 計算：完全由程式中其他已抓取序列推導，不另外下載。",
        "",
    ]
    OUT.write_text("\n".join(lines),encoding="utf-8")
    print(f"Wrote {OUT} with {len(SPECS)} rows; warnings={len(errors)}")

if __name__=="__main__": main()
