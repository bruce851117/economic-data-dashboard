# 美國總體經濟數據：待確認項目

> 更新時間：2026-08-07 06:15 UTC  
> 其他已成功指標仍會在背景抓取、接受來源修訂並更新Cache，只是不顯示於本表。
> Conference Board原始回應會保存至 `data/us_macro_debug/`，供後續判斷GitHub Actions實際收到的HTML。

| 指標 | 最新資料月份 | 來源 | 抓取方式 | 官方序列／定義 | 2026/08/31 |
|---|---:|---|---|---|---:|
| 中小企hiring plan | 2026/08/31 | NFIB | HTML（NFIB官方Jobs Report） | Plans to Increase Employment | 12 |
| Job Plentiful | N/A | The Conference Board | HTML（Conference Board官方發布頁） | Jobs plentiful | N/A |
| Job Hard to get | 2026/08/31 | The Conference Board | HTML（Conference Board官方發布頁） | Jobs hard to get | 0.7 |
| CB | 2026/08/31 | The Conference Board | HTML（Conference Board官方發布頁） | Consumer Confidence Index | 90.8 |

## Census MARTS 零售銷售原始資料

> 以下為API回傳的全部季調月銷售額（data_type_code=SM、seasonally_adj=yes）。
> 控制組採用Census MARTS官方彙總代碼 `441X`（Auto and Other Motor Vehicle Dealers）。

| category_code | Census分類名稱 | 2026/06/30 | 2026/05/31 | 2026/04/30 | 2026/03/31 | 2026/02/28 |
|---|---|---:|---:|---:|---:|---:|
| 44000 | Retail Trade | 666056 | 664439 | 657830 | 653772 | 641038 |
| 441 | Motor Vehicle and Parts Dealers | 143529 | 140889 | 139343 | 139855 | 139020 |
| 441X | Auto and Other Motor Vehicle Dealers | 131763 | 129141 | 127537 | 128151 | 127214 |
| 442 | Furniture and Home Furnishings Stores | 11323 | 11326 | 11152 | 11283 | 11023 |
| 443 | Electronics and Appliance Stores | 8249 | 8182 | 8200 | 8069 | 7953 |
| 444 | Building Material and Garden Equipment and Supplies Dealers | 41785 | 41739 | 41853 | 41828 | 41290 |
| 445 | Food and Beverage Stores | 85449 | 85612 | 85455 | 84983 | 84066 |
| 4451 | Grocery Stores | 76937 | 77254 | 77117 | 76694 | 75785 |
| 446 | Health and Personal Care Stores | 39917 | 40241 | 40086 | 40178 | 39681 |
| 447 | Gasoline Stations | 60587 | 63959 | 62364 | 60123 | 52660 |
| 448 | Clothing and Clothing Accessories Stores | 27864 | 27952 | 27706 | 27854 | 27797 |
| 44W72 | Retail Trade and Food Services, ex Auto and Gas | 564437 | 562028 | 557390 | 554035 | 549598 |
| 44X72 | Retail Trade and Food Services, Total | 768553 | 766876 | 759097 | 754013 | 741278 |
| 44Y72 | Retail Trade and Food Services, ex Auto | 625024 | 625987 | 619754 | 614158 | 602258 |
| 44Z72 | Retail Trade and Food Services, ex Gas | 707966 | 702917 | 696733 | 693890 | 688618 |
| 451 | Sporting Goods, Hobby, Musical Instrument, and Book Stores | 9071 | 8952 | 8885 | 8659 | 8634 |
| 452 | General Merchandise Stores | 79478 | 79433 | 79080 | 79077 | 77868 |
| 4522 | Census API未附標籤，請依category_code判斷 | 3325 | 3321 | 3289 | 3294 | 3140 |
| 453 | Miscellaneous Store Retailers | 16139 | 16188 | 15671 | 15833 | 16120 |
| 454 | Nonstore Retailers | 142665 | 139966 | 138035 | 136030 | 134926 |
| 722 | Food Services and Drinking Places | 102497 | 102437 | 101267 | 100241 | 100240 |
