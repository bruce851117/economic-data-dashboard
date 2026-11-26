# 美國總體經濟數據：待確認項目

> 更新時間：2026-11-26 23:01 UTC  
> 其他已成功指標仍會在背景抓取、接受來源修訂並更新Cache，只是不顯示於本表。
> Conference Board原始回應會保存至 `data/us_macro_debug/`，供後續判斷GitHub Actions實際收到的HTML。

| 指標 | 最新資料月份 | 來源 | 抓取方式 | 官方序列／定義 | 2026/11/30 | 2026/10/31 | 2026/09/30 | 2026/08/31 | 2026/07/31 |
|---|---:|---|---|---|---:|---:|---:|---:|---:|
| 中小企hiring plan | 2026/10/31 | NFIB | REST API（NFIB SBET getTotals2） | Plans to Increase Employment | N/A | 5.797 | 6.341 | 5.074 | 4.397 |
| Job Plentiful | 2026/11/30 | The Conference Board | HTML（Conference Board官方發布頁） | Jobs plentiful | 30.8 | 26.7 | 23.6 | 27 | 24.6 |
| Job Hard to get | 2026/11/30 | The Conference Board | HTML（Conference Board官方發布頁） | Jobs hard to get | 18.4 | 21.4 | 21.9 | 19.5 | 21.5 |
| CB | 2026/11/30 | The Conference Board | HTML（Conference Board官方發布頁） | Consumer Confidence Index | 103.3 | 91.9 | 84.2 | 88.6 | 90.2 |
| 密大_Current | 2026/11/30 | University of Michigan | CSV（University of Michigan官方下載檔） | ICC | 49.4 | 46.7 | 50.9 | 51.9 | 54.8 |
| 密大_Expect | 2026/11/30 | University of Michigan | CSV（University of Michigan官方下載檔） | ICE | 52.9 | 48.8 | 46.3 | 51.5 | 55.4 |

## Census MARTS 零售銷售原始資料

> 以下為API回傳的全部季調月銷售額（data_type_code=SM、seasonally_adj=yes）。
> 控制組採用Census MARTS官方彙總代碼 `441X`（Auto and Other Motor Vehicle Dealers）。

| category_code | Census分類名稱 | 2026/10/31 | 2026/09/30 | 2026/08/31 | 2026/07/31 | 2026/06/30 |
|---|---|---:|---:|---:|---:|---:|
| 44000 | Retail Trade | 655299 | 653943 | 648652 | 639263 | 642793 |
| 441 | Motor Vehicle and Parts Dealers | 136994 | 139228 | 139501 | 138578 | 140955 |
| 441X | Auto and Other Motor Vehicle Dealers | 124905 | 127132 | 127459 | 126750 | 129255 |
| 442 | Furniture and Home Furnishings Stores | 10685 | 10931 | 10555 | 10538 | 10571 |
| 443 | Electronics and Appliance Stores | 7818 | 7816 | 7796 | 7646 | 7624 |
| 444 | Building Material and Garden Equipment and Supplies Dealers | 44164 | 43959 | 44305 | 44233 | 44366 |
| 445 | Food and Beverage Stores | 85057 | 85211 | 84709 | 84556 | 84687 |
| 4451 | Grocery Stores | 77158 | 77293 | 76774 | 76589 | 76684 |
| 446 | Health and Personal Care Stores | 40327 | 39738 | 39353 | 38777 | 38451 |
| 447 | Gasoline Stations | 68608 | 67581 | 63781 | 61509 | 61634 |
| 448 | Clothing and Clothing Accessories Stores | 26377 | 26575 | 26505 | 26327 | 25987 |
| 44W72 | Retail Trade and Food Services, ex Auto and Gas | 542618 | 539828 | 537220 | 529828 | 530309 |
| 44X72 | Retail Trade and Food Services, Total | 748220 | 746637 | 740502 | 729915 | 732898 |
| 44Y72 | Retail Trade and Food Services, ex Auto | 611226 | 607409 | 601001 | 591337 | 591943 |
| 44Z72 | Retail Trade and Food Services, ex Gas | 679612 | 679056 | 676721 | 668406 | 671264 |
| 451 | Sporting Goods, Hobby, Musical Instrument, and Book Stores | 8670 | 8730 | 8734 | 8640 | 8680 |
| 452 | General Merchandise Stores | 81828 | 81718 | 81825 | 81233 | 80870 |
| 4522 | Census API未附標籤，請依category_code判斷 | 3972 | 3975 | 3933 | 3985 | 3959 |
| 453 | Miscellaneous Store Retailers | 16539 | 15795 | 16288 | 15759 | 15756 |
| 454 | Nonstore Retailers | 128232 | 126661 | 125300 | 121467 | 123212 |
| 722 | Food Services and Drinking Places | 92921 | 92694 | 91850 | 90652 | 90105 |

## 更新警告

- Atlanta Fed: 404 Client Error: Not Found for url: https://www.atlantafed.org/error
- ADP: ADP Pay Insights ZIP could not be parsed; https://payinsights.adp.com/artifacts/us_wage/20261126/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20261125/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20261124/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20261123/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20261122/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20261121/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20261120/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20261119/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20261118/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20261117/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20261116/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20261115/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20261114/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20261113/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html) | https://payinsights.adp.com/artifacts/us_wage/20261112/documents/ADP_PAY_history.zip: response is not a ZIP file (text/html)
- NY Fed SCE: NY Fed workbook missing sheets: Five-year ahead Infl Exp
