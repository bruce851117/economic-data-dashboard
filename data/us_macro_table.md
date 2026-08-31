# 美國總體經濟數據：待確認項目

> 更新時間：2026-08-31 20:08 UTC  
> 其他已成功指標仍會在背景抓取、接受來源修訂並更新Cache，只是不顯示於本表。
> Conference Board原始回應會保存至 `data/us_macro_debug/`，供後續判斷GitHub Actions實際收到的HTML。

| 指標 | 最新資料月份 | 來源 | 抓取方式 | 官方序列／定義 | 2026/08/31 | 2026/07/31 | 2026/06/30 | 2026/05/31 | 2026/04/30 |
|---|---:|---|---|---|---:|---:|---:|---:|---:|
| 中小企hiring plan | 2026/07/31 | NFIB | REST API（NFIB SBET getTotals2） | Plans to Increase Employment | N/A | 4.397 | 3.97 | 3.571 | 3.778 |
| Job Plentiful | 2026/08/31 | The Conference Board | HTML（Conference Board官方發布頁） | Jobs plentiful | 27 | 24.6 | N/A | N/A | N/A |
| Job Hard to get | 2026/08/31 | The Conference Board | HTML（Conference Board官方發布頁） | Jobs hard to get | 19.5 | 21.5 | N/A | N/A | N/A |
| CB | 2026/08/31 | The Conference Board | HTML（Conference Board官方發布頁） | Consumer Confidence Index | 89.4 | 90.2 | 92.2 | N/A | N/A |
| 密大_Current | 2026/08/31 | University of Michigan | CSV（University of Michigan官方下載檔） | ICC | 51.9 | 54.8 | 47.7 | 45.8 | 52.5 |
| 密大_Expect | 2026/08/31 | University of Michigan | CSV（University of Michigan官方下載檔） | ICE | 51.5 | 55.4 | 50.7 | 44.1 | 48.1 |

## Census MARTS 零售銷售原始資料

> 以下為API回傳的全部季調月銷售額（data_type_code=SM、seasonally_adj=yes）。
> 控制組採用Census MARTS官方彙總代碼 `441X`（Auto and Other Motor Vehicle Dealers）。

| category_code | Census分類名稱 | 2026/07/31 | 2026/06/30 | 2026/05/31 | 2026/04/30 | 2026/03/31 |
|---|---|---:|---:|---:|---:|---:|
| 44000 | Retail Trade | 660047 | 665054 | 663604 | 657830 | 653772 |
| 441 | Motor Vehicle and Parts Dealers | 141426 | 143986 | 140675 | 139343 | 139855 |
| 441X | Auto and Other Motor Vehicle Dealers | 129310 | 132013 | 128891 | 127537 | 128151 |
| 442 | Furniture and Home Furnishings Stores | 11346 | 11315 | 11327 | 11152 | 11283 |
| 443 | Electronics and Appliance Stores | 8113 | 8152 | 8149 | 8200 | 8069 |
| 444 | Building Material and Garden Equipment and Supplies Dealers | 42583 | 42456 | 41956 | 41853 | 41828 |
| 445 | Food and Beverage Stores | 85526 | 85487 | 85588 | 85455 | 84983 |
| 4451 | Grocery Stores | 76993 | 77044 | 77209 | 77117 | 76694 |
| 446 | Health and Personal Care Stores | 40505 | 40224 | 40372 | 40086 | 40178 |
| 447 | Gasoline Stations | 59879 | 60430 | 64138 | 62364 | 60123 |
| 448 | Clothing and Clothing Accessories Stores | 28313 | 27786 | 27986 | 27706 | 27854 |
| 44W72 | Retail Trade and Food Services, ex Auto and Gas | 562297 | 563656 | 561379 | 557390 | 554035 |
| 44X72 | Retail Trade and Food Services, Total | 763602 | 768072 | 766192 | 759097 | 754013 |
| 44Y72 | Retail Trade and Food Services, ex Auto | 622176 | 624086 | 625517 | 619754 | 614158 |
| 44Z72 | Retail Trade and Food Services, ex Gas | 703723 | 707642 | 702054 | 696733 | 693890 |
| 451 | Sporting Goods, Hobby, Musical Instrument, and Book Stores | 8936 | 8940 | 8897 | 8885 | 8659 |
| 452 | General Merchandise Stores | 79761 | 79558 | 79432 | 79080 | 79077 |
| 4522 | Census API未附標籤，請依category_code判斷 | 3329 | 3327 | 3327 | 3289 | 3294 |
| 453 | Miscellaneous Store Retailers | 16760 | 16673 | 16324 | 15671 | 15833 |
| 454 | Nonstore Retailers | 136899 | 140047 | 138760 | 138035 | 136030 |
| 722 | Food Services and Drinking Places | 103555 | 103018 | 102588 | 101267 | 100241 |

## 更新警告

- BLS: ['Your request has failed. Please check your input parameters, and try your request again.']
- ADP: ADP Pay Insights ZIP could not be parsed; https://payinsights.adp.com/artifacts/us_wage/20260831/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20260830/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20260829/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20260828/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20260827/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20260826/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20260825/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20260824/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20260823/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20260822/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20260821/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20260820/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20260819/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20260818/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20260817/ADP_PAY_history.zip: response is not a ZIP file (text/html)
