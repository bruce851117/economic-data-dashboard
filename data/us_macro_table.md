# 美國總體經濟數據：待確認項目

> 更新時間：2026-10-22 18:34 UTC  
> 其他已成功指標仍會在背景抓取、接受來源修訂並更新Cache，只是不顯示於本表。
> Conference Board原始回應會保存至 `data/us_macro_debug/`，供後續判斷GitHub Actions實際收到的HTML。

| 指標 | 最新資料月份 | 來源 | 抓取方式 | 官方序列／定義 | 2026/09/30 | 2026/08/31 | 2026/07/31 | 2026/06/30 | 2026/05/31 |
|---|---:|---|---|---|---:|---:|---:|---:|---:|
| 中小企hiring plan | 2026/09/30 | NFIB | REST API（NFIB SBET getTotals2） | Plans to Increase Employment | 6.341 | 5.074 | 4.397 | 3.97 | 3.571 |
| Job Plentiful | 2026/09/30 | The Conference Board | HTML（Conference Board官方發布頁） | Jobs plentiful | 23.6 | 27 | 24.6 | N/A | N/A |
| Job Hard to get | 2026/09/30 | The Conference Board | HTML（Conference Board官方發布頁） | Jobs hard to get | 21.9 | 19.5 | 21.5 | N/A | N/A |
| CB | 2026/09/30 | The Conference Board | HTML（Conference Board官方發布頁） | Consumer Confidence Index | 81.9 | 88.6 | 90.2 | 92.2 | N/A |
| 密大_Current | 2026/09/30 | University of Michigan | CSV（University of Michigan官方下載檔） | ICC | 50.9 | 51.9 | 54.8 | 47.7 | 45.8 |
| 密大_Expect | 2026/09/30 | University of Michigan | CSV（University of Michigan官方下載檔） | ICE | 46.3 | 51.5 | 55.4 | 50.7 | 44.1 |

## Census MARTS 零售銷售原始資料

> 以下為API回傳的全部季調月銷售額（data_type_code=SM、seasonally_adj=yes）。
> 控制組採用Census MARTS官方彙總代碼 `441X`（Auto and Other Motor Vehicle Dealers）。

| category_code | Census分類名稱 | 2026/09/30 | 2026/08/31 | 2026/07/31 | 2026/06/30 | 2026/05/31 |
|---|---|---:|---:|---:|---:|---:|
| 44000 | Retail Trade | 652115 | 647440 | 639263 | 642793 | 641883 |
| 441 | Motor Vehicle and Parts Dealers | 139833 | 139525 | 138578 | 140955 | 137902 |
| 441X | Auto and Other Motor Vehicle Dealers | 127788 | 127555 | 126750 | 129255 | 126367 |
| 442 | Furniture and Home Furnishings Stores | 10696 | 10559 | 10538 | 10571 | 10645 |
| 443 | Electronics and Appliance Stores | 7853 | 7806 | 7646 | 7624 | 7616 |
| 444 | Building Material and Garden Equipment and Supplies Dealers | 44077 | 44323 | 44233 | 44366 | 43841 |
| 445 | Food and Beverage Stores | 85056 | 84727 | 84556 | 84687 | 84883 |
| 4451 | Grocery Stores | 77152 | 76783 | 76589 | 76684 | 76946 |
| 446 | Health and Personal Care Stores | 39535 | 39248 | 38777 | 38451 | 38448 |
| 447 | Gasoline Stations | 68021 | 63950 | 61509 | 61634 | 65205 |
| 448 | Clothing and Clothing Accessories Stores | 26478 | 26486 | 26327 | 25987 | 26136 |
| 44W72 | Retail Trade and Food Services, ex Auto and Gas | 537167 | 535847 | 529828 | 530309 | 528308 |
| 44X72 | Retail Trade and Food Services, Total | 745021 | 739322 | 729915 | 732898 | 731415 |
| 44Y72 | Retail Trade and Food Services, ex Auto | 605188 | 599797 | 591337 | 591943 | 593513 |
| 44Z72 | Retail Trade and Food Services, ex Gas | 677000 | 675372 | 668406 | 671264 | 666210 |
| 451 | Sporting Goods, Hobby, Musical Instrument, and Book Stores | 8681 | 8727 | 8640 | 8680 | 8643 |
| 452 | General Merchandise Stores | 81776 | 81844 | 81233 | 80870 | 80798 |
| 4522 | Census API未附標籤，請依category_code判斷 | 4028 | 3963 | 3985 | 3959 | 3963 |
| 453 | Miscellaneous Store Retailers | 15826 | 16319 | 15759 | 15756 | 15458 |
| 454 | Nonstore Retailers | 124283 | 123926 | 121467 | 123212 | 122308 |
| 722 | Food Services and Drinking Places | 92906 | 91882 | 90652 | 90105 | 89532 |

## 更新警告

- BLS: 503 Server Error: Service Unavailable for url: https://api.bls.gov/publicAPI/v2/timeseries/data/
- ADP: ADP Pay Insights ZIP could not be parsed; https://payinsights.adp.com/artifacts/us_wage/20261022/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20261021/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20261020/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20261019/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20261018/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20261017/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20261016/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20261015/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20261014/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20261013/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20261012/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20261011/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20261010/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20261009/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20261008/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html)
- NY Fed SCE: NY Fed workbook missing sheets: Five-year ahead Infl Exp
