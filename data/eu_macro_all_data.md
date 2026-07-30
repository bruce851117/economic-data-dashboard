# EU Macro Data Debug Snapshot

- Generated at: `2026-07-30T04:02:25.705029+00:00`
- Script version: `2026-07-30-eu-production-v3-commit-markdown`
- Series count: `31`
- Observation count: `3106`

> 此檔案由 update_eu_macro.py 自動產生，完整列出 eu_macro.json 目前保存的所有資料，供人工核對日期、數值、來源及修訂狀態。

## Latest Value Overview

| Block | Series ID | Name | Frequency | Latest Date | Latest Value | Source URL | Release Type |
|---|---|---|---|---|---:|---|---|
| 通膨 | es_core_cpi | 西班牙 Core CPI YoY | monthly | 2026-06-01 | 2.9 | https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/76130?tip=AM&nult=24 |  |
| 通膨 | fr_core_cpi | 法國 Core CPI YoY | monthly | 2026-06-01 | 1 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/011814145?lastNObservations=30 |  |
| 通膨 | de_core_cpi | 德國 Core CPI YoY | monthly | 2026-06-01 | 2.4513947591 | https://www.destatis.de/EN/Themes/Economy/Short-Term-Indicators/Basic-Data/vpi041a.html |  |
| 通膨 | ea_core_cpi | 歐元區 Core CPI YoY | monthly | 2026-06-01 | 2.4 | https://ec.europa.eu/eurostat/web/products-euro-indicators/w/2-01072026-ap |  |
| 失業率 | fr_unemployment_rate | 法國失業率 | quarterly | 2026-03-01 | 8.1 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001688527?lastNObservations=24 |  |
| 失業率 | es_unemployment_rate | 西班牙失業率 | quarterly | 2026-06-01 | 9.87 | https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/65219?tip=AM&nult=24 |  |
| 失業率 | de_unemployment_rate_swda | 德國失業率（季調） | monthly | 2026-06-01 | 6.3 | https://api.statistiken.bundesbank.de/rest/data/BBDL1/M.DE.Y.UNE.UBA000.A0000.A01.D00.0.R00.A?format=sdmx_csv&lang=en&startPeriod=2025-01 |  |
| 失業率 | ea_unemployment_rate | 歐元區失業率 | monthly | 2026-05-01 | 6.2 | https://ec.europa.eu/eurostat/web/products-euro-indicators/w/3-02072026-ap |  |
| 其他就業 | es_employment_change | 西班牙就業變動 | monthly | 2026-06-01 | 92.531 | https://revista.seg-social.es/-/espa%C3%B1a-suma-621.925-afiliados-en-los-primeros-seis-meses-del-a%C3%B1o-y-supera-la-cota-de-los-22-4-millones-de-ocupados |  |
| 其他就業 | de_unemployed_change | 德國失業人口變動 | monthly | 2026-06-01 | 2984 | https://api.statistiken.bundesbank.de/rest/data/BBDL1/M.DE.Y.UNE.UBA000.A0000.A01.D00.0.ABA.A?format=sdmx_csv&lang=en&startPeriod=2025-01 |  |
| 零售 | es_retail | 西班牙零售 | monthly | 2026-05-01 | -0.4 | https://www.ine.es/dyngs/Prensa/en/ICM0526.htm?print=1 |  |
| 零售 | de_retail | 德國零售 | monthly | 2026-05-01 | 1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |
| 零售 | ea_real_retail | 歐元區實質零售 | monthly | 2026-05-01 | 1.6 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |
| 工業 | de_industrial_production | 德國工業生產 | monthly | 2026-05-01 | 0 | https://genesis.destatis.de/genesisWS/downloads/00/tables/42153-0001_00.csv |  |
| 消費者信心 | fr_consumer_confidence | 法國消費者信心 | monthly | 2026-07-01 | 86 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001587668?lastNObservations=24 |  |
| 消費者信心 | de_gfk_consumer_confidence | 德國 GfK 消費者信心 | monthly | 2026-08-01 | -29.6 | https://www.nim.org/en/consumer-climate/detail-consumer-climate/konsumklima-verharrt-auf-niedrigem-niveau |  |
| 消費者信心 | de_zew_current | 德國 ZEW 現況指數 | monthly | 2026-07-01 | -77.6 | https://www.zew.de/en/press/latest-press-releases/strong-rise-in-expectations-1 |  |
| 消費者信心 | de_zew_expectations | 德國 ZEW 預期指數 | monthly | 2026-07-01 | 26.3 | https://www.zew.de/en/press/latest-press-releases/strong-rise-in-expectations-1 |  |
| 製造業 | de_manufacturing_pmi | 德國製造業 PMI | monthly | 2026-07-01 | 52.2 | https://www.pmi.spglobal.com/Public/Home/PressRelease/33afc7650b4243d49379ecc2c469b446 | flash |
| 製造業 | fr_manufacturing_pmi | 法國製造業 PMI | monthly | 2026-07-01 | 50 | https://tradingeconomics.com/france/manufacturing-pmi | flash |
| 製造業 | fr_manufacturing_confidence | 法國製造業信心 | monthly | 2026-07-01 | 101.3 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001585934?lastNObservations=24 |  |
| 製造業 | es_manufacturing_pmi | 西班牙製造業 PMI | monthly | 2026-06-01 | 49.7 | https://tradingeconomics.com/spain/manufacturing-pmi | final |
| 服務業 | de_services_pmi | 德國服務業 PMI | monthly | 2026-07-01 | 49.6 | https://www.pmi.spglobal.com/Public/Home/PressRelease/33afc7650b4243d49379ecc2c469b446 | flash |
| 服務業 | fr_services_pmi | 法國服務業 PMI | monthly | 2026-07-01 | 49.8 | https://tradingeconomics.com/france/services-pmi | flash |
| 服務業 | es_services_pmi | 西班牙服務業 PMI | monthly | 2026-06-01 | 54.2 | https://tradingeconomics.com/spain/services-pmi | final |
| 企業信心 | fr_business_confidence | 法國企業信心 | monthly | 2026-07-01 | 97.2 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001565530?lastNObservations=24 |  |
| 企業信心 | de_ifo_business_climate | 德國 ifo 企業信心 | monthly | 2026-07-01 | 86.6 | https://www.ifo.de/en/survey/ifo-business-climate-index-germany |  |
| GDP | de_gdp_yoy | 德國 GDP YoY | quarterly | 2026-03-01 | 0.5 | https://www.destatis.de/EN/Press/2026/05/PE26_173_811.html |  |
| GDP | es_gdp_yoy | 西班牙 GDP YoY | quarterly | 2026-03-01 | 2.7 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |
| GDP | fr_gdp_yoy | 法國 GDP YoY | quarterly | 2026-03-01 | 0.9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |
| GDP | ea_gdp_yoy | 歐元區 GDP YoY | quarterly | 2026-03-01 | 0.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |

## Complete Historical Data

### 西班牙 Core CPI YoY

- Block: `通膨`
- Series ID: `es_core_cpi`
- Original ticker/label: `西Core CPI`
- Frequency: `monthly`
- Observations: `138`

| Date | Value | Source URL | Source Frequency | Release Type | Status | Note |
|---|---:|---|---|---|---|---|
| 2015-01-01 | 0.2 |  |  |  |  |  |
| 2015-02-01 | 0.2 |  |  |  |  |  |
| 2015-03-01 | 0.2 |  |  |  |  |  |
| 2015-04-01 | 0.3 |  |  |  |  |  |
| 2015-05-01 | 0.5 |  |  |  |  |  |
| 2015-06-01 | 0.6 |  |  |  |  |  |
| 2015-07-01 | 0.8 |  |  |  |  |  |
| 2015-08-01 | 0.7 |  |  |  |  |  |
| 2015-09-01 | 0.8 |  |  |  |  |  |
| 2015-10-01 | 0.9 |  |  |  |  |  |
| 2015-11-01 | 1 |  |  |  |  |  |
| 2015-12-01 | 0.9 |  |  |  |  |  |
| 2016-01-01 | 0.9 |  |  |  |  |  |
| 2016-02-01 | 1 |  |  |  |  |  |
| 2016-03-01 | 1.1 |  |  |  |  |  |
| 2016-04-01 | 0.7 |  |  |  |  |  |
| 2016-05-01 | 0.7 |  |  |  |  |  |
| 2016-06-01 | 0.6 |  |  |  |  |  |
| 2016-07-01 | 0.7 |  |  |  |  |  |
| 2016-08-01 | 0.9 |  |  |  |  |  |
| 2016-09-01 | 0.8 |  |  |  |  |  |
| 2016-10-01 | 0.8 |  |  |  |  |  |
| 2016-11-01 | 0.8 |  |  |  |  |  |
| 2016-12-01 | 1 |  |  |  |  |  |
| 2017-01-01 | 1.1 |  |  |  |  |  |
| 2017-02-01 | 1 |  |  |  |  |  |
| 2017-03-01 | 0.9 |  |  |  |  |  |
| 2017-04-01 | 1.2 |  |  |  |  |  |
| 2017-05-01 | 1 |  |  |  |  |  |
| 2017-06-01 | 1.2 |  |  |  |  |  |
| 2017-07-01 | 1.4 |  |  |  |  |  |
| 2017-08-01 | 1.2 |  |  |  |  |  |
| 2017-09-01 | 1.2 |  |  |  |  |  |
| 2017-10-01 | 0.9 |  |  |  |  |  |
| 2017-11-01 | 0.8 |  |  |  |  |  |
| 2017-12-01 | 0.8 |  |  |  |  |  |
| 2018-01-01 | 0.8 |  |  |  |  |  |
| 2018-02-01 | 1.1 |  |  |  |  |  |
| 2018-03-01 | 1.2 |  |  |  |  |  |
| 2018-04-01 | 0.8 |  |  |  |  |  |
| 2018-05-01 | 1.1 |  |  |  |  |  |
| 2018-06-01 | 1 |  |  |  |  |  |
| 2018-07-01 | 0.9 |  |  |  |  |  |
| 2018-08-01 | 0.8 |  |  |  |  |  |
| 2018-09-01 | 0.8 |  |  |  |  |  |
| 2018-10-01 | 1 |  |  |  |  |  |
| 2018-11-01 | 0.9 |  |  |  |  |  |
| 2018-12-01 | 0.9 |  |  |  |  |  |
| 2019-01-01 | 0.8 |  |  |  |  |  |
| 2019-02-01 | 0.7 |  |  |  |  |  |
| 2019-03-01 | 0.7 |  |  |  |  |  |
| 2019-04-01 | 0.9 |  |  |  |  |  |
| 2019-05-01 | 0.7 |  |  |  |  |  |
| 2019-06-01 | 0.9 |  |  |  |  |  |
| 2019-07-01 | 0.9 |  |  |  |  |  |
| 2019-08-01 | 0.9 |  |  |  |  |  |
| 2019-09-01 | 1 |  |  |  |  |  |
| 2019-10-01 | 1 |  |  |  |  |  |
| 2019-11-01 | 1 |  |  |  |  |  |
| 2019-12-01 | 1 |  |  |  |  |  |
| 2020-01-01 | 1 |  |  |  |  |  |
| 2020-02-01 | 1.2 |  |  |  |  |  |
| 2020-03-01 | 1.1 |  |  |  |  |  |
| 2020-04-01 | 1.1 |  |  |  |  |  |
| 2020-05-01 | 1.1 |  |  |  |  |  |
| 2020-06-01 | 1 |  |  |  |  |  |
| 2020-07-01 | 0.6 |  |  |  |  |  |
| 2020-08-01 | 0.4 |  |  |  |  |  |
| 2020-09-01 | 0.4 |  |  |  |  |  |
| 2020-10-01 | 0.3 |  |  |  |  |  |
| 2020-11-01 | 0.2 |  |  |  |  |  |
| 2020-12-01 | 0.1 |  |  |  |  |  |
| 2021-01-01 | 0.6 |  |  |  |  |  |
| 2021-02-01 | 0.3 |  |  |  |  |  |
| 2021-03-01 | 0.3 |  |  |  |  |  |
| 2021-04-01 | 0 |  |  |  |  |  |
| 2021-05-01 | 0.2 |  |  |  |  |  |
| 2021-06-01 | 0.2 |  |  |  |  |  |
| 2021-07-01 | 0.6 |  |  |  |  |  |
| 2021-08-01 | 0.7 |  |  |  |  |  |
| 2021-09-01 | 1 |  |  |  |  |  |
| 2021-10-01 | 1.4 |  |  |  |  |  |
| 2021-11-01 | 1.7 |  |  |  |  |  |
| 2021-12-01 | 2.1 |  |  |  |  |  |
| 2022-01-01 | 2.4 |  |  |  |  |  |
| 2022-02-01 | 3 |  |  |  |  |  |
| 2022-03-01 | 3.4 |  |  |  |  |  |
| 2022-04-01 | 4.4 |  |  |  |  |  |
| 2022-05-01 | 4.9 |  |  |  |  |  |
| 2022-06-01 | 5.5 |  |  |  |  |  |
| 2022-07-01 | 6.1 |  |  |  |  |  |
| 2022-08-01 | 6.4 |  |  |  |  |  |
| 2022-09-01 | 6.2 |  |  |  |  |  |
| 2022-10-01 | 6.2 |  |  |  |  |  |
| 2022-11-01 | 6.3 |  |  |  |  |  |
| 2022-12-01 | 7 |  |  |  |  |  |
| 2023-01-01 | 7.5 |  |  |  |  |  |
| 2023-02-01 | 7.6 |  |  |  |  |  |
| 2023-03-01 | 7.5 |  |  |  |  |  |
| 2023-04-01 | 6.6 |  |  |  |  |  |
| 2023-05-01 | 6.1 |  |  |  |  |  |
| 2023-06-01 | 5.9 |  |  |  |  |  |
| 2023-07-01 | 6.2 |  |  |  |  |  |
| 2023-08-01 | 6.1 |  |  |  |  |  |
| 2023-09-01 | 5.8 |  |  |  |  |  |
| 2023-10-01 | 5.2 |  |  |  |  |  |
| 2023-11-01 | 4.5 |  |  |  |  |  |
| 2023-12-01 | 3.8 |  |  |  |  |  |
| 2024-01-01 | 3.6 |  |  |  |  |  |
| 2024-02-01 | 3.5 |  |  |  |  |  |
| 2024-03-01 | 3.3 |  |  |  |  |  |
| 2024-04-01 | 2.9 |  |  |  |  |  |
| 2024-05-01 | 3 |  |  |  |  |  |
| 2024-06-01 | 3 |  |  |  |  |  |
| 2024-07-01 | 2.8 |  |  |  |  |  |
| 2024-08-01 | 2.7 |  |  |  |  |  |
| 2024-09-01 | 2.4 |  |  |  |  |  |
| 2024-10-01 | 2.5 |  |  |  |  |  |
| 2024-11-01 | 2.4 |  |  |  |  |  |
| 2024-12-01 | 2.6 |  |  |  |  |  |
| 2025-01-01 | 2.4 |  |  |  |  |  |
| 2025-02-01 | 2.2 |  |  |  |  |  |
| 2025-03-01 | 2 |  |  |  |  |  |
| 2025-04-01 | 2.445415 |  |  |  |  |  |
| 2025-05-01 | 2.2 |  |  |  |  |  |
| 2025-06-01 | 2.2 |  |  |  |  |  |
| 2025-07-01 | 2.3 |  |  |  |  |  |
| 2025-08-01 | 2.4 |  |  |  |  |  |
| 2025-09-01 | 2.4 |  |  |  |  |  |
| 2025-10-01 | 2.5 |  |  |  |  |  |
| 2025-11-01 | 2.6 |  |  |  |  |  |
| 2025-12-01 | 2.6 |  |  |  |  |  |
| 2026-01-01 | 2.6 | https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/76130?tip=AM&nult=24 |  |  |  | INE table=76130; series=IPC292510; Nacional. Subyacente: General sin alimentos no elaborados ni productos energéticos. Variación anual.; stitched at 2026-01 (Base 2021 historical + Base 2025 current) |
| 2026-02-01 | 2.7 | https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/76130?tip=AM&nult=24 |  |  |  | INE table=76130; series=IPC292510; Nacional. Subyacente: General sin alimentos no elaborados ni productos energéticos. Variación anual.; stitched at 2026-01 (Base 2021 historical + Base 2025 current) |
| 2026-03-01 | 2.9 | https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/76130?tip=AM&nult=24 |  |  |  | INE table=76130; series=IPC292510; Nacional. Subyacente: General sin alimentos no elaborados ni productos energéticos. Variación anual.; stitched at 2026-01 (Base 2021 historical + Base 2025 current) |
| 2026-04-01 | 2.8 | https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/76130?tip=AM&nult=24 |  |  |  | INE table=76130; series=IPC292510; Nacional. Subyacente: General sin alimentos no elaborados ni productos energéticos. Variación anual.; stitched at 2026-01 (Base 2021 historical + Base 2025 current) |
| 2026-05-01 | 3 | https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/76130?tip=AM&nult=24 |  |  |  | INE table=76130; series=IPC292510; Nacional. Subyacente: General sin alimentos no elaborados ni productos energéticos. Variación anual.; stitched at 2026-01 (Base 2021 historical + Base 2025 current) |
| 2026-06-01 | 2.9 | https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/76130?tip=AM&nult=24 |  |  |  | INE table=76130; series=IPC292510; Nacional. Subyacente: General sin alimentos no elaborados ni productos energéticos. Variación anual.; stitched at 2026-01 (Base 2021 historical + Base 2025 current) |

### 法國 Core CPI YoY

- Block: `通膨`
- Series ID: `fr_core_cpi`
- Original ticker/label: `法 Core CPI`
- Frequency: `monthly`
- Observations: `138`

| Date | Value | Source URL | Source Frequency | Release Type | Status | Note |
|---|---:|---|---|---|---|---|
| 2015-01-01 | 0.1 |  |  |  |  |  |
| 2015-02-01 | 0.2 |  |  |  |  |  |
| 2015-03-01 | 0.2 |  |  |  |  |  |
| 2015-04-01 | 0.3 |  |  |  |  |  |
| 2015-05-01 | 0.4 |  |  |  |  |  |
| 2015-06-01 | 0.5 |  |  |  |  |  |
| 2015-07-01 | 0.6 |  |  |  |  |  |
| 2015-08-01 | 0.4 |  |  |  |  |  |
| 2015-09-01 | 0.6 |  |  |  |  |  |
| 2015-10-01 | 0.8 |  |  |  |  |  |
| 2015-11-01 | 0.9 |  |  |  |  |  |
| 2015-12-01 | 1 |  |  |  |  |  |
| 2016-01-01 | 0.8 |  |  |  |  |  |
| 2016-02-01 | 0.9 |  |  |  |  |  |
| 2016-03-01 | 0.7 |  |  |  |  |  |
| 2016-04-01 | 0.6 |  |  |  |  |  |
| 2016-05-01 | 0.6 |  |  |  |  |  |
| 2016-06-01 | 0.6 |  |  |  |  |  |
| 2016-07-01 | 0.5 |  |  |  |  |  |
| 2016-08-01 | 0.4 |  |  |  |  |  |
| 2016-09-01 | 0.6 |  |  |  |  |  |
| 2016-10-01 | 0.5 |  |  |  |  |  |
| 2016-11-01 | 0.5 |  |  |  |  |  |
| 2016-12-01 | 0.4 |  |  |  |  |  |
| 2017-01-01 | 0.6 |  |  |  |  |  |
| 2017-02-01 | 0.1 |  |  |  |  |  |
| 2017-03-01 | 0.4 |  |  |  |  |  |
| 2017-04-01 | 0.5 |  |  |  |  |  |
| 2017-05-01 | 0.4 |  |  |  |  |  |
| 2017-06-01 | 0.4 |  |  |  |  |  |
| 2017-07-01 | 0.5 |  |  |  |  |  |
| 2017-08-01 | 0.5 |  |  |  |  |  |
| 2017-09-01 | 0.5 |  |  |  |  |  |
| 2017-10-01 | 0.5 |  |  |  |  |  |
| 2017-11-01 | 0.5 |  |  |  |  |  |
| 2017-12-01 | 0.6 |  |  |  |  |  |
| 2018-01-01 | 0.8 |  |  |  |  |  |
| 2018-02-01 | 0.7 |  |  |  |  |  |
| 2018-03-01 | 0.9 |  |  |  |  |  |
| 2018-04-01 | 0.8 |  |  |  |  |  |
| 2018-05-01 | 1 |  |  |  |  |  |
| 2018-06-01 | 0.8 |  |  |  |  |  |
| 2018-07-01 | 0.8 |  |  |  |  |  |
| 2018-08-01 | 0.9 |  |  |  |  |  |
| 2018-09-01 | 0.7 |  |  |  |  |  |
| 2018-10-01 | 0.8 |  |  |  |  |  |
| 2018-11-01 | 0.7 |  |  |  |  |  |
| 2018-12-01 | 0.7 |  |  |  |  |  |
| 2019-01-01 | 0.7 |  |  |  |  |  |
| 2019-02-01 | 0.6 |  |  |  |  |  |
| 2019-03-01 | 0.5 |  |  |  |  |  |
| 2019-04-01 | 0.8 |  |  |  |  |  |
| 2019-05-01 | 0.5 |  |  |  |  |  |
| 2019-06-01 | 0.9 |  |  |  |  |  |
| 2019-07-01 | 0.9 |  |  |  |  |  |
| 2019-08-01 | 0.7 |  |  |  |  |  |
| 2019-09-01 | 0.9 |  |  |  |  |  |
| 2019-10-01 | 1 |  |  |  |  |  |
| 2019-11-01 | 1 |  |  |  |  |  |
| 2019-12-01 | 1.1 |  |  |  |  |  |
| 2020-01-01 | 1 |  |  |  |  |  |
| 2020-02-01 | 1.2 |  |  |  |  |  |
| 2020-03-01 | 0.7 |  |  |  |  |  |
| 2020-04-01 | 0.3 |  |  |  |  |  |
| 2020-05-01 | 0.6 |  |  |  |  |  |
| 2020-06-01 | 0.3 |  |  |  |  |  |
| 2020-07-01 | 1.3 |  |  |  |  |  |
| 2020-08-01 | 0.5 |  |  |  |  |  |
| 2020-09-01 | 0.5 |  |  |  |  |  |
| 2020-10-01 | 0.3 |  |  |  |  |  |
| 2020-11-01 | 0.4 |  |  |  |  |  |
| 2020-12-01 | 0.2 |  |  |  |  |  |
| 2021-01-01 | 1.1 |  |  |  |  |  |
| 2021-02-01 | 0.5 |  |  |  |  |  |
| 2021-03-01 | 1 |  |  |  |  |  |
| 2021-04-01 | 1 |  |  |  |  |  |
| 2021-05-01 | 0.9 |  |  |  |  |  |
| 2021-06-01 | 1 |  |  |  |  |  |
| 2021-07-01 | 0 |  |  |  |  |  |
| 2021-08-01 | 1 |  |  |  |  |  |
| 2021-09-01 | 1.4 |  |  |  |  |  |
| 2021-10-01 | 1.5 |  |  |  |  |  |
| 2021-11-01 | 1.9 |  |  |  |  |  |
| 2021-12-01 | 2 |  |  |  |  |  |
| 2022-01-01 | 1.6 |  |  |  |  |  |
| 2022-02-01 | 2.3 |  |  |  |  |  |
| 2022-03-01 | 2.6 |  |  |  |  |  |
| 2022-04-01 | 3.1 |  |  |  |  |  |
| 2022-05-01 | 3.6 |  |  |  |  |  |
| 2022-06-01 | 3.7 |  |  |  |  |  |
| 2022-07-01 | 4.3 |  |  |  |  |  |
| 2022-08-01 | 4.7 |  |  |  |  |  |
| 2022-09-01 | 4.6 |  |  |  |  |  |
| 2022-10-01 | 5 |  |  |  |  |  |
| 2022-11-01 | 5.3 |  |  |  |  |  |
| 2022-12-01 | 5.4 |  |  |  |  |  |
| 2023-01-01 | 5.5 |  |  |  |  |  |
| 2023-02-01 | 5.8 |  |  |  |  |  |
| 2023-03-01 | 6 |  |  |  |  |  |
| 2023-04-01 | 6.1 |  |  |  |  |  |
| 2023-05-01 | 5.7 |  |  |  |  |  |
| 2023-06-01 | 5.7 |  |  |  |  |  |
| 2023-07-01 | 5.4 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001768593?lastNObservations=30 |  |  |  | INSEE Base 2015 official annual underlying inflation; idbank=001768593 |
| 2023-08-01 | 5 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001768593?lastNObservations=30 |  |  |  | INSEE Base 2015 official annual underlying inflation; idbank=001768593 |
| 2023-09-01 | 4.6 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001768593?lastNObservations=30 |  |  |  | INSEE Base 2015 official annual underlying inflation; idbank=001768593 |
| 2023-10-01 | 4.2 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001768593?lastNObservations=30 |  |  |  | INSEE Base 2015 official annual underlying inflation; idbank=001768593 |
| 2023-11-01 | 3.5 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001768593?lastNObservations=30 |  |  |  | INSEE Base 2015 official annual underlying inflation; idbank=001768593 |
| 2023-12-01 | 3.4 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001768593?lastNObservations=30 |  |  |  | INSEE Base 2015 official annual underlying inflation; idbank=001768593 |
| 2024-01-01 | 3 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001768593?lastNObservations=30 |  |  |  | INSEE Base 2015 official annual underlying inflation; idbank=001768593 |
| 2024-02-01 | 2.6 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001768593?lastNObservations=30 |  |  |  | INSEE Base 2015 official annual underlying inflation; idbank=001768593 |
| 2024-03-01 | 2.2 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001768593?lastNObservations=30 |  |  |  | INSEE Base 2015 official annual underlying inflation; idbank=001768593 |
| 2024-04-01 | 1.9 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001768593?lastNObservations=30 |  |  |  | INSEE Base 2015 official annual underlying inflation; idbank=001768593 |
| 2024-05-01 | 1.7 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001768593?lastNObservations=30 |  |  |  | INSEE Base 2015 official annual underlying inflation; idbank=001768593 |
| 2024-06-01 | 1.8 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001768593?lastNObservations=30 |  |  |  | INSEE Base 2015 official annual underlying inflation; idbank=001768593 |
| 2024-07-01 | 1.5 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001768593?lastNObservations=30 |  |  |  | INSEE Base 2015 official annual underlying inflation; idbank=001768593 |
| 2024-08-01 | 1.7 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001768593?lastNObservations=30 |  |  |  | INSEE Base 2015 official annual underlying inflation; idbank=001768593 |
| 2024-09-01 | 1.4 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001768593?lastNObservations=30 |  |  |  | INSEE Base 2015 official annual underlying inflation; idbank=001768593 |
| 2024-10-01 | 1.4 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001768593?lastNObservations=30 |  |  |  | INSEE Base 2015 official annual underlying inflation; idbank=001768593 |
| 2024-11-01 | 1.5 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001768593?lastNObservations=30 |  |  |  | INSEE Base 2015 official annual underlying inflation; idbank=001768593 |
| 2024-12-01 | 1.3 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001768593?lastNObservations=30 |  |  |  | INSEE Base 2015 official annual underlying inflation; idbank=001768593 |
| 2025-01-01 | 1.4 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001768593?lastNObservations=30 |  |  |  | INSEE Base 2015 official annual underlying inflation; idbank=001768593 |
| 2025-02-01 | 1.3 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001768593?lastNObservations=30 |  |  |  | INSEE Base 2015 official annual underlying inflation; idbank=001768593 |
| 2025-03-01 | 1.3 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001768593?lastNObservations=30 |  |  |  | INSEE Base 2015 official annual underlying inflation; idbank=001768593 |
| 2025-04-01 | 1.3 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001768593?lastNObservations=30 |  |  |  | INSEE Base 2015 official annual underlying inflation; idbank=001768593 |
| 2025-05-01 | 1.1 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001768593?lastNObservations=30 |  |  |  | INSEE Base 2015 official annual underlying inflation; idbank=001768593 |
| 2025-06-01 | 1.2 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001768593?lastNObservations=30 |  |  |  | INSEE Base 2015 official annual underlying inflation; idbank=001768593 |
| 2025-07-01 | 1.5 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001768593?lastNObservations=30 |  |  |  | INSEE Base 2015 official annual underlying inflation; idbank=001768593 |
| 2025-08-01 | 1.2 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001768593?lastNObservations=30 |  |  |  | INSEE Base 2015 official annual underlying inflation; idbank=001768593 |
| 2025-09-01 | 1.3 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001768593?lastNObservations=30 |  |  |  | INSEE Base 2015 official annual underlying inflation; idbank=001768593 |
| 2025-10-01 | 1.2 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001768593?lastNObservations=30 |  |  |  | INSEE Base 2015 official annual underlying inflation; idbank=001768593 |
| 2025-11-01 | 1 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001768593?lastNObservations=30 |  |  |  | INSEE Base 2015 official annual underlying inflation; idbank=001768593 |
| 2025-12-01 | 1.1 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001768593?lastNObservations=30 |  |  |  | INSEE Base 2015 official annual underlying inflation; idbank=001768593 |
| 2026-01-01 | 0.7 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/011814145?lastNObservations=30 |  |  |  | INSEE Base 2025 official annual underlying inflation; idbank=011814145 |
| 2026-02-01 | 0.9 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/011814145?lastNObservations=30 |  |  |  | INSEE Base 2025 official annual underlying inflation; idbank=011814145 |
| 2026-03-01 | 1.1 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/011814145?lastNObservations=30 |  |  |  | INSEE Base 2025 official annual underlying inflation; idbank=011814145 |
| 2026-04-01 | 1.2 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/011814145?lastNObservations=30 |  |  |  | INSEE Base 2025 official annual underlying inflation; idbank=011814145 |
| 2026-05-01 | 1.5 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/011814145?lastNObservations=30 |  |  |  | INSEE Base 2025 official annual underlying inflation; idbank=011814145 |
| 2026-06-01 | 1 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/011814145?lastNObservations=30 |  |  |  | INSEE Base 2025 official annual underlying inflation; idbank=011814145 |

### 德國 Core CPI YoY

- Block: `通膨`
- Series ID: `de_core_cpi`
- Original ticker/label: `德 Core CPI`
- Frequency: `monthly`
- Observations: `138`

| Date | Value | Source URL | Source Frequency | Release Type | Status | Note |
|---|---:|---|---|---|---|---|
| 2015-01-01 | 1.19957 |  |  |  |  |  |
| 2015-02-01 | 1.0846 |  |  |  |  |  |
| 2015-03-01 | 1.1879 |  |  |  |  |  |
| 2015-04-01 | 1.83982 |  |  |  |  |  |
| 2015-05-01 | 2.16685 |  |  |  |  |  |
| 2015-06-01 | 1.94385 |  |  |  |  |  |
| 2015-07-01 | 1.93756 |  |  |  |  |  |
| 2015-08-01 | 2.04082 |  |  |  |  |  |
| 2015-09-01 | 1.93341 |  |  |  |  |  |
| 2015-10-01 | 2.04301 |  |  |  |  |  |
| 2015-11-01 | 1.18152 |  |  |  |  |  |
| 2015-12-01 | 0.96154 |  |  |  |  |  |
| 2016-01-01 | 1.18534 |  |  |  |  |  |
| 2016-02-01 | 1.18026 |  |  |  |  |  |
| 2016-03-01 | 1.28069 |  |  |  |  |  |
| 2016-04-01 | 0.95643 |  |  |  |  |  |
| 2016-05-01 | 1.16649 |  |  |  |  |  |
| 2016-06-01 | 1.16525 |  |  |  |  |  |
| 2016-07-01 | 1.37276 |  |  |  |  |  |
| 2016-08-01 | 1.05263 |  |  |  |  |  |
| 2016-09-01 | 1.15911 |  |  |  |  |  |
| 2016-10-01 | 1.26449 |  |  |  |  |  |
| 2016-11-01 | 1.16773 |  |  |  |  |  |
| 2016-12-01 | 1.26984 |  |  |  |  |  |
| 2017-01-01 | 0.95847 |  |  |  |  |  |
| 2017-02-01 | 1.06045 |  |  |  |  |  |
| 2017-03-01 | 0.94837 |  |  |  |  |  |
| 2017-04-01 | 1.36842 |  |  |  |  |  |
| 2017-05-01 | 1.04822 |  |  |  |  |  |
| 2017-06-01 | 1.46597 |  |  |  |  |  |
| 2017-07-01 | 1.45833 |  |  |  |  |  |
| 2017-08-01 | 1.45833 |  |  |  |  |  |
| 2017-09-01 | 1.35417 |  |  |  |  |  |
| 2017-10-01 | 1.04058 |  |  |  |  |  |
| 2017-11-01 | 1.15425 |  |  |  |  |  |
| 2017-12-01 | 1.25392 |  |  |  |  |  |
| 2018-01-01 | 1.3713 |  |  |  |  |  |
| 2018-02-01 | 1.25918 |  |  |  |  |  |
| 2018-03-01 | 1.46137 |  |  |  |  |  |
| 2018-04-01 | 1.03842 |  |  |  |  |  |
| 2018-05-01 | 1.55602 |  |  |  |  |  |
| 2018-06-01 | 1.13519 |  |  |  |  |  |
| 2018-07-01 | 1.23203 |  |  |  |  |  |
| 2018-08-01 | 1.23203 |  |  |  |  |  |
| 2018-09-01 | 1.2333 |  |  |  |  |  |
| 2018-10-01 | 1.64778 |  |  |  |  |  |
| 2018-11-01 | 1.34854 |  |  |  |  |  |
| 2018-12-01 | 1.23839 |  |  |  |  |  |
| 2019-01-01 | 1.2487 |  |  |  |  |  |
| 2019-02-01 | 1.34715 |  |  |  |  |  |
| 2019-03-01 | 1.13169 |  |  |  |  |  |
| 2019-04-01 | 1.84994 |  |  |  |  |  |
| 2019-05-01 | 1.22574 |  |  |  |  |  |
| 2019-06-01 | 1.63265 |  |  |  |  |  |
| 2019-07-01 | 1.5213 |  |  |  |  |  |
| 2019-08-01 | 1.5213 |  |  |  |  |  |
| 2019-09-01 | 1.52284 |  |  |  |  |  |
| 2019-10-01 | 1.51976 |  |  |  |  |  |
| 2019-11-01 | 1.53531 |  |  |  |  |  |
| 2019-12-01 | 1.73293 |  |  |  |  |  |
| 2020-01-01 | 2.0555 |  |  |  |  |  |
| 2020-02-01 | 1.84049 |  |  |  |  |  |
| 2020-03-01 | 1.7294 |  |  |  |  |  |
| 2020-04-01 | 1.2109 |  |  |  |  |  |
| 2020-05-01 | 1.31181 |  |  |  |  |  |
| 2020-06-01 | 0.90362 |  |  |  |  |  |
| 2020-07-01 | -0.2997 |  |  |  |  |  |
| 2020-08-01 | -0.1998 |  |  |  |  |  |
| 2020-09-01 | 0 |  |  |  |  |  |
| 2020-10-01 | 0 |  |  |  |  |  |
| 2020-11-01 | 0.80645 |  |  |  |  |  |
| 2020-12-01 | 0.3006 |  |  |  |  |  |
| 2021-01-01 | 1.40986 |  |  |  |  |  |
| 2021-02-01 | 1.50602 |  |  |  |  |  |
| 2021-03-01 | 1.5 |  |  |  |  |  |
| 2021-04-01 | 1.39581 |  |  |  |  |  |
| 2021-05-01 | 1.59362 |  |  |  |  |  |
| 2021-06-01 | 1.89055 |  |  |  |  |  |
| 2021-07-01 | 3.00601 |  |  |  |  |  |
| 2021-08-01 | 3.003 |  |  |  |  |  |
| 2021-09-01 | 3.1 |  |  |  |  |  |
| 2021-10-01 | 3.09382 |  |  |  |  |  |
| 2021-11-01 | 3.3 |  |  |  |  |  |
| 2021-12-01 | 3.5964 |  |  |  |  |  |
| 2022-01-01 | 2.68124 |  |  |  |  |  |
| 2022-02-01 | 2.76954 |  |  |  |  |  |
| 2022-03-01 | 2.95567 |  |  |  |  |  |
| 2022-04-01 | 3.44149 |  |  |  |  |  |
| 2022-05-01 | 3.72549 |  |  |  |  |  |
| 2022-06-01 | 3.32031 |  |  |  |  |  |
| 2022-07-01 | 3.50194 |  |  |  |  |  |
| 2022-08-01 | 3.6929 |  |  |  |  |  |
| 2022-09-01 | 4.55869 |  |  |  |  |  |
| 2022-10-01 | 4.84027 |  |  |  |  |  |
| 2022-11-01 | 5.03388 |  |  |  |  |  |
| 2022-12-01 | 5.20733 |  |  |  |  |  |
| 2023-01-01 | 5.60928 |  |  |  |  |  |
| 2023-02-01 | 5.67854 |  |  |  |  |  |
| 2023-03-01 | 5.83732 |  |  |  |  |  |
| 2023-04-01 | 5.79849 |  |  |  |  |  |
| 2023-05-01 | 5.38752 |  |  |  |  |  |
| 2023-06-01 | 5.76559 |  |  |  |  |  |
| 2023-07-01 | 5.54511 |  |  |  |  |  |
| 2023-08-01 | 5.52952 |  |  |  |  |  |
| 2023-09-01 | 4.63822 |  |  |  |  |  |
| 2023-10-01 | 4.33979 |  |  |  |  |  |
| 2023-11-01 | 3.7788 |  |  |  |  |  |
| 2023-12-01 | 3.48305 |  |  |  |  |  |
| 2024-01-01 | 3.38828 |  |  |  |  |  |
| 2024-02-01 | 3.36976 |  |  |  |  |  |
| 2024-03-01 | 3.34539 |  |  |  |  |  |
| 2024-04-01 | 2.96496 |  |  |  |  |  |
| 2024-05-01 | 3.04933 |  |  |  |  |  |
| 2024-06-01 | 2.94906 |  |  |  |  |  |
| 2024-07-01 | 2.93855 |  |  |  |  |  |
| 2024-08-01 | 2.75311 |  |  |  |  |  |
| 2024-09-01 | 2.74823 |  |  |  |  |  |
| 2024-10-01 | 2.92036 |  |  |  |  |  |
| 2024-11-01 | 3.01954 |  |  |  |  |  |
| 2024-12-01 | 3.27723 |  |  |  |  |  |
| 2025-01-01 | 2.92294 |  |  |  |  |  |
| 2025-02-01 | 2.73128 |  |  |  |  |  |
| 2025-03-01 | 2.62467 |  |  |  |  |  |
| 2025-04-01 | 2.87958 |  |  |  |  |  |
| 2025-05-01 | 2.78503 |  |  |  |  |  |
| 2025-06-01 | 2.69098 |  |  |  |  |  |
| 2025-07-01 | 2.68166 |  |  |  |  |  |
| 2025-08-01 | 2.67935 |  |  |  |  |  |
| 2025-09-01 | 2.761 |  |  |  |  |  |
| 2025-10-01 | 2.83749 |  |  |  |  |  |
| 2025-11-01 | 2.67241 |  |  |  |  |  |
| 2025-12-01 | 2.40137 |  |  |  |  |  |
| 2026-01-01 | 2.4957 |  |  |  |  |  |
| 2026-02-01 | 2.48714 |  |  |  |  |  |
| 2026-03-01 | 2.47229 |  |  |  |  |  |
| 2026-04-01 | 2.2900763359 | https://www.destatis.de/EN/Themes/Economy/Short-Term-Indicators/Basic-Data/vpi041a.html |  |  |  | YoY from official Destatis core CPI levels; API preferred, official HTML table fallback |
| 2026-05-01 | 2.5402201524 | https://www.destatis.de/EN/Themes/Economy/Short-Term-Indicators/Basic-Data/vpi041a.html |  |  |  | YoY from official Destatis core CPI levels; API preferred, official HTML table fallback |
| 2026-06-01 | 2.4513947591 | https://www.destatis.de/EN/Themes/Economy/Short-Term-Indicators/Basic-Data/vpi041a.html |  |  |  | YoY from official Destatis core CPI levels; API preferred, official HTML table fallback |

### 歐元區 Core CPI YoY

- Block: `通膨`
- Series ID: `ea_core_cpi`
- Original ticker/label: `歐 Core CPI`
- Frequency: `monthly`
- Observations: `137`

| Date | Value | Source URL | Source Frequency | Release Type | Status | Note |
|---|---:|---|---|---|---|---|
| 2015-01-01 | 0.6 |  |  |  |  |  |
| 2015-02-01 | 0.7 |  |  |  |  |  |
| 2015-03-01 | 0.7 |  |  |  |  |  |
| 2015-04-01 | 0.9 |  |  |  |  |  |
| 2015-05-01 | 1.3 |  |  |  |  |  |
| 2015-06-01 | 1.2 |  |  |  |  |  |
| 2015-07-01 | 1.4 |  |  |  |  |  |
| 2015-08-01 | 1.4 |  |  |  |  |  |
| 2015-09-01 | 1.3 |  |  |  |  |  |
| 2015-10-01 | 1.4 |  |  |  |  |  |
| 2015-11-01 | 0.9 |  |  |  |  |  |
| 2015-12-01 | 0.9 |  |  |  |  |  |
| 2016-01-01 | 1 |  |  |  |  |  |
| 2016-02-01 | 0.9 |  |  |  |  |  |
| 2016-03-01 | 1 |  |  |  |  |  |
| 2016-04-01 | 0.7 |  |  |  |  |  |
| 2016-05-01 | 0.8 |  |  |  |  |  |
| 2016-06-01 | 0.8 |  |  |  |  |  |
| 2016-07-01 | 0.9 |  |  |  |  |  |
| 2016-08-01 | 0.8 |  |  |  |  |  |
| 2016-09-01 | 0.8 |  |  |  |  |  |
| 2016-10-01 | 0.8 |  |  |  |  |  |
| 2016-11-01 | 0.8 |  |  |  |  |  |
| 2016-12-01 | 0.9 |  |  |  |  |  |
| 2017-01-01 | 0.9 |  |  |  |  |  |
| 2017-02-01 | 0.8 |  |  |  |  |  |
| 2017-03-01 | 0.7 |  |  |  |  |  |
| 2017-04-01 | 1.3 |  |  |  |  |  |
| 2017-05-01 | 0.9 |  |  |  |  |  |
| 2017-06-01 | 1.2 |  |  |  |  |  |
| 2017-07-01 | 1.2 |  |  |  |  |  |
| 2017-08-01 | 1.2 |  |  |  |  |  |
| 2017-09-01 | 1.1 |  |  |  |  |  |
| 2017-10-01 | 0.9 |  |  |  |  |  |
| 2017-11-01 | 0.9 |  |  |  |  |  |
| 2017-12-01 | 0.9 |  |  |  |  |  |
| 2018-01-01 | 1 |  |  |  |  |  |
| 2018-02-01 | 1 |  |  |  |  |  |
| 2018-03-01 | 1.1 |  |  |  |  |  |
| 2018-04-01 | 0.7 |  |  |  |  |  |
| 2018-05-01 | 1.2 |  |  |  |  |  |
| 2018-06-01 | 1 |  |  |  |  |  |
| 2018-07-01 | 1.1 |  |  |  |  |  |
| 2018-08-01 | 1 |  |  |  |  |  |
| 2018-09-01 | 1 |  |  |  |  |  |
| 2018-10-01 | 1.2 |  |  |  |  |  |
| 2018-11-01 | 0.9 |  |  |  |  |  |
| 2018-12-01 | 0.9 |  |  |  |  |  |
| 2019-01-01 | 1.1 |  |  |  |  |  |
| 2019-02-01 | 1 |  |  |  |  |  |
| 2019-03-01 | 0.8 |  |  |  |  |  |
| 2019-04-01 | 1.3 |  |  |  |  |  |
| 2019-05-01 | 0.8 |  |  |  |  |  |
| 2019-06-01 | 1.1 |  |  |  |  |  |
| 2019-07-01 | 0.9 |  |  |  |  |  |
| 2019-08-01 | 1 |  |  |  |  |  |
| 2019-09-01 | 1 |  |  |  |  |  |
| 2019-10-01 | 1.1 |  |  |  |  |  |
| 2019-11-01 | 1.3 |  |  |  |  |  |
| 2019-12-01 | 1.3 |  |  |  |  |  |
| 2020-01-01 | 1.1 |  |  |  |  |  |
| 2020-02-01 | 1.2 |  |  |  |  |  |
| 2020-03-01 | 1 |  |  |  |  |  |
| 2020-04-01 | 0.9 |  |  |  |  |  |
| 2020-05-01 | 0.9 |  |  |  |  |  |
| 2020-06-01 | 0.8 |  |  |  |  |  |
| 2020-07-01 | 1.2 |  |  |  |  |  |
| 2020-08-01 | 0.4 |  |  |  |  |  |
| 2020-09-01 | 0.2 |  |  |  |  |  |
| 2020-10-01 | 0.2 |  |  |  |  |  |
| 2020-11-01 | 0.3 |  |  |  |  |  |
| 2020-12-01 | 0.2 |  |  |  |  |  |
| 2021-01-01 | 1.4 |  |  |  |  |  |
| 2021-02-01 | 1.1 |  |  |  |  |  |
| 2021-03-01 | 0.9 |  |  |  |  |  |
| 2021-04-01 | 0.7 |  |  |  |  |  |
| 2021-05-01 | 0.9 |  |  |  |  |  |
| 2021-06-01 | 0.9 |  |  |  |  |  |
| 2021-07-01 | 0.7 |  |  |  |  |  |
| 2021-08-01 | 1.5 |  |  |  |  |  |
| 2021-09-01 | 1.9 |  |  |  |  |  |
| 2021-10-01 | 2.1 |  |  |  |  |  |
| 2021-11-01 | 2.6 |  |  |  |  |  |
| 2021-12-01 | 2.6 |  |  |  |  |  |
| 2022-01-01 | 2.3 |  |  |  |  |  |
| 2022-02-01 | 2.7 |  |  |  |  |  |
| 2022-03-01 | 3 |  |  |  |  |  |
| 2022-04-01 | 3.5 |  |  |  |  |  |
| 2022-05-01 | 3.8 |  |  |  |  |  |
| 2022-06-01 | 3.7 |  |  |  |  |  |
| 2022-07-01 | 4 |  |  |  |  |  |
| 2022-08-01 | 4.3 |  |  |  |  |  |
| 2022-09-01 | 4.7 |  |  |  |  |  |
| 2022-10-01 | 5 |  |  |  |  |  |
| 2022-11-01 | 5 |  |  |  |  |  |
| 2022-12-01 | 5.2 |  |  |  |  |  |
| 2023-01-01 | 5.3 |  |  |  |  |  |
| 2023-02-01 | 5.6 |  |  |  |  |  |
| 2023-03-01 | 5.7 |  |  |  |  |  |
| 2023-04-01 | 5.6 |  |  |  |  |  |
| 2023-05-01 | 5.3 |  |  |  |  |  |
| 2023-06-01 | 5.5 |  |  |  |  |  |
| 2023-07-01 | 5.5 |  |  |  |  |  |
| 2023-08-01 | 5.3 |  |  |  |  |  |
| 2023-09-01 | 4.5 |  |  |  |  |  |
| 2023-10-01 | 4.2 |  |  |  |  |  |
| 2023-11-01 | 3.6 |  |  |  |  |  |
| 2023-12-01 | 3.4 |  |  |  |  |  |
| 2024-01-01 | 3.3 |  |  |  |  |  |
| 2024-02-01 | 3.1 |  |  |  |  |  |
| 2024-03-01 | 2.9 |  |  |  |  |  |
| 2024-04-01 | 2.7 |  |  |  |  |  |
| 2024-05-01 | 2.9 |  |  |  |  |  |
| 2024-06-01 | 2.9 |  |  |  |  |  |
| 2024-07-01 | 2.8 |  |  |  |  |  |
| 2024-08-01 | 2.8 |  |  |  |  |  |
| 2024-09-01 | 2.7 |  |  |  |  |  |
| 2024-10-01 | 2.7 |  |  |  |  |  |
| 2024-11-01 | 2.7 |  |  |  |  |  |
| 2024-12-01 | 2.7 |  |  |  |  |  |
| 2025-01-01 | 2.7 |  |  |  |  |  |
| 2025-02-01 | 2.6 |  |  |  |  |  |
| 2025-03-01 | 2.4 |  |  |  |  |  |
| 2025-04-01 | 2.7 |  |  |  |  |  |
| 2025-05-01 | 2.3 |  |  |  |  |  |
| 2025-06-01 | 2.3 |  |  |  |  |  |
| 2025-07-01 | 2.3 |  |  |  |  |  |
| 2025-08-01 | 2.3 |  |  |  |  |  |
| 2025-09-01 | 2.4 |  |  |  |  |  |
| 2025-10-01 | 2.4 |  |  |  |  |  |
| 2025-11-01 | 2.4 |  |  |  |  |  |
| 2025-12-01 | 2.3 |  |  |  |  |  |
| 2026-01-01 | 2.2 |  |  |  |  |  |
| 2026-02-01 | 2.4 |  |  |  |  |  |
| 2026-03-01 | 2.3 |  |  |  |  |  |
| 2026-04-01 | 2.2 |  |  |  |  |  |
| 2026-06-01 | 2.4 | https://ec.europa.eu/eurostat/web/products-euro-indicators/w/2-01072026-ap |  |  |  | official Eurostat release table |

### 法國失業率

- Block: `失業率`
- Series ID: `fr_unemployment_rate`
- Original ticker/label: `法 失業率`
- Frequency: `quarterly`
- Observations: `45`

| Date | Value | Source URL | Source Frequency | Release Type | Status | Note |
|---|---:|---|---|---|---|---|
| 2015-03-01 | 10.3 |  |  |  |  |  |
| 2015-06-01 | 10.5 |  |  |  |  |  |
| 2015-09-01 | 10.3 |  |  |  |  |  |
| 2015-12-01 | 10.2 |  |  |  |  |  |
| 2016-03-01 | 10.2 |  |  |  |  |  |
| 2016-06-01 | 10 |  |  |  |  |  |
| 2016-09-01 | 9.9 |  |  |  |  |  |
| 2016-12-01 | 10 |  |  |  |  |  |
| 2017-03-01 | 9.6 |  |  |  |  |  |
| 2017-06-01 | 9.5 |  |  |  |  |  |
| 2017-09-01 | 9.5 |  |  |  |  |  |
| 2017-12-01 | 9 |  |  |  |  |  |
| 2018-03-01 | 9.3 |  |  |  |  |  |
| 2018-06-01 | 9.1 |  |  |  |  |  |
| 2018-09-01 | 8.9 |  |  |  |  |  |
| 2018-12-01 | 8.8 |  |  |  |  |  |
| 2019-03-01 | 8.8 |  |  |  |  |  |
| 2019-06-01 | 8.4 |  |  |  |  |  |
| 2019-09-01 | 8.3 |  |  |  |  |  |
| 2019-12-01 | 8.2 |  |  |  |  |  |
| 2020-03-01 | 7.9 |  |  |  |  |  |
| 2020-06-01 | 7.1 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001688527?lastNObservations=24 |  |  | A |  |
| 2020-09-01 | 9 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001688527?lastNObservations=24 |  |  | A |  |
| 2020-12-01 | 8.1 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001688527?lastNObservations=24 |  |  | A |  |
| 2021-03-01 | 8.2 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001688527?lastNObservations=24 |  |  | A |  |
| 2021-06-01 | 7.9 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001688527?lastNObservations=24 |  |  | A |  |
| 2021-09-01 | 7.9 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001688527?lastNObservations=24 |  |  | A |  |
| 2021-12-01 | 7.4 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001688527?lastNObservations=24 |  |  | A |  |
| 2022-03-01 | 7.4 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001688527?lastNObservations=24 |  |  | A |  |
| 2022-06-01 | 7.4 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001688527?lastNObservations=24 |  |  | A |  |
| 2022-09-01 | 7.2 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001688527?lastNObservations=24 |  |  | A |  |
| 2022-12-01 | 7.2 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001688527?lastNObservations=24 |  |  | A |  |
| 2023-03-01 | 7.1 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001688527?lastNObservations=24 |  |  | A |  |
| 2023-06-01 | 7.2 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001688527?lastNObservations=24 |  |  | A |  |
| 2023-09-01 | 7.4 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001688527?lastNObservations=24 |  |  | A |  |
| 2023-12-01 | 7.6 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001688527?lastNObservations=24 |  |  | A |  |
| 2024-03-01 | 7.5 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001688527?lastNObservations=24 |  |  | A |  |
| 2024-06-01 | 7.3 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001688527?lastNObservations=24 |  |  | A |  |
| 2024-09-01 | 7.4 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001688527?lastNObservations=24 |  |  | A |  |
| 2024-12-01 | 7.3 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001688527?lastNObservations=24 |  |  | A |  |
| 2025-03-01 | 7.4 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001688527?lastNObservations=24 |  |  | A |  |
| 2025-06-01 | 7.6 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001688527?lastNObservations=24 |  |  | A |  |
| 2025-09-01 | 7.7 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001688527?lastNObservations=24 |  |  | A |  |
| 2025-12-01 | 7.9 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001688527?lastNObservations=24 |  |  | A |  |
| 2026-03-01 | 8.1 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001688527?lastNObservations=24 |  |  | A |  |

### 西班牙失業率

- Block: `失業率`
- Series ID: `es_unemployment_rate`
- Original ticker/label: `西 失業率`
- Frequency: `quarterly`
- Observations: `46`

| Date | Value | Source URL | Source Frequency | Release Type | Status | Note |
|---|---:|---|---|---|---|---|
| 2015-03-01 | 23.78 |  |  |  |  |  |
| 2015-06-01 | 22.37 |  |  |  |  |  |
| 2015-09-01 | 21.18 |  |  |  |  |  |
| 2015-12-01 | 20.9 |  |  |  |  |  |
| 2016-03-01 | 21 |  |  |  |  |  |
| 2016-06-01 | 20 |  |  |  |  |  |
| 2016-09-01 | 18.91 |  |  |  |  |  |
| 2016-12-01 | 18.63 |  |  |  |  |  |
| 2017-03-01 | 18.75 |  |  |  |  |  |
| 2017-06-01 | 17.22 |  |  |  |  |  |
| 2017-09-01 | 16.38 |  |  |  |  |  |
| 2017-12-01 | 16.55 |  |  |  |  |  |
| 2018-03-01 | 16.74 |  |  |  |  |  |
| 2018-06-01 | 15.28 |  |  |  |  |  |
| 2018-09-01 | 14.55 |  |  |  |  |  |
| 2018-12-01 | 14.45 |  |  |  |  |  |
| 2019-03-01 | 14.7 |  |  |  |  |  |
| 2019-06-01 | 14.02 |  |  |  |  |  |
| 2019-09-01 | 13.92 |  |  |  |  |  |
| 2019-12-01 | 13.78 |  |  |  |  |  |
| 2020-03-01 | 14.41 |  |  |  |  |  |
| 2020-06-01 | 15.33 |  |  |  |  |  |
| 2020-09-01 | 16.26 | https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/65219?tip=AM&nult=24 |  |  |  | INE table=65219; series=EPA423474; Total Nacional. Tasa de paro de la población. Ambos sexos. Total. |
| 2020-12-01 | 16.13 | https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/65219?tip=AM&nult=24 |  |  |  | INE table=65219; series=EPA423474; Total Nacional. Tasa de paro de la población. Ambos sexos. Total. |
| 2021-03-01 | 16.14 | https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/65219?tip=AM&nult=24 |  |  |  | INE table=65219; series=EPA423474; Total Nacional. Tasa de paro de la población. Ambos sexos. Total. |
| 2021-06-01 | 15.39 | https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/65219?tip=AM&nult=24 |  |  |  | INE table=65219; series=EPA423474; Total Nacional. Tasa de paro de la población. Ambos sexos. Total. |
| 2021-09-01 | 14.71 | https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/65219?tip=AM&nult=24 |  |  |  | INE table=65219; series=EPA423474; Total Nacional. Tasa de paro de la población. Ambos sexos. Total. |
| 2021-12-01 | 13.44 | https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/65219?tip=AM&nult=24 |  |  |  | INE table=65219; series=EPA423474; Total Nacional. Tasa de paro de la población. Ambos sexos. Total. |
| 2022-03-01 | 13.73 | https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/65219?tip=AM&nult=24 |  |  |  | INE table=65219; series=EPA423474; Total Nacional. Tasa de paro de la población. Ambos sexos. Total. |
| 2022-06-01 | 12.69 | https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/65219?tip=AM&nult=24 |  |  |  | INE table=65219; series=EPA423474; Total Nacional. Tasa de paro de la población. Ambos sexos. Total. |
| 2022-09-01 | 12.73 | https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/65219?tip=AM&nult=24 |  |  |  | INE table=65219; series=EPA423474; Total Nacional. Tasa de paro de la población. Ambos sexos. Total. |
| 2022-12-01 | 12.99 | https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/65219?tip=AM&nult=24 |  |  |  | INE table=65219; series=EPA423474; Total Nacional. Tasa de paro de la población. Ambos sexos. Total. |
| 2023-03-01 | 13.38 | https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/65219?tip=AM&nult=24 |  |  |  | INE table=65219; series=EPA423474; Total Nacional. Tasa de paro de la población. Ambos sexos. Total. |
| 2023-06-01 | 11.67 | https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/65219?tip=AM&nult=24 |  |  |  | INE table=65219; series=EPA423474; Total Nacional. Tasa de paro de la población. Ambos sexos. Total. |
| 2023-09-01 | 11.89 | https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/65219?tip=AM&nult=24 |  |  |  | INE table=65219; series=EPA423474; Total Nacional. Tasa de paro de la población. Ambos sexos. Total. |
| 2023-12-01 | 11.8 | https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/65219?tip=AM&nult=24 |  |  |  | INE table=65219; series=EPA423474; Total Nacional. Tasa de paro de la población. Ambos sexos. Total. |
| 2024-03-01 | 12.29 | https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/65219?tip=AM&nult=24 |  |  |  | INE table=65219; series=EPA423474; Total Nacional. Tasa de paro de la población. Ambos sexos. Total. |
| 2024-06-01 | 11.27 | https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/65219?tip=AM&nult=24 |  |  |  | INE table=65219; series=EPA423474; Total Nacional. Tasa de paro de la población. Ambos sexos. Total. |
| 2024-09-01 | 11.21 | https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/65219?tip=AM&nult=24 |  |  |  | INE table=65219; series=EPA423474; Total Nacional. Tasa de paro de la población. Ambos sexos. Total. |
| 2024-12-01 | 10.61 | https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/65219?tip=AM&nult=24 |  |  |  | INE table=65219; series=EPA423474; Total Nacional. Tasa de paro de la población. Ambos sexos. Total. |
| 2025-03-01 | 11.36 | https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/65219?tip=AM&nult=24 |  |  |  | INE table=65219; series=EPA423474; Total Nacional. Tasa de paro de la población. Ambos sexos. Total. |
| 2025-06-01 | 10.29 | https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/65219?tip=AM&nult=24 |  |  |  | INE table=65219; series=EPA423474; Total Nacional. Tasa de paro de la población. Ambos sexos. Total. |
| 2025-09-01 | 10.45 | https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/65219?tip=AM&nult=24 |  |  |  | INE table=65219; series=EPA423474; Total Nacional. Tasa de paro de la población. Ambos sexos. Total. |
| 2025-12-01 | 9.93 | https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/65219?tip=AM&nult=24 |  |  |  | INE table=65219; series=EPA423474; Total Nacional. Tasa de paro de la población. Ambos sexos. Total. |
| 2026-03-01 | 10.83 | https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/65219?tip=AM&nult=24 |  |  |  | INE table=65219; series=EPA423474; Total Nacional. Tasa de paro de la población. Ambos sexos. Total. |
| 2026-06-01 | 9.87 | https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/65219?tip=AM&nult=24 |  |  |  | INE table=65219; series=EPA423474; Total Nacional. Tasa de paro de la población. Ambos sexos. Total. |

### 德國失業率（季調）

- Block: `失業率`
- Series ID: `de_unemployment_rate_swda`
- Original ticker/label: `德 Unemployment Rate SWDA`
- Frequency: `monthly`
- Observations: `138`

| Date | Value | Source URL | Source Frequency | Release Type | Status | Note |
|---|---:|---|---|---|---|---|
| 2015-01-01 | 6.5 |  |  |  |  |  |
| 2015-02-01 | 6.5 |  |  |  |  |  |
| 2015-03-01 | 6.5 |  |  |  |  |  |
| 2015-04-01 | 6.5 |  |  |  |  |  |
| 2015-05-01 | 6.4 |  |  |  |  |  |
| 2015-06-01 | 6.4 |  |  |  |  |  |
| 2015-07-01 | 6.4 |  |  |  |  |  |
| 2015-08-01 | 6.3 |  |  |  |  |  |
| 2015-09-01 | 6.3 |  |  |  |  |  |
| 2015-10-01 | 6.3 |  |  |  |  |  |
| 2015-11-01 | 6.3 |  |  |  |  |  |
| 2015-12-01 | 6.3 |  |  |  |  |  |
| 2016-01-01 | 6.2 |  |  |  |  |  |
| 2016-02-01 | 6.2 |  |  |  |  |  |
| 2016-03-01 | 6.2 |  |  |  |  |  |
| 2016-04-01 | 6.2 |  |  |  |  |  |
| 2016-05-01 | 6.1 |  |  |  |  |  |
| 2016-06-01 | 6.1 |  |  |  |  |  |
| 2016-07-01 | 6.1 |  |  |  |  |  |
| 2016-08-01 | 6 |  |  |  |  |  |
| 2016-09-01 | 6 |  |  |  |  |  |
| 2016-10-01 | 6 |  |  |  |  |  |
| 2016-11-01 | 6 |  |  |  |  |  |
| 2016-12-01 | 6 |  |  |  |  |  |
| 2017-01-01 | 5.9 |  |  |  |  |  |
| 2017-02-01 | 5.9 |  |  |  |  |  |
| 2017-03-01 | 5.8 |  |  |  |  |  |
| 2017-04-01 | 5.8 |  |  |  |  |  |
| 2017-05-01 | 5.7 |  |  |  |  |  |
| 2017-06-01 | 5.7 |  |  |  |  |  |
| 2017-07-01 | 5.7 |  |  |  |  |  |
| 2017-08-01 | 5.6 |  |  |  |  |  |
| 2017-09-01 | 5.6 |  |  |  |  |  |
| 2017-10-01 | 5.6 |  |  |  |  |  |
| 2017-11-01 | 5.5 |  |  |  |  |  |
| 2017-12-01 | 5.5 |  |  |  |  |  |
| 2018-01-01 | 5.4 |  |  |  |  |  |
| 2018-02-01 | 5.4 |  |  |  |  |  |
| 2018-03-01 | 5.3 |  |  |  |  |  |
| 2018-04-01 | 5.3 |  |  |  |  |  |
| 2018-05-01 | 5.2 |  |  |  |  |  |
| 2018-06-01 | 5.2 |  |  |  |  |  |
| 2018-07-01 | 5.2 |  |  |  |  |  |
| 2018-08-01 | 5.1 |  |  |  |  |  |
| 2018-09-01 | 5.1 |  |  |  |  |  |
| 2018-10-01 | 5.1 |  |  |  |  |  |
| 2018-11-01 | 5 |  |  |  |  |  |
| 2018-12-01 | 5 |  |  |  |  |  |
| 2019-01-01 | 5 |  |  |  |  |  |
| 2019-02-01 | 5 |  |  |  |  |  |
| 2019-03-01 | 5 |  |  |  |  |  |
| 2019-04-01 | 4.9 |  |  |  |  |  |
| 2019-05-01 | 5 |  |  |  |  |  |
| 2019-06-01 | 5 |  |  |  |  |  |
| 2019-07-01 | 5 |  |  |  |  |  |
| 2019-08-01 | 5 |  |  |  |  |  |
| 2019-09-01 | 5 |  |  |  |  |  |
| 2019-10-01 | 5 |  |  |  |  |  |
| 2019-11-01 | 5 |  |  |  |  |  |
| 2019-12-01 | 5 |  |  |  |  |  |
| 2020-01-01 | 5 |  |  |  |  |  |
| 2020-02-01 | 5 |  |  |  |  |  |
| 2020-03-01 | 5 |  |  |  |  |  |
| 2020-04-01 | 5.8 |  |  |  |  |  |
| 2020-05-01 | 6.2 |  |  |  |  |  |
| 2020-06-01 | 6.4 |  |  |  |  |  |
| 2020-07-01 | 6.4 |  |  |  |  |  |
| 2020-08-01 | 6.3 |  |  |  |  |  |
| 2020-09-01 | 6.3 |  |  |  |  |  |
| 2020-10-01 | 6.2 |  |  |  |  |  |
| 2020-11-01 | 6.1 |  |  |  |  |  |
| 2020-12-01 | 6.1 |  |  |  |  |  |
| 2021-01-01 | 6 |  |  |  |  |  |
| 2021-02-01 | 6.1 |  |  |  |  |  |
| 2021-03-01 | 6 |  |  |  |  |  |
| 2021-04-01 | 6 |  |  |  |  |  |
| 2021-05-01 | 6 |  |  |  |  |  |
| 2021-06-01 | 5.8 |  |  |  |  |  |
| 2021-07-01 | 5.6 |  |  |  |  |  |
| 2021-08-01 | 5.5 |  |  |  |  |  |
| 2021-09-01 | 5.4 |  |  |  |  |  |
| 2021-10-01 | 5.3 |  |  |  |  |  |
| 2021-11-01 | 5.2 |  |  |  |  |  |
| 2021-12-01 | 5.2 |  |  |  |  |  |
| 2022-01-01 | 5.1 |  |  |  |  |  |
| 2022-02-01 | 5.1 |  |  |  |  |  |
| 2022-03-01 | 5 |  |  |  |  |  |
| 2022-04-01 | 5 |  |  |  |  |  |
| 2022-05-01 | 5 |  |  |  |  |  |
| 2022-06-01 | 5.3 |  |  |  |  |  |
| 2022-07-01 | 5.4 |  |  |  |  |  |
| 2022-08-01 | 5.5 |  |  |  |  |  |
| 2022-09-01 | 5.5 |  |  |  |  |  |
| 2022-10-01 | 5.5 |  |  |  |  |  |
| 2022-11-01 | 5.5 |  |  |  |  |  |
| 2022-12-01 | 5.5 |  |  |  |  |  |
| 2023-01-01 | 5.5 |  |  |  |  |  |
| 2023-02-01 | 5.5 |  |  |  |  |  |
| 2023-03-01 | 5.6 |  |  |  |  |  |
| 2023-04-01 | 5.6 |  |  |  |  |  |
| 2023-05-01 | 5.6 |  |  |  |  |  |
| 2023-06-01 | 5.6 |  |  |  |  |  |
| 2023-07-01 | 5.7 |  |  |  |  |  |
| 2023-08-01 | 5.7 |  |  |  |  |  |
| 2023-09-01 | 5.7 |  |  |  |  |  |
| 2023-10-01 | 5.8 |  |  |  |  |  |
| 2023-11-01 | 5.8 |  |  |  |  |  |
| 2023-12-01 | 5.9 |  |  |  |  |  |
| 2024-01-01 | 5.9 |  |  |  |  |  |
| 2024-02-01 | 5.9 |  |  |  |  |  |
| 2024-03-01 | 5.9 |  |  |  |  |  |
| 2024-04-01 | 5.9 |  |  |  |  |  |
| 2024-05-01 | 5.9 |  |  |  |  |  |
| 2024-06-01 | 5.9 |  |  |  |  |  |
| 2024-07-01 | 6 |  |  |  |  |  |
| 2024-08-01 | 6 |  |  |  |  |  |
| 2024-09-01 | 6 |  |  |  |  |  |
| 2024-10-01 | 6.1 |  |  |  |  |  |
| 2024-11-01 | 6.1 |  |  |  |  |  |
| 2024-12-01 | 6.2 |  |  |  |  |  |
| 2025-01-01 | 6.2 | https://api.statistiken.bundesbank.de/rest/data/BBDL1/M.DE.Y.UNE.UBA000.A0000.A01.D00.0.R00.A?format=sdmx_csv&lang=en&startPeriod=2025-01 |  |  |  |  |
| 2025-02-01 | 6.2 | https://api.statistiken.bundesbank.de/rest/data/BBDL1/M.DE.Y.UNE.UBA000.A0000.A01.D00.0.R00.A?format=sdmx_csv&lang=en&startPeriod=2025-01 |  |  |  |  |
| 2025-03-01 | 6.3 | https://api.statistiken.bundesbank.de/rest/data/BBDL1/M.DE.Y.UNE.UBA000.A0000.A01.D00.0.R00.A?format=sdmx_csv&lang=en&startPeriod=2025-01 |  |  |  |  |
| 2025-04-01 | 6.3 | https://api.statistiken.bundesbank.de/rest/data/BBDL1/M.DE.Y.UNE.UBA000.A0000.A01.D00.0.R00.A?format=sdmx_csv&lang=en&startPeriod=2025-01 |  |  |  |  |
| 2025-05-01 | 6.3 | https://api.statistiken.bundesbank.de/rest/data/BBDL1/M.DE.Y.UNE.UBA000.A0000.A01.D00.0.R00.A?format=sdmx_csv&lang=en&startPeriod=2025-01 |  |  |  |  |
| 2025-06-01 | 6.3 | https://api.statistiken.bundesbank.de/rest/data/BBDL1/M.DE.Y.UNE.UBA000.A0000.A01.D00.0.R00.A?format=sdmx_csv&lang=en&startPeriod=2025-01 |  |  |  |  |
| 2025-07-01 | 6.3 | https://api.statistiken.bundesbank.de/rest/data/BBDL1/M.DE.Y.UNE.UBA000.A0000.A01.D00.0.R00.A?format=sdmx_csv&lang=en&startPeriod=2025-01 |  |  |  |  |
| 2025-08-01 | 6.3 | https://api.statistiken.bundesbank.de/rest/data/BBDL1/M.DE.Y.UNE.UBA000.A0000.A01.D00.0.R00.A?format=sdmx_csv&lang=en&startPeriod=2025-01 |  |  |  |  |
| 2025-09-01 | 6.3 | https://api.statistiken.bundesbank.de/rest/data/BBDL1/M.DE.Y.UNE.UBA000.A0000.A01.D00.0.R00.A?format=sdmx_csv&lang=en&startPeriod=2025-01 |  |  |  |  |
| 2025-10-01 | 6.3 | https://api.statistiken.bundesbank.de/rest/data/BBDL1/M.DE.Y.UNE.UBA000.A0000.A01.D00.0.R00.A?format=sdmx_csv&lang=en&startPeriod=2025-01 |  |  |  |  |
| 2025-11-01 | 6.3 | https://api.statistiken.bundesbank.de/rest/data/BBDL1/M.DE.Y.UNE.UBA000.A0000.A01.D00.0.R00.A?format=sdmx_csv&lang=en&startPeriod=2025-01 |  |  |  |  |
| 2025-12-01 | 6.3 | https://api.statistiken.bundesbank.de/rest/data/BBDL1/M.DE.Y.UNE.UBA000.A0000.A01.D00.0.R00.A?format=sdmx_csv&lang=en&startPeriod=2025-01 |  |  |  |  |
| 2026-01-01 | 6.3 | https://api.statistiken.bundesbank.de/rest/data/BBDL1/M.DE.Y.UNE.UBA000.A0000.A01.D00.0.R00.A?format=sdmx_csv&lang=en&startPeriod=2025-01 |  |  |  |  |
| 2026-02-01 | 6.3 | https://api.statistiken.bundesbank.de/rest/data/BBDL1/M.DE.Y.UNE.UBA000.A0000.A01.D00.0.R00.A?format=sdmx_csv&lang=en&startPeriod=2025-01 |  |  |  |  |
| 2026-03-01 | 6.3 | https://api.statistiken.bundesbank.de/rest/data/BBDL1/M.DE.Y.UNE.UBA000.A0000.A01.D00.0.R00.A?format=sdmx_csv&lang=en&startPeriod=2025-01 |  |  |  |  |
| 2026-04-01 | 6.4 | https://api.statistiken.bundesbank.de/rest/data/BBDL1/M.DE.Y.UNE.UBA000.A0000.A01.D00.0.R00.A?format=sdmx_csv&lang=en&startPeriod=2025-01 |  |  |  |  |
| 2026-05-01 | 6.3 | https://api.statistiken.bundesbank.de/rest/data/BBDL1/M.DE.Y.UNE.UBA000.A0000.A01.D00.0.R00.A?format=sdmx_csv&lang=en&startPeriod=2025-01 |  |  |  |  |
| 2026-06-01 | 6.3 | https://api.statistiken.bundesbank.de/rest/data/BBDL1/M.DE.Y.UNE.UBA000.A0000.A01.D00.0.R00.A?format=sdmx_csv&lang=en&startPeriod=2025-01 |  |  |  |  |

### 歐元區失業率

- Block: `失業率`
- Series ID: `ea_unemployment_rate`
- Original ticker/label: `歐 失業率`
- Frequency: `monthly`
- Observations: `137`

| Date | Value | Source URL | Source Frequency | Release Type | Status | Note |
|---|---:|---|---|---|---|---|
| 2015-01-01 | 11.4 |  |  |  |  |  |
| 2015-02-01 | 11.3 |  |  |  |  |  |
| 2015-03-01 | 11.3 |  |  |  |  |  |
| 2015-04-01 | 11.2 |  |  |  |  |  |
| 2015-05-01 | 11.1 |  |  |  |  |  |
| 2015-06-01 | 11.1 |  |  |  |  |  |
| 2015-07-01 | 10.8 |  |  |  |  |  |
| 2015-08-01 | 10.7 |  |  |  |  |  |
| 2015-09-01 | 10.7 |  |  |  |  |  |
| 2015-10-01 | 10.7 |  |  |  |  |  |
| 2015-11-01 | 10.6 |  |  |  |  |  |
| 2015-12-01 | 10.5 |  |  |  |  |  |
| 2016-01-01 | 10.5 |  |  |  |  |  |
| 2016-02-01 | 10.4 |  |  |  |  |  |
| 2016-03-01 | 10.3 |  |  |  |  |  |
| 2016-04-01 | 10.3 |  |  |  |  |  |
| 2016-05-01 | 10.2 |  |  |  |  |  |
| 2016-06-01 | 10.1 |  |  |  |  |  |
| 2016-07-01 | 10 |  |  |  |  |  |
| 2016-08-01 | 9.9 |  |  |  |  |  |
| 2016-09-01 | 9.9 |  |  |  |  |  |
| 2016-10-01 | 9.8 |  |  |  |  |  |
| 2016-11-01 | 9.8 |  |  |  |  |  |
| 2016-12-01 | 9.7 |  |  |  |  |  |
| 2017-01-01 | 9.6 |  |  |  |  |  |
| 2017-02-01 | 9.5 |  |  |  |  |  |
| 2017-03-01 | 9.4 |  |  |  |  |  |
| 2017-04-01 | 9.3 |  |  |  |  |  |
| 2017-05-01 | 9.2 |  |  |  |  |  |
| 2017-06-01 | 9.1 |  |  |  |  |  |
| 2017-07-01 | 9 |  |  |  |  |  |
| 2017-08-01 | 9 |  |  |  |  |  |
| 2017-09-01 | 8.9 |  |  |  |  |  |
| 2017-10-01 | 8.8 |  |  |  |  |  |
| 2017-11-01 | 8.7 |  |  |  |  |  |
| 2017-12-01 | 8.7 |  |  |  |  |  |
| 2018-01-01 | 8.7 |  |  |  |  |  |
| 2018-02-01 | 8.6 |  |  |  |  |  |
| 2018-03-01 | 8.5 |  |  |  |  |  |
| 2018-04-01 | 8.4 |  |  |  |  |  |
| 2018-05-01 | 8.3 |  |  |  |  |  |
| 2018-06-01 | 8.2 |  |  |  |  |  |
| 2018-07-01 | 8.1 |  |  |  |  |  |
| 2018-08-01 | 8 |  |  |  |  |  |
| 2018-09-01 | 8 |  |  |  |  |  |
| 2018-10-01 | 8 |  |  |  |  |  |
| 2018-11-01 | 7.9 |  |  |  |  |  |
| 2018-12-01 | 7.8 |  |  |  |  |  |
| 2019-01-01 | 7.8 |  |  |  |  |  |
| 2019-02-01 | 7.8 |  |  |  |  |  |
| 2019-03-01 | 7.7 |  |  |  |  |  |
| 2019-04-01 | 7.7 |  |  |  |  |  |
| 2019-05-01 | 7.6 |  |  |  |  |  |
| 2019-06-01 | 7.5 |  |  |  |  |  |
| 2019-07-01 | 7.5 |  |  |  |  |  |
| 2019-08-01 | 7.4 |  |  |  |  |  |
| 2019-09-01 | 7.4 |  |  |  |  |  |
| 2019-10-01 | 7.4 |  |  |  |  |  |
| 2019-11-01 | 7.4 |  |  |  |  |  |
| 2019-12-01 | 7.4 |  |  |  |  |  |
| 2020-01-01 | 7.4 |  |  |  |  |  |
| 2020-02-01 | 7.3 |  |  |  |  |  |
| 2020-03-01 | 7.2 |  |  |  |  |  |
| 2020-04-01 | 7.4 |  |  |  |  |  |
| 2020-05-01 | 7.6 |  |  |  |  |  |
| 2020-06-01 | 8.1 |  |  |  |  |  |
| 2020-07-01 | 8.5 |  |  |  |  |  |
| 2020-08-01 | 8.6 |  |  |  |  |  |
| 2020-09-01 | 8.5 |  |  |  |  |  |
| 2020-10-01 | 8.4 |  |  |  |  |  |
| 2020-11-01 | 8.2 |  |  |  |  |  |
| 2020-12-01 | 8.2 |  |  |  |  |  |
| 2021-01-01 | 8.2 |  |  |  |  |  |
| 2021-02-01 | 8.2 |  |  |  |  |  |
| 2021-03-01 | 8.2 |  |  |  |  |  |
| 2021-04-01 | 8.2 |  |  |  |  |  |
| 2021-05-01 | 8.1 |  |  |  |  |  |
| 2021-06-01 | 7.8 |  |  |  |  |  |
| 2021-07-01 | 7.6 |  |  |  |  |  |
| 2021-08-01 | 7.5 |  |  |  |  |  |
| 2021-09-01 | 7.4 |  |  |  |  |  |
| 2021-10-01 | 7.2 |  |  |  |  |  |
| 2021-11-01 | 7.1 |  |  |  |  |  |
| 2021-12-01 | 7 |  |  |  |  |  |
| 2022-01-01 | 6.9 |  |  |  |  |  |
| 2022-02-01 | 6.8 |  |  |  |  |  |
| 2022-03-01 | 6.8 |  |  |  |  |  |
| 2022-04-01 | 6.8 |  |  |  |  |  |
| 2022-05-01 | 6.7 |  |  |  |  |  |
| 2022-06-01 | 6.7 |  |  |  |  |  |
| 2022-07-01 | 6.7 |  |  |  |  |  |
| 2022-08-01 | 6.7 |  |  |  |  |  |
| 2022-09-01 | 6.7 |  |  |  |  |  |
| 2022-10-01 | 6.7 |  |  |  |  |  |
| 2022-11-01 | 6.7 |  |  |  |  |  |
| 2022-12-01 | 6.7 |  |  |  |  |  |
| 2023-01-01 | 6.6 |  |  |  |  |  |
| 2023-02-01 | 6.6 |  |  |  |  |  |
| 2023-03-01 | 6.5 |  |  |  |  |  |
| 2023-04-01 | 6.5 |  |  |  |  |  |
| 2023-05-01 | 6.5 |  |  |  |  |  |
| 2023-06-01 | 6.4 |  |  |  |  |  |
| 2023-07-01 | 6.6 |  |  |  |  |  |
| 2023-08-01 | 6.5 |  |  |  |  |  |
| 2023-09-01 | 6.6 |  |  |  |  |  |
| 2023-10-01 | 6.6 |  |  |  |  |  |
| 2023-11-01 | 6.5 |  |  |  |  |  |
| 2023-12-01 | 6.5 |  |  |  |  |  |
| 2024-01-01 | 6.5 |  |  |  |  |  |
| 2024-02-01 | 6.5 |  |  |  |  |  |
| 2024-03-01 | 6.4 |  |  |  |  |  |
| 2024-04-01 | 6.4 |  |  |  |  |  |
| 2024-05-01 | 6.4 |  |  |  |  |  |
| 2024-06-01 | 6.4 |  |  |  |  |  |
| 2024-07-01 | 6.4 |  |  |  |  |  |
| 2024-08-01 | 6.3 |  |  |  |  |  |
| 2024-09-01 | 6.3 |  |  |  |  |  |
| 2024-10-01 | 6.2 |  |  |  |  |  |
| 2024-11-01 | 6.2 |  |  |  |  |  |
| 2024-12-01 | 6.2 |  |  |  |  |  |
| 2025-01-01 | 6.3 |  |  |  |  |  |
| 2025-02-01 | 6.3 |  |  |  |  |  |
| 2025-03-01 | 6.3 |  |  |  |  |  |
| 2025-04-01 | 6.3 |  |  |  |  |  |
| 2025-05-01 | 6.3 |  |  |  |  |  |
| 2025-06-01 | 6.3 |  |  |  |  |  |
| 2025-07-01 | 6.3 |  |  |  |  |  |
| 2025-08-01 | 6.3 |  |  |  |  |  |
| 2025-09-01 | 6.3 |  |  |  |  |  |
| 2025-10-01 | 6.3 |  |  |  |  |  |
| 2025-11-01 | 6.3 |  |  |  |  |  |
| 2025-12-01 | 6.3 |  |  |  |  |  |
| 2026-01-01 | 6.3 |  |  |  |  |  |
| 2026-02-01 | 6.4 |  |  |  |  |  |
| 2026-03-01 | 6.3 |  |  |  |  |  |
| 2026-04-01 | 6.2 |  |  |  |  |  |
| 2026-05-01 | 6.2 | https://ec.europa.eu/eurostat/web/products-euro-indicators/w/3-02072026-ap |  |  |  |  |

### 西班牙就業變動

- Block: `其他就業`
- Series ID: `es_employment_change`
- Original ticker/label: `西 就業`
- Frequency: `monthly`
- Observations: `137`

| Date | Value | Source URL | Source Frequency | Release Type | Status | Note |
|---|---:|---|---|---|---|---|
| 2015-01-01 | 27.7793 |  |  |  |  |  |
| 2015-02-01 | 71.13585 |  |  |  |  |  |
| 2015-03-01 | 76.86826 |  |  |  |  |  |
| 2015-04-01 | 65.17521 |  |  |  |  |  |
| 2015-05-01 | 53.27545 |  |  |  |  |  |
| 2015-06-01 | 9.15121 |  |  |  |  |  |
| 2015-07-01 | 28.19477 |  |  |  |  |  |
| 2015-08-01 | 27.9864 |  |  |  |  |  |
| 2015-09-01 | 34.99524 |  |  |  |  |  |
| 2015-10-01 | 14.4625 |  |  |  |  |  |
| 2015-11-01 | 63.68983 |  |  |  |  |  |
| 2015-12-01 | 64.51192 |  |  |  |  |  |
| 2016-01-01 | 28.01653 |  |  |  |  |  |
| 2016-02-01 | 35.09105 |  |  |  |  |  |
| 2016-03-01 | 49.86955 |  |  |  |  |  |
| 2016-04-01 | 39.58923 |  |  |  |  |  |
| 2016-05-01 | 39.30532 |  |  |  |  |  |
| 2016-06-01 | 64.35452 |  |  |  |  |  |
| 2016-07-01 | 59.87128 |  |  |  |  |  |
| 2016-08-01 | 35.8308 |  |  |  |  |  |
| 2016-09-01 | 40.28805 |  |  |  |  |  |
| 2016-10-01 | 64.8551 |  |  |  |  |  |
| 2016-11-01 | 35.77126 |  |  |  |  |  |
| 2016-12-01 | 50.5614 |  |  |  |  |  |
| 2017-01-01 | 61.46426 |  |  |  |  |  |
| 2017-02-01 | 49.51426 |  |  |  |  |  |
| 2017-03-01 | 67.78653 |  |  |  |  |  |
| 2017-04-01 | 83.15673 |  |  |  |  |  |
| 2017-05-01 | 62.27339 |  |  |  |  |  |
| 2017-06-01 | 50.471 |  |  |  |  |  |
| 2017-07-01 | 36.23577 |  |  |  |  |  |
| 2017-08-01 | 19.13589 |  |  |  |  |  |
| 2017-09-01 | 48.22958 |  |  |  |  |  |
| 2017-10-01 | 49.07135 |  |  |  |  |  |
| 2017-11-01 | 52.27468 |  |  |  |  |  |
| 2017-12-01 | 30.75749 |  |  |  |  |  |
| 2018-01-01 | 64.70254 |  |  |  |  |  |
| 2018-02-01 | 55.32777 |  |  |  |  |  |
| 2018-03-01 | 41.46503 |  |  |  |  |  |
| 2018-04-01 | 50.13313 |  |  |  |  |  |
| 2018-05-01 | 72.69139 |  |  |  |  |  |
| 2018-06-01 | 52.34529 |  |  |  |  |  |
| 2018-07-01 | 20.09234 |  |  |  |  |  |
| 2018-08-01 | 0.16126 |  |  |  |  |  |
| 2018-09-01 | 42.1795 |  |  |  |  |  |
| 2018-10-01 | 69.00271 |  |  |  |  |  |
| 2018-11-01 | 22.64054 |  |  |  |  |  |
| 2018-12-01 | 64.21436 |  |  |  |  |  |
| 2019-01-01 | 50.60827 |  |  |  |  |  |
| 2019-02-01 | 41.97382 |  |  |  |  |  |
| 2019-03-01 | 59.66164 |  |  |  |  |  |
| 2019-04-01 | 61.95229 |  |  |  |  |  |
| 2019-05-01 | 55.37479 |  |  |  |  |  |
| 2019-06-01 | 33.68996 |  |  |  |  |  |
| 2019-07-01 | -2.16285 |  |  |  |  |  |
| 2019-08-01 | -18.8478 |  |  |  |  |  |
| 2019-09-01 | 17.39687 |  |  |  |  |  |
| 2019-10-01 | 39.48222 |  |  |  |  |  |
| 2019-11-01 | 7.71559 |  |  |  |  |  |
| 2019-12-01 | 25.24812 |  |  |  |  |  |
| 2020-01-01 | 17.22551 |  |  |  |  |  |
| 2020-02-01 | 56.10273 |  |  |  |  |  |
| 2020-03-01 | -326.63704 |  |  |  |  |  |
| 2020-04-01 | -667.72647 |  |  |  |  |  |
| 2020-05-01 | -41.49106 |  |  |  |  |  |
| 2020-06-01 | 29.52026 |  |  |  |  |  |
| 2020-07-01 | 139.20952 |  |  |  |  |  |
| 2020-08-01 | 176.65792 |  |  |  |  |  |
| 2020-09-01 | 92.04731 |  |  |  |  |  |
| 2020-10-01 | 46.44166 |  |  |  |  |  |
| 2020-11-01 | 74.41493 |  |  |  |  |  |
| 2020-12-01 | 33.58947 |  |  |  |  |  |
| 2021-01-01 | 31.68208 |  |  |  |  |  |
| 2021-02-01 | 28.10816 |  |  |  |  |  |
| 2021-03-01 | 19.64139 |  |  |  |  |  |
| 2021-04-01 | 29.34778 |  |  |  |  |  |
| 2021-05-01 | 57.99006 |  |  |  |  |  |
| 2021-06-01 | 178.31758 |  |  |  |  |  |
| 2021-07-01 | 89.68018 |  |  |  |  |  |
| 2021-08-01 | 77.94602 |  |  |  |  |  |
| 2021-09-01 | 59.1162 |  |  |  |  |  |
| 2021-10-01 | 73.17817 |  |  |  |  |  |
| 2021-11-01 | 86.1881 |  |  |  |  |  |
| 2021-12-01 | 74.40365 |  |  |  |  |  |
| 2022-01-01 | 61.95905 |  |  |  |  |  |
| 2022-02-01 | 56.7629 |  |  |  |  |  |
| 2022-03-01 | 54.5691 |  |  |  |  |  |
| 2022-04-01 | 52.93 |  |  |  |  |  |
| 2022-05-01 | 60.38 |  |  |  |  |  |
| 2022-06-01 | 54.34 |  |  |  |  |  |
| 2022-07-01 | 21.81 |  |  |  |  |  |
| 2022-08-01 | 23.26 |  |  |  |  |  |
| 2022-09-01 | 35.71 |  |  |  |  |  |
| 2022-10-01 | 33.58 |  |  |  |  |  |
| 2022-11-01 | 30.99 |  |  |  |  |  |
| 2022-12-01 | 27.49 |  |  |  |  |  |
| 2023-01-01 | 44.39 |  |  |  |  |  |
| 2023-02-01 | 63.98 |  |  |  |  |  |
| 2023-03-01 | 88.31 |  |  |  |  |  |
| 2023-04-01 | 79.93 |  |  |  |  |  |
| 2023-05-01 | 37.89 |  |  |  |  |  |
| 2023-06-01 | 21.33 |  |  |  |  |  |
| 2023-07-01 | 43.04 |  |  |  |  |  |
| 2023-08-01 | 46.25 |  |  |  |  |  |
| 2023-09-01 | 32.15 |  |  |  |  |  |
| 2023-10-01 | 22.82 |  |  |  |  |  |
| 2023-11-01 | 33.84 |  |  |  |  |  |
| 2023-12-01 | 41.09 |  |  |  |  |  |
| 2024-01-01 | 44.75 |  |  |  |  |  |
| 2024-02-01 | 58.66 |  |  |  |  |  |
| 2024-03-01 | 57.35 |  |  |  |  |  |
| 2024-04-01 | 41.32 |  |  |  |  |  |
| 2024-05-01 | 46.62 |  |  |  |  |  |
| 2024-06-01 | 38.41 |  |  |  |  |  |
| 2024-07-01 | 29.1 |  |  |  |  |  |
| 2024-08-01 | 33.64 |  |  |  |  |  |
| 2024-09-01 | 35.98 |  |  |  |  |  |
| 2024-10-01 | 41.33 |  |  |  |  |  |
| 2024-11-01 | 35.03 |  |  |  |  |  |
| 2024-12-01 | 41.31 |  |  |  |  |  |
| 2025-01-01 | 44.49 |  |  |  |  |  |
| 2025-02-01 | 43.09 |  |  |  |  |  |
| 2025-03-01 | 39.4 |  |  |  |  |  |
| 2025-04-01 | 45.11 |  |  |  |  |  |
| 2025-05-01 | 37.21 |  |  |  |  |  |
| 2025-06-01 | 38.69 |  |  |  |  |  |
| 2025-07-01 | 41.49 |  |  |  |  |  |
| 2025-08-01 | 41.67 |  |  |  |  |  |
| 2025-09-01 | 47.98 |  |  |  |  |  |
| 2025-10-01 | 50.22 |  |  |  |  |  |
| 2025-11-01 | 42.93 |  |  |  |  |  |
| 2025-12-01 | 35.48 |  |  |  |  |  |
| 2026-01-01 | 17.31 |  |  |  |  |  |
| 2026-02-01 | 45.22 |  |  |  |  |  |
| 2026-03-01 | 80.27 |  |  |  |  |  |
| 2026-04-01 | 41.75 |  |  |  |  |  |
| 2026-06-01 | 92.531 | https://revista.seg-social.es/-/espa%C3%B1a-suma-621.925-afiliados-en-los-primeros-seis-meses-del-a%C3%B1o-y-supera-la-cota-de-los-22-4-millones-de-ocupados |  |  |  | official adjusted monthly change; persons converted to thousand |

### 德國失業人口變動

- Block: `其他就業`
- Series ID: `de_unemployed_change`
- Original ticker/label: `德 失業人口`
- Frequency: `monthly`
- Observations: `138`

| Date | Value | Source URL | Source Frequency | Release Type | Status | Note |
|---|---:|---|---|---|---|---|
| 2015-01-01 | 3 |  |  |  |  |  |
| 2015-02-01 | -14 |  |  |  |  |  |
| 2015-03-01 | -11 |  |  |  |  |  |
| 2015-04-01 | 0 |  |  |  |  |  |
| 2015-05-01 | -9 |  |  |  |  |  |
| 2015-06-01 | -9 |  |  |  |  |  |
| 2015-07-01 | 3 |  |  |  |  |  |
| 2015-08-01 | -14 |  |  |  |  |  |
| 2015-09-01 | -5 |  |  |  |  |  |
| 2015-10-01 | -8 |  |  |  |  |  |
| 2015-11-01 | -15 |  |  |  |  |  |
| 2015-12-01 | -8 |  |  |  |  |  |
| 2016-01-01 | -8 |  |  |  |  |  |
| 2016-02-01 | -7 |  |  |  |  |  |
| 2016-03-01 | 7 |  |  |  |  |  |
| 2016-04-01 | -16 |  |  |  |  |  |
| 2016-05-01 | -14 |  |  |  |  |  |
| 2016-06-01 | -16 |  |  |  |  |  |
| 2016-07-01 | -14 |  |  |  |  |  |
| 2016-08-01 | -15 |  |  |  |  |  |
| 2016-09-01 | 3 |  |  |  |  |  |
| 2016-10-01 | -19 |  |  |  |  |  |
| 2016-11-01 | -4 |  |  |  |  |  |
| 2016-12-01 | -14 |  |  |  |  |  |
| 2017-01-01 | -21 |  |  |  |  |  |
| 2017-02-01 | -10 |  |  |  |  |  |
| 2017-03-01 | -25 |  |  |  |  |  |
| 2017-04-01 | -19 |  |  |  |  |  |
| 2017-05-01 | -11 |  |  |  |  |  |
| 2017-06-01 | 2 |  |  |  |  |  |
| 2017-07-01 | -16 |  |  |  |  |  |
| 2017-08-01 | -13 |  |  |  |  |  |
| 2017-09-01 | -19 |  |  |  |  |  |
| 2017-10-01 | -15 |  |  |  |  |  |
| 2017-11-01 | -12 |  |  |  |  |  |
| 2017-12-01 | -28 |  |  |  |  |  |
| 2018-01-01 | -25 |  |  |  |  |  |
| 2018-02-01 | -13 |  |  |  |  |  |
| 2018-03-01 | -20 |  |  |  |  |  |
| 2018-04-01 | -11 |  |  |  |  |  |
| 2018-05-01 | -13 |  |  |  |  |  |
| 2018-06-01 | -19 |  |  |  |  |  |
| 2018-07-01 | -9 |  |  |  |  |  |
| 2018-08-01 | -14 |  |  |  |  |  |
| 2018-09-01 | -22 |  |  |  |  |  |
| 2018-10-01 | -12 |  |  |  |  |  |
| 2018-11-01 | -5 |  |  |  |  |  |
| 2018-12-01 | -13 |  |  |  |  |  |
| 2019-01-01 | 1 |  |  |  |  |  |
| 2019-02-01 | -19 |  |  |  |  |  |
| 2019-03-01 | -10 |  |  |  |  |  |
| 2019-04-01 | -18 |  |  |  |  |  |
| 2019-05-01 | 59 |  |  |  |  |  |
| 2019-06-01 | -1 |  |  |  |  |  |
| 2019-07-01 | 2 |  |  |  |  |  |
| 2019-08-01 | 0 |  |  |  |  |  |
| 2019-09-01 | -13 |  |  |  |  |  |
| 2019-10-01 | 12 |  |  |  |  |  |
| 2019-11-01 | -7 |  |  |  |  |  |
| 2019-12-01 | 15 |  |  |  |  |  |
| 2020-01-01 | 9 |  |  |  |  |  |
| 2020-02-01 | -16 |  |  |  |  |  |
| 2020-03-01 | -4 |  |  |  |  |  |
| 2020-04-01 | 355 |  |  |  |  |  |
| 2020-05-01 | 232 |  |  |  |  |  |
| 2020-06-01 | 63 |  |  |  |  |  |
| 2020-07-01 | -15 |  |  |  |  |  |
| 2020-08-01 | -14 |  |  |  |  |  |
| 2020-09-01 | -17 |  |  |  |  |  |
| 2020-10-01 | -36 |  |  |  |  |  |
| 2020-11-01 | -37 |  |  |  |  |  |
| 2020-12-01 | -27 |  |  |  |  |  |
| 2021-01-01 | -17 |  |  |  |  |  |
| 2021-02-01 | 12 |  |  |  |  |  |
| 2021-03-01 | -15 |  |  |  |  |  |
| 2021-04-01 | -5 |  |  |  |  |  |
| 2021-05-01 | -25 |  |  |  |  |  |
| 2021-06-01 | -56 |  |  |  |  |  |
| 2021-07-01 | -86 |  |  |  |  |  |
| 2021-08-01 | -65 |  |  |  |  |  |
| 2021-09-01 | -37 |  |  |  |  |  |
| 2021-10-01 | -44 |  |  |  |  |  |
| 2021-11-01 | -38 |  |  |  |  |  |
| 2021-12-01 | -15 |  |  |  |  |  |
| 2022-01-01 | -30 |  |  |  |  |  |
| 2022-02-01 | -28 |  |  |  |  |  |
| 2022-03-01 | -18 |  |  |  |  |  |
| 2022-04-01 | -18 |  |  |  |  |  |
| 2022-05-01 | -3 |  |  |  |  |  |
| 2022-06-01 | 119 |  |  |  |  |  |
| 2022-07-01 | 54 |  |  |  |  |  |
| 2022-08-01 | 26 |  |  |  |  |  |
| 2022-09-01 | 12 |  |  |  |  |  |
| 2022-10-01 | 0 |  |  |  |  |  |
| 2022-11-01 | 16 |  |  |  |  |  |
| 2022-12-01 | -4 |  |  |  |  |  |
| 2023-01-01 | 4 |  |  |  |  |  |
| 2023-02-01 | 9 |  |  |  |  |  |
| 2023-03-01 | 19 |  |  |  |  |  |
| 2023-04-01 | 25 |  |  |  |  |  |
| 2023-05-01 | 6 |  |  |  |  |  |
| 2023-06-01 | 26 |  |  |  |  |  |
| 2023-07-01 | 7 |  |  |  |  |  |
| 2023-08-01 | 26 |  |  |  |  |  |
| 2023-09-01 | 7 |  |  |  |  |  |
| 2023-10-01 | 24 |  |  |  |  |  |
| 2023-11-01 | 23 |  |  |  |  |  |
| 2023-12-01 | 8 |  |  |  |  |  |
| 2024-01-01 | 7 |  |  |  |  |  |
| 2024-02-01 | 17 |  |  |  |  |  |
| 2024-03-01 | 3 |  |  |  |  |  |
| 2024-04-01 | 11 |  |  |  |  |  |
| 2024-05-01 | 20 |  |  |  |  |  |
| 2024-06-01 | 17 |  |  |  |  |  |
| 2024-07-01 | 25 |  |  |  |  |  |
| 2024-08-01 | 10 |  |  |  |  |  |
| 2024-09-01 | 15 |  |  |  |  |  |
| 2024-10-01 | 28 |  |  |  |  |  |
| 2024-11-01 | 9 |  |  |  |  |  |
| 2024-12-01 | 12 |  |  |  |  |  |
| 2025-01-01 | 2889 | https://api.statistiken.bundesbank.de/rest/data/BBDL1/M.DE.Y.UNE.UBA000.A0000.A01.D00.0.ABA.A?format=sdmx_csv&lang=en&startPeriod=2025-01 |  |  |  |  |
| 2025-02-01 | 2899 | https://api.statistiken.bundesbank.de/rest/data/BBDL1/M.DE.Y.UNE.UBA000.A0000.A01.D00.0.ABA.A?format=sdmx_csv&lang=en&startPeriod=2025-01 |  |  |  |  |
| 2025-03-01 | 2924 | https://api.statistiken.bundesbank.de/rest/data/BBDL1/M.DE.Y.UNE.UBA000.A0000.A01.D00.0.ABA.A?format=sdmx_csv&lang=en&startPeriod=2025-01 |  |  |  |  |
| 2025-04-01 | 2921 | https://api.statistiken.bundesbank.de/rest/data/BBDL1/M.DE.Y.UNE.UBA000.A0000.A01.D00.0.ABA.A?format=sdmx_csv&lang=en&startPeriod=2025-01 |  |  |  |  |
| 2025-05-01 | 2956 | https://api.statistiken.bundesbank.de/rest/data/BBDL1/M.DE.Y.UNE.UBA000.A0000.A01.D00.0.ABA.A?format=sdmx_csv&lang=en&startPeriod=2025-01 |  |  |  |  |
| 2025-06-01 | 2964 | https://api.statistiken.bundesbank.de/rest/data/BBDL1/M.DE.Y.UNE.UBA000.A0000.A01.D00.0.ABA.A?format=sdmx_csv&lang=en&startPeriod=2025-01 |  |  |  |  |
| 2025-07-01 | 2968 | https://api.statistiken.bundesbank.de/rest/data/BBDL1/M.DE.Y.UNE.UBA000.A0000.A01.D00.0.ABA.A?format=sdmx_csv&lang=en&startPeriod=2025-01 |  |  |  |  |
| 2025-08-01 | 2961 | https://api.statistiken.bundesbank.de/rest/data/BBDL1/M.DE.Y.UNE.UBA000.A0000.A01.D00.0.ABA.A?format=sdmx_csv&lang=en&startPeriod=2025-01 |  |  |  |  |
| 2025-09-01 | 2974 | https://api.statistiken.bundesbank.de/rest/data/BBDL1/M.DE.Y.UNE.UBA000.A0000.A01.D00.0.ABA.A?format=sdmx_csv&lang=en&startPeriod=2025-01 |  |  |  |  |
| 2025-10-01 | 2973 | https://api.statistiken.bundesbank.de/rest/data/BBDL1/M.DE.Y.UNE.UBA000.A0000.A01.D00.0.ABA.A?format=sdmx_csv&lang=en&startPeriod=2025-01 |  |  |  |  |
| 2025-11-01 | 2974 | https://api.statistiken.bundesbank.de/rest/data/BBDL1/M.DE.Y.UNE.UBA000.A0000.A01.D00.0.ABA.A?format=sdmx_csv&lang=en&startPeriod=2025-01 |  |  |  |  |
| 2025-12-01 | 2977 | https://api.statistiken.bundesbank.de/rest/data/BBDL1/M.DE.Y.UNE.UBA000.A0000.A01.D00.0.ABA.A?format=sdmx_csv&lang=en&startPeriod=2025-01 |  |  |  |  |
| 2026-01-01 | 2978 | https://api.statistiken.bundesbank.de/rest/data/BBDL1/M.DE.Y.UNE.UBA000.A0000.A01.D00.0.ABA.A?format=sdmx_csv&lang=en&startPeriod=2025-01 |  |  |  |  |
| 2026-02-01 | 2979 | https://api.statistiken.bundesbank.de/rest/data/BBDL1/M.DE.Y.UNE.UBA000.A0000.A01.D00.0.ABA.A?format=sdmx_csv&lang=en&startPeriod=2025-01 |  |  |  |  |
| 2026-03-01 | 2979 | https://api.statistiken.bundesbank.de/rest/data/BBDL1/M.DE.Y.UNE.UBA000.A0000.A01.D00.0.ABA.A?format=sdmx_csv&lang=en&startPeriod=2025-01 |  |  |  |  |
| 2026-04-01 | 2998 | https://api.statistiken.bundesbank.de/rest/data/BBDL1/M.DE.Y.UNE.UBA000.A0000.A01.D00.0.ABA.A?format=sdmx_csv&lang=en&startPeriod=2025-01 |  |  |  |  |
| 2026-05-01 | 2986 | https://api.statistiken.bundesbank.de/rest/data/BBDL1/M.DE.Y.UNE.UBA000.A0000.A01.D00.0.ABA.A?format=sdmx_csv&lang=en&startPeriod=2025-01 |  |  |  |  |
| 2026-06-01 | 2984 | https://api.statistiken.bundesbank.de/rest/data/BBDL1/M.DE.Y.UNE.UBA000.A0000.A01.D00.0.ABA.A?format=sdmx_csv&lang=en&startPeriod=2025-01 |  |  |  |  |

### 西班牙零售

- Block: `零售`
- Series ID: `es_retail`
- Original ticker/label: `西 零售`
- Frequency: `monthly`
- Observations: `137`

| Date | Value | Source URL | Source Frequency | Release Type | Status | Note |
|---|---:|---|---|---|---|---|
| 2015-01-01 | 4.3 |  |  |  |  |  |
| 2015-02-01 | 3.1 |  |  |  |  |  |
| 2015-03-01 | 4.4 |  |  |  |  |  |
| 2015-04-01 | 3.2 |  |  |  |  |  |
| 2015-05-01 | 2.4 |  |  |  |  |  |
| 2015-06-01 | 4.6 |  |  |  |  |  |
| 2015-07-01 | 4.7 |  |  |  |  |  |
| 2015-08-01 | 3.9 |  |  |  |  |  |
| 2015-09-01 | 5.5 |  |  |  |  |  |
| 2015-10-01 | 5.8 |  |  |  |  |  |
| 2015-11-01 | 5.1 |  |  |  |  |  |
| 2015-12-01 | 3.7 |  |  |  |  |  |
| 2016-01-01 | 2.3 |  |  |  |  |  |
| 2016-02-01 | 7.7 |  |  |  |  |  |
| 2016-03-01 | 4.7 |  |  |  |  |  |
| 2016-04-01 | 6.6 |  |  |  |  |  |
| 2016-05-01 | 3 |  |  |  |  |  |
| 2016-06-01 | 6.1 |  |  |  |  |  |
| 2016-07-01 | 3.5 |  |  |  |  |  |
| 2016-08-01 | 5.2 |  |  |  |  |  |
| 2016-09-01 | 3.6 |  |  |  |  |  |
| 2016-10-01 | 0.7 |  |  |  |  |  |
| 2016-11-01 | 4.1 |  |  |  |  |  |
| 2016-12-01 | 1.2 |  |  |  |  |  |
| 2017-01-01 | -0.3 |  |  |  |  |  |
| 2017-02-01 | -3.3 |  |  |  |  |  |
| 2017-03-01 | 2.3 |  |  |  |  |  |
| 2017-04-01 | -1.3 |  |  |  |  |  |
| 2017-05-01 | 3.4 |  |  |  |  |  |
| 2017-06-01 | 2.6 |  |  |  |  |  |
| 2017-07-01 | 0.5 |  |  |  |  |  |
| 2017-08-01 | 0.8 |  |  |  |  |  |
| 2017-09-01 | 1.5 |  |  |  |  |  |
| 2017-10-01 | -1.8 |  |  |  |  |  |
| 2017-11-01 | 2.5 |  |  |  |  |  |
| 2017-12-01 | 1.1 |  |  |  |  |  |
| 2018-01-01 | 2.5 |  |  |  |  |  |
| 2018-02-01 | 2.1 |  |  |  |  |  |
| 2018-03-01 | 1.5 |  |  |  |  |  |
| 2018-04-01 | 0.8 |  |  |  |  |  |
| 2018-05-01 | -0.2 |  |  |  |  |  |
| 2018-06-01 | 0.7 |  |  |  |  |  |
| 2018-07-01 | -0.7 |  |  |  |  |  |
| 2018-08-01 | 0.3 |  |  |  |  |  |
| 2018-09-01 | -3.1 |  |  |  |  |  |
| 2018-10-01 | 4.5 |  |  |  |  |  |
| 2018-11-01 | 1.5 |  |  |  |  |  |
| 2018-12-01 | 0.1 |  |  |  |  |  |
| 2019-01-01 | 1.7 |  |  |  |  |  |
| 2019-02-01 | 1.7 |  |  |  |  |  |
| 2019-03-01 | 0.1 |  |  |  |  |  |
| 2019-04-01 | 2 |  |  |  |  |  |
| 2019-05-01 | 3.1 |  |  |  |  |  |
| 2019-06-01 | 0.4 |  |  |  |  |  |
| 2019-07-01 | 4.8 |  |  |  |  |  |
| 2019-08-01 | 3.3 |  |  |  |  |  |
| 2019-09-01 | 3.6 |  |  |  |  |  |
| 2019-10-01 | 2.6 |  |  |  |  |  |
| 2019-11-01 | 3 |  |  |  |  |  |
| 2019-12-01 | 2 |  |  |  |  |  |
| 2020-01-01 | 0.9 |  |  |  |  |  |
| 2020-02-01 | 5.6 |  |  |  |  |  |
| 2020-03-01 | -13.5 |  |  |  |  |  |
| 2020-04-01 | -29.8 |  |  |  |  |  |
| 2020-05-01 | -19 |  |  |  |  |  |
| 2020-06-01 | -3 |  |  |  |  |  |
| 2020-07-01 | -3.5 |  |  |  |  |  |
| 2020-08-01 | -4.5 |  |  |  |  |  |
| 2020-09-01 | -1.9 |  |  |  |  |  |
| 2020-10-01 | -2 |  |  |  |  |  |
| 2020-11-01 | -5.5 |  |  |  |  |  |
| 2020-12-01 | -0.2 |  |  |  |  |  |
| 2021-01-01 | -9.9 |  |  |  |  |  |
| 2021-02-01 | -9.8 |  |  |  |  |  |
| 2021-03-01 | 16.4 |  |  |  |  |  |
| 2021-04-01 | 36 |  |  |  |  |  |
| 2021-05-01 | 18.1 |  |  |  |  |  |
| 2021-06-01 | 2.2 |  |  |  |  |  |
| 2021-07-01 | 0.6 |  |  |  |  |  |
| 2021-08-01 | 1 |  |  |  |  |  |
| 2021-09-01 | 1.6 |  |  |  |  |  |
| 2021-10-01 | -0.2 |  |  |  |  |  |
| 2021-11-01 | 7.7 |  |  |  |  |  |
| 2021-12-01 | 0 |  |  |  |  |  |
| 2022-01-01 | 6 |  |  |  |  |  |
| 2022-02-01 | 5.5 |  |  |  |  |  |
| 2022-03-01 | -0.7 |  |  |  |  |  |
| 2022-04-01 | 5.4 |  |  |  |  |  |
| 2022-05-01 | 4.7 |  |  |  |  |  |
| 2022-06-01 | 2.1 |  |  |  |  |  |
| 2022-07-01 | -0.3 |  |  |  |  |  |
| 2022-08-01 | 4 |  |  |  |  |  |
| 2022-09-01 | 1.8 |  |  |  |  |  |
| 2022-10-01 | 0 |  |  |  |  |  |
| 2022-11-01 | -2.2 |  |  |  |  |  |
| 2022-12-01 | 0.8 |  |  |  |  |  |
| 2023-01-01 | 2.9 |  |  |  |  |  |
| 2023-02-01 | 0.4 |  |  |  |  |  |
| 2023-03-01 | 4.3 |  |  |  |  |  |
| 2023-04-01 | 1.6 |  |  |  |  |  |
| 2023-05-01 | 3.4 |  |  |  |  |  |
| 2023-06-01 | 3.5 |  |  |  |  |  |
| 2023-07-01 | 3.1 |  |  |  |  |  |
| 2023-08-01 | 1.1 |  |  |  |  |  |
| 2023-09-01 | 1.6 |  |  |  |  |  |
| 2023-10-01 | 1.8 |  |  |  |  |  |
| 2023-11-01 | 3.7 |  |  |  |  |  |
| 2023-12-01 | 1.1 |  |  |  |  |  |
| 2024-01-01 | 2.3 |  |  |  |  |  |
| 2024-02-01 | 4.9 |  |  |  |  |  |
| 2024-03-01 | -1.4 |  |  |  |  |  |
| 2024-04-01 | 2.7 |  |  |  |  |  |
| 2024-05-01 | 0.4 |  |  |  |  |  |
| 2024-06-01 | -1.4 |  |  |  |  |  |
| 2024-07-01 | 2.9 |  |  |  |  |  |
| 2024-08-01 | 3.1 |  |  |  |  |  |
| 2024-09-01 | 1.8 |  |  |  |  |  |
| 2024-10-01 | 5.4 |  |  |  |  |  |
| 2024-11-01 | 1.8 |  |  |  |  |  |
| 2024-12-01 | 3.7 |  |  |  |  |  |
| 2025-01-01 | 2.2 |  |  |  |  |  |
| 2025-02-01 | 0.8 |  |  |  |  |  |
| 2025-03-01 | 3.8 |  |  |  |  |  |
| 2025-04-01 | 3.7 |  |  |  |  |  |
| 2025-05-01 | 5 |  |  |  |  |  |
| 2025-06-01 | 6.3 |  |  |  |  |  |
| 2025-07-01 | 4.3 |  |  |  |  |  |
| 2025-08-01 | 3.1 |  |  |  |  |  |
| 2025-09-01 | 6.1 |  |  |  |  |  |
| 2025-10-01 | 4.5 |  |  |  |  |  |
| 2025-11-01 | 3.9 |  |  |  |  |  |
| 2025-12-01 | 4.6 |  |  |  |  |  |
| 2026-01-01 | 3.7 |  |  |  |  |  |
| 2026-02-01 | 2.1 |  |  |  |  |  |
| 2026-03-01 | 3.8 |  |  |  |  |  |
| 2026-04-01 | 0.2 |  |  |  |  |  |
| 2026-05-01 | -0.4 | https://www.ine.es/dyngs/Prensa/en/ICM0526.htm?print=1 |  |  |  |  |

### 德國零售

- Block: `零售`
- Series ID: `de_retail`
- Original ticker/label: `德 零售`
- Frequency: `monthly`
- Observations: `137`

| Date | Value | Source URL | Source Frequency | Release Type | Status | Note |
|---|---:|---|---|---|---|---|
| 2015-01-01 | 2.1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2015-02-01 | -0.1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2015-03-01 | -0.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2015-04-01 | 0.1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2015-05-01 | 2.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2015-06-01 | -0.8 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2015-07-01 | 1.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2015-08-01 | 0.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2015-09-01 | -0.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2015-10-01 | 0.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2015-11-01 | 0.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2015-12-01 | 1.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2016-01-01 | 0 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2016-02-01 | -0.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2016-03-01 | -1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2016-04-01 | -0.7 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2016-05-01 | 1.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2016-06-01 | -0.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2016-07-01 | 1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2016-08-01 | 0.6 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2016-09-01 | -0.9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2016-10-01 | 2.9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2016-11-01 | -2.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2016-12-01 | 1.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2017-01-01 | -0.7 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2017-02-01 | 0.8 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2017-03-01 | 1.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2017-04-01 | -0.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2017-05-01 | 0.6 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2017-06-01 | 0.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2017-07-01 | -0.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2017-08-01 | -0.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2017-09-01 | 1.6 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2017-10-01 | -2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2017-11-01 | 1.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2017-12-01 | 0.7 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2018-01-01 | -0.9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2018-02-01 | -0.6 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2018-03-01 | -0.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2018-04-01 | 4.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2018-05-01 | -2.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2018-06-01 | 0.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2018-07-01 | -0.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2018-08-01 | 0.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2018-09-01 | 0 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2018-10-01 | 0.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2018-11-01 | 0 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2018-12-01 | -0.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2019-01-01 | 3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2019-02-01 | 0.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2019-03-01 | -1.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2019-04-01 | 1.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2019-05-01 | -2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2019-06-01 | 2.9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2019-07-01 | -1.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2019-08-01 | 0.8 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2019-09-01 | 0.1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2019-10-01 | -1.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2019-11-01 | 0.7 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2019-12-01 | 0 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2020-01-01 | 2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2020-02-01 | 0.9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2020-03-01 | -3.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2020-04-01 | -3.7 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2020-05-01 | 11.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2020-06-01 | -1.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2020-07-01 | -0.1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2020-08-01 | 2.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2020-09-01 | -1.7 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2020-10-01 | 2.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2020-11-01 | 0.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2020-12-01 | -3.6 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2021-01-01 | -9.7 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2021-02-01 | 3.8 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2021-03-01 | 8.6 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2021-04-01 | -4.6 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2021-05-01 | 3.7 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2021-06-01 | 4.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2021-07-01 | -4.9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2021-08-01 | 2.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2021-09-01 | -2.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2021-10-01 | 2.6 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2021-11-01 | -0.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2021-12-01 | -0.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2022-01-01 | 2.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2022-02-01 | -0.6 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2022-03-01 | -1.6 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2022-04-01 | -1.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2022-05-01 | -0.9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2022-06-01 | -0.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2022-07-01 | 0.8 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2022-08-01 | -1.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2022-09-01 | 1.1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2022-10-01 | -1.8 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2022-11-01 | 0.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2022-12-01 | -1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2023-01-01 | -0.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2023-02-01 | 0.1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2023-03-01 | -1.8 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2023-04-01 | 1.6 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2023-05-01 | 1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2023-06-01 | 0.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2023-07-01 | -0.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2023-08-01 | -1.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2023-09-01 | -0.7 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2023-10-01 | 1.6 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2023-11-01 | -0.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2023-12-01 | -0.7 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2024-01-01 | 0.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2024-02-01 | 0 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2024-03-01 | 1.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2024-04-01 | 0 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2024-05-01 | 0.1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2024-06-01 | -0.9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2024-07-01 | 0.9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2024-08-01 | 1.7 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2024-09-01 | 1.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2024-10-01 | -0.8 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2024-11-01 | 0.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2024-12-01 | -1.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2025-01-01 | 1.9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2025-02-01 | 0.1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2025-03-01 | 0.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2025-04-01 | 1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2025-05-01 | -1.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2025-06-01 | 1.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2025-07-01 | -0.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2025-08-01 | -0.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2025-09-01 | -0.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2025-10-01 | 0.8 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2025-11-01 | -0.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2025-12-01 | 0.6 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2026-01-01 | 0.1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2026-02-01 | -0.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2026-03-01 | 0.1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2026-04-01 | -0.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |
| 2026-05-01 | 1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=DE&unit=PCH_PRE&s_adj=SCA&nace_r2=G47 |  |  | p |  |

### 歐元區實質零售

- Block: `零售`
- Series ID: `ea_real_retail`
- Original ticker/label: `歐 Real零售`
- Frequency: `monthly`
- Observations: `137`

| Date | Value | Source URL | Source Frequency | Release Type | Status | Note |
|---|---:|---|---|---|---|---|
| 2015-01-01 | 1.9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2015-02-01 | 2.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2015-03-01 | 1.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2015-04-01 | 1.8 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2015-05-01 | 2.9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2015-06-01 | 2.7 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2015-07-01 | 3.8 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2015-08-01 | 2.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2015-09-01 | 2.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2015-10-01 | 1.6 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2015-11-01 | 0.8 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2015-12-01 | 1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2016-01-01 | 1.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2016-02-01 | 2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2016-03-01 | 1.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2016-04-01 | 1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2016-05-01 | 0.8 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2016-06-01 | 1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2016-07-01 | 0.9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2016-08-01 | 1.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2016-09-01 | 1.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2016-10-01 | 2.7 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2016-11-01 | 2.7 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2016-12-01 | 0.8 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2017-01-01 | 1.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2017-02-01 | 1.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2017-03-01 | 3.1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2017-04-01 | 2.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2017-05-01 | 2.8 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2017-06-01 | 3.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2017-07-01 | 2.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2017-08-01 | 2.1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2017-09-01 | 3.7 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2017-10-01 | 0.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2017-11-01 | 4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2017-12-01 | 2.6 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2018-01-01 | 1.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2018-02-01 | 2.1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2018-03-01 | 1.6 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2018-04-01 | 2.1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2018-05-01 | 2.1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2018-06-01 | 1.9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2018-07-01 | 1.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2018-08-01 | 2.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2018-09-01 | 0.6 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2018-10-01 | 2.8 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2018-11-01 | 1.8 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2018-12-01 | 0.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2019-01-01 | 2.6 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2019-02-01 | 2.9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2019-03-01 | 2.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2019-04-01 | 2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2019-05-01 | 1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2019-06-01 | 3.1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2019-07-01 | 2.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2019-08-01 | 2.8 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2019-09-01 | 2.6 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2019-10-01 | 1.9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2019-11-01 | 2.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2019-12-01 | 2.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2020-01-01 | 2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2020-02-01 | 2.8 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2020-03-01 | -8.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2020-04-01 | -19.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2020-05-01 | -2.8 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2020-06-01 | 1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2020-07-01 | 0.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2020-08-01 | 4.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2020-09-01 | 2.6 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2020-10-01 | 4.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2020-11-01 | -1.8 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2020-12-01 | 1.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2021-01-01 | -5.6 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2021-02-01 | -2.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2021-03-01 | 14.1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2021-04-01 | 24 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2021-05-01 | 9.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2021-06-01 | 6.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2021-07-01 | 3.9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2021-08-01 | 1.6 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2021-09-01 | 2.9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2021-10-01 | 2.6 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2021-11-01 | 9.7 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2021-12-01 | 3.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2022-01-01 | 9.9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2022-02-01 | 6.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2022-03-01 | 3.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2022-04-01 | 5.6 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2022-05-01 | 1.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2022-06-01 | -1.6 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2022-07-01 | -0.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2022-08-01 | -0.7 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2022-09-01 | 0.6 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2022-10-01 | -2.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2022-11-01 | -1.9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2022-12-01 | -2.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2023-01-01 | -2.1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2023-02-01 | -2.9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2023-03-01 | -3.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2023-04-01 | -2.9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2023-05-01 | -2.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2023-06-01 | -1.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2023-07-01 | -1.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2023-08-01 | -2.1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2023-09-01 | -3.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2023-10-01 | -1.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2023-11-01 | -0.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2023-12-01 | -0.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2024-01-01 | -0.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2024-02-01 | 0.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2024-03-01 | 1.1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2024-04-01 | 1.1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2024-05-01 | 0.8 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2024-06-01 | -0.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2024-07-01 | 0.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2024-08-01 | 2.9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2024-09-01 | 3.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2024-10-01 | 2.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2024-11-01 | 1.9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2024-12-01 | 2.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2025-01-01 | 2.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2025-02-01 | 2.1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2025-03-01 | 2.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2025-04-01 | 3.1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2025-05-01 | 2.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2025-06-01 | 3.9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2025-07-01 | 2.7 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2025-08-01 | 1.8 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2025-09-01 | 1.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2025-10-01 | 2.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2025-11-01 | 2.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2025-12-01 | 2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2026-01-01 | 2.1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2026-02-01 | 1.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2026-03-01 | 2.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2026-04-01 | 0.9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |
| 2026-05-01 | 1.6 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&lang=EN&geo=EA21&unit=PCH_SM&s_adj=CA&nace_r2=G47 |  |  |  |  |

### 德國工業生產

- Block: `工業`
- Series ID: `de_industrial_production`
- Original ticker/label: `德 工業`
- Frequency: `monthly`
- Observations: `137`

| Date | Value | Source URL | Source Frequency | Release Type | Status | Note |
|---|---:|---|---|---|---|---|
| 2015-01-01 | -2.3178807947 |  |  |  |  |  |
| 2015-02-01 | -1.2658227848 |  |  |  |  |  |
| 2015-03-01 | 0.5644402634 |  |  |  |  |  |
| 2015-04-01 | 1.2182741117 |  |  |  |  |  |
| 2015-05-01 | 2.786377709 |  |  |  |  |  |
| 2015-06-01 | 2.1739130435 |  |  |  |  |  |
| 2015-07-01 | 1.8572825024 |  |  |  |  |  |
| 2015-08-01 | 3.3695652174 |  |  |  |  |  |
| 2015-09-01 | 1.0536398467 |  |  |  |  |  |
| 2015-10-01 | 0.7611798287 |  |  |  |  |  |
| 2015-11-01 | 0.2803738318 |  |  |  |  |  |
| 2015-12-01 | 0.7186858316 |  |  |  |  |  |
| 2016-01-01 | 2.8248587571 |  |  |  |  |  |
| 2016-02-01 | 2.8846153846 |  |  |  |  |  |
| 2016-03-01 | 1.4031805426 |  |  |  |  |  |
| 2016-04-01 | 1.1033099298 |  |  |  |  |  |
| 2016-05-01 | -0.5020080321 |  |  |  |  |  |
| 2016-06-01 | 1.3539651838 |  |  |  |  |  |
| 2016-07-01 | -0.8637236084 |  |  |  |  |  |
| 2016-08-01 | 2.4185068349 |  |  |  |  |  |
| 2016-09-01 | 2.2748815166 |  |  |  |  |  |
| 2016-10-01 | 1.7941454202 |  |  |  |  |  |
| 2016-11-01 | 2.8890959925 |  |  |  |  |  |
| 2016-12-01 | 0.4077471967 |  |  |  |  |  |
| 2017-01-01 | -0.5494505495 |  |  |  |  |  |
| 2017-02-01 | 0.9345794393 |  |  |  |  |  |
| 2017-03-01 | 1.3837638376 |  |  |  |  |  |
| 2017-04-01 | 2.876984127 |  |  |  |  |  |
| 2017-05-01 | 4.3390514632 |  |  |  |  |  |
| 2017-06-01 | 2.6717557252 |  |  |  |  |  |
| 2017-07-01 | 3.8722168441 |  |  |  |  |  |
| 2017-08-01 | 4.2094455852 |  |  |  |  |  |
| 2017-09-01 | 3.7998146432 |  |  |  |  |  |
| 2017-10-01 | 2.0408163265 |  |  |  |  |  |
| 2017-11-01 | 5.3442028986 |  |  |  |  |  |
| 2017-12-01 | 6.4974619289 |  |  |  |  |  |
| 2018-01-01 | 6.0773480663 |  |  |  |  |  |
| 2018-02-01 | 1.9547325103 |  |  |  |  |  |
| 2018-03-01 | 3.5486806187 |  |  |  |  |  |
| 2018-04-01 | 0.9643201543 |  |  |  |  |  |
| 2018-05-01 | 2.7079303675 |  |  |  |  |  |
| 2018-06-01 | 2.3234200743 |  |  |  |  |  |
| 2018-07-01 | 0.3727865797 |  |  |  |  |  |
| 2018-08-01 | -0.4926108374 |  |  |  |  |  |
| 2018-09-01 | -0.1785714286 |  |  |  |  |  |
| 2018-10-01 | 0.5454545455 |  |  |  |  |  |
| 2018-11-01 | -3.9552880482 |  |  |  |  |  |
| 2018-12-01 | -2.0972354623 |  |  |  |  |  |
| 2019-01-01 | -1.7708333333 |  |  |  |  |  |
| 2019-02-01 | 0.5045408678 |  |  |  |  |  |
| 2019-03-01 | -0.3514938489 |  |  |  |  |  |
| 2019-04-01 | -1.4326647564 |  |  |  |  |  |
| 2019-05-01 | -2.8248587571 |  |  |  |  |  |
| 2019-06-01 | -3.3605812897 |  |  |  |  |  |
| 2019-07-01 | -2.4141132776 |  |  |  |  |  |
| 2019-08-01 | -3.1683168317 |  |  |  |  |  |
| 2019-09-01 | -3.1305903399 |  |  |  |  |  |
| 2019-10-01 | -3.5262206148 |  |  |  |  |  |
| 2019-11-01 | -1.0743061773 |  |  |  |  |  |
| 2019-12-01 | -4.4790652386 |  |  |  |  |  |
| 2020-01-01 | -0.7423117709 |  |  |  |  |  |
| 2020-02-01 | -0.5020080321 |  |  |  |  |  |
| 2020-03-01 | -9.9647266314 |  |  |  |  |  |
| 2020-04-01 | -25.2906976744 |  |  |  |  |  |
| 2020-05-01 | -18.8953488372 |  |  |  |  |  |
| 2020-06-01 | -10.0563909774 |  |  |  |  |  |
| 2020-07-01 | -8.7535680304 |  |  |  |  |  |
| 2020-08-01 | -8.691206544 |  |  |  |  |  |
| 2020-09-01 | -6.1865189289 |  |  |  |  |  |
| 2020-10-01 | -2.3430178069 |  |  |  |  |  |
| 2020-11-01 | -1.5384615385 |  |  |  |  |  |
| 2020-12-01 | 1.7329255861 |  |  |  |  |  |
| 2021-01-01 | -3.952991453 |  |  |  |  |  |
| 2021-02-01 | -5.6508577195 |  |  |  |  |  |
| 2021-03-01 | 6.7580803134 |  |  |  |  |  |
| 2021-04-01 | 29.831387808 |  |  |  |  |  |
| 2021-05-01 | 17.6821983274 |  |  |  |  |  |
| 2021-06-01 | 5.329153605 |  |  |  |  |  |
| 2021-07-01 | 5.5265901981 |  |  |  |  |  |
| 2021-08-01 | 0.6718924972 |  |  |  |  |  |
| 2021-09-01 | -1.1811023622 |  |  |  |  |  |
| 2021-10-01 | -1.1516314779 |  |  |  |  |  |
| 2021-11-01 | -1.5625 |  |  |  |  |  |
| 2021-12-01 | -1.503006012 |  |  |  |  |  |
| 2022-01-01 | 0.4449388209 |  |  |  |  |  |
| 2022-02-01 | 2.5668449198 |  |  |  |  |  |
| 2022-03-01 | -4.6788990826 |  |  |  |  |  |
| 2022-04-01 | -3.4965034965 |  |  |  |  |  |
| 2022-05-01 | -1.6243654822 |  |  |  |  |  |
| 2022-06-01 | 0.3968253968 |  |  |  |  |  |
| 2022-07-01 | -1.3833992095 |  |  |  |  |  |
| 2022-08-01 | 1.8909899889 |  |  |  |  |  |
| 2022-09-01 | 3.6852589641 |  |  |  |  |  |
| 2022-10-01 | -0.6796116505 |  |  |  |  |  |
| 2022-11-01 | -0.1867413632 |  |  |  |  |  |
| 2022-12-01 | -3.8657171923 |  |  |  |  |  |
| 2023-01-01 | -2.1040974529 |  |  |  |  |  |
| 2023-02-01 | 0.3128258603 |  |  |  |  |  |
| 2023-03-01 | 2.5986525505 |  |  |  |  |  |
| 2023-04-01 | 0.5175983437 |  |  |  |  |  |
| 2023-05-01 | 0.4127966976 |  |  |  |  |  |
| 2023-06-01 | -1.8774703557 |  |  |  |  |  |
| 2023-07-01 | -2.2044088176 |  |  |  |  |  |
| 2023-08-01 | -2.1834061135 |  |  |  |  |  |
| 2023-09-01 | -3.9385206532 |  |  |  |  |  |
| 2023-10-01 | -3.9100684262 |  |  |  |  |  |
| 2023-11-01 | -4.4901777362 |  |  |  |  |  |
| 2023-12-01 | -3.5978835979 |  |  |  |  |  |
| 2024-01-01 | -5.4298642534 |  |  |  |  |  |
| 2024-02-01 | -5.5093555094 |  |  |  |  |  |
| 2024-03-01 | -4.4090056285 |  |  |  |  |  |
| 2024-04-01 | -4.1194644696 |  |  |  |  |  |
| 2024-05-01 | -7.7081192189 |  |  |  |  |  |
| 2024-06-01 | -3.8267875126 |  |  |  |  |  |
| 2024-07-01 | -5.4303278689 |  |  |  |  |  |
| 2024-08-01 | -3.4598214286 |  |  |  |  |  |
| 2024-09-01 | -4.3 |  |  |  |  |  |
| 2024-10-01 | -3.9674465921 |  |  |  |  |  |
| 2024-11-01 | -2.6444662096 |  |  |  |  |  |
| 2024-12-01 | -2.1953896817 |  |  |  |  |  |
| 2025-01-01 | -0.4784688995 |  |  |  |  |  |
| 2025-02-01 | -3.7403740374 |  |  |  |  |  |
| 2025-03-01 | 0.2944062807 |  |  |  |  |  |
| 2025-04-01 | -1.9334049409 |  |  |  |  |  |
| 2025-05-01 | 0.6681514477 |  |  |  |  |  |
| 2025-06-01 | -1.5706806283 |  |  |  |  |  |
| 2025-07-01 | 0.6500541712 |  |  |  |  |  |
| 2025-08-01 | -3.0057803468 |  |  |  |  |  |
| 2025-09-01 | -0.7314524556 |  |  |  |  |  |
| 2025-10-01 | 0.2118644068 |  |  |  |  |  |
| 2025-11-01 | -0.1006036217 |  |  |  |  |  |
| 2025-12-01 | 0.5611672278 |  |  |  |  |  |
| 2026-01-01 | -2.0432692308 |  |  |  |  |  |
| 2026-02-01 | -0.6857142857 |  |  |  |  |  |
| 2026-03-01 | -3.4246575342 |  |  |  |  |  |
| 2026-04-01 | -0.8762322015 | https://genesis.destatis.de/genesisWS/downloads/00/tables/42153-0001_00.csv |  |  |  | YoY from GENESIS X13 calendar-adjusted production levels |
| 2026-05-01 | 0 | https://genesis.destatis.de/genesisWS/downloads/00/tables/42153-0001_00.csv |  |  |  | YoY from GENESIS X13 calendar-adjusted production levels |

### 法國消費者信心

- Block: `消費者信心`
- Series ID: `fr_consumer_confidence`
- Original ticker/label: `法 信心`
- Frequency: `monthly`
- Observations: `139`

| Date | Value | Source URL | Source Frequency | Release Type | Status | Note |
|---|---:|---|---|---|---|---|
| 2015-01-01 | 90 |  |  |  |  |  |
| 2015-02-01 | 93 |  |  |  |  |  |
| 2015-03-01 | 95 |  |  |  |  |  |
| 2015-04-01 | 96 |  |  |  |  |  |
| 2015-05-01 | 94 |  |  |  |  |  |
| 2015-06-01 | 95 |  |  |  |  |  |
| 2015-07-01 | 94 |  |  |  |  |  |
| 2015-08-01 | 95 |  |  |  |  |  |
| 2015-09-01 | 99 |  |  |  |  |  |
| 2015-10-01 | 97 |  |  |  |  |  |
| 2015-11-01 | 97 |  |  |  |  |  |
| 2015-12-01 | 98 |  |  |  |  |  |
| 2016-01-01 | 99 |  |  |  |  |  |
| 2016-02-01 | 97 |  |  |  |  |  |
| 2016-03-01 | 96 |  |  |  |  |  |
| 2016-04-01 | 95 |  |  |  |  |  |
| 2016-05-01 | 99 |  |  |  |  |  |
| 2016-06-01 | 97 |  |  |  |  |  |
| 2016-07-01 | 97 |  |  |  |  |  |
| 2016-08-01 | 97 |  |  |  |  |  |
| 2016-09-01 | 98 |  |  |  |  |  |
| 2016-10-01 | 99 |  |  |  |  |  |
| 2016-11-01 | 100 |  |  |  |  |  |
| 2016-12-01 | 101 |  |  |  |  |  |
| 2017-01-01 | 102 |  |  |  |  |  |
| 2017-02-01 | 102 |  |  |  |  |  |
| 2017-03-01 | 102 |  |  |  |  |  |
| 2017-04-01 | 101 |  |  |  |  |  |
| 2017-05-01 | 103 |  |  |  |  |  |
| 2017-06-01 | 109 |  |  |  |  |  |
| 2017-07-01 | 105 |  |  |  |  |  |
| 2017-08-01 | 103 |  |  |  |  |  |
| 2017-09-01 | 102 |  |  |  |  |  |
| 2017-10-01 | 100 |  |  |  |  |  |
| 2017-11-01 | 104 |  |  |  |  |  |
| 2017-12-01 | 107 |  |  |  |  |  |
| 2018-01-01 | 105 |  |  |  |  |  |
| 2018-02-01 | 101 |  |  |  |  |  |
| 2018-03-01 | 102 |  |  |  |  |  |
| 2018-04-01 | 102 |  |  |  |  |  |
| 2018-05-01 | 100 |  |  |  |  |  |
| 2018-06-01 | 97 |  |  |  |  |  |
| 2018-07-01 | 97 |  |  |  |  |  |
| 2018-08-01 | 97 |  |  |  |  |  |
| 2018-09-01 | 94 |  |  |  |  |  |
| 2018-10-01 | 96 |  |  |  |  |  |
| 2018-11-01 | 92 |  |  |  |  |  |
| 2018-12-01 | 89 |  |  |  |  |  |
| 2019-01-01 | 94 |  |  |  |  |  |
| 2019-02-01 | 97 |  |  |  |  |  |
| 2019-03-01 | 98 |  |  |  |  |  |
| 2019-04-01 | 99 |  |  |  |  |  |
| 2019-05-01 | 100 |  |  |  |  |  |
| 2019-06-01 | 101 |  |  |  |  |  |
| 2019-07-01 | 102 |  |  |  |  |  |
| 2019-08-01 | 103 |  |  |  |  |  |
| 2019-09-01 | 104 |  |  |  |  |  |
| 2019-10-01 | 105 |  |  |  |  |  |
| 2019-11-01 | 106 |  |  |  |  |  |
| 2019-12-01 | 102 |  |  |  |  |  |
| 2020-01-01 | 104 |  |  |  |  |  |
| 2020-02-01 | 105 |  |  |  |  |  |
| 2020-03-01 | 103 |  |  |  |  |  |
| 2020-04-01 | 91 |  |  |  |  |  |
| 2020-05-01 | 89 |  |  |  |  |  |
| 2020-06-01 | 95 |  |  |  |  |  |
| 2020-07-01 | 93 |  |  |  |  |  |
| 2020-08-01 | 94 |  |  |  |  |  |
| 2020-09-01 | 95 |  |  |  |  |  |
| 2020-10-01 | 94 |  |  |  |  |  |
| 2020-11-01 | 89 |  |  |  |  |  |
| 2020-12-01 | 96 |  |  |  |  |  |
| 2021-01-01 | 93 |  |  |  |  |  |
| 2021-02-01 | 92 |  |  |  |  |  |
| 2021-03-01 | 96 |  |  |  |  |  |
| 2021-04-01 | 97 |  |  |  |  |  |
| 2021-05-01 | 99 |  |  |  |  |  |
| 2021-06-01 | 105 |  |  |  |  |  |
| 2021-07-01 | 103 |  |  |  |  |  |
| 2021-08-01 | 99 |  |  |  |  |  |
| 2021-09-01 | 103 |  |  |  |  |  |
| 2021-10-01 | 100 |  |  |  |  |  |
| 2021-11-01 | 98 |  |  |  |  |  |
| 2021-12-01 | 99 |  |  |  |  |  |
| 2022-01-01 | 98 |  |  |  |  |  |
| 2022-02-01 | 97 |  |  |  |  |  |
| 2022-03-01 | 89 |  |  |  |  |  |
| 2022-04-01 | 87 |  |  |  |  |  |
| 2022-05-01 | 85 |  |  |  |  |  |
| 2022-06-01 | 82 |  |  |  |  |  |
| 2022-07-01 | 80 |  |  |  |  |  |
| 2022-08-01 | 83 |  |  |  |  |  |
| 2022-09-01 | 80 |  |  |  |  |  |
| 2022-10-01 | 83 |  |  |  |  |  |
| 2022-11-01 | 84 |  |  |  |  |  |
| 2022-12-01 | 82 |  |  |  |  |  |
| 2023-01-01 | 82 |  |  |  |  |  |
| 2023-02-01 | 82 |  |  |  |  |  |
| 2023-03-01 | 81 |  |  |  |  |  |
| 2023-04-01 | 83 |  |  |  |  |  |
| 2023-05-01 | 84 |  |  |  |  |  |
| 2023-06-01 | 86 |  |  |  |  |  |
| 2023-07-01 | 87 |  |  |  |  |  |
| 2023-08-01 | 86 |  |  |  |  |  |
| 2023-09-01 | 85 |  |  |  |  |  |
| 2023-10-01 | 85 |  |  |  |  |  |
| 2023-11-01 | 89 |  |  |  |  |  |
| 2023-12-01 | 89 |  |  |  |  |  |
| 2024-01-01 | 91 |  |  |  |  |  |
| 2024-02-01 | 89 |  |  |  |  |  |
| 2024-03-01 | 91 |  |  |  |  |  |
| 2024-04-01 | 90 |  |  |  |  |  |
| 2024-05-01 | 91 |  |  |  |  |  |
| 2024-06-01 | 91 |  |  |  |  |  |
| 2024-07-01 | 92 |  |  |  |  |  |
| 2024-08-01 | 93 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001587668?lastNObservations=24 |  |  | A |  |
| 2024-09-01 | 96 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001587668?lastNObservations=24 |  |  | A |  |
| 2024-10-01 | 93 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001587668?lastNObservations=24 |  |  | A |  |
| 2024-11-01 | 90 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001587668?lastNObservations=24 |  |  | A |  |
| 2024-12-01 | 88 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001587668?lastNObservations=24 |  |  | A |  |
| 2025-01-01 | 91 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001587668?lastNObservations=24 |  |  | A |  |
| 2025-02-01 | 93 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001587668?lastNObservations=24 |  |  | A |  |
| 2025-03-01 | 91 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001587668?lastNObservations=24 |  |  | A |  |
| 2025-04-01 | 92 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001587668?lastNObservations=24 |  |  | A |  |
| 2025-05-01 | 89 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001587668?lastNObservations=24 |  |  | A |  |
| 2025-06-01 | 90 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001587668?lastNObservations=24 |  |  | A |  |
| 2025-07-01 | 89 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001587668?lastNObservations=24 |  |  | A |  |
| 2025-08-01 | 88 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001587668?lastNObservations=24 |  |  | A |  |
| 2025-09-01 | 88 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001587668?lastNObservations=24 |  |  | A |  |
| 2025-10-01 | 90 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001587668?lastNObservations=24 |  |  | A |  |
| 2025-11-01 | 89 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001587668?lastNObservations=24 |  |  | A |  |
| 2025-12-01 | 90 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001587668?lastNObservations=24 |  |  | A |  |
| 2026-01-01 | 89 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001587668?lastNObservations=24 |  |  | A |  |
| 2026-02-01 | 92 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001587668?lastNObservations=24 |  |  | A |  |
| 2026-03-01 | 89 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001587668?lastNObservations=24 |  |  | A |  |
| 2026-04-01 | 84 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001587668?lastNObservations=24 |  |  | A |  |
| 2026-05-01 | 82 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001587668?lastNObservations=24 |  |  | A |  |
| 2026-06-01 | 84 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001587668?lastNObservations=24 |  |  | A |  |
| 2026-07-01 | 86 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001587668?lastNObservations=24 |  |  | A |  |

### 德國 GfK 消費者信心

- Block: `消費者信心`
- Series ID: `de_gfk_consumer_confidence`
- Original ticker/label: `德 GfK Consumer Confidence`
- Frequency: `monthly`
- Observations: `139`

| Date | Value | Source URL | Source Frequency | Release Type | Status | Note |
|---|---:|---|---|---|---|---|
| 2015-01-01 | 8.8 |  |  |  |  |  |
| 2015-02-01 | 9.1 |  |  |  |  |  |
| 2015-03-01 | 9.5 |  |  |  |  |  |
| 2015-04-01 | 9.8 |  |  |  |  |  |
| 2015-05-01 | 9.9 |  |  |  |  |  |
| 2015-06-01 | 10 |  |  |  |  |  |
| 2015-07-01 | 9.9 |  |  |  |  |  |
| 2015-08-01 | 9.9 |  |  |  |  |  |
| 2015-09-01 | 9.7 |  |  |  |  |  |
| 2015-10-01 | 9.4 |  |  |  |  |  |
| 2015-11-01 | 9.2 |  |  |  |  |  |
| 2015-12-01 | 9.1 |  |  |  |  |  |
| 2016-01-01 | 9.2 |  |  |  |  |  |
| 2016-02-01 | 9.2 |  |  |  |  |  |
| 2016-03-01 | 9.3 |  |  |  |  |  |
| 2016-04-01 | 9.2 |  |  |  |  |  |
| 2016-05-01 | 9.5 |  |  |  |  |  |
| 2016-06-01 | 9.6 |  |  |  |  |  |
| 2016-07-01 | 9.9 |  |  |  |  |  |
| 2016-08-01 | 9.8 |  |  |  |  |  |
| 2016-09-01 | 10 |  |  |  |  |  |
| 2016-10-01 | 9.8 |  |  |  |  |  |
| 2016-11-01 | 9.5 |  |  |  |  |  |
| 2016-12-01 | 9.6 |  |  |  |  |  |
| 2017-01-01 | 9.7 |  |  |  |  |  |
| 2017-02-01 | 10 |  |  |  |  |  |
| 2017-03-01 | 9.8 |  |  |  |  |  |
| 2017-04-01 | 9.6 |  |  |  |  |  |
| 2017-05-01 | 10 |  |  |  |  |  |
| 2017-06-01 | 10.2 |  |  |  |  |  |
| 2017-07-01 | 10.4 |  |  |  |  |  |
| 2017-08-01 | 10.6 |  |  |  |  |  |
| 2017-09-01 | 10.7 |  |  |  |  |  |
| 2017-10-01 | 10.6 |  |  |  |  |  |
| 2017-11-01 | 10.5 |  |  |  |  |  |
| 2017-12-01 | 10.5 |  |  |  |  |  |
| 2018-01-01 | 10.6 |  |  |  |  |  |
| 2018-02-01 | 10.8 |  |  |  |  |  |
| 2018-03-01 | 10.6 |  |  |  |  |  |
| 2018-04-01 | 10.7 |  |  |  |  |  |
| 2018-05-01 | 10.6 |  |  |  |  |  |
| 2018-06-01 | 10.5 |  |  |  |  |  |
| 2018-07-01 | 10.5 |  |  |  |  |  |
| 2018-08-01 | 10.4 |  |  |  |  |  |
| 2018-09-01 | 10.3 |  |  |  |  |  |
| 2018-10-01 | 10.4 |  |  |  |  |  |
| 2018-11-01 | 10.4 |  |  |  |  |  |
| 2018-12-01 | 10.2 |  |  |  |  |  |
| 2019-01-01 | 10.3 |  |  |  |  |  |
| 2019-02-01 | 10.6 |  |  |  |  |  |
| 2019-03-01 | 10.5 |  |  |  |  |  |
| 2019-04-01 | 10.2 |  |  |  |  |  |
| 2019-05-01 | 10.2 |  |  |  |  |  |
| 2019-06-01 | 10.1 |  |  |  |  |  |
| 2019-07-01 | 9.8 |  |  |  |  |  |
| 2019-08-01 | 9.7 |  |  |  |  |  |
| 2019-09-01 | 9.7 |  |  |  |  |  |
| 2019-10-01 | 9.8 |  |  |  |  |  |
| 2019-11-01 | 9.6 |  |  |  |  |  |
| 2019-12-01 | 9.7 |  |  |  |  |  |
| 2020-01-01 | 9.7 |  |  |  |  |  |
| 2020-02-01 | 9.1 |  |  |  |  |  |
| 2020-03-01 | 8.1 |  |  |  |  |  |
| 2020-04-01 | 2.3 |  |  |  |  |  |
| 2020-05-01 | -23.1 |  |  |  |  |  |
| 2020-06-01 | -18.6 |  |  |  |  |  |
| 2020-07-01 | -9.4 |  |  |  |  |  |
| 2020-08-01 | -0.2 |  |  |  |  |  |
| 2020-09-01 | -1.8 |  |  |  |  |  |
| 2020-10-01 | -1.7 |  |  |  |  |  |
| 2020-11-01 | -3.2 |  |  |  |  |  |
| 2020-12-01 | -6.8 |  |  |  |  |  |
| 2021-01-01 | -7.5 |  |  |  |  |  |
| 2021-02-01 | -15.5 |  |  |  |  |  |
| 2021-03-01 | -12.7 |  |  |  |  |  |
| 2021-04-01 | -6.1 |  |  |  |  |  |
| 2021-05-01 | -8.6 |  |  |  |  |  |
| 2021-06-01 | -6.9 |  |  |  |  |  |
| 2021-07-01 | -0.3 |  |  |  |  |  |
| 2021-08-01 | -0.4 |  |  |  |  |  |
| 2021-09-01 | -1.1 |  |  |  |  |  |
| 2021-10-01 | 0.4 |  |  |  |  |  |
| 2021-11-01 | 1 |  |  |  |  |  |
| 2021-12-01 | -1.8 |  |  |  |  |  |
| 2022-01-01 | -6.9 |  |  |  |  |  |
| 2022-02-01 | -6.7 |  |  |  |  |  |
| 2022-03-01 | -8.5 |  |  |  |  |  |
| 2022-04-01 | -15.7 |  |  |  |  |  |
| 2022-05-01 | -26.6 |  |  |  |  |  |
| 2022-06-01 | -26.2 |  |  |  |  |  |
| 2022-07-01 | -27.7 |  |  |  |  |  |
| 2022-08-01 | -30.9 |  |  |  |  |  |
| 2022-09-01 | -36.8 |  |  |  |  |  |
| 2022-10-01 | -42.8 |  |  |  |  |  |
| 2022-11-01 | -41.9 |  |  |  |  |  |
| 2022-12-01 | -40.1 |  |  |  |  |  |
| 2023-01-01 | -37.6 |  |  |  |  |  |
| 2023-02-01 | -33.8 |  |  |  |  |  |
| 2023-03-01 | -30.6 |  |  |  |  |  |
| 2023-04-01 | -29.3 |  |  |  |  |  |
| 2023-05-01 | -25.8 |  |  |  |  |  |
| 2023-06-01 | -24.4 |  |  |  |  |  |
| 2023-07-01 | -25.2 |  |  |  |  |  |
| 2023-08-01 | -24.6 |  |  |  |  |  |
| 2023-09-01 | -25.6 |  |  |  |  |  |
| 2023-10-01 | -26.7 |  |  |  |  |  |
| 2023-11-01 | -28.3 |  |  |  |  |  |
| 2023-12-01 | -27.6 |  |  |  |  |  |
| 2024-01-01 | -25.4 |  |  |  |  |  |
| 2024-02-01 | -29.6 |  |  |  |  |  |
| 2024-03-01 | -28.8 |  |  |  |  |  |
| 2024-04-01 | -27.3 |  |  |  |  |  |
| 2024-05-01 | -24 |  |  |  |  |  |
| 2024-06-01 | -21 |  |  |  |  |  |
| 2024-07-01 | -21.6 |  |  |  |  |  |
| 2024-08-01 | -18.6 |  |  |  |  |  |
| 2024-09-01 | -21.9 |  |  |  |  |  |
| 2024-10-01 | -21 |  |  |  |  |  |
| 2024-11-01 | -18.4 |  |  |  |  |  |
| 2024-12-01 | -23.1 |  |  |  |  |  |
| 2025-01-01 | -21.4 |  |  |  |  |  |
| 2025-02-01 | -22.6 |  |  |  |  |  |
| 2025-03-01 | -24.6 |  |  |  |  |  |
| 2025-04-01 | -24.3 |  |  |  |  |  |
| 2025-05-01 | -20.8 |  |  |  |  |  |
| 2025-06-01 | -20 |  |  |  |  |  |
| 2025-07-01 | -20.3 |  |  |  |  |  |
| 2025-08-01 | -21.7 |  |  |  |  |  |
| 2025-09-01 | -23.5 |  |  |  |  |  |
| 2025-10-01 | -22.5 |  |  |  |  |  |
| 2025-11-01 | -24.1 |  |  |  |  |  |
| 2025-12-01 | -23.4 |  |  |  |  |  |
| 2026-01-01 | -26.9 |  |  |  |  |  |
| 2026-02-01 | -24.2 |  |  |  |  |  |
| 2026-03-01 | -24.8 |  |  |  |  |  |
| 2026-04-01 | -28.1 |  |  |  |  |  |
| 2026-05-01 | -33.1 |  |  |  |  |  |
| 2026-07-01 | -29.3 | https://www.nim.org/en/consumer-climate/detail-consumer-climate/konsumklima-verharrt-auf-niedrigem-niveau |  |  |  | previous month revised |
| 2026-08-01 | -29.6 | https://www.nim.org/en/consumer-climate/detail-consumer-climate/konsumklima-verharrt-auf-niedrigem-niveau |  |  |  | forecast month |

### 德國 ZEW 現況指數

- Block: `消費者信心`
- Series ID: `de_zew_current`
- Original ticker/label: `德信心 Current`
- Frequency: `monthly`
- Observations: `138`

| Date | Value | Source URL | Source Frequency | Release Type | Status | Note |
|---|---:|---|---|---|---|---|
| 2015-01-01 | 22.4 |  |  |  |  |  |
| 2015-02-01 | 45.5 |  |  |  |  |  |
| 2015-03-01 | 55.1 |  |  |  |  |  |
| 2015-04-01 | 70.2 |  |  |  |  |  |
| 2015-05-01 | 65.7 |  |  |  |  |  |
| 2015-06-01 | 62.9 |  |  |  |  |  |
| 2015-07-01 | 63.9 |  |  |  |  |  |
| 2015-08-01 | 65.7 |  |  |  |  |  |
| 2015-09-01 | 67.5 |  |  |  |  |  |
| 2015-10-01 | 55.2 |  |  |  |  |  |
| 2015-11-01 | 54.4 |  |  |  |  |  |
| 2015-12-01 | 55 |  |  |  |  |  |
| 2016-01-01 | 59.7 |  |  |  |  |  |
| 2016-02-01 | 52.3 |  |  |  |  |  |
| 2016-03-01 | 50.7 |  |  |  |  |  |
| 2016-04-01 | 47.7 |  |  |  |  |  |
| 2016-05-01 | 53.1 |  |  |  |  |  |
| 2016-06-01 | 54.5 |  |  |  |  |  |
| 2016-07-01 | 49.8 |  |  |  |  |  |
| 2016-08-01 | 57.6 |  |  |  |  |  |
| 2016-09-01 | 55.1 |  |  |  |  |  |
| 2016-10-01 | 59.5 |  |  |  |  |  |
| 2016-11-01 | 58.8 |  |  |  |  |  |
| 2016-12-01 | 63.5 |  |  |  |  |  |
| 2017-01-01 | 77.3 |  |  |  |  |  |
| 2017-02-01 | 76.4 |  |  |  |  |  |
| 2017-03-01 | 77.3 |  |  |  |  |  |
| 2017-04-01 | 80.1 |  |  |  |  |  |
| 2017-05-01 | 83.9 |  |  |  |  |  |
| 2017-06-01 | 88 |  |  |  |  |  |
| 2017-07-01 | 86.4 |  |  |  |  |  |
| 2017-08-01 | 86.7 |  |  |  |  |  |
| 2017-09-01 | 87.9 |  |  |  |  |  |
| 2017-10-01 | 87 |  |  |  |  |  |
| 2017-11-01 | 88.8 |  |  |  |  |  |
| 2017-12-01 | 89.3 |  |  |  |  |  |
| 2018-01-01 | 95.2 |  |  |  |  |  |
| 2018-02-01 | 92.3 |  |  |  |  |  |
| 2018-03-01 | 90.7 |  |  |  |  |  |
| 2018-04-01 | 87.9 |  |  |  |  |  |
| 2018-05-01 | 87.4 |  |  |  |  |  |
| 2018-06-01 | 80.6 |  |  |  |  |  |
| 2018-07-01 | 72.4 |  |  |  |  |  |
| 2018-08-01 | 72.6 |  |  |  |  |  |
| 2018-09-01 | 76 |  |  |  |  |  |
| 2018-10-01 | 70.1 |  |  |  |  |  |
| 2018-11-01 | 58.2 |  |  |  |  |  |
| 2018-12-01 | 45.3 |  |  |  |  |  |
| 2019-01-01 | 27.6 |  |  |  |  |  |
| 2019-02-01 | 15 |  |  |  |  |  |
| 2019-03-01 | 11.1 |  |  |  |  |  |
| 2019-04-01 | 5.5 |  |  |  |  |  |
| 2019-05-01 | 8.2 |  |  |  |  |  |
| 2019-06-01 | 7.8 |  |  |  |  |  |
| 2019-07-01 | -1.1 |  |  |  |  |  |
| 2019-08-01 | -13.5 |  |  |  |  |  |
| 2019-09-01 | -19.9 |  |  |  |  |  |
| 2019-10-01 | -25.3 |  |  |  |  |  |
| 2019-11-01 | -24.7 |  |  |  |  |  |
| 2019-12-01 | -19.9 |  |  |  |  |  |
| 2020-01-01 | -9.5 |  |  |  |  |  |
| 2020-02-01 | -15.7 |  |  |  |  |  |
| 2020-03-01 | -43.1 |  |  |  |  |  |
| 2020-04-01 | -91.5 |  |  |  |  |  |
| 2020-05-01 | -93.5 |  |  |  |  |  |
| 2020-06-01 | -83.1 |  |  |  |  |  |
| 2020-07-01 | -80.9 |  |  |  |  |  |
| 2020-08-01 | -81.3 |  |  |  |  |  |
| 2020-09-01 | -66.2 |  |  |  |  |  |
| 2020-10-01 | -59.5 |  |  |  |  |  |
| 2020-11-01 | -64.3 |  |  |  |  |  |
| 2020-12-01 | -66.5 |  |  |  |  |  |
| 2021-01-01 | -66.4 |  |  |  |  |  |
| 2021-02-01 | -67.2 |  |  |  |  |  |
| 2021-03-01 | -61 |  |  |  |  |  |
| 2021-04-01 | -48.8 |  |  |  |  |  |
| 2021-05-01 | -40.1 |  |  |  |  |  |
| 2021-06-01 | -9.1 |  |  |  |  |  |
| 2021-07-01 | 21.9 |  |  |  |  |  |
| 2021-08-01 | 29.3 |  |  |  |  |  |
| 2021-09-01 | 31.9 |  |  |  |  |  |
| 2021-10-01 | 21.6 |  |  |  |  |  |
| 2021-11-01 | 12.5 |  |  |  |  |  |
| 2021-12-01 | -7.4 |  |  |  |  |  |
| 2022-01-01 | -10.2 |  |  |  |  |  |
| 2022-02-01 | -8.1 |  |  |  |  |  |
| 2022-03-01 | -21.4 |  |  |  |  |  |
| 2022-04-01 | -30.8 |  |  |  |  |  |
| 2022-05-01 | -36.5 |  |  |  |  |  |
| 2022-06-01 | -27.6 |  |  |  |  |  |
| 2022-07-01 | -45.8 |  |  |  |  |  |
| 2022-08-01 | -47.6 |  |  |  |  |  |
| 2022-09-01 | -60.5 |  |  |  |  |  |
| 2022-10-01 | -72.2 |  |  |  |  |  |
| 2022-11-01 | -64.5 |  |  |  |  |  |
| 2022-12-01 | -61.4 |  |  |  |  |  |
| 2023-01-01 | -58.6 |  |  |  |  |  |
| 2023-02-01 | -45.1 |  |  |  |  |  |
| 2023-03-01 | -46.5 |  |  |  |  |  |
| 2023-04-01 | -32.5 |  |  |  |  |  |
| 2023-05-01 | -34.8 |  |  |  |  |  |
| 2023-06-01 | -56.5 |  |  |  |  |  |
| 2023-07-01 | -59.5 |  |  |  |  |  |
| 2023-08-01 | -71.3 |  |  |  |  |  |
| 2023-09-01 | -79.4 |  |  |  |  |  |
| 2023-10-01 | -79.9 |  |  |  |  |  |
| 2023-11-01 | -79.8 |  |  |  |  |  |
| 2023-12-01 | -77.1 |  |  |  |  |  |
| 2024-01-01 | -77.3 |  |  |  |  |  |
| 2024-02-01 | -81.7 |  |  |  |  |  |
| 2024-03-01 | -80.5 |  |  |  |  |  |
| 2024-04-01 | -79.2 |  |  |  |  |  |
| 2024-05-01 | -72.3 |  |  |  |  |  |
| 2024-06-01 | -73.8 |  |  |  |  |  |
| 2024-07-01 | -68.9 |  |  |  |  |  |
| 2024-08-01 | -77.3 |  |  |  |  |  |
| 2024-09-01 | -84.5 |  |  |  |  |  |
| 2024-10-01 | -86.9 |  |  |  |  |  |
| 2024-11-01 | -91.4 |  |  |  |  |  |
| 2024-12-01 | -93.1 |  |  |  |  |  |
| 2025-01-01 | -90.4 |  |  |  |  |  |
| 2025-02-01 | -88.5 |  |  |  |  |  |
| 2025-03-01 | -87.6 |  |  |  |  |  |
| 2025-04-01 | -81.2 |  |  |  |  |  |
| 2025-05-01 | -82 |  |  |  |  |  |
| 2025-06-01 | -72 |  |  |  |  |  |
| 2025-07-01 | -59.5 |  |  |  |  |  |
| 2025-08-01 | -68.6 |  |  |  |  |  |
| 2025-09-01 | -76.4 |  |  |  |  |  |
| 2025-10-01 | -80 |  |  |  |  |  |
| 2025-11-01 | -78.7 |  |  |  |  |  |
| 2025-12-01 | -81 |  |  |  |  |  |
| 2026-01-01 | -72.7 |  |  |  |  |  |
| 2026-02-01 | -65.9 |  |  |  |  |  |
| 2026-03-01 | -62.9 |  |  |  |  |  |
| 2026-04-01 | -73.7 |  |  |  |  |  |
| 2026-05-01 | -77.8 |  |  |  |  |  |
| 2026-07-01 | -77.6 | https://www.zew.de/en/press/latest-press-releases/strong-rise-in-expectations-1 |  |  |  |  |

### 德國 ZEW 預期指數

- Block: `消費者信心`
- Series ID: `de_zew_expectations`
- Original ticker/label: `德信心 expect`
- Frequency: `monthly`
- Observations: `138`

| Date | Value | Source URL | Source Frequency | Release Type | Status | Note |
|---|---:|---|---|---|---|---|
| 2015-01-01 | 48.4 |  |  |  |  |  |
| 2015-02-01 | 53 |  |  |  |  |  |
| 2015-03-01 | 54.8 |  |  |  |  |  |
| 2015-04-01 | 53.3 |  |  |  |  |  |
| 2015-05-01 | 41.9 |  |  |  |  |  |
| 2015-06-01 | 31.5 |  |  |  |  |  |
| 2015-07-01 | 29.7 |  |  |  |  |  |
| 2015-08-01 | 25 |  |  |  |  |  |
| 2015-09-01 | 12.1 |  |  |  |  |  |
| 2015-10-01 | 1.9 |  |  |  |  |  |
| 2015-11-01 | 10.4 |  |  |  |  |  |
| 2015-12-01 | 16.1 |  |  |  |  |  |
| 2016-01-01 | 10.2 |  |  |  |  |  |
| 2016-02-01 | 1 |  |  |  |  |  |
| 2016-03-01 | 4.3 |  |  |  |  |  |
| 2016-04-01 | 11.2 |  |  |  |  |  |
| 2016-05-01 | 6.4 |  |  |  |  |  |
| 2016-06-01 | 19.2 |  |  |  |  |  |
| 2016-07-01 | -6.8 |  |  |  |  |  |
| 2016-08-01 | 0.5 |  |  |  |  |  |
| 2016-09-01 | 0.5 |  |  |  |  |  |
| 2016-10-01 | 6.2 |  |  |  |  |  |
| 2016-11-01 | 13.8 |  |  |  |  |  |
| 2016-12-01 | 13.8 |  |  |  |  |  |
| 2017-01-01 | 16.6 |  |  |  |  |  |
| 2017-02-01 | 10.4 |  |  |  |  |  |
| 2017-03-01 | 12.8 |  |  |  |  |  |
| 2017-04-01 | 19.5 |  |  |  |  |  |
| 2017-05-01 | 20.6 |  |  |  |  |  |
| 2017-06-01 | 18.6 |  |  |  |  |  |
| 2017-07-01 | 17.5 |  |  |  |  |  |
| 2017-08-01 | 10 |  |  |  |  |  |
| 2017-09-01 | 17 |  |  |  |  |  |
| 2017-10-01 | 17.6 |  |  |  |  |  |
| 2017-11-01 | 18.7 |  |  |  |  |  |
| 2017-12-01 | 17.4 |  |  |  |  |  |
| 2018-01-01 | 20.4 |  |  |  |  |  |
| 2018-02-01 | 17.8 |  |  |  |  |  |
| 2018-03-01 | 5.1 |  |  |  |  |  |
| 2018-04-01 | -8.2 |  |  |  |  |  |
| 2018-05-01 | -8.2 |  |  |  |  |  |
| 2018-06-01 | -16.1 |  |  |  |  |  |
| 2018-07-01 | -24.7 |  |  |  |  |  |
| 2018-08-01 | -13.7 |  |  |  |  |  |
| 2018-09-01 | -10.6 |  |  |  |  |  |
| 2018-10-01 | -24.7 |  |  |  |  |  |
| 2018-11-01 | -24.1 |  |  |  |  |  |
| 2018-12-01 | -17.5 |  |  |  |  |  |
| 2019-01-01 | -15 |  |  |  |  |  |
| 2019-02-01 | -13.4 |  |  |  |  |  |
| 2019-03-01 | -3.6 |  |  |  |  |  |
| 2019-04-01 | 3.1 |  |  |  |  |  |
| 2019-05-01 | -2.1 |  |  |  |  |  |
| 2019-06-01 | -21.1 |  |  |  |  |  |
| 2019-07-01 | -24.5 |  |  |  |  |  |
| 2019-08-01 | -44.1 |  |  |  |  |  |
| 2019-09-01 | -22.5 |  |  |  |  |  |
| 2019-10-01 | -22.8 |  |  |  |  |  |
| 2019-11-01 | -2.1 |  |  |  |  |  |
| 2019-12-01 | 10.7 |  |  |  |  |  |
| 2020-01-01 | 26.7 |  |  |  |  |  |
| 2020-02-01 | 8.7 |  |  |  |  |  |
| 2020-03-01 | -49.5 |  |  |  |  |  |
| 2020-04-01 | 28.2 |  |  |  |  |  |
| 2020-05-01 | 51 |  |  |  |  |  |
| 2020-06-01 | 63.4 |  |  |  |  |  |
| 2020-07-01 | 59.3 |  |  |  |  |  |
| 2020-08-01 | 71.5 |  |  |  |  |  |
| 2020-09-01 | 77.4 |  |  |  |  |  |
| 2020-10-01 | 56.1 |  |  |  |  |  |
| 2020-11-01 | 39 |  |  |  |  |  |
| 2020-12-01 | 55 |  |  |  |  |  |
| 2021-01-01 | 61.8 |  |  |  |  |  |
| 2021-02-01 | 71.2 |  |  |  |  |  |
| 2021-03-01 | 76.6 |  |  |  |  |  |
| 2021-04-01 | 70.7 |  |  |  |  |  |
| 2021-05-01 | 84.4 |  |  |  |  |  |
| 2021-06-01 | 79.8 |  |  |  |  |  |
| 2021-07-01 | 63.3 |  |  |  |  |  |
| 2021-08-01 | 40.4 |  |  |  |  |  |
| 2021-09-01 | 26.5 |  |  |  |  |  |
| 2021-10-01 | 22.3 |  |  |  |  |  |
| 2021-11-01 | 31.7 |  |  |  |  |  |
| 2021-12-01 | 29.9 |  |  |  |  |  |
| 2022-01-01 | 51.7 |  |  |  |  |  |
| 2022-02-01 | 54.3 |  |  |  |  |  |
| 2022-03-01 | -39.3 |  |  |  |  |  |
| 2022-04-01 | -41 |  |  |  |  |  |
| 2022-05-01 | -34.3 |  |  |  |  |  |
| 2022-06-01 | -28 |  |  |  |  |  |
| 2022-07-01 | -53.8 |  |  |  |  |  |
| 2022-08-01 | -55.3 |  |  |  |  |  |
| 2022-09-01 | -61.9 |  |  |  |  |  |
| 2022-10-01 | -59.2 |  |  |  |  |  |
| 2022-11-01 | -36.7 |  |  |  |  |  |
| 2022-12-01 | -23.3 |  |  |  |  |  |
| 2023-01-01 | 16.9 |  |  |  |  |  |
| 2023-02-01 | 28.1 |  |  |  |  |  |
| 2023-03-01 | 13 |  |  |  |  |  |
| 2023-04-01 | 4.1 |  |  |  |  |  |
| 2023-05-01 | -10.7 |  |  |  |  |  |
| 2023-06-01 | -8.5 |  |  |  |  |  |
| 2023-07-01 | -14.7 |  |  |  |  |  |
| 2023-08-01 | -12.3 |  |  |  |  |  |
| 2023-09-01 | -11.4 |  |  |  |  |  |
| 2023-10-01 | -1.1 |  |  |  |  |  |
| 2023-11-01 | 9.8 |  |  |  |  |  |
| 2023-12-01 | 12.8 |  |  |  |  |  |
| 2024-01-01 | 15.2 |  |  |  |  |  |
| 2024-02-01 | 19.9 |  |  |  |  |  |
| 2024-03-01 | 31.7 |  |  |  |  |  |
| 2024-04-01 | 42.9 |  |  |  |  |  |
| 2024-05-01 | 47.1 |  |  |  |  |  |
| 2024-06-01 | 47.5 |  |  |  |  |  |
| 2024-07-01 | 41.8 |  |  |  |  |  |
| 2024-08-01 | 19.2 |  |  |  |  |  |
| 2024-09-01 | 3.6 |  |  |  |  |  |
| 2024-10-01 | 13.1 |  |  |  |  |  |
| 2024-11-01 | 7.4 |  |  |  |  |  |
| 2024-12-01 | 15.7 |  |  |  |  |  |
| 2025-01-01 | 10.3 |  |  |  |  |  |
| 2025-02-01 | 26 |  |  |  |  |  |
| 2025-03-01 | 51.6 |  |  |  |  |  |
| 2025-04-01 | -14 |  |  |  |  |  |
| 2025-05-01 | 25.2 |  |  |  |  |  |
| 2025-06-01 | 47.5 |  |  |  |  |  |
| 2025-07-01 | 52.7 |  |  |  |  |  |
| 2025-08-01 | 34.7 |  |  |  |  |  |
| 2025-09-01 | 37.3 |  |  |  |  |  |
| 2025-10-01 | 39.3 |  |  |  |  |  |
| 2025-11-01 | 38.5 |  |  |  |  |  |
| 2025-12-01 | 45.8 |  |  |  |  |  |
| 2026-01-01 | 59.6 |  |  |  |  |  |
| 2026-02-01 | 58.3 |  |  |  |  |  |
| 2026-03-01 | -0.5 |  |  |  |  |  |
| 2026-04-01 | -17.2 |  |  |  |  |  |
| 2026-05-01 | -10.2 |  |  |  |  |  |
| 2026-07-01 | 26.3 | https://www.zew.de/en/press/latest-press-releases/strong-rise-in-expectations-1 |  |  |  |  |

### 德國製造業 PMI

- Block: `製造業`
- Series ID: `de_manufacturing_pmi`
- Original ticker/label: `德 製造業PMI`
- Frequency: `monthly`
- Observations: `36`

| Date | Value | Source URL | Source Frequency | Release Type | Status | Note |
|---|---:|---|---|---|---|---|
| 2023-07-01 | 38.8 |  |  |  |  |  |
| 2023-08-01 | 39.1 |  |  |  |  |  |
| 2023-09-01 | 39.6 |  |  |  |  |  |
| 2023-10-01 | 40.8 |  |  |  |  |  |
| 2023-11-01 | 42.6 |  |  |  |  |  |
| 2023-12-01 | 43.3 |  |  |  |  |  |
| 2024-01-01 | 45.5 |  |  |  |  |  |
| 2024-02-01 | 42.5 |  |  |  |  |  |
| 2024-03-01 | 41.9 |  |  |  |  |  |
| 2024-04-01 | 42.5 |  |  |  |  |  |
| 2024-05-01 | 45.4 |  |  |  |  |  |
| 2024-06-01 | 43.5 |  |  |  |  |  |
| 2024-07-01 | 43.2 |  |  |  |  |  |
| 2024-08-01 | 42.4 |  |  |  |  |  |
| 2024-09-01 | 40.6 |  |  |  |  |  |
| 2024-10-01 | 43 |  |  |  |  |  |
| 2024-11-01 | 43 |  |  |  |  |  |
| 2024-12-01 | 42.5 |  |  |  |  |  |
| 2025-01-01 | 45 |  |  |  |  |  |
| 2025-02-01 | 46.5 |  |  |  |  |  |
| 2025-03-01 | 48.3 |  |  |  |  |  |
| 2025-04-01 | 48.4 |  |  |  |  |  |
| 2025-05-01 | 48.3 |  |  |  |  |  |
| 2025-06-01 | 49 |  |  |  |  |  |
| 2025-07-01 | 49.1 |  |  |  |  |  |
| 2025-08-01 | 49.8 |  |  |  |  |  |
| 2025-09-01 | 49.5 |  |  |  |  |  |
| 2025-10-01 | 49.6 |  |  |  |  |  |
| 2025-11-01 | 48.2 |  |  |  |  |  |
| 2025-12-01 | 47 |  |  |  |  |  |
| 2026-01-01 | 49.1 |  |  |  |  |  |
| 2026-02-01 | 50.9 |  |  |  |  |  |
| 2026-03-01 | 52.2 |  |  |  |  |  |
| 2026-04-01 | 51.4 |  |  |  |  |  |
| 2026-05-01 | 50.1 |  |  |  |  |  |
| 2026-07-01 | 52.2 | https://www.pmi.spglobal.com/Public/Home/PressRelease/33afc7650b4243d49379ecc2c469b446 |  | flash | flash | matched UK-template label: Flash Germany Manufacturing PMI: 52.2 |

### 法國製造業 PMI

- Block: `製造業`
- Series ID: `fr_manufacturing_pmi`
- Original ticker/label: `法 製造業PMI`
- Frequency: `monthly`
- Observations: `36`

| Date | Value | Source URL | Source Frequency | Release Type | Status | Note |
|---|---:|---|---|---|---|---|
| 2023-07-01 | 45.1 |  |  |  |  |  |
| 2023-08-01 | 46 |  |  |  |  |  |
| 2023-09-01 | 44.2 |  |  |  |  |  |
| 2023-10-01 | 42.8 |  |  |  |  |  |
| 2023-11-01 | 42.9 |  |  |  |  |  |
| 2023-12-01 | 42.1 |  |  |  |  |  |
| 2024-01-01 | 43.1 |  |  |  |  |  |
| 2024-02-01 | 47.1 |  |  |  |  |  |
| 2024-03-01 | 46.2 |  |  |  |  |  |
| 2024-04-01 | 45.3 |  |  |  |  |  |
| 2024-05-01 | 46.4 |  |  |  |  |  |
| 2024-06-01 | 45.4 |  |  |  |  |  |
| 2024-07-01 | 44 |  |  |  |  |  |
| 2024-08-01 | 43.9 |  |  |  |  |  |
| 2024-09-01 | 44.6 |  |  |  |  |  |
| 2024-10-01 | 44.5 |  |  |  |  |  |
| 2024-11-01 | 43.1 |  |  |  |  |  |
| 2024-12-01 | 41.9 |  |  |  |  |  |
| 2025-01-01 | 45 |  |  |  |  |  |
| 2025-02-01 | 45.8 |  |  |  |  |  |
| 2025-03-01 | 48.5 |  |  |  |  |  |
| 2025-04-01 | 48.7 |  |  |  |  |  |
| 2025-05-01 | 49.8 |  |  |  |  |  |
| 2025-06-01 | 48.1 |  |  |  |  |  |
| 2025-07-01 | 48.2 |  |  |  |  |  |
| 2025-08-01 | 50.4 |  |  |  |  |  |
| 2025-09-01 | 48.2 |  |  |  |  |  |
| 2025-10-01 | 48.8 |  |  |  |  |  |
| 2025-11-01 | 47.8 |  |  |  |  |  |
| 2025-12-01 | 50.7 |  |  |  |  |  |
| 2026-01-01 | 51.2 |  |  |  |  |  |
| 2026-02-01 | 50.1 |  |  |  |  |  |
| 2026-03-01 | 50 |  |  |  |  |  |
| 2026-04-01 | 52.8 |  |  |  |  |  |
| 2026-05-01 | 49.7 |  |  |  |  |  |
| 2026-07-01 | 50 | https://tradingeconomics.com/france/manufacturing-pmi |  | flash | flash | public indicator page; underlying source explicitly S&P Global; flash |

### 法國製造業信心

- Block: `製造業`
- Series ID: `fr_manufacturing_confidence`
- Original ticker/label: `法 製造業信心`
- Frequency: `monthly`
- Observations: `139`

| Date | Value | Source URL | Source Frequency | Release Type | Status | Note |
|---|---:|---|---|---|---|---|
| 2015-01-01 | 98.7 |  |  |  |  |  |
| 2015-02-01 | 98.3 |  |  |  |  |  |
| 2015-03-01 | 98.8 |  |  |  |  |  |
| 2015-04-01 | 101.5 |  |  |  |  |  |
| 2015-05-01 | 101.7 |  |  |  |  |  |
| 2015-06-01 | 100.2 |  |  |  |  |  |
| 2015-07-01 | 101.5 |  |  |  |  |  |
| 2015-08-01 | 103.5 |  |  |  |  |  |
| 2015-09-01 | 104.8 |  |  |  |  |  |
| 2015-10-01 | 103.1 |  |  |  |  |  |
| 2015-11-01 | 102.3 |  |  |  |  |  |
| 2015-12-01 | 102.5 |  |  |  |  |  |
| 2016-01-01 | 102.7 |  |  |  |  |  |
| 2016-02-01 | 102.9 |  |  |  |  |  |
| 2016-03-01 | 102.5 |  |  |  |  |  |
| 2016-04-01 | 104.7 |  |  |  |  |  |
| 2016-05-01 | 104.3 |  |  |  |  |  |
| 2016-06-01 | 101.4 |  |  |  |  |  |
| 2016-07-01 | 101.5 |  |  |  |  |  |
| 2016-08-01 | 101.5 |  |  |  |  |  |
| 2016-09-01 | 103.5 |  |  |  |  |  |
| 2016-10-01 | 102.1 |  |  |  |  |  |
| 2016-11-01 | 102.1 |  |  |  |  |  |
| 2016-12-01 | 105.8 |  |  |  |  |  |
| 2017-01-01 | 105.8 |  |  |  |  |  |
| 2017-02-01 | 106.5 |  |  |  |  |  |
| 2017-03-01 | 105.3 |  |  |  |  |  |
| 2017-04-01 | 108.3 |  |  |  |  |  |
| 2017-05-01 | 108.3 |  |  |  |  |  |
| 2017-06-01 | 109 |  |  |  |  |  |
| 2017-07-01 | 108.5 |  |  |  |  |  |
| 2017-08-01 | 110 |  |  |  |  |  |
| 2017-09-01 | 111.6 |  |  |  |  |  |
| 2017-10-01 | 111.9 |  |  |  |  |  |
| 2017-11-01 | 112.1 |  |  |  |  |  |
| 2017-12-01 | 112.1 |  |  |  |  |  |
| 2018-01-01 | 113.7 |  |  |  |  |  |
| 2018-02-01 | 112.3 |  |  |  |  |  |
| 2018-03-01 | 110.5 |  |  |  |  |  |
| 2018-04-01 | 110.3 |  |  |  |  |  |
| 2018-05-01 | 109.6 |  |  |  |  |  |
| 2018-06-01 | 109.5 |  |  |  |  |  |
| 2018-07-01 | 108.5 |  |  |  |  |  |
| 2018-08-01 | 108.6 |  |  |  |  |  |
| 2018-09-01 | 108 |  |  |  |  |  |
| 2018-10-01 | 104.9 |  |  |  |  |  |
| 2018-11-01 | 105.6 |  |  |  |  |  |
| 2018-12-01 | 103.6 |  |  |  |  |  |
| 2019-01-01 | 103 |  |  |  |  |  |
| 2019-02-01 | 102.8 |  |  |  |  |  |
| 2019-03-01 | 103.4 |  |  |  |  |  |
| 2019-04-01 | 101.1 |  |  |  |  |  |
| 2019-05-01 | 103.4 |  |  |  |  |  |
| 2019-06-01 | 101.8 |  |  |  |  |  |
| 2019-07-01 | 101 |  |  |  |  |  |
| 2019-08-01 | 101.9 |  |  |  |  |  |
| 2019-09-01 | 102.4 |  |  |  |  |  |
| 2019-10-01 | 100.2 |  |  |  |  |  |
| 2019-11-01 | 102.5 |  |  |  |  |  |
| 2019-12-01 | 99.1 |  |  |  |  |  |
| 2020-01-01 | 101.9 |  |  |  |  |  |
| 2020-02-01 | 100.1 |  |  |  |  |  |
| 2020-03-01 | 97.4 |  |  |  |  |  |
| 2020-04-01 | 66.2 |  |  |  |  |  |
| 2020-05-01 | 69.5 |  |  |  |  |  |
| 2020-06-01 | 76.6 |  |  |  |  |  |
| 2020-07-01 | 81.2 |  |  |  |  |  |
| 2020-08-01 | 91.3 |  |  |  |  |  |
| 2020-09-01 | 95.1 |  |  |  |  |  |
| 2020-10-01 | 95 |  |  |  |  |  |
| 2020-11-01 | 92.4 |  |  |  |  |  |
| 2020-12-01 | 94.9 |  |  |  |  |  |
| 2021-01-01 | 95.8 |  |  |  |  |  |
| 2021-02-01 | 97 |  |  |  |  |  |
| 2021-03-01 | 98.5 |  |  |  |  |  |
| 2021-04-01 | 103.8 |  |  |  |  |  |
| 2021-05-01 | 107.4 |  |  |  |  |  |
| 2021-06-01 | 107.3 |  |  |  |  |  |
| 2021-07-01 | 109.2 |  |  |  |  |  |
| 2021-08-01 | 109.5 |  |  |  |  |  |
| 2021-09-01 | 107.7 |  |  |  |  |  |
| 2021-10-01 | 108 |  |  |  |  |  |
| 2021-11-01 | 110.1 |  |  |  |  |  |
| 2021-12-01 | 109.3 |  |  |  |  |  |
| 2022-01-01 | 112.3 |  |  |  |  |  |
| 2022-02-01 | 111.3 |  |  |  |  |  |
| 2022-03-01 | 107.5 |  |  |  |  |  |
| 2022-04-01 | 107.9 |  |  |  |  |  |
| 2022-05-01 | 106.6 |  |  |  |  |  |
| 2022-06-01 | 107.3 |  |  |  |  |  |
| 2022-07-01 | 105.3 |  |  |  |  |  |
| 2022-08-01 | 103.3 |  |  |  |  |  |
| 2022-09-01 | 102.7 |  |  |  |  |  |
| 2022-10-01 | 103.7 |  |  |  |  |  |
| 2022-11-01 | 101.6 |  |  |  |  |  |
| 2022-12-01 | 101.4 |  |  |  |  |  |
| 2023-01-01 | 102.2 |  |  |  |  |  |
| 2023-02-01 | 103.3 |  |  |  |  |  |
| 2023-03-01 | 103.6 |  |  |  |  |  |
| 2023-04-01 | 100.9 |  |  |  |  |  |
| 2023-05-01 | 98.9 |  |  |  |  |  |
| 2023-06-01 | 100.1 |  |  |  |  |  |
| 2023-07-01 | 100.7 |  |  |  |  |  |
| 2023-08-01 | 96.8 |  |  |  |  |  |
| 2023-09-01 | 99.1 |  |  |  |  |  |
| 2023-10-01 | 98.8 |  |  |  |  |  |
| 2023-11-01 | 98.6 |  |  |  |  |  |
| 2023-12-01 | 99.3 |  |  |  |  |  |
| 2024-01-01 | 99 |  |  |  |  |  |
| 2024-02-01 | 100.7 |  |  |  |  |  |
| 2024-03-01 | 102 |  |  |  |  |  |
| 2024-04-01 | 100 |  |  |  |  |  |
| 2024-05-01 | 99.5 |  |  |  |  |  |
| 2024-06-01 | 98.9 |  |  |  |  |  |
| 2024-07-01 | 95.4 |  |  |  |  |  |
| 2024-08-01 | 99.9 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001585934?lastNObservations=24 |  |  | A |  |
| 2024-09-01 | 98.5 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001585934?lastNObservations=24 |  |  | A |  |
| 2024-10-01 | 92.6 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001585934?lastNObservations=24 |  |  | A |  |
| 2024-11-01 | 96.3 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001585934?lastNObservations=24 |  |  | A |  |
| 2024-12-01 | 96.5 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001585934?lastNObservations=24 |  |  | A |  |
| 2025-01-01 | 95.6 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001585934?lastNObservations=24 |  |  | A |  |
| 2025-02-01 | 97.5 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001585934?lastNObservations=24 |  |  | A |  |
| 2025-03-01 | 96.8 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001585934?lastNObservations=24 |  |  | A |  |
| 2025-04-01 | 99.9 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001585934?lastNObservations=24 |  |  | A |  |
| 2025-05-01 | 97.1 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001585934?lastNObservations=24 |  |  | A |  |
| 2025-06-01 | 96.6 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001585934?lastNObservations=24 |  |  | A |  |
| 2025-07-01 | 96 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001585934?lastNObservations=24 |  |  | A |  |
| 2025-08-01 | 97.7 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001585934?lastNObservations=24 |  |  | A |  |
| 2025-09-01 | 96.9 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001585934?lastNObservations=24 |  |  | A |  |
| 2025-10-01 | 100.8 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001585934?lastNObservations=24 |  |  | A |  |
| 2025-11-01 | 98.2 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001585934?lastNObservations=24 |  |  | A |  |
| 2025-12-01 | 101.9 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001585934?lastNObservations=24 |  |  | A |  |
| 2026-01-01 | 105 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001585934?lastNObservations=24 |  |  | A |  |
| 2026-02-01 | 101.8 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001585934?lastNObservations=24 |  |  | A |  |
| 2026-03-01 | 99.8 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001585934?lastNObservations=24 |  |  | A |  |
| 2026-04-01 | 100.2 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001585934?lastNObservations=24 |  |  | A |  |
| 2026-05-01 | 102.2 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001585934?lastNObservations=24 |  |  | A |  |
| 2026-06-01 | 100.2 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001585934?lastNObservations=24 |  |  | A |  |
| 2026-07-01 | 101.3 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001585934?lastNObservations=24 |  |  | A |  |

### 西班牙製造業 PMI

- Block: `製造業`
- Series ID: `es_manufacturing_pmi`
- Original ticker/label: `西 製造業PMI`
- Frequency: `monthly`
- Observations: `36`

| Date | Value | Source URL | Source Frequency | Release Type | Status | Note |
|---|---:|---|---|---|---|---|
| 2023-07-01 | 47.8 |  |  |  |  |  |
| 2023-08-01 | 46.5 |  |  |  |  |  |
| 2023-09-01 | 47.7 |  |  |  |  |  |
| 2023-10-01 | 45.1 |  |  |  |  |  |
| 2023-11-01 | 46.3 |  |  |  |  |  |
| 2023-12-01 | 46.2 |  |  |  |  |  |
| 2024-01-01 | 49.2 |  |  |  |  |  |
| 2024-02-01 | 51.5 |  |  |  |  |  |
| 2024-03-01 | 51.4 |  |  |  |  |  |
| 2024-04-01 | 52.2 |  |  |  |  |  |
| 2024-05-01 | 54 |  |  |  |  |  |
| 2024-06-01 | 52.3 |  |  |  |  |  |
| 2024-07-01 | 51 |  |  |  |  |  |
| 2024-08-01 | 50.5 |  |  |  |  |  |
| 2024-09-01 | 53 |  |  |  |  |  |
| 2024-10-01 | 54.5 |  |  |  |  |  |
| 2024-11-01 | 53.1 |  |  |  |  |  |
| 2024-12-01 | 53.3 |  |  |  |  |  |
| 2025-01-01 | 50.9 |  |  |  |  |  |
| 2025-02-01 | 49.7 |  |  |  |  |  |
| 2025-03-01 | 49.5 |  |  |  |  |  |
| 2025-04-01 | 48.1 |  |  |  |  |  |
| 2025-05-01 | 50.5 |  |  |  |  |  |
| 2025-06-01 | 51.4 |  |  |  |  |  |
| 2025-07-01 | 51.9 |  |  |  |  |  |
| 2025-08-01 | 54.3 |  |  |  |  |  |
| 2025-09-01 | 51.5 |  |  |  |  |  |
| 2025-10-01 | 52.1 |  |  |  |  |  |
| 2025-11-01 | 51.5 |  |  |  |  |  |
| 2025-12-01 | 49.6 |  |  |  |  |  |
| 2026-01-01 | 49.2 |  |  |  |  |  |
| 2026-02-01 | 50 |  |  |  |  |  |
| 2026-03-01 | 48.7 |  |  |  |  |  |
| 2026-04-01 | 51.7 |  |  |  |  |  |
| 2026-05-01 | 51.2 |  |  |  |  |  |
| 2026-06-01 | 49.7 | https://tradingeconomics.com/spain/manufacturing-pmi |  | final | final | public indicator page; underlying source explicitly S&P Global; final |

### 德國服務業 PMI

- Block: `服務業`
- Series ID: `de_services_pmi`
- Original ticker/label: `德 服務業PMI`
- Frequency: `monthly`
- Observations: `36`

| Date | Value | Source URL | Source Frequency | Release Type | Status | Note |
|---|---:|---|---|---|---|---|
| 2023-07-01 | 52.3 |  |  |  |  |  |
| 2023-08-01 | 47.3 |  |  |  |  |  |
| 2023-09-01 | 50.3 |  |  |  |  |  |
| 2023-10-01 | 48.2 |  |  |  |  |  |
| 2023-11-01 | 49.6 |  |  |  |  |  |
| 2023-12-01 | 49.3 |  |  |  |  |  |
| 2024-01-01 | 47.7 |  |  |  |  |  |
| 2024-02-01 | 48.3 |  |  |  |  |  |
| 2024-03-01 | 50.1 |  |  |  |  |  |
| 2024-04-01 | 53.2 |  |  |  |  |  |
| 2024-05-01 | 54.2 |  |  |  |  |  |
| 2024-06-01 | 53.1 |  |  |  |  |  |
| 2024-07-01 | 52.5 |  |  |  |  |  |
| 2024-08-01 | 51.2 |  |  |  |  |  |
| 2024-09-01 | 50.6 |  |  |  |  |  |
| 2024-10-01 | 51.6 |  |  |  |  |  |
| 2024-11-01 | 49.3 |  |  |  |  |  |
| 2024-12-01 | 51.2 |  |  |  |  |  |
| 2025-01-01 | 52.5 |  |  |  |  |  |
| 2025-02-01 | 51.1 |  |  |  |  |  |
| 2025-03-01 | 50.9 |  |  |  |  |  |
| 2025-04-01 | 49 |  |  |  |  |  |
| 2025-05-01 | 47.1 |  |  |  |  |  |
| 2025-06-01 | 49.7 |  |  |  |  |  |
| 2025-07-01 | 50.6 |  |  |  |  |  |
| 2025-08-01 | 49.3 |  |  |  |  |  |
| 2025-09-01 | 51.5 |  |  |  |  |  |
| 2025-10-01 | 54.6 |  |  |  |  |  |
| 2025-11-01 | 53.1 |  |  |  |  |  |
| 2025-12-01 | 52.7 |  |  |  |  |  |
| 2026-01-01 | 52.4 |  |  |  |  |  |
| 2026-02-01 | 53.5 |  |  |  |  |  |
| 2026-03-01 | 50.9 |  |  |  |  |  |
| 2026-04-01 | 46.9 |  |  |  |  |  |
| 2026-05-01 | 48.1 |  |  |  |  |  |
| 2026-07-01 | 49.6 | https://www.pmi.spglobal.com/Public/Home/PressRelease/33afc7650b4243d49379ecc2c469b446 |  | flash | flash | matched UK-template label: Flash Germany Services PMI Business Activity Index: 49.6 |

### 法國服務業 PMI

- Block: `服務業`
- Series ID: `fr_services_pmi`
- Original ticker/label: `法 服務業PMI`
- Frequency: `monthly`
- Observations: `36`

| Date | Value | Source URL | Source Frequency | Release Type | Status | Note |
|---|---:|---|---|---|---|---|
| 2023-07-01 | 47.1 |  |  |  |  |  |
| 2023-08-01 | 46 |  |  |  |  |  |
| 2023-09-01 | 44.4 |  |  |  |  |  |
| 2023-10-01 | 45.2 |  |  |  |  |  |
| 2023-11-01 | 45.4 |  |  |  |  |  |
| 2023-12-01 | 45.7 |  |  |  |  |  |
| 2024-01-01 | 45.4 |  |  |  |  |  |
| 2024-02-01 | 48.4 |  |  |  |  |  |
| 2024-03-01 | 48.3 |  |  |  |  |  |
| 2024-04-01 | 51.3 |  |  |  |  |  |
| 2024-05-01 | 49.3 |  |  |  |  |  |
| 2024-06-01 | 49.6 |  |  |  |  |  |
| 2024-07-01 | 50.1 |  |  |  |  |  |
| 2024-08-01 | 55 |  |  |  |  |  |
| 2024-09-01 | 49.6 |  |  |  |  |  |
| 2024-10-01 | 49.2 |  |  |  |  |  |
| 2024-11-01 | 46.9 |  |  |  |  |  |
| 2024-12-01 | 49.3 |  |  |  |  |  |
| 2025-01-01 | 48.2 |  |  |  |  |  |
| 2025-02-01 | 45.3 |  |  |  |  |  |
| 2025-03-01 | 47.9 |  |  |  |  |  |
| 2025-04-01 | 47.3 |  |  |  |  |  |
| 2025-05-01 | 48.9 |  |  |  |  |  |
| 2025-06-01 | 49.6 |  |  |  |  |  |
| 2025-07-01 | 48.5 |  |  |  |  |  |
| 2025-08-01 | 49.8 |  |  |  |  |  |
| 2025-09-01 | 48.5 |  |  |  |  |  |
| 2025-10-01 | 48 |  |  |  |  |  |
| 2025-11-01 | 51.4 |  |  |  |  |  |
| 2025-12-01 | 50.1 |  |  |  |  |  |
| 2026-01-01 | 48.4 |  |  |  |  |  |
| 2026-02-01 | 49.6 |  |  |  |  |  |
| 2026-03-01 | 48.8 |  |  |  |  |  |
| 2026-04-01 | 46.5 |  |  |  |  |  |
| 2026-05-01 | 44.3 |  |  |  |  |  |
| 2026-07-01 | 49.8 | https://tradingeconomics.com/france/services-pmi |  | flash | flash | public indicator page; underlying source explicitly S&P Global; flash |

### 西班牙服務業 PMI

- Block: `服務業`
- Series ID: `es_services_pmi`
- Original ticker/label: `西 服務業PMI`
- Frequency: `monthly`
- Observations: `36`

| Date | Value | Source URL | Source Frequency | Release Type | Status | Note |
|---|---:|---|---|---|---|---|
| 2023-07-01 | 52.8 |  |  |  |  |  |
| 2023-08-01 | 49.3 |  |  |  |  |  |
| 2023-09-01 | 50.5 |  |  |  |  |  |
| 2023-10-01 | 51.1 |  |  |  |  |  |
| 2023-11-01 | 51 |  |  |  |  |  |
| 2023-12-01 | 51.5 |  |  |  |  |  |
| 2024-01-01 | 52.1 |  |  |  |  |  |
| 2024-02-01 | 54.7 |  |  |  |  |  |
| 2024-03-01 | 56.1 |  |  |  |  |  |
| 2024-04-01 | 56.2 |  |  |  |  |  |
| 2024-05-01 | 56.9 |  |  |  |  |  |
| 2024-06-01 | 56.8 |  |  |  |  |  |
| 2024-07-01 | 53.9 |  |  |  |  |  |
| 2024-08-01 | 54.6 |  |  |  |  |  |
| 2024-09-01 | 57 |  |  |  |  |  |
| 2024-10-01 | 54.9 |  |  |  |  |  |
| 2024-11-01 | 53.1 |  |  |  |  |  |
| 2024-12-01 | 57.3 |  |  |  |  |  |
| 2025-01-01 | 54.9 |  |  |  |  |  |
| 2025-02-01 | 56.2 |  |  |  |  |  |
| 2025-03-01 | 54.7 |  |  |  |  |  |
| 2025-04-01 | 53.4 |  |  |  |  |  |
| 2025-05-01 | 51.3 |  |  |  |  |  |
| 2025-06-01 | 51.9 |  |  |  |  |  |
| 2025-07-01 | 55.1 |  |  |  |  |  |
| 2025-08-01 | 53.2 |  |  |  |  |  |
| 2025-09-01 | 54.3 |  |  |  |  |  |
| 2025-10-01 | 56.6 |  |  |  |  |  |
| 2025-11-01 | 55.6 |  |  |  |  |  |
| 2025-12-01 | 57.1 |  |  |  |  |  |
| 2026-01-01 | 53.5 |  |  |  |  |  |
| 2026-02-01 | 51.9 |  |  |  |  |  |
| 2026-03-01 | 53.3 |  |  |  |  |  |
| 2026-04-01 | 47.9 |  |  |  |  |  |
| 2026-05-01 | 50.1 |  |  |  |  |  |
| 2026-06-01 | 54.2 | https://tradingeconomics.com/spain/services-pmi |  | final | final | public indicator page; underlying source explicitly S&P Global; final |

### 法國企業信心

- Block: `企業信心`
- Series ID: `fr_business_confidence`
- Original ticker/label: `法 企業信心`
- Frequency: `monthly`
- Observations: `139`

| Date | Value | Source URL | Source Frequency | Release Type | Status | Note |
|---|---:|---|---|---|---|---|
| 2015-01-01 | 94.9 |  |  |  |  |  |
| 2015-02-01 | 95.9 |  |  |  |  |  |
| 2015-03-01 | 97.1 |  |  |  |  |  |
| 2015-04-01 | 98.7 |  |  |  |  |  |
| 2015-05-01 | 99.7 |  |  |  |  |  |
| 2015-06-01 | 100.9 |  |  |  |  |  |
| 2015-07-01 | 101.4 |  |  |  |  |  |
| 2015-08-01 | 103.2 |  |  |  |  |  |
| 2015-09-01 | 102.4 |  |  |  |  |  |
| 2015-10-01 | 103.2 |  |  |  |  |  |
| 2015-11-01 | 103.3 |  |  |  |  |  |
| 2015-12-01 | 101.8 |  |  |  |  |  |
| 2016-01-01 | 104.3 |  |  |  |  |  |
| 2016-02-01 | 103.3 |  |  |  |  |  |
| 2016-03-01 | 103.2 |  |  |  |  |  |
| 2016-04-01 | 102.5 |  |  |  |  |  |
| 2016-05-01 | 104.6 |  |  |  |  |  |
| 2016-06-01 | 103.2 |  |  |  |  |  |
| 2016-07-01 | 104 |  |  |  |  |  |
| 2016-08-01 | 103.6 |  |  |  |  |  |
| 2016-09-01 | 103.7 |  |  |  |  |  |
| 2016-10-01 | 103.8 |  |  |  |  |  |
| 2016-11-01 | 103.9 |  |  |  |  |  |
| 2016-12-01 | 106.3 |  |  |  |  |  |
| 2017-01-01 | 106.2 |  |  |  |  |  |
| 2017-02-01 | 107.1 |  |  |  |  |  |
| 2017-03-01 | 106.7 |  |  |  |  |  |
| 2017-04-01 | 107.5 |  |  |  |  |  |
| 2017-05-01 | 107.9 |  |  |  |  |  |
| 2017-06-01 | 108.9 |  |  |  |  |  |
| 2017-07-01 | 109.9 |  |  |  |  |  |
| 2017-08-01 | 110.6 |  |  |  |  |  |
| 2017-09-01 | 111.1 |  |  |  |  |  |
| 2017-10-01 | 111.1 |  |  |  |  |  |
| 2017-11-01 | 112.2 |  |  |  |  |  |
| 2017-12-01 | 113.4 |  |  |  |  |  |
| 2018-01-01 | 113 |  |  |  |  |  |
| 2018-02-01 | 112 |  |  |  |  |  |
| 2018-03-01 | 111.9 |  |  |  |  |  |
| 2018-04-01 | 111.4 |  |  |  |  |  |
| 2018-05-01 | 109.7 |  |  |  |  |  |
| 2018-06-01 | 109.1 |  |  |  |  |  |
| 2018-07-01 | 108.2 |  |  |  |  |  |
| 2018-08-01 | 107.8 |  |  |  |  |  |
| 2018-09-01 | 107.4 |  |  |  |  |  |
| 2018-10-01 | 106.5 |  |  |  |  |  |
| 2018-11-01 | 106.9 |  |  |  |  |  |
| 2018-12-01 | 103.7 |  |  |  |  |  |
| 2019-01-01 | 104.5 |  |  |  |  |  |
| 2019-02-01 | 104.6 |  |  |  |  |  |
| 2019-03-01 | 106.3 |  |  |  |  |  |
| 2019-04-01 | 107.5 |  |  |  |  |  |
| 2019-05-01 | 107.3 |  |  |  |  |  |
| 2019-06-01 | 107.1 |  |  |  |  |  |
| 2019-07-01 | 106.1 |  |  |  |  |  |
| 2019-08-01 | 106.3 |  |  |  |  |  |
| 2019-09-01 | 106.9 |  |  |  |  |  |
| 2019-10-01 | 106.9 |  |  |  |  |  |
| 2019-11-01 | 107 |  |  |  |  |  |
| 2019-12-01 | 106.7 |  |  |  |  |  |
| 2020-01-01 | 106.7 |  |  |  |  |  |
| 2020-02-01 | 106.1 |  |  |  |  |  |
| 2020-03-01 | 93.9 |  |  |  |  |  |
| 2020-04-01 | 45.7 |  |  |  |  |  |
| 2020-05-01 | 58.5 |  |  |  |  |  |
| 2020-06-01 | 84.8 |  |  |  |  |  |
| 2020-07-01 | 90.6 |  |  |  |  |  |
| 2020-08-01 | 94.2 |  |  |  |  |  |
| 2020-09-01 | 93.7 |  |  |  |  |  |
| 2020-10-01 | 90.1 |  |  |  |  |  |
| 2020-11-01 | 77.4 |  |  |  |  |  |
| 2020-12-01 | 92.6 |  |  |  |  |  |
| 2021-01-01 | 93.8 |  |  |  |  |  |
| 2021-02-01 | 90.9 |  |  |  |  |  |
| 2021-03-01 | 98.2 |  |  |  |  |  |
| 2021-04-01 | 97.2 |  |  |  |  |  |
| 2021-05-01 | 111.2 |  |  |  |  |  |
| 2021-06-01 | 115.9 |  |  |  |  |  |
| 2021-07-01 | 113.6 |  |  |  |  |  |
| 2021-08-01 | 111.2 |  |  |  |  |  |
| 2021-09-01 | 112.2 |  |  |  |  |  |
| 2021-10-01 | 114.4 |  |  |  |  |  |
| 2021-11-01 | 115 |  |  |  |  |  |
| 2021-12-01 | 110.2 |  |  |  |  |  |
| 2022-01-01 | 108.6 |  |  |  |  |  |
| 2022-02-01 | 114.1 |  |  |  |  |  |
| 2022-03-01 | 107.6 |  |  |  |  |  |
| 2022-04-01 | 107.2 |  |  |  |  |  |
| 2022-05-01 | 106.5 |  |  |  |  |  |
| 2022-06-01 | 104.9 |  |  |  |  |  |
| 2022-07-01 | 103.6 |  |  |  |  |  |
| 2022-08-01 | 104.1 |  |  |  |  |  |
| 2022-09-01 | 102.4 |  |  |  |  |  |
| 2022-10-01 | 103.1 |  |  |  |  |  |
| 2022-11-01 | 102.6 |  |  |  |  |  |
| 2022-12-01 | 103 |  |  |  |  |  |
| 2023-01-01 | 102.5 |  |  |  |  |  |
| 2023-02-01 | 103.5 |  |  |  |  |  |
| 2023-03-01 | 103.1 |  |  |  |  |  |
| 2023-04-01 | 103.5 |  |  |  |  |  |
| 2023-05-01 | 100.9 |  |  |  |  |  |
| 2023-06-01 | 100.9 |  |  |  |  |  |
| 2023-07-01 | 100.7 |  |  |  |  |  |
| 2023-08-01 | 100.4 |  |  |  |  |  |
| 2023-09-01 | 100.1 |  |  |  |  |  |
| 2023-10-01 | 99.1 |  |  |  |  |  |
| 2023-11-01 | 97.9 |  |  |  |  |  |
| 2023-12-01 | 98.4 |  |  |  |  |  |
| 2024-01-01 | 99.1 |  |  |  |  |  |
| 2024-02-01 | 99 |  |  |  |  |  |
| 2024-03-01 | 100.3 |  |  |  |  |  |
| 2024-04-01 | 99.8 |  |  |  |  |  |
| 2024-05-01 | 100.1 |  |  |  |  |  |
| 2024-06-01 | 99.6 |  |  |  |  |  |
| 2024-07-01 | 94.4 |  |  |  |  |  |
| 2024-08-01 | 97 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001565530?lastNObservations=24 |  |  | A |  |
| 2024-09-01 | 97.8 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001565530?lastNObservations=24 |  |  | A |  |
| 2024-10-01 | 97.7 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001565530?lastNObservations=24 |  |  | A |  |
| 2024-11-01 | 95.8 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001565530?lastNObservations=24 |  |  | A |  |
| 2024-12-01 | 94.5 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001565530?lastNObservations=24 |  |  | A |  |
| 2025-01-01 | 95.1 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001565530?lastNObservations=24 |  |  | A |  |
| 2025-02-01 | 96.1 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001565530?lastNObservations=24 |  |  | A |  |
| 2025-03-01 | 96.7 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001565530?lastNObservations=24 |  |  | A |  |
| 2025-04-01 | 96.9 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001565530?lastNObservations=24 |  |  | A |  |
| 2025-05-01 | 95.6 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001565530?lastNObservations=24 |  |  | A |  |
| 2025-06-01 | 96 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001565530?lastNObservations=24 |  |  | A |  |
| 2025-07-01 | 95.9 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001565530?lastNObservations=24 |  |  | A |  |
| 2025-08-01 | 96.5 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001565530?lastNObservations=24 |  |  | A |  |
| 2025-09-01 | 96.3 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001565530?lastNObservations=24 |  |  | A |  |
| 2025-10-01 | 97.3 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001565530?lastNObservations=24 |  |  | A |  |
| 2025-11-01 | 97.4 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001565530?lastNObservations=24 |  |  | A |  |
| 2025-12-01 | 98.2 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001565530?lastNObservations=24 |  |  | A |  |
| 2026-01-01 | 99.1 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001565530?lastNObservations=24 |  |  | A |  |
| 2026-02-01 | 98.8 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001565530?lastNObservations=24 |  |  | A |  |
| 2026-03-01 | 97.7 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001565530?lastNObservations=24 |  |  | A |  |
| 2026-04-01 | 94.1 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001565530?lastNObservations=24 |  |  | A |  |
| 2026-05-01 | 93.9 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001565530?lastNObservations=24 |  |  | A |  |
| 2026-06-01 | 95 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001565530?lastNObservations=24 |  |  | A |  |
| 2026-07-01 | 97.2 | https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001565530?lastNObservations=24 |  |  | A |  |

### 德國 ifo 企業信心

- Block: `企業信心`
- Series ID: `de_ifo_business_climate`
- Original ticker/label: `德 企業信心`
- Frequency: `monthly`
- Observations: `138`

| Date | Value | Source URL | Source Frequency | Release Type | Status | Note |
|---|---:|---|---|---|---|---|
| 2015-01-01 | 98.8 |  |  |  |  |  |
| 2015-02-01 | 98.8 |  |  |  |  |  |
| 2015-03-01 | 99.1 |  |  |  |  |  |
| 2015-04-01 | 100.2 |  |  |  |  |  |
| 2015-05-01 | 100.4 |  |  |  |  |  |
| 2015-06-01 | 100.1 |  |  |  |  |  |
| 2015-07-01 | 99.7 |  |  |  |  |  |
| 2015-08-01 | 100.6 |  |  |  |  |  |
| 2015-09-01 | 100.1 |  |  |  |  |  |
| 2015-10-01 | 100.6 |  |  |  |  |  |
| 2015-11-01 | 101 |  |  |  |  |  |
| 2015-12-01 | 100.7 |  |  |  |  |  |
| 2016-01-01 | 99.7 |  |  |  |  |  |
| 2016-02-01 | 98.7 |  |  |  |  |  |
| 2016-03-01 | 99.1 |  |  |  |  |  |
| 2016-04-01 | 100.1 |  |  |  |  |  |
| 2016-05-01 | 99.8 |  |  |  |  |  |
| 2016-06-01 | 100 |  |  |  |  |  |
| 2016-07-01 | 100 |  |  |  |  |  |
| 2016-08-01 | 99.6 |  |  |  |  |  |
| 2016-09-01 | 100.8 |  |  |  |  |  |
| 2016-10-01 | 101.3 |  |  |  |  |  |
| 2016-11-01 | 101.6 |  |  |  |  |  |
| 2016-12-01 | 101 |  |  |  |  |  |
| 2017-01-01 | 101.3 |  |  |  |  |  |
| 2017-02-01 | 101.3 |  |  |  |  |  |
| 2017-03-01 | 101.9 |  |  |  |  |  |
| 2017-04-01 | 103.7 |  |  |  |  |  |
| 2017-05-01 | 102.7 |  |  |  |  |  |
| 2017-06-01 | 102.7 |  |  |  |  |  |
| 2017-07-01 | 103.8 |  |  |  |  |  |
| 2017-08-01 | 103.6 |  |  |  |  |  |
| 2017-09-01 | 103.9 |  |  |  |  |  |
| 2017-10-01 | 104.3 |  |  |  |  |  |
| 2017-11-01 | 104.9 |  |  |  |  |  |
| 2017-12-01 | 104.7 |  |  |  |  |  |
| 2018-01-01 | 105 |  |  |  |  |  |
| 2018-02-01 | 104 |  |  |  |  |  |
| 2018-03-01 | 103.9 |  |  |  |  |  |
| 2018-04-01 | 103.5 |  |  |  |  |  |
| 2018-05-01 | 102.9 |  |  |  |  |  |
| 2018-06-01 | 101.6 |  |  |  |  |  |
| 2018-07-01 | 101.6 |  |  |  |  |  |
| 2018-08-01 | 103.7 |  |  |  |  |  |
| 2018-09-01 | 103.8 |  |  |  |  |  |
| 2018-10-01 | 102.8 |  |  |  |  |  |
| 2018-11-01 | 102.3 |  |  |  |  |  |
| 2018-12-01 | 101.2 |  |  |  |  |  |
| 2019-01-01 | 99.6 |  |  |  |  |  |
| 2019-02-01 | 98.7 |  |  |  |  |  |
| 2019-03-01 | 99.9 |  |  |  |  |  |
| 2019-04-01 | 100.7 |  |  |  |  |  |
| 2019-05-01 | 98.3 |  |  |  |  |  |
| 2019-06-01 | 96.8 |  |  |  |  |  |
| 2019-07-01 | 95.5 |  |  |  |  |  |
| 2019-08-01 | 94.1 |  |  |  |  |  |
| 2019-09-01 | 94.8 |  |  |  |  |  |
| 2019-10-01 | 94.9 |  |  |  |  |  |
| 2019-11-01 | 95.3 |  |  |  |  |  |
| 2019-12-01 | 96.5 |  |  |  |  |  |
| 2020-01-01 | 96.1 |  |  |  |  |  |
| 2020-02-01 | 96 |  |  |  |  |  |
| 2020-03-01 | 86.3 |  |  |  |  |  |
| 2020-04-01 | 75.1 |  |  |  |  |  |
| 2020-05-01 | 79.5 |  |  |  |  |  |
| 2020-06-01 | 85.3 |  |  |  |  |  |
| 2020-07-01 | 89.4 |  |  |  |  |  |
| 2020-08-01 | 92 |  |  |  |  |  |
| 2020-09-01 | 93.5 |  |  |  |  |  |
| 2020-10-01 | 92.9 |  |  |  |  |  |
| 2020-11-01 | 91.6 |  |  |  |  |  |
| 2020-12-01 | 93.2 |  |  |  |  |  |
| 2021-01-01 | 90.7 |  |  |  |  |  |
| 2021-02-01 | 92.7 |  |  |  |  |  |
| 2021-03-01 | 96.2 |  |  |  |  |  |
| 2021-04-01 | 96.1 |  |  |  |  |  |
| 2021-05-01 | 98.3 |  |  |  |  |  |
| 2021-06-01 | 100.9 |  |  |  |  |  |
| 2021-07-01 | 100.7 |  |  |  |  |  |
| 2021-08-01 | 100.1 |  |  |  |  |  |
| 2021-09-01 | 100 |  |  |  |  |  |
| 2021-10-01 | 98.8 |  |  |  |  |  |
| 2021-11-01 | 97.2 |  |  |  |  |  |
| 2021-12-01 | 95.3 |  |  |  |  |  |
| 2022-01-01 | 96.2 |  |  |  |  |  |
| 2022-02-01 | 98.6 |  |  |  |  |  |
| 2022-03-01 | 90 |  |  |  |  |  |
| 2022-04-01 | 91.3 |  |  |  |  |  |
| 2022-05-01 | 92.3 |  |  |  |  |  |
| 2022-06-01 | 92 |  |  |  |  |  |
| 2022-07-01 | 88.6 |  |  |  |  |  |
| 2022-08-01 | 89.1 |  |  |  |  |  |
| 2022-09-01 | 85.7 |  |  |  |  |  |
| 2022-10-01 | 85.3 |  |  |  |  |  |
| 2022-11-01 | 86.8 |  |  |  |  |  |
| 2022-12-01 | 89.2 |  |  |  |  |  |
| 2023-01-01 | 90.5 |  |  |  |  |  |
| 2023-02-01 | 91.1 |  |  |  |  |  |
| 2023-03-01 | 92.7 |  |  |  |  |  |
| 2023-04-01 | 92.9 |  |  |  |  |  |
| 2023-05-01 | 90.9 |  |  |  |  |  |
| 2023-06-01 | 88.2 |  |  |  |  |  |
| 2023-07-01 | 87.3 |  |  |  |  |  |
| 2023-08-01 | 85.8 |  |  |  |  |  |
| 2023-09-01 | 86.2 |  |  |  |  |  |
| 2023-10-01 | 86.9 |  |  |  |  |  |
| 2023-11-01 | 87.3 |  |  |  |  |  |
| 2023-12-01 | 86.8 |  |  |  |  |  |
| 2024-01-01 | 85.7 |  |  |  |  |  |
| 2024-02-01 | 85.8 |  |  |  |  |  |
| 2024-03-01 | 87.8 |  |  |  |  |  |
| 2024-04-01 | 89.1 |  |  |  |  |  |
| 2024-05-01 | 88.8 |  |  |  |  |  |
| 2024-06-01 | 88.2 |  |  |  |  |  |
| 2024-07-01 | 86.9 |  |  |  |  |  |
| 2024-08-01 | 86.5 |  |  |  |  |  |
| 2024-09-01 | 85.5 |  |  |  |  |  |
| 2024-10-01 | 86.4 |  |  |  |  |  |
| 2024-11-01 | 85.6 |  |  |  |  |  |
| 2024-12-01 | 84.9 |  |  |  |  |  |
| 2025-01-01 | 85.5 |  |  |  |  |  |
| 2025-02-01 | 85.3 |  |  |  |  |  |
| 2025-03-01 | 86.8 |  |  |  |  |  |
| 2025-04-01 | 86.9 |  |  |  |  |  |
| 2025-05-01 | 87.4 |  |  |  |  |  |
| 2025-06-01 | 88.3 |  |  |  |  |  |
| 2025-07-01 | 88.5 |  |  |  |  |  |
| 2025-08-01 | 88.8 |  |  |  |  |  |
| 2025-09-01 | 87.6 |  |  |  |  |  |
| 2025-10-01 | 88.4 |  |  |  |  |  |
| 2025-11-01 | 88 |  |  |  |  |  |
| 2025-12-01 | 87.6 |  |  |  |  |  |
| 2026-01-01 | 87.6 |  |  |  |  |  |
| 2026-02-01 | 88.5 |  |  |  |  |  |
| 2026-03-01 | 86.3 |  |  |  |  |  |
| 2026-04-01 | 84.5 |  |  |  |  |  |
| 2026-05-01 | 85 |  |  |  |  |  |
| 2026-07-01 | 86.6 | https://www.ifo.de/en/survey/ifo-business-climate-index-germany |  |  |  | official ifo survey/time-series page |

### 德國 GDP YoY

- Block: `GDP`
- Series ID: `de_gdp_yoy`
- Original ticker/label: `德 GDP`
- Frequency: `quarterly`
- Observations: `45`

| Date | Value | Source URL | Source Frequency | Release Type | Status | Note |
|---|---:|---|---|---|---|---|
| 2015-03-01 | 1.2369172217 |  |  |  |  |  |
| 2015-06-01 | 1.6163334751 |  |  |  |  |  |
| 2015-09-01 | 1.6410469464 |  |  |  |  |  |
| 2015-12-01 | 2.1429303804 |  |  |  |  |  |
| 2016-03-01 | 2.1407685881 |  |  |  |  |  |
| 2016-06-01 | 3.5370447886 |  |  |  |  |  |
| 2016-09-01 | 1.8189249949 |  |  |  |  |  |
| 2016-12-01 | 1.4153784381 |  |  |  |  |  |
| 2017-03-01 | 3.6192618342 |  |  |  |  |  |
| 2017-06-01 | 1.5160703457 |  |  |  |  |  |
| 2017-09-01 | 2.8101164191 |  |  |  |  |  |
| 2017-12-01 | 3.2762545778 |  |  |  |  |  |
| 2018-03-01 | 1.4405525407 |  |  |  |  |  |
| 2018-06-01 | 2.2401433692 |  |  |  |  |  |
| 2018-09-01 | 0.4490433424 |  |  |  |  |  |
| 2018-12-01 | 0.4408663983 |  |  |  |  |  |
| 2019-03-01 | 1.1769283144 |  |  |  |  |  |
| 2019-06-01 | 0.0681663258 |  |  |  |  |  |
| 2019-09-01 | 2.0116618076 |  |  |  |  |  |
| 2019-12-01 | 0.6393129771 |  |  |  |  |  |
| 2020-03-01 | -1.5477792732 |  |  |  |  |  |
| 2020-06-01 | -10.8018684313 |  |  |  |  |  |
| 2020-09-01 | -3.1913880156 |  |  |  |  |  |
| 2020-12-01 | -1.0998388167 |  |  |  |  |  |
| 2021-03-01 | -0.7030563422 |  |  |  |  |  |
| 2021-06-01 | 12.0117826751 |  |  |  |  |  |
| 2021-09-01 | 2.8144066129 |  |  |  |  |  |
| 2021-12-01 | 2.3967021379 |  |  |  |  |  |
| 2022-03-01 | 4.0121939227 |  |  |  |  |  |
| 2022-06-01 | 1.4902113568 |  |  |  |  |  |
| 2022-09-01 | 1.6175344564 |  |  |  |  |  |
| 2022-12-01 | 0.1966108042 |  |  |  |  |  |
| 2023-03-01 | -0.0283634301 |  |  |  |  |  |
| 2023-06-01 | -1.113243762 |  |  |  |  |  |
| 2023-09-01 | -1.3186399171 |  |  |  |  |  |
| 2023-12-01 | -1.0278452626 |  |  |  |  |  |
| 2024-03-01 | -1.1064876111 |  |  |  |  |  |
| 2024-06-01 | -0.2911490683 |  |  |  |  |  |
| 2024-09-01 | -0.181349623 |  |  |  |  |  |
| 2024-12-01 | -0.3965256798 |  |  |  |  |  |
| 2025-03-01 | 0.1 |  |  |  |  |  |
| 2025-06-01 | 0 |  |  |  |  |  |
| 2025-09-01 | 0.3 |  |  |  |  |  |
| 2025-12-01 | 0.5 |  |  |  |  |  |
| 2026-03-01 | 0.5 | https://www.destatis.de/EN/Press/2026/05/PE26_173_811.html |  |  |  |  |

### 西班牙 GDP YoY

- Block: `GDP`
- Series ID: `es_gdp_yoy`
- Original ticker/label: `西 GDP`
- Frequency: `quarterly`
- Observations: `45`

| Date | Value | Source URL | Source Frequency | Release Type | Status | Note |
|---|---:|---|---|---|---|---|
| 2015-03-01 | 3.6 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2015-06-01 | 4.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2015-09-01 | 4.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2015-12-01 | 4.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2016-03-01 | 3.7 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2016-06-01 | 2.9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2016-09-01 | 2.7 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2016-12-01 | 2.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2017-03-01 | 2.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2017-06-01 | 3.1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2017-09-01 | 3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2017-12-01 | 3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2018-03-01 | 2.7 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2018-06-01 | 2.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2018-09-01 | 2.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2018-12-01 | 2.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2019-03-01 | 2.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2019-06-01 | 2.1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2019-09-01 | 1.7 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2019-12-01 | 1.7 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2020-03-01 | -4.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2020-06-01 | -21.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2020-09-01 | -9.1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2020-12-01 | -9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2021-03-01 | -2.9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2021-06-01 | 19.8 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2021-09-01 | 5.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2021-12-01 | 6.7 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2022-03-01 | 7.1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2022-06-01 | 7.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2022-09-01 | 6.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2022-12-01 | 4.7 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2023-03-01 | 3.6 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  | p |  |
| 2023-06-01 | 2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  | p |  |
| 2023-09-01 | 2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  | p |  |
| 2023-12-01 | 2.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  | p |  |
| 2024-03-01 | 2.9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  | p |  |
| 2024-06-01 | 3.7 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  | p |  |
| 2024-09-01 | 3.6 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  | p |  |
| 2024-12-01 | 3.7 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  | p |  |
| 2025-03-01 | 3.1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  | p |  |
| 2025-06-01 | 2.9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  | p |  |
| 2025-09-01 | 2.7 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  | p |  |
| 2025-12-01 | 2.6 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  | p |  |
| 2026-03-01 | 2.7 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=ES&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  | p |  |

### 法國 GDP YoY

- Block: `GDP`
- Series ID: `fr_gdp_yoy`
- Original ticker/label: `法GDP`
- Frequency: `quarterly`
- Observations: `45`

| Date | Value | Source URL | Source Frequency | Release Type | Status | Note |
|---|---:|---|---|---|---|---|
| 2015-03-01 | 1.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2015-06-01 | 1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2015-09-01 | 0.6 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2015-12-01 | 1.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2016-03-01 | 0.9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2016-06-01 | 0.6 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2016-09-01 | 0.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2016-12-01 | 0.9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2017-03-01 | 1.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2017-06-01 | 2.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2017-09-01 | 2.8 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2017-12-01 | 2.8 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2018-03-01 | 2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2018-06-01 | 1.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2018-09-01 | 1.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2018-12-01 | 1.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2019-03-01 | 2.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2019-06-01 | 2.7 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2019-09-01 | 2.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2019-12-01 | 1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2020-03-01 | -5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2020-06-01 | -17 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2020-09-01 | -4.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2020-12-01 | -4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2021-03-01 | 1.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2021-06-01 | 17 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2021-09-01 | 4.7 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2021-12-01 | 5.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2022-03-01 | 4.7 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2022-06-01 | 3.9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2022-09-01 | 1.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2022-12-01 | 1.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2023-03-01 | 1.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2023-06-01 | 2.1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2023-09-01 | 1.9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2023-12-01 | 2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2024-03-01 | 2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2024-06-01 | 1.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2024-09-01 | 1.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2024-12-01 | 0.8 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2025-03-01 | 0.8 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2025-06-01 | 0.8 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2025-09-01 | 0.8 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2025-12-01 | 1.1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2026-03-01 | 0.9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=FR&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |

### 歐元區 GDP YoY

- Block: `GDP`
- Series ID: `ea_gdp_yoy`
- Original ticker/label: `歐GDP`
- Frequency: `quarterly`
- Observations: `45`

| Date | Value | Source URL | Source Frequency | Release Type | Status | Note |
|---|---:|---|---|---|---|---|
| 2015-03-01 | 1.9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2015-06-01 | 2.1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2015-09-01 | 2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2015-12-01 | 2.1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2016-03-01 | 1.8 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2016-06-01 | 1.6 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2016-09-01 | 1.7 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2016-12-01 | 2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2017-03-01 | 2.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2017-06-01 | 2.8 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2017-09-01 | 3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2017-12-01 | 3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2018-03-01 | 2.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2018-06-01 | 2.1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2018-09-01 | 1.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2018-12-01 | 1.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2019-03-01 | 1.9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2019-06-01 | 1.7 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2019-09-01 | 1.8 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2019-12-01 | 1.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2020-03-01 | -2.8 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2020-06-01 | -13.9 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2020-09-01 | -4.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2020-12-01 | -3.8 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2021-03-01 | 0.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2021-06-01 | 15.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2021-09-01 | 5.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2021-12-01 | 5.7 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2022-03-01 | 5.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2022-06-01 | 4.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2022-09-01 | 3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2022-12-01 | 2.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2023-03-01 | 1.3 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2023-06-01 | 0.6 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2023-09-01 | 0.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2023-12-01 | 0.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2024-03-01 | 0.7 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2024-06-01 | 0.7 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2024-09-01 | 1.1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2024-12-01 | 1.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2025-03-01 | 1.6 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2025-06-01 | 1.4 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2025-09-01 | 1.2 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2025-12-01 | 1.1 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
| 2026-03-01 | 0.5 | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&lang=EN&geo=EA21&na_item=B1GQ&unit=CLV_PCH_SM&s_adj=SCA |  |  |  |  |
