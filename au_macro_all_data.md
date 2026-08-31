# 澳洲總體資料 Debug 表

更新時間：2026-08-31T07:49:44.867682+00:00

> 色階用於快速檢查近期數值。多數指標數值越高越偏紅、越低越偏綠；消費信心則反向顯示。空白代表該期尚無資料。

<table>
  <thead>
    <tr>
      <th style="min-width:60px"></th>
      <th style="min-width:180px"></th>
      <th align="center" style="min-width:90px">2026/7/31</th>
      <th align="center" style="min-width:90px">2026/6/30</th>
      <th align="center" style="min-width:90px">2026/5/31</th>
      <th align="center" style="min-width:90px">2026/4/30</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="7" align="center" valign="middle">就業</th>
      <td>就業新增</td>
      <td align="right" bgcolor="#97d4a7">-16</td>
      <td align="right" bgcolor="#f86971">80</td>
      <td align="right" bgcolor="#fdd7d9">38</td>
      <td align="right" bgcolor="#63be7b">-35</td>
    </tr>
    <tr>
      <td>失業率</td>
      <td align="right" bgcolor="#fcb8bc">4.46</td>
      <td align="right" bgcolor="#f4fbf6">4.43</td>
      <td align="right" bgcolor="#63be7b">4.38</td>
      <td align="right" bgcolor="#f86971">4.49</td>
    </tr>
    <tr>
      <td>職缺</td>
      <td align="right"></td>
      <td align="right"></td>
      <td align="right" bgcolor="#ffffff">330</td>
      <td align="right"></td>
    </tr>
    <tr>
      <td>ANZ職缺廣告數</td>
      <td align="right"></td>
      <td align="right"></td>
      <td align="right"></td>
      <td align="right"></td>
    </tr>
    <tr>
      <td>時薪YoY</td>
      <td align="right"></td>
      <td align="right"></td>
      <td align="right"></td>
      <td align="right"></td>
    </tr>
    <tr>
      <td>預計離職</td>
      <td align="right"></td>
      <td align="right"></td>
      <td align="right"></td>
      <td align="right"></td>
    </tr>
    <tr>
      <td>失業預期</td>
      <td align="right"></td>
      <td align="right"></td>
      <td align="right"></td>
      <td align="right"></td>
    </tr>
    <tr>
      <th rowspan="3" align="center" valign="middle">通膨</th>
      <td>CPI</td>
      <td align="right"></td>
      <td align="right"></td>
      <td align="right"></td>
      <td align="right"></td>
    </tr>
    <tr>
      <td>Trim mean</td>
      <td align="right"></td>
      <td align="right"></td>
      <td align="right"></td>
      <td align="right"></td>
    </tr>
    <tr>
      <td>零售</td>
      <td align="right"></td>
      <td align="right"></td>
      <td align="right"></td>
      <td align="right"></td>
    </tr>
    <tr>
      <th rowspan="4" align="center" valign="middle">調查</th>
      <td>NAB企業調查 售價</td>
      <td align="right"></td>
      <td align="right"></td>
      <td align="right"></td>
      <td align="right"></td>
    </tr>
    <tr>
      <td>消費信心</td>
      <td align="right"></td>
      <td align="right"></td>
      <td align="right"></td>
      <td align="right"></td>
    </tr>
    <tr>
      <td>PMI製造業</td>
      <td align="right"></td>
      <td align="right"></td>
      <td align="right"></td>
      <td align="right"></td>
    </tr>
    <tr>
      <td>PMI服務業</td>
      <td align="right"></td>
      <td align="right"></td>
      <td align="right"></td>
      <td align="right"></td>
    </tr>
  </tbody>
</table>

<br>

<table>
  <thead>
    <tr>
      <th style="min-width:60px"></th>
      <th style="min-width:180px"></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="3" align="center" valign="middle">GDP</th>
      <td>GDP</td>
    </tr>
    <tr>
      <td>GDP 私人消費</td>
    </tr>
    <tr>
      <td>GDP投資</td>
    </tr>
  </tbody>
</table>

## 更新狀態

| 指標 | 狀態 | 新增 | 修訂 | 官方最新期 | 官方最新值 | 錯誤 |
|---|---|---:|---:|---|---:|---|
| 就業新增 | OK | 0 | 0 | 2026-07 | -15.826502660000187 |  |
| 失業率 | OK | 0 | 0 | 2026-07 | 4.46182469 |  |
| 就業不足率 | OK | 0 | 0 | 2026-07 | 6.3612462 |  |
| 勞動力未充分利用率 | OK | 0 | 0 | 2026-07 | 10.8230708 |  |
| Employment Ratio | OK | 0 | 0 | 2026-07 | 63.87044554 |  |
| 職缺 | OK | 0 | 0 | 2026-05 | 329.5 |  |
| ANZ職缺廣告 | ERROR | 0 | 0 |  |  | KeyError: 'auanzjobads' |
| 時薪YoY | ERROR | 0 | 0 |  |  | KeyError: 'auwageyoy' |
| 預計離職 | ERROR | 0 | 0 |  |  | KeyError: 'auexitleave' |
| 失業預期 | ERROR | 0 | 0 |  |  | KeyError: 'auunempexp' |
| CPI YoY | ERROR | 0 | 0 |  |  | KeyError: 'aucpi' |
| Trimmed Mean YoY | ERROR | 0 | 0 |  |  | KeyError: 'autrimmed' |
| 零售 | ERROR | 0 | 0 |  |  | KeyError: 'auretail' |
| NAB企業售價 | ERROR | 0 | 0 |  |  | KeyError: 'aunabprices' |
| 消費信心 | ERROR | 0 | 0 |  |  | KeyError: 'auconsconf' |
| 製造業PMI | ERROR | 0 | 0 |  |  | KeyError: 'aumanpmi' |
| 服務業PMI | ERROR | 0 | 0 |  |  | KeyError: 'auservpmi' |
| GDP YoY | ERROR | 0 | 0 |  |  | KeyError: 'augdpyoy' |
| GDP私人消費YoY | ERROR | 0 | 0 |  |  | KeyError: 'auconsumptionyoy' |
| GDP投資YoY | ERROR | 0 | 0 |  |  | KeyError: 'auinvestmentyoy' |
| 就業新增-全職 | OK | 138 | 0 | 2026-07 | 16.333391529999062 |  |
| 就業新增-兼職 | OK | 138 | 0 | 2026-07 | -32.15989419000016 |  |
| 勞參率 | OK | 139 | 0 | 2026-07 | 66.85332364 |  |
| 工時 | OK | 139 | 0 | 2026-07 | 23183.24700005 |  |
| Indeed職缺 | OK | 0 | 0 | 2026-08 | 149.45 |  |
| 私人企業時薪ex bonus | OK | 46 | 0 | 2026-Q2 | 3.2 |  |
| 政府時薪ex bonus | OK | 46 | 0 | 2026-Q2 | 3.3 |  |
| 家戶消費 Goods | OK | 91 | 0 | 2026-07 | 7.2 |  |
| 家戶消費 Services | OK | 91 | 0 | 2026-07 | 6.8 |  |
| 資本支出_住房 | OK | 29 | 0 | 2026-Q2 | 0.0 |  |
| 資本支出 設備廠房 | OK | 29 | 0 | 2026-Q2 | 0.0 |  |
| Building Approvals YoY | ERROR | 0 | 0 |  |  | RuntimeError: ABS dataflow attempts failed: BA: HTTP 404: Could not find Dataflow and/or DSD related with this data request |
| 房貸總還款 | OK | 70 | 0 | 2026-Q2 | 33442.0 |  |
| 房貸利息還款 | OK | 70 | 0 | 2026-Q2 | 21334.0 |  |
| 房租季增率 | OK | 46 | 0 | 2026-Q2 | 0.8 |  |
| Income | OK | 45 | 0 | 2026-Q1 | 570611.0 |  |
| 利息支出等 | OK | 45 | 0 | 2026-Q1 | 26372.0 |  |
| 所得稅 保險 | OK | 45 | 0 | 2026-Q1 | 26372.0 |  |
| DPI | OK | 45 | 0 | 2026-Q1 | 466688.0 |  |
| 支出 | OK | 45 | 0 | 2026-Q1 | 466688.0 |  |
| 固定資本消耗 | OK | 45 | 0 | 2026-Q1 | 26372.0 |  |
| Net Saving | OK | 45 | 0 | 2026-Q1 | 25490.0 |  |
| 房貸餘額(房屋持有) | ERROR | 0 | 0 |  |  | RuntimeError: No exact RBA series matched reference values; b18: HTTPError: 404 Client Error: Not Found for url: https://www.rba.gov.au/statistics/tables/csv/b18-data.csv; b19: HTTPError: 404 Client Error: Not Found for url: https://www.rba.gov.au/statistics/tables/csv/b19-data.csv; b29: HTTPError: 404 Client Error: Not Found for url: https://www.rba.gov.au/statistics/tables/csv/b29-data.csv; b30: HTTPError: 404 Client Error: Not Found for url: https://www.rba.gov.au/statistics/tables/csv/b30-data.csv |
| 房貸餘額(投資人) | ERROR | 0 | 0 |  |  | RuntimeError: No exact RBA series matched reference values; b18: HTTPError: 404 Client Error: Not Found for url: https://www.rba.gov.au/statistics/tables/csv/b18-data.csv; b19: HTTPError: 404 Client Error: Not Found for url: https://www.rba.gov.au/statistics/tables/csv/b19-data.csv; b29: HTTPError: 404 Client Error: Not Found for url: https://www.rba.gov.au/statistics/tables/csv/b29-data.csv; b30: HTTPError: 404 Client Error: Not Found for url: https://www.rba.gov.au/statistics/tables/csv/b30-data.csv |
| 房貸餘額(房屋持有) YoY | ERROR | 0 | 0 |  |  | RuntimeError: No exact RBA series matched reference values; b18: HTTPError: 404 Client Error: Not Found for url: https://www.rba.gov.au/statistics/tables/csv/b18-data.csv; b19: HTTPError: 404 Client Error: Not Found for url: https://www.rba.gov.au/statistics/tables/csv/b19-data.csv; b29: HTTPError: 404 Client Error: Not Found for url: https://www.rba.gov.au/statistics/tables/csv/b29-data.csv; b30: HTTPError: 404 Client Error: Not Found for url: https://www.rba.gov.au/statistics/tables/csv/b30-data.csv |
| 房貸餘額(投資人) YoY | ERROR | 0 | 0 |  |  | RuntimeError: No exact RBA series matched reference values; b18: HTTPError: 404 Client Error: Not Found for url: https://www.rba.gov.au/statistics/tables/csv/b18-data.csv; b19: HTTPError: 404 Client Error: Not Found for url: https://www.rba.gov.au/statistics/tables/csv/b19-data.csv; b29: HTTPError: 404 Client Error: Not Found for url: https://www.rba.gov.au/statistics/tables/csv/b29-data.csv; b30: HTTPError: 404 Client Error: Not Found for url: https://www.rba.gov.au/statistics/tables/csv/b30-data.csv |
| Disposable Income | OK | 45 | 0 | 2026-Q1 | 466688.0 |  |
