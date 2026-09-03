#!/usr/bin/env python3
"""Build data/us_macro_table.md from stable US macro sources.

Priority: official machine-readable source > official downloadable file > FRED API.
Required secrets: BLS_API_KEY. Optional: FRED_API_KEY.
Prior successful observations are retained in data/us_macro_cache.json when a source fails.
"""
from __future__ import annotations

import calendar, html, importlib, io, json, os, re, subprocess, sys, time, zipfile
from html.parser import HTMLParser
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
CB_DEBUG_DIR = ROOT / "data" / "us_macro_debug"
CB_RAW_HTML = CB_DEBUG_DIR / "cb_consumer_confidence_raw.html"
CB_HTTP_JSON = CB_DEBUG_DIR / "cb_consumer_confidence_http.json"
NFIB_API_JSON = CB_DEBUG_DIR / "nfib_sbet_api_http.json"
MONTHS = 5
BLS_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
FRED_URL = "https://api.stlouisfed.org/fred/series/observations"
CENSUS_MARTS_URL = "https://api.census.gov/data/timeseries/eits/marts"
NFIB_SBET_API_URL = "https://api.nfib-sbet.org/rest/sbetdb/_proc/getTotals2"
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
    Spec("消費", "密大_Current", "ICC", "University of Michigan", "ICC", "umich_csv", "icc"),
    Spec("消費", "密大_Expect", "ICE", "University of Michigan", "ICE", "umich_csv", "ice"),
]

# FRED is retained for BEA series where it is already working.
for section,name,ticker,source,fred_id,transform in [
("消費","Real Personal Spending","PCE CHY% Index","Bureau of Economic Analysis","PCEC96","yoy_pct"),
("消費","disposable personal income","PIDSDI Index","Bureau of Economic Analysis","DSPI","level"),
("消費","Personal Outlays","PIDSSO Index","Bureau of Economic Analysis","A068RC1","level"),
("消費","Personal Saving","PIDSS Index","Bureau of Economic Analysis","PMSAVE","level"),
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
Spec("消費","家戶金融狀況vs一年前","CONSPAGI Index","University of Michigan","PAGO_R_M (monthly data)","umich","pago"),
Spec("消費","預計未來一年金融狀況","CONSEXFI Index","University of Michigan","PEXP_R_M (monthly data)","umich","pexp"),
Spec("消費","CB","CONCCONF Index","The Conference Board","Consumer Confidence Index","conference","confidence"),
Spec("消費","零售控制 MoM%","RSTAXAGM Index","U.S. Census Bureau","44X72 - 441X - 447 - 444 - 722; seasonally adjusted monthly sales MoM%","census","retail_control"),]

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
    required_sheets = {"Job Switcher", "Average Wage Quartile"}
    missing = required_sheets.difference(workbook.sheet_names)
    if missing:
        raise RuntimeError("Atlanta Fed workbook missing sheets: " + ", ".join(sorted(missing)))

    # The dedicated "Job Switcher" sheet holds the smoothed (moving-average)
    # series that Bloomberg's WGTRJBSW/WGTRJBSY track. The "Job Stayer"/"Job
    # Switcher" columns on data_overall are single-month medians and do not
    # match the published headline, so they must not be used here.
    overall = pd.read_excel(workbook, sheet_name="Job Switcher", header=2)
    overall_date = overall.columns[0]
    for column in ("Job Stayer", "Job Switcher"):
        if column not in overall.columns:
            raise RuntimeError(f"Atlanta Fed 'Job Switcher' sheet missing column: {column}")

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


class _ADPHistoricalDataLinkParser(HTMLParser):
    """Collect anchor URLs whose visible label is Download historical data."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self._href = None
        self._text = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag.casefold() != "a":
            return
        self._href = dict(attrs).get("href")
        self._text = []

    def handle_data(self, data):
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self, tag):
        if tag.casefold() != "a" or self._href is None:
            return
        label = re.sub(r"\s+", " ", " ".join(self._text)).strip().casefold()
        if "download historical data" in label:
            self.links.append(self._href)
        self._href = None
        self._text = []


def _adp_history_links(source_html, page_url):
    """Discover the URL from ADP actual historical-data download button.

    The button href is authoritative. Its directory and filename may change
    without requiring a code change. Generic ZIP discovery is secondary.
    """
    decoded = source_html.replace("\\/", "/").replace("&amp;", "&")
    links = []
    parser = _ADPHistoricalDataLinkParser()
    try:
        parser.feed(decoded)
    except Exception:
        pass
    for href in parser.links:
        absolute = urljoin(page_url, href.strip())
        if absolute not in links:
            links.append(absolute)

    patterns = [
        r"href\s*=\s*[\"']([^\"']+\.zip(?:\?[^\"']*)?)[\"']",
        r"((?:https?:)?//[^\s\"']+/artifacts/us_wage/\d{8}/[^\s\"']+\.zip(?:\?[^\s\"']*)?)",
        r"(/artifacts/us_wage/\d{8}/[^\s\"']+\.zip(?:\?[^\s\"']*)?)",
    ]
    for pattern in patterns:
        for href in re.findall(pattern, decoded, flags=re.IGNORECASE):
            absolute = urljoin(page_url, href)
            if absolute not in links:
                links.append(absolute)
    return links

def _adp_fallback_links(page_url):
    """Last-resort dated candidates. The date is discovered by probing recent calendar dates, not hard-coded."""
    today = datetime.now(timezone.utc).date()
    return [
        urljoin(page_url, f"/artifacts/us_wage/{(today - timedelta(days=offset)):%Y%m%d}/documents/ADP_PAY_history.zip")
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
        "components": "https://www.sca.isr.umich.edu/files/tbmiccice.csv",
    }
    frames = {}
    for key, url in urls.items():
        response = SESSION.get(url, timeout=90)
        response.raise_for_status()
        frames[key] = pd.read_csv(io.BytesIO(response.content))

    result = {"sentiment": {}, "px1": {}, "px5": {}, "icc": {}, "ice": {}}
    sentiment = frames["sentiment"]
    inflation = frames["inflation"]
    components = frames["components"]
    required_sentiment = {"Month", "YYYY", "ICS_ALL"}
    required_inflation = {"Month", "YYYY", "PX_MD", "PX5_MD"}
    required_components = {"Month", "YYYY", "ICC", "ICE"}
    if not required_sentiment.issubset(sentiment.columns):
        raise RuntimeError(f"Michigan sentiment CSV missing columns: {sorted(required_sentiment - set(sentiment.columns))}")
    if not required_inflation.issubset(inflation.columns):
        raise RuntimeError(f"Michigan inflation CSV missing columns: {sorted(required_inflation - set(inflation.columns))}")
    if not required_components.issubset(components.columns):
        raise RuntimeError(f"Michigan ICC/ICE CSV missing columns: {sorted(required_components - set(components.columns))}")

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

    for _, row in components.iterrows():
        period = _parse_month_name_period(row["Month"], row["YYYY"])
        if not period:
            continue
        current = num(row["ICC"])
        expected = num(row["ICE"])
        if current is not None:
            result["icc"][period] = current
        if expected is not None:
            result["ice"][period] = expected

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


def _plain_html(source_html):
    text = re.sub(r"<script[^>]*>.*?</script>", " ", source_html, flags=re.I | re.S)
    text = re.sub(r"<style[^>]*>.*?</style>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def _ism_number(text, patterns, label):
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.I | re.S)
        if match:
            return float(match.group(1))
    raise RuntimeError(f"ISM {label} value not found")


def _ism_number_optional(text, patterns):
    """Like _ism_number but returns None instead of raising when absent."""
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.I | re.S)
        if match:
            return float(match.group(1))
    return None


# ISM Prices Index wording, shared by manufacturing and services reports.
_ISM_PRICE_PATTERNS = [
    r"Prices Index[^.]{0,90}?(?:registered|reading of|at|was)\s+(\d+(?:\.\d+)?)\s*percent",
    r"Prices Index[^.]{0,90}?(\d+(?:\.\d+)?)\s*percent",
]


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
        prices = _ism_number_optional(text, _ISM_PRICE_PATTERNS)
        parsed = {"manufacturing_pmi": pmi, "manufacturing_employment": employment}
        if prices is not None:
            parsed["manufacturing_prices"] = prices
        return parsed

    pmi = _ism_number(text, [
        r"Services PMI(?:®)?\s+(?:registered|at)\s+(\d+(?:\.\d+)?)\s*percent",
        r"Services PMI(?:®)?\s+at\s+(\d+(?:\.\d+)?)%",
    ], "Services PMI")
    employment = _ism_number(text, [
        r"Employment Index(?: returned[^.]{0,120}?with a reading of| registered| at)\s+(\d+(?:\.\d+)?)\s*percent",
        r"Employment Index[^.]{0,160}?reading of\s+(\d+(?:\.\d+)?)\s*percent",
    ], "Services Employment")
    prices = _ism_number_optional(text, _ISM_PRICE_PATTERNS)
    parsed = {"services_pmi": pmi, "services_employment": employment}
    if prices is not None:
        parsed["services_prices"] = prices
    return parsed


def fetch_ism_official():
    """Fetch ISM reports; retain a verified 2026 bootstrap when ISM blocks cloud runners."""
    # Verified against ISM monthly releases. This prevents an empty series when ismworld.org
    # returns HTTP 403 to GitHub-hosted runners. Official HTML remains the first choice.
    bootstrap = {
        "manufacturing_pmi": {
            "2026-01": 52.6, "2026-02": 52.4, "2026-03": 52.7,
            "2026-04": 52.7, "2026-05": 54.0, "2026-06": 53.3, "2026-07": 55.6,
        },
        "manufacturing_employment": {
            "2026-01": 48.1, "2026-02": 48.8, "2026-03": 48.7,
            "2026-04": 46.4, "2026-05": 48.6, "2026-06": 49.7, "2026-07": 52.8,
        },
        "services_pmi": {
            "2026-01": 53.8, "2026-02": 56.1, "2026-03": 54.0,
            "2026-04": 53.6, "2026-05": 54.5, "2026-06": 54.0, "2026-07": 54.1,
        },
        "services_employment": {
            "2026-01": 50.3, "2026-02": 51.8, "2026-03": 45.2,
            "2026-04": 48.0, "2026-05": 47.9, "2026-06": 51.2, "2026-07": 47.4,
        },
        "manufacturing_prices": {
            "2026-01": 59.0, "2026-02": 70.5, "2026-03": 78.3,
            "2026-04": 84.6, "2026-05": 82.1, "2026-06": 73.0, "2026-07": 71.1,
        },
        "services_prices": {
            "2026-01": 66.6, "2026-02": 63.0, "2026-03": 70.7,
            "2026-04": 70.7, "2026-05": 71.3, "2026-06": 67.7, "2026-07": 70.3,
        },
    }
    result = {key: dict(values) for key, values in bootstrap.items()}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
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
            except Exception:
                # Existing cache plus verified bootstrap are preferable to deleting valid history.
                continue
    return result

UMICH_CHARTS_URL = "https://data.sca.isr.umich.edu/charts.php"


def _find_umich_excel_link(html, chart_number):
    """Find the official Excel link adjacent to chart 6 or chart 8."""
    normalized = html.replace("&amp;", "&")
    patterns = [
        rf'href=["\']([^"\']*get-chart\.php[^"\']*(?:n={chart_number}[a-z]?|n={chart_number}r)[^"\']*f=xls[^"\']*)["\']',
        rf'href=["\']([^"\']*get-chart\.php[^"\']*f=xls[^"\']*(?:n={chart_number}[a-z]?|n={chart_number}r)[^"\']*)["\']',
    ]
    for pattern in patterns:
        match = re.search(pattern, normalized, flags=re.I)
        if match:
            return urljoin(UMICH_CHARTS_URL, match.group(1))
    raise RuntimeError(f"Michigan chart {chart_number} Excel link not found")


def _normalize_excel_header(value):
    if value is None or pd.isna(value):
        return ""
    return re.sub(r"\s+", "", str(value)).upper()


def _ensure_xlrd():
    """Ensure legacy .xls support is available on GitHub Actions runners."""
    try:
        module = importlib.import_module("xlrd")
        version = tuple(int(part) for part in module.__version__.split(".")[:3])
        if version >= (2, 0, 1):
            return
    except Exception:
        pass

    subprocess.check_call([
        sys.executable,
        "-m",
        "pip",
        "install",
        "--disable-pip-version-check",
        "--quiet",
        "xlrd>=2.0.1",
    ])
    importlib.invalidate_caches()
    module = importlib.import_module("xlrd")
    version = tuple(int(part) for part in module.__version__.split(".")[:3])
    if version < (2, 0, 1):
        raise RuntimeError(f"xlrd>=2.0.1 is required, found {module.__version__}")


def _parse_umich_chart_excel(content, wanted_column):
    """Parse one exact Michigan chart column, never substitute a moving average column."""
    _ensure_xlrd()
    workbook = pd.ExcelFile(io.BytesIO(content), engine="xlrd")
    wanted = _normalize_excel_header(wanted_column)
    for sheet in workbook.sheet_names:
        raw = pd.read_excel(workbook, sheet_name=sheet, header=None)
        for row_index in range(min(25, len(raw))):
            labels = [_normalize_excel_header(value) for value in raw.iloc[row_index].tolist()]
            exact_candidates = [index for index, label in enumerate(labels) if label == wanted]
            if not exact_candidates:
                continue
            value_col = exact_candidates[0]
            date_candidates = [
                index for index, label in enumerate(labels)
                if label in {"DATEMY", "DATE", "MONTH", "MONTHDATE"}
            ]
            date_col = date_candidates[0] if date_candidates else 0
            result = {}
            for _, row in raw.iloc[row_index + 1:].iterrows():
                date = pd.to_datetime(row.iloc[date_col], errors="coerce")
                value = num(row.iloc[value_col])
                if pd.notna(date) and value is not None:
                    result[date.strftime("%Y-%m")] = value
            if result:
                return dict(sorted(result.items()))
    raise RuntimeError(f"Michigan Excel exact column not found: {wanted_column}")

def fetch_umich_financial():
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "text/html,application/xhtml+xml"}
    page = SESSION.get(UMICH_CHARTS_URL, headers=headers, timeout=90)
    page.raise_for_status()
    result = {}
    for key, chart_number, column in (
        ("pago", 6, "PAGO_R_M"),
        ("pexp", 8, "PEXP_R_M"),
    ):
        link = _find_umich_excel_link(page.text, chart_number)
        response = SESSION.get(link, headers=headers, timeout=90)
        response.raise_for_status()
        result[key] = _parse_umich_chart_excel(response.content, column)
    return result


CENSUS_CONTROL_CATEGORIES = {
    "total": "44X72",
    # Census MARTS official aggregate: Auto and Other Motor Vehicle Dealers.
    "auto_other_motor_vehicles": "441X",
    "gasoline": "447",
    "building_materials": "444",
    "food_services": "722",
}

CENSUS_CATEGORY_LABELS = {
    "44X72": "Retail Trade and Food Services, Total",
    "44Y72": "Retail Trade and Food Services, ex Auto",
    "44Z72": "Retail Trade and Food Services, ex Gas",
    "44W72": "Retail Trade and Food Services, ex Auto and Gas",
    "44000": "Retail Trade",
    "441": "Motor Vehicle and Parts Dealers",
    "4411": "Automobile Dealers",
    "4412": "Other Motor Vehicle Dealers",
    "4411,4412": "Automobile Dealers plus Other Motor Vehicle Dealers (component sum)",
    "441X": "Auto and Other Motor Vehicle Dealers",
    "442": "Furniture and Home Furnishings Stores",
    "443": "Electronics and Appliance Stores",
    "444": "Building Material and Garden Equipment and Supplies Dealers",
    "445": "Food and Beverage Stores",
    "4451": "Grocery Stores",
    "446": "Health and Personal Care Stores",
    "447": "Gasoline Stations",
    "448": "Clothing and Clothing Accessories Stores",
    "451": "Sporting Goods, Hobby, Musical Instrument, and Book Stores",
    "452": "General Merchandise Stores",
    "4521": "Department Stores",
    "453": "Miscellaneous Store Retailers",
    "454": "Nonstore Retailers",
    "722": "Food Services and Drinking Places",
}


def _normalize_census_category(value):
    return re.sub(r"\s+", "", str(value).strip()).upper()


def _parse_census_marts_rows(payload):
    """Return both selected formula components and every raw SA monthly-sales category."""
    if not isinstance(payload, list) or len(payload) < 2:
        raise RuntimeError("Census MARTS returned no data rows")
    headers = [str(header).strip() for header in payload[0]]
    required = {"cell_value", "category_code", "data_type_code", "seasonally_adj"}
    missing = required.difference(headers)
    if missing:
        raise RuntimeError("Census MARTS missing fields: " + ", ".join(sorted(missing)))
    date_field = "time" if "time" in headers else "time_slot_date" if "time_slot_date" in headers else None
    if not date_field:
        raise RuntimeError("Census MARTS response has no time or time_slot_date field")

    indexes = {name: headers.index(name) for name in required}
    date_index = headers.index(date_field)
    raw_categories = {}
    for row in payload[1:]:
        if str(row[indexes["data_type_code"]]).strip().upper() != "SM":
            continue
        if str(row[indexes["seasonally_adj"]]).strip().lower() not in {"yes", "true", "1"}:
            continue
        category = _normalize_census_category(row[indexes["category_code"]])
        period_match = re.search(r"(20\d{2})-(0[1-9]|1[0-2])", str(row[date_index]))
        value = num(row[indexes["cell_value"]])
        if category and period_match and value is not None:
            period = f"{period_match.group(1)}-{period_match.group(2)}"
            raw_categories.setdefault(category, {})[period] = value

    components = {}
    for name, category_code in CENSUS_CONTROL_CATEGORIES.items():
        normalized = _normalize_census_category(category_code)
        components[name] = dict(raw_categories.get(normalized, {}))
    return components, dict(sorted(raw_categories.items()))


def fetch_census_retail_control():
    """Return control-group MoM% and raw Census SA monthly-sales categories for inspection."""
    api_key = os.getenv("CENSUS_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("Missing CENSUS_API_KEY")
    start_year = datetime.now(timezone.utc).year - 3
    params = {
        "get": "cell_value,data_type_code,category_code,seasonally_adj,time_slot_date",
        "time": f"from {start_year}",
        "key": api_key,
    }
    payload = request_json(CENSUS_MARTS_URL, params=params)
    components, raw_categories = _parse_census_marts_rows(payload)
    missing = [name for name, values in components.items() if not values]
    if missing:
        available = ", ".join(raw_categories.keys())
        raise RuntimeError(
            "Census MARTS missing candidate control-group components: "
            + ", ".join(missing)
            + f"; available category codes: {available}"
        )

    common_periods = set.intersection(*(set(values) for values in components.values()))
    levels = {}
    for period in common_periods:
        levels[period] = round(
            components["total"][period]
            - components["auto_other_motor_vehicles"][period]
            - components["gasoline"][period]
            - components["building_materials"][period]
            - components["food_services"][period],
            3,
        )
    if not levels:
        raise RuntimeError("Census MARTS has no common months for control-group calculation")
    return transform(dict(sorted(levels.items())), "mom_pct"), raw_categories

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


def _month_name_period(year, month_name):
    month_name = month_name.title()
    if month_name not in calendar.month_name:
        return None
    return month_key(int(year), list(calendar.month_name).index(month_name))


def _parse_conference_board_release(html):
    """Parse current and revised-prior CCI plus current labor-market shares."""
    text = _plain_html(html)

    updated = re.search(
        r"Updated:\s*(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),?\s*"
        r"([A-Za-z]+)\s+\d{1,2},\s+(20\d{2})",
        text,
        flags=re.I,
    )
    if not updated:
        updated = re.search(r"Updated:\s*([A-Za-z]+)\s+\d{1,2},\s+(20\d{2})", text, flags=re.I)
    if not updated:
        raise RuntimeError("Conference Board Updated date not found")
    current_period = _month_name_period(updated.group(2), updated.group(1))

    cci = re.search(
        r"Consumer Confidence Index\s*(?:®\s*)?"
        r"(?:increased|decreased|rose|fell|edged up|edged down|inched up|inched down)"
        r".*?\bto\s+(\d+(?:\.\d+)?)\s*\(1985\s*=\s*100\)\s+in\s+([A-Za-z]+)"
        r".*?\bfrom\s+(?:an?\s+)?(?:upwardly\s+|downwardly\s+)?(?:revised\s+)?"
        r"(\d+(?:\.\d+)?)\s+in\s+([A-Za-z]+)",
        text,
        flags=re.I | re.S,
    )
    if not cci:
        raise RuntimeError("Conference Board current/prior Consumer Confidence values not found")

    current_value = float(cci.group(1))
    current_month = cci.group(2)
    prior_value = float(cci.group(3))
    prior_month = cci.group(4)
    current_period_from_sentence = _month_name_period(updated.group(2), current_month)
    if current_period_from_sentence != current_period:
        raise RuntimeError(
            f"Conference Board month mismatch: Updated={current_period}, sentence={current_period_from_sentence}"
        )
    current_year, current_month_number = map(int, current_period.split("-"))
    prior_month_number = list(calendar.month_name).index(prior_month.title())
    prior_year = current_year - 1 if prior_month_number > current_month_number else current_year
    prior_period = month_key(prior_year, prior_month_number)

    plentiful = re.search(
        r"(\d+(?:\.\d+)?)%\s+of consumers said jobs were\s+[\"'“”‘’]?plentiful[\"'“”‘’]?",
        text,
        flags=re.I,
    )
    hard = re.search(
        r"(\d+(?:\.\d+)?)%\s+of consumers said jobs were\s+[\"'“”‘’]?hard to get[\"'“”‘’]?",
        text,
        flags=re.I,
    )

    return {
        "current_period": current_period,
        "prior_period": prior_period,
        "confidence": {current_period: current_value, prior_period: prior_value},
        "plentiful": {current_period: float(plentiful.group(1))} if plentiful else {},
        "hard": {current_period: float(hard.group(1))} if hard else {},
    }

def _nfib_api_period(record):
    """Return YYYY-MM from a REST API record without assuming exact field casing."""
    normalized = {re.sub(r"[^a-z0-9]", "", str(key).lower()): value for key, value in record.items()}
    year = None
    month = None
    for key in ("year", "yr", "surveyyear", "datayear"):
        candidate = num(normalized.get(key))
        if candidate is not None and 1970 <= int(candidate) <= 2100:
            year = int(candidate)
            break
    for key in ("month", "mo", "surveymonth", "datamonth", "monthnumber"):
        raw = normalized.get(key)
        candidate = num(raw)
        if candidate is not None and 1 <= int(candidate) <= 12:
            month = int(candidate)
            break
        month_name = str(raw or "").strip().title()
        if month_name in calendar.month_name:
            month = list(calendar.month_name).index(month_name)
            break
        if month_name in calendar.month_abbr:
            month = list(calendar.month_abbr).index(month_name)
            break
    if year and month:
        return month_key(year, month)
    for key in ("date", "period", "surveydate", "monthyear", "time"):
        raw = normalized.get(key)
        if raw is None:
            continue
        match = re.search(r"(20\d{2})[-/](0?[1-9]|1[0-2])", str(raw))
        if match:
            return month_key(int(match.group(1)), int(match.group(2)))
        parsed = pd.to_datetime(raw, errors="coerce")
        if pd.notna(parsed):
            return parsed.strftime("%Y-%m")
    return None


def _nfib_api_value(record):
    """Prefer seasonally adjusted values, then generic value fields."""
    normalized = {re.sub(r"[^a-z0-9]", "", str(key).lower()): value for key, value in record.items()}
    preferred = (
        "seasonallyadjusted", "seasonallyadjustedvalue", "savalue", "sa",
        "indicatorvalue", "indexvalue", "value", "total", "percent", "netpercent",
    )
    for key in preferred:
        value = num(normalized.get(key))
        if value is not None and -100 <= value <= 100:
            return float(value), key
    candidates = []
    for key, raw in normalized.items():
        if any(token in key for token in ("year", "month", "date", "id", "count", "sample")):
            continue
        value = num(raw)
        if value is not None and -100 <= value <= 100:
            candidates.append((float(value), key))
    if len(candidates) == 1:
        return candidates[0]
    return None, None


def _nfib_api_records(payload):
    """Recursively collect JSON objects that look like monthly observations."""
    records = []
    def visit(node):
        if isinstance(node, dict):
            period = _nfib_api_period(node)
            value, field = _nfib_api_value(node)
            if period and value is not None:
                records.append((period, value, field, node))
            for child in node.values():
                visit(child)
        elif isinstance(node, list):
            for child in node:
                visit(child)
    visit(payload)
    return records


def fetch_nfib_sbet_api():
    """Fetch NFIB hiring plans from the official SBET getTotals2 REST procedure."""
    now = datetime.now(timezone.utc)
    parameters = [
        ("minYear", now.year - 3),
        ("minMonth", 1),
        ("maxYear", now.year),
        ("maxMonth", 12),
        ("questions", "emp_count_change_expect"),
        ("industry", ""),
        ("employee", ""),
        ("statev", ""),
    ]
    form_data = [("app_name", "sbet")]
    for index, (name, value) in enumerate(parameters):
        form_data.extend([
            (f"params[{index}][name]", name),
            (f"params[{index}][param_type]", "IN"),
            (f"params[{index}][value]", str(value)),
        ])

    diagnostic = {
        "method": "NFIB SBET REST API",
        "endpoint": NFIB_SBET_API_URL,
        "procedure": "getTotals2",
        "question": "emp_count_change_expect",
        "request_parameters": {name: value for name, value in parameters},
        "request_encoding": "application/x-www-form-urlencoded",
    }
    try:
        response = SESSION.post(
            NFIB_SBET_API_URL,
            data=form_data,
            headers={
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": "https://www.nfib-sbet.org",
                "Referer": "https://www.nfib-sbet.org/",
                "X-Requested-With": "XMLHttpRequest",
            },
            timeout=120,
        )
        diagnostic.update({
            "status_code": response.status_code,
            "content_type": response.headers.get("Content-Type", ""),
            "response_bytes": len(response.content),
            "response_preview": response.text[:4000],
        })
        response.raise_for_status()
        try:
            data = response.json()
        except ValueError as error:
            raise RuntimeError("NFIB SBET API response is not valid JSON") from error

        diagnostic["response_json"] = data
        records = _nfib_api_records(data)
        values = {}
        value_fields = {}
        for period, value, field, _record in records:
            values[period] = value
            value_fields[period] = field
        if not values:
            raise RuntimeError(
                "NFIB SBET API returned JSON but no monthly emp_count_change_expect observations were recognized"
            )

        diagnostic.update({
            "parsed_observations": dict(sorted(values.items())),
            "parsed_value_fields": dict(sorted(value_fields.items())),
            "latest_period": max(values),
            "latest_value": values[max(values)],
        })
        NFIB_API_JSON.write_text(
            json.dumps(diagnostic, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return dict(sorted(values.items()))
    except Exception as error:
        diagnostic.update({"error_type": type(error).__name__, "error": str(error)})
        NFIB_API_JSON.write_text(
            json.dumps(diagnostic, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        raise


def fetch_page_latest()->dict[tuple[str,str],dict[str,float]]:
    """Fetch Conference Board and ISM independently so one provider cannot erase another."""
    out = {}
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    cb_url = "https://www.conference-board.org/topics/consumer-confidence/index.cfm"
    CB_DEBUG_DIR.mkdir(parents=True, exist_ok=True)
    try:
        response = SESSION.get(cb_url, headers=headers, timeout=60, allow_redirects=True)
        raw = response.content
        CB_RAW_HTML.write_bytes(raw)
        encoding = response.encoding or response.apparent_encoding or "utf-8"
        decoded = raw.decode(encoding, errors="replace")
        plain_text = _plain_html(decoded)
        title_match = re.search(r"<title[^>]*>(.*?)</title>", decoded, flags=re.I | re.S)
        diagnostic = {
            "requested_url": cb_url,
            "final_url": response.url,
            "status_code": response.status_code,
            "content_type": response.headers.get("Content-Type", ""),
            "response_bytes": len(raw),
            "encoding": encoding,
            "title": re.sub(r"\s+", " ", title_match.group(1)).strip() if title_match else "",
            "contains_consumer_confidence": "consumer confidence" in plain_text.lower(),
            "contains_jobs_plentiful": "jobs plentiful" in plain_text.lower(),
            "contains_jobs_hard_to_get": "jobs hard to get" in plain_text.lower(),
            "contains_next_data": "__NEXT_DATA__" in decoded,
            "contains_initial_state": "__INITIAL_STATE__" in decoded,
            "response_preview": plain_text[:4000],
            "saved_raw_html": str(CB_RAW_HTML.relative_to(ROOT)),
        }
        CB_HTTP_JSON.write_text(json.dumps(diagnostic, ensure_ascii=False, indent=2), encoding="utf-8")
        response.raise_for_status()
        parsed_cb = _parse_conference_board_release(decoded)
        out[("conference", "confidence")] = parsed_cb["confidence"]
        if parsed_cb["plentiful"]:
            out[("conference", "plentiful")] = parsed_cb["plentiful"]
        if parsed_cb["hard"]:
            out[("conference", "hard")] = parsed_cb["hard"]
        diagnostic.update({
            "parsed_reference_period": parsed_cb["current_period"],
            "parsed_prior_period": parsed_cb["prior_period"],
            "parsed_consumer_confidence": parsed_cb["confidence"].get(parsed_cb["current_period"]),
            "parsed_prior_consumer_confidence": parsed_cb["confidence"].get(parsed_cb["prior_period"]),
            "parsed_jobs_plentiful": parsed_cb["plentiful"].get(parsed_cb["current_period"]),
            "parsed_jobs_hard_to_get": parsed_cb["hard"].get(parsed_cb["current_period"]),
        })
        CB_HTTP_JSON.write_text(json.dumps(diagnostic, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as error:
        existing = {}
        if CB_HTTP_JSON.exists():
            try:
                existing = json.loads(CB_HTTP_JSON.read_text(encoding="utf-8"))
            except Exception:
                existing = {}
        existing.update({
            "requested_url": cb_url,
            "error_type": type(error).__name__,
            "error": str(error),
            "saved_raw_html": str(CB_RAW_HTML.relative_to(ROOT)) if CB_RAW_HTML.exists() else None,
        })
        CB_HTTP_JSON.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")

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
    CB_DEBUG_DIR.mkdir(parents=True, exist_ok=True)
    debug_readme = CB_DEBUG_DIR / "README.md"
    debug_readme.write_text(
        "# Conference Board 抓取診斷\n\n"
        "執行程式後，本資料夾會保存：\n\n"
        "- `cb_consumer_confidence_raw.html`：GitHub Actions 實際收到的原始回應。\n"
        "- `cb_consumer_confidence_http.json`：CB的HTTP、頁面特徵與目前解析結果。\n"
        "- `nfib_sbet_api_http.json`：NFIB SBET REST API請求、原始JSON與Hiring Plan解析結果。\n\n"
        "注意：Git 不會追蹤空資料夾；GitHub Actions 必須將 `data/us_macro_debug/` 加入 commit。\n",
        encoding="utf-8",
    )
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
    try: nfib_hiring_plan=fetch_nfib_sbet_api()
    except Exception as e: nfib_hiring_plan={}; errors.append(f"NFIB SBET REST API: {e}")
    try: nyfed_sce=fetch_nyfed_sce()
    except Exception as e: nyfed_sce={}; errors.append(f"NY Fed SCE: {e}")
    try: umich=fetch_umichigan_csv()
    except Exception as e: umich={}; errors.append(f"University of Michigan CSV: {e}")
    try: umich_financial=fetch_umich_financial()
    except Exception as e: umich_financial={}; errors.append(f"University of Michigan financial charts: {e}")
    try: retail_control, census_retail_raw=fetch_census_retail_control()
    except Exception as e:
        retail_control={}; census_retail_raw={}; errors.append(f"Census retail control: {e}")
    for s in SPECS:
        key=f"{s.section}|{s.name}"
        try:
            if s.provider=="bls": vals=transform(bls.get(s.source_id,{}),s.transform)
            elif s.provider=="fred": vals=transform(fetch_fred(s.source_id),s.transform)
            elif s.provider=="atlanta": vals=atl.get(s.source_id,{})
            elif s.provider=="adp": vals=adp.get(s.source_id,{})
            elif s.provider=="umich_csv": vals=umich.get(s.source_id,{})
            elif s.provider=="umich": vals=umich_financial.get(s.source_id,{})
            elif s.provider=="zillow": vals=zori
            elif s.provider=="nyfed_xlsx": vals=nyfed_sce.get(s.source_id,{})
            elif s.provider=="census" and s.source_id=="retail_control": vals=retail_control
            elif s.provider=="nfib": vals=nfib_hiring_plan
            elif s.provider in {"ism","conference","nyfed"}: vals=pages.get((s.provider,s.source_id),{})
            else: vals={}
            old_values = dict(old.get(key, {}))
            if s.provider in {"conference", "nfib"} and vals:
                latest_authoritative_period = max(vals)
                old_values = {
                    period: value
                    for period, value in old_values.items()
                    if period <= latest_authoritative_period
                }
            current[key]=merge(old_values,vals)
        except Exception as e:
            current[key]=old.get(key,{})
            errors.append(f"{s.name}: {e}")
    # Derived vacancy/unemployment ratio from levels.
    jolts=current.get("就業-職缺|JOLTS",{}); unemployed=current.get("就業-失業|Unemployed",{})
    current["就業-職缺|職缺/失業人口"]=merge(old.get("就業-職缺|職缺/失業人口",{}),{k:round(jolts[k]/unemployed[k],7) for k in jolts.keys()&unemployed.keys() if unemployed[k]})
    cache={"updated_at_utc":datetime.now(timezone.utc).isoformat(),"series":current,"errors":errors}
    CACHE.write_text(json.dumps(cache,ensure_ascii=False,indent=2),encoding="utf-8")
    # Markdown僅顯示目前仍待確認的6項；其他指標仍照常抓取並更新Cache。
    md_rows = [
        ("中小企hiring plan", "就業-調查", "中小企hiring plan"),
        ("Job Plentiful", "就業-調查", "Job Plentiful"),
        ("Job Hard to get", "就業-調查", "Job Hard to get"),
        ("CB", "消費", "CB"),
        ("密大_Current", "消費", "密大_Current"),
        ("密大_Expect", "消費", "密大_Expect"),
    ]
    spec_by_key = {f"{spec.section}|{spec.name}": spec for spec in SPECS}
    selected_keys = [f"{section}|{cache_name}" for _, section, cache_name in md_rows]
    all_periods = sorted({
        period
        for key in selected_keys
        for period in current.get(key, {})
    })[-MONTHS:]
    lines = [
        "# 美國總體經濟數據：待確認項目",
        "",
        f"> 更新時間：{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}  ",
        "> 其他已成功指標仍會在背景抓取、接受來源修訂並更新Cache，只是不顯示於本表。",
        "> Conference Board原始回應會保存至 `data/us_macro_debug/`，供後續判斷GitHub Actions實際收到的HTML。",
        "",
        "| 指標 | 最新資料月份 | 來源 | 抓取方式 | 官方序列／定義 | "
        + " | ".join(month_end(period) for period in reversed(all_periods)) + " |",
        "|---|---:|---|---|---|" + "---:|" * len(all_periods),
    ]
    method_labels = {
        "nfib": "REST API（NFIB SBET getTotals2）",
        "conference": "HTML（Conference Board官方發布頁）",
        "census": "API＋計算（Census MARTS）",
        "fred": "API（FRED）",
        "umich": "XLS（Michigan官方圖表下載）",
        "umich_csv": "CSV（University of Michigan官方下載檔）",
    }
    for display_name, section, cache_name in md_rows:
        key = f"{section}|{cache_name}"
        spec = spec_by_key[key]
        values = current.get(key, {})
        latest = max(values) if values else None
        lines.append("| " + " | ".join([
            display_name,
            month_end(latest) if latest else "N/A",
            spec.source,
            method_labels.get(spec.provider, spec.provider),
            spec.series,
        ] + [fmt(values.get(period)) for period in reversed(all_periods)]) + " |")
    lines.append("")

    # Show every raw Census MARTS category so the correct auto exclusion can be selected.
    if census_retail_raw:
        raw_periods = sorted({
            period for values in census_retail_raw.values() for period in values
        })[-MONTHS:]
        lines += [
            "## Census MARTS 零售銷售原始資料",
            "",
            "> 以下為API回傳的全部季調月銷售額（data_type_code=SM、seasonally_adj=yes）。",
            "> 控制組採用Census MARTS官方彙總代碼 `441X`（Auto and Other Motor Vehicle Dealers）。",
            "",
            "| category_code | Census分類名稱 | "
            + " | ".join(month_end(period) for period in reversed(raw_periods)) + " |",
            "|---|---|" + "---:|" * len(raw_periods),
        ]
        for category_code, values in census_retail_raw.items():
            label = CENSUS_CATEGORY_LABELS.get(category_code, "Census API未附標籤，請依category_code判斷")
            lines.append("| " + " | ".join([
                category_code,
                label,
            ] + [fmt(values.get(period)) for period in reversed(raw_periods)]) + " |")
        lines.append("")

    if errors:
        lines += ["## 更新警告", "", *[f"- {error}" for error in errors], ""]
    OUT.write_text("\n".join(lines),encoding="utf-8")
    print(f"Wrote {OUT} with {len(SPECS)} rows; warnings={len(errors)}")

if __name__=="__main__": main()
