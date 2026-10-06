# 美國總體經濟數據：待確認項目

> 更新時間：2026-10-06 19:34 UTC  
> 其他已成功指標仍會在背景抓取、接受來源修訂並更新Cache，只是不顯示於本表。
> Conference Board原始回應會保存至 `data/us_macro_debug/`，供後續判斷GitHub Actions實際收到的HTML。

| 指標 | 最新資料月份 | 來源 | 抓取方式 | 官方序列／定義 | 2026/09/30 | 2026/08/31 | 2026/07/31 | 2026/06/30 | 2026/05/31 |
|---|---:|---|---|---|---:|---:|---:|---:|---:|
| 中小企hiring plan | 2026/08/31 | NFIB | REST API（NFIB SBET getTotals2） | Plans to Increase Employment | N/A | 5.074 | 4.397 | 3.97 | 3.571 |
| Job Plentiful | 2026/09/30 | The Conference Board | HTML（Conference Board官方發布頁） | Jobs plentiful | 23.6 | 27 | 24.6 | N/A | N/A |
| Job Hard to get | 2026/09/30 | The Conference Board | HTML（Conference Board官方發布頁） | Jobs hard to get | 21.9 | 19.5 | 21.5 | N/A | N/A |
| CB | 2026/09/30 | The Conference Board | HTML（Conference Board官方發布頁） | Consumer Confidence Index | 81.9 | 88.6 | 90.2 | 92.2 | N/A |
| 密大_Current | 2026/09/30 | University of Michigan | CSV（University of Michigan官方下載檔） | ICC | 50.9 | 51.9 | 54.8 | 47.7 | 45.8 |
| 密大_Expect | 2026/09/30 | University of Michigan | CSV（University of Michigan官方下載檔） | ICE | 46.3 | 51.5 | 55.4 | 50.7 | 44.1 |

## Census MARTS 零售銷售原始資料

> 以下為API回傳的全部季調月銷售額（data_type_code=SM、seasonally_adj=yes）。
> 控制組採用Census MARTS官方彙總代碼 `441X`（Auto and Other Motor Vehicle Dealers）。

| category_code | Census分類名稱 | 2026/08/31 | 2026/07/31 | 2026/06/30 | 2026/05/31 | 2026/04/30 |
|---|---|---:|---:|---:|---:|---:|
| 44000 | Retail Trade | 646347 | 639031 | 642793 | 641883 | 635221 |
| 441 | Motor Vehicle and Parts Dealers | 139178 | 138534 | 140955 | 137902 | 136157 |
| 441X | Auto and Other Motor Vehicle Dealers | 127246 | 126743 | 129255 | 126367 | 124602 |
| 442 | Furniture and Home Furnishings Stores | 10611 | 10537 | 10571 | 10645 | 10446 |
| 443 | Electronics and Appliance Stores | 7735 | 7610 | 7624 | 7616 | 7637 |
| 444 | Building Material and Garden Equipment and Supplies Dealers | 44308 | 44294 | 44366 | 43841 | 43909 |
| 445 | Food and Beverage Stores | 84880 | 84507 | 84687 | 84883 | 84723 |
| 4451 | Grocery Stores | 76870 | 76518 | 76684 | 76946 | 76812 |
| 446 | Health and Personal Care Stores | 39216 | 38746 | 38451 | 38448 | 38100 |
| 447 | Gasoline Stations | 63432 | 61607 | 61634 | 65205 | 63594 |
| 448 | Clothing and Clothing Accessories Stores | 26503 | 26311 | 25987 | 26136 | 25864 |
| 44W72 | Retail Trade and Food Services, ex Auto and Gas | 535153 | 529397 | 530309 | 528308 | 524170 |
| 44X72 | Retail Trade and Food Services, Total | 737763 | 729538 | 732898 | 731415 | 723921 |
| 44Y72 | Retail Trade and Food Services, ex Auto | 598585 | 591004 | 591943 | 593513 | 587764 |
| 44Z72 | Retail Trade and Food Services, ex Gas | 674331 | 667931 | 671264 | 666210 | 660327 |
| 451 | Sporting Goods, Hobby, Musical Instrument, and Book Stores | 8752 | 8674 | 8680 | 8643 | 8601 |
| 452 | General Merchandise Stores | 81743 | 81280 | 80870 | 80798 | 80466 |
| 4522 | Census API未附標籤，請依category_code判斷 | 3928 | 3963 | 3959 | 3963 | 3918 |
| 453 | Miscellaneous Store Retailers | 16023 | 15727 | 15756 | 15458 | 14942 |
| 454 | Nonstore Retailers | 123966 | 121204 | 123212 | 122308 | 120782 |
| 722 | Food Services and Drinking Places | 91416 | 90507 | 90105 | 89532 | 88700 |

## 更新警告

- ADP: ADP Pay Insights ZIP could not be parsed; https://payinsights.adp.com/artifacts/us_wage/20261006/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20261005/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20261004/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20261003/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20261002/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20261001/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20260930/documents/ADP_PAY_history.zip: ADP base-pay history returned no usable data for: changer, stayer | https://payinsights.adp.com/artifacts/us_wage/20260929/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20260928/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20260927/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20260926/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20260925/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20260924/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20260923/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20260922/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html)
