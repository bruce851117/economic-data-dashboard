# 美國總體經濟數據：待確認項目

> 更新時間：2026-08-07 02:51 UTC  
> 其他已成功指標仍會在背景抓取並更新Cache，只是不顯示於本表。

| 指標 | 最新資料月份 | 來源 | 抓取方式 | 官方序列／定義 | 2026/08/31 | 2026/07/31 | 2026/06/30 | 2026/05/31 | 2026/04/30 |
|---|---:|---|---|---|---:|---:|---:|---:|---:|
| ISM服務就業 | 2026/07/31 | Institute for Supply Management | HTML（ISM官方月報；雲端阻擋時使用已驗證基準值） | Official monthly report | N/A | 47.4 | 51.2 | 47.9 | 48 |
| ISM製造就業 | 2026/07/31 | Institute for Supply Management | HTML（ISM官方月報；雲端阻擋時使用已驗證基準值） | Official monthly report | N/A | 52.8 | 49.7 | 48.6 | 46.4 |
| 中小企hiring plan | 2026/08/31 | NFIB | HTML（NFIB官方Jobs Report） | Plans to Increase Employment | 12 | N/A | N/A | N/A | N/A |
| Job Plentiful | N/A | The Conference Board | HTML（Conference Board官方發布頁） | Jobs plentiful | N/A | N/A | N/A | N/A | N/A |
| Job Hard to get | 2026/08/31 | The Conference Board | HTML（Conference Board官方發布頁） | Jobs hard to get | 0.7 | N/A | N/A | N/A | N/A |
| 零售控制 | N/A | U.S. Census Bureau | API＋計算（Census MARTS） | MRTS control group | N/A | N/A | N/A | N/A | N/A |
| Personal Saving | 2026/06/30 | Bureau of Economic Analysis | API（FRED） | PMSAVE | N/A | N/A | 646.1 | 667.8 | 694.4 |
| 家戶金融狀況vs一年前 | N/A | University of Michigan | XLS（Michigan官方圖表下載） | PAGO_R_ALL | N/A | N/A | N/A | N/A | N/A |
| 預計未來一年金融狀況 | N/A | University of Michigan | XLS（Michigan官方圖表下載） | PEXP_R_ALL | N/A | N/A | N/A | N/A | N/A |
| CB | 2026/08/31 | The Conference Board | HTML（Conference Board官方發布頁） | Consumer Confidence Index | 90.8 | N/A | N/A | N/A | N/A |
| ISM製造 | 2026/07/31 | Institute for Supply Management | HTML（ISM官方月報；雲端阻擋時使用已驗證基準值） | Official monthly report | N/A | 55.6 | 53.3 | 54 | 52.7 |
| ISM服務 | 2026/07/31 | Institute for Supply Management | HTML（ISM官方月報；雲端阻擋時使用已驗證基準值） | Official monthly report | N/A | 54.1 | 54 | 54.5 | 53.6 |

## 更新警告

- BLS: ['Your request has failed. Please check your input parameters, and try your request again.']
- University of Michigan financial charts: `Import xlrd` failed. Install xlrd >= 2.0.1 for xls Excel support Use pip or conda to install the xlrd package.
- Census retail control: 400 Client Error:  for url: https://api.census.gov/data/timeseries/eits/marts?get=cell_value%2Cdata_type_code%2Ccategory_code%2Cseasonally_adj%2Ctime&time=from+2023-01&data_type_code=SM&key=fdf5925e609b0443a8812f1caa5b7703d6a235f3
