# 美國總體經濟數據

> 更新時間：2026-08-07 01:25 UTC  
> 日期為資料所屬月份月底。N/A 代表該月份尚未發布，或官方來源未提供可穩定自動下載的歷史值。

| 指標 | Bloomberg | 最新資料月份 | 來源 | 官方序列 / 定義 | 2026/08/31 | 2026/07/31 | 2026/06/30 | 2026/05/31 | 2026/04/30 |
|---|---|---:|---|---|---:|---:|---:|---:|---:|
| ADP Pay Job Changers薪資 | ADPUJCPG Index | 2026/07/31 | ADP Research | Median YoY job changers | N/A | 7 | 6.8 | 6.5 | 6.6 |
| ADP Pay Job Stayers薪資 | ADPUJSPG Index | 2026/07/31 | ADP Research | Median YoY job stayers | N/A | 4.4 | 4.4 | 4.4 | 4.4 |
| ISM服務就業 | NAPMNEMP Index | N/A | Institute for Supply Management | Official monthly report | N/A | N/A | N/A | N/A | N/A |
| ISM製造就業 | NAPMEMPL Index | N/A | Institute for Supply Management | Official monthly report | N/A | N/A | N/A | N/A | N/A |
| 中小企hiring plan | SBOIHIRE Index | 2026/08/31 | NFIB | Plans to Increase Employment | 12 | N/A | N/A | N/A | N/A |
| 失去工作機率調查 | NYCNJSLJ Index | 2026/06/30 | Federal Reserve Bank of New York | Mean probability of losing a job | N/A | N/A | 14.139 | 15.116 | 14.587 |
| 自願離職調查 | NYCNJSJV Index | 2026/06/30 | Federal Reserve Bank of New York | Mean probability of leaving a job voluntarily | N/A | N/A | 17.267 | 20.755 | 18.171 |
| Job Plentiful | CONCJOBP Index | N/A | The Conference Board | Jobs plentiful | N/A | N/A | N/A | N/A | N/A |
| Job Hard to get | CONCJOBH Index | 2026/08/31 | The Conference Board | Jobs hard to get | 0.7 | N/A | N/A | N/A | N/A |
| NY FED 1y通膨預期 | NYCNM1IR Index | 2026/06/30 | Federal Reserve Bank of New York | Median one-year ahead expected inflation rate | N/A | N/A | 3.673 | 3.462 | 3.637 |
| NY FED 5y通膨預期 | NYCN5IMD Index | 2026/06/30 | Federal Reserve Bank of New York | Median five-year ahead expected inflation rate | N/A | N/A | 3 | 3.015 | 3.009 |
| 密大1y通膨預期 | CONSPXMD Index | 2026/07/31 | University of Michigan | PX_MD | N/A | 4.2 | 4.6 | 4.8 | 4.7 |
| 密大5~10y通膨預期 | CONSP5MD Index | 2026/07/31 | University of Michigan | PX5_MD | N/A | 3.3 | 3.3 | 3.9 | 3.5 |
| 零售控制 | RSTAXAGM Index | N/A | U.S. Census Bureau | MRTS control group | N/A | N/A | N/A | N/A | N/A |
| disposable personal income | PIDSDI Index | 2026/06/30 | Bureau of Economic Analysis | DSPI | N/A | N/A | 23722.6 | 23674.3 | 23508.7 |
| Personal Saving | PIDSS Index | 2026/04/30 | Bureau of Economic Analysis | PSAVE | N/A | N/A | N/A | N/A | 669.435 |
| 家戶金融狀況vs一年前 | CONSPAGI Index | N/A | University of Michigan | PAGO_R_ALL | N/A | N/A | N/A | N/A | N/A |
| 預計未來一年金融狀況 | CONSEXFI Index | N/A | University of Michigan | PEXP_R_ALL | N/A | N/A | N/A | N/A | N/A |
| 密大 | CONSSENT Index | 2026/07/31 | University of Michigan | ICS_ALL | N/A | 55.2 | 49.5 | 44.8 | 49.8 |
| CB | CONCCONF Index | 2026/08/31 | The Conference Board | Consumer Confidence Index | 90.8 | N/A | N/A | N/A | N/A |
| ISM製造 | NAPMPMI Index | N/A | Institute for Supply Management | Official monthly report | N/A | N/A | N/A | N/A | N/A |
| ISM服務 | NAPMNMI Index | N/A | Institute for Supply Management | Official monthly report | N/A | N/A | N/A | N/A | N/A |

## 更新警告

- Official pages: All Investing.com ISM tables failed; services_employment: 403 Client Error: Forbidden for url: https://www.investing.com/economic-calendar/ism-non-manufacturing-employment-1048 | manufacturing_employment: 403 Client Error: Forbidden for url: https://www.investing.com/economic-calendar/ism-manufacturing-employment-1046 | manufacturing_pmi: 403 Client Error: Forbidden for url: https://www.investing.com/economic-calendar/ism-manufacturing-pmi-173 | services_pmi: 403 Client Error: Forbidden for url: https://www.investing.com/economic-calendar/ism-non-manufacturing-pmi-176

## 來源策略

- BLS：Public Data API v2，涵蓋 CPI、PPI 等官方資料。
- Atlanta Fed、ADP：優先使用官方 XLSX、ZIP/CSV。
- University of Michigan：使用官方 tbmics.csv 與 tbmpx1px5.csv；BEA其餘序列沿用FRED API。
- NY Fed SCE：使用官方FRBNY-SCE-Data.xlsx，讀取1年／5年通膨預期、失去工作機率與自願離職機率；ISM四項使用Investing.com經濟日曆歷史表的Actual欄。
