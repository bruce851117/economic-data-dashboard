# 美國總體經濟數據：待確認項目

> 更新時間：2026-09-23 18:25 UTC  
> 其他已成功指標仍會在背景抓取、接受來源修訂並更新Cache，只是不顯示於本表。
> Conference Board原始回應會保存至 `data/us_macro_debug/`，供後續判斷GitHub Actions實際收到的HTML。

| 指標 | 最新資料月份 | 來源 | 抓取方式 | 官方序列／定義 | 2026/08/31 | 2026/07/31 | 2026/06/30 | 2026/05/31 | 2026/04/30 |
|---|---:|---|---|---|---:|---:|---:|---:|---:|
| 中小企hiring plan | 2026/08/31 | NFIB | REST API（NFIB SBET getTotals2） | Plans to Increase Employment | 5.074 | 4.397 | 3.97 | 3.571 | 3.778 |
| Job Plentiful | 2026/08/31 | The Conference Board | HTML（Conference Board官方發布頁） | Jobs plentiful | 27 | 24.6 | N/A | N/A | N/A |
| Job Hard to get | 2026/08/31 | The Conference Board | HTML（Conference Board官方發布頁） | Jobs hard to get | 19.5 | 21.5 | N/A | N/A | N/A |
| CB | 2026/08/31 | The Conference Board | HTML（Conference Board官方發布頁） | Consumer Confidence Index | 89.4 | 90.2 | 92.2 | N/A | N/A |
| 密大_Current | 2026/08/31 | University of Michigan | CSV（University of Michigan官方下載檔） | ICC | 51.9 | 54.8 | 47.7 | 45.8 | 52.5 |
| 密大_Expect | 2026/08/31 | University of Michigan | CSV（University of Michigan官方下載檔） | ICE | 51.5 | 55.4 | 50.7 | 44.1 | 48.1 |

## Census MARTS 零售銷售原始資料

> 以下為API回傳的全部季調月銷售額（data_type_code=SM、seasonally_adj=yes）。
> 控制組採用Census MARTS官方彙總代碼 `441X`（Auto and Other Motor Vehicle Dealers）。

| category_code | Census分類名稱 | 2026/08/31 | 2026/07/31 | 2026/06/30 | 2026/05/31 | 2026/04/30 |
|---|---|---:|---:|---:|---:|---:|
| 44000 | Retail Trade | 668877 | 660638 | 665247 | 663604 | 657830 |
| 441 | Motor Vehicle and Parts Dealers | 142379 | 141565 | 144140 | 140675 | 139343 |
| 441X | Auto and Other Motor Vehicle Dealers | 130107 | 129461 | 132145 | 128891 | 127537 |
| 442 | Furniture and Home Furnishings Stores | 11398 | 11296 | 11319 | 11327 | 11152 |
| 443 | Electronics and Appliance Stores | 8307 | 8180 | 8189 | 8149 | 8200 |
| 444 | Building Material and Garden Equipment and Supplies Dealers | 42227 | 42318 | 42380 | 41956 | 41853 |
| 445 | Food and Beverage Stores | 85580 | 85214 | 85408 | 85588 | 85455 |
| 4451 | Grocery Stores | 77153 | 76800 | 76968 | 77209 | 77117 |
| 446 | Health and Personal Care Stores | 40721 | 40355 | 40238 | 40372 | 40086 |
| 447 | Gasoline Stations | 62303 | 60455 | 60586 | 64138 | 62364 |
| 448 | Clothing and Clothing Accessories Stores | 28353 | 28163 | 27792 | 27986 | 27706 |
| 44W72 | Retail Trade and Food Services, ex Auto and Gas | 569265 | 562442 | 563861 | 561379 | 557390 |
| 44X72 | Retail Trade and Food Services, Total | 773947 | 764462 | 768587 | 766192 | 759097 |
| 44Y72 | Retail Trade and Food Services, ex Auto | 631568 | 622897 | 624447 | 625517 | 619754 |
| 44Z72 | Retail Trade and Food Services, ex Gas | 711644 | 704007 | 708001 | 702054 | 696733 |
| 451 | Sporting Goods, Hobby, Musical Instrument, and Book Stores | 9061 | 8951 | 8934 | 8897 | 8885 |
| 452 | General Merchandise Stores | 80388 | 79854 | 79442 | 79432 | 79080 |
| 4522 | Census API未附標籤，請依category_code判斷 | 3297 | 3323 | 3323 | 3327 | 3289 |
| 453 | Miscellaneous Store Retailers | 16821 | 16515 | 16612 | 16324 | 15671 |
| 454 | Nonstore Retailers | 141339 | 137772 | 140207 | 138760 | 138035 |
| 722 | Food Services and Drinking Places | 105070 | 103824 | 103340 | 102588 | 101267 |

## 更新警告

- ADP: ADP Pay Insights ZIP could not be parsed; https://payinsights.adp.com/artifacts/us_wage/20260923/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20260922/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20260921/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20260920/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20260919/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20260918/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20260917/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20260916/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20260915/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20260914/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20260913/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20260912/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20260911/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20260910/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20260909/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html)
