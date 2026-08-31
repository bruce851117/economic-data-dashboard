# 澳洲總體資料 Debug 表

更新時間：2026-08-31T07:36:33.763287+00:00

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
| 就業不足率 | OK | 0 | 139 | 2026-07 | 6.3612462 |  |
| 勞動力未充分利用率 | OK | 0 | 139 | 2026-07 | 10.8230708 |  |
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
