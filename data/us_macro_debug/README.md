# Conference Board 抓取診斷

執行程式後，本資料夾會保存：

- `cb_consumer_confidence_raw.html`：GitHub Actions 實際收到的原始回應。
- `cb_consumer_confidence_http.json`：CB的HTTP、頁面特徵與目前解析結果。
- `nfib_jobs_report_raw.html`：NFIB Jobs Report原始回應。
- `nfib_jobs_report_http.json`：NFIB請求方式、參考月份與Hiring Plan解析結果。

注意：Git 不會追蹤空資料夾；GitHub Actions 必須將 `data/us_macro_debug/` 加入 commit。
