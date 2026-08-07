# 美國總體經濟數據

> 更新時間：2026-08-07 02:19 UTC  
> 日期為資料所屬月份月底。N/A 代表該月份尚未發布，或官方來源未提供可穩定自動下載的歷史值。

| 指標 | Bloomberg | 最新資料月份 | 來源 | 官方序列 / 定義 | 2026/08/31 |
|---|---|---:|---|---|---:|
| CB | CONCCONF Index | 2026/08/31 | The Conference Board | Consumer Confidence Index | 90.8 |
| ISM製造 | NAPMPMI Index | N/A | Institute for Supply Management | Official monthly report | N/A |
| ISM服務 | NAPMNMI Index | N/A | Institute for Supply Management | Official monthly report | N/A |

## 更新警告

- Official pages: All ISM official monthly reports failed; manufacturing 2026-08: ISM report does not identify August 2026 | services 2026-08: ISM Services PMI value not found | manufacturing 2026-07: ISM Manufacturing PMI value not found | services 2026-07: ISM Services PMI value not found | manufacturing 2026-06: ISM Manufacturing PMI value not found | services 2026-06: ISM Services PMI value not found | manufacturing 2026-05: ISM Manufacturing PMI value not found | services 2026-05: ISM Services PMI value not found | manufacturing 2026-04: ISM Manufacturing PMI value not found | services 2026-04: ISM Services PMI value not found | manufacturing 2026-03: ISM Manufacturing PMI value not found | services 2026-03: ISM Services PMI value not found | manufacturing 2026-02: ISM Manufacturing PMI value not found | services 2026-02: ISM Services PMI value not found | manufacturing 2026-01: ISM Manufacturing PMI value not found | services 2026-01: ISM Services PMI value not found
- Census retail control: Missing CENSUS_API_KEY

## 來源策略

- BLS：Public Data API v2，涵蓋 CPI、PPI 等官方資料。
- Atlanta Fed、ADP：優先使用官方 XLSX、ZIP/CSV。
- University of Michigan：使用官方 tbmics.csv 與 tbmpx1px5.csv；BEA其餘序列沿用FRED API。
- NY Fed SCE使用官方FRBNY-SCE-Data.xlsx；ISM四項改用ISM官方月報；零售控制組使用Census MARTS API的季調月銷售額自行計算。
