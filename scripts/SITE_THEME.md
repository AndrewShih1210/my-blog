# Shared site theme / 全站共用主題

The published content pages use `assets/site-shell.css` and
`assets/site-shell.js`. Chinese and English pages share the same navigation,
mobile menu, focus treatment, typography and blue/white theme.

After running any page generator, run:

```sh
python scripts/unify_site_shell.py
python scripts/build_public_summary.py --check
```

`unify_site_shell.py` requires `beautifulsoup4`. It preserves body content,
metadata and JSON-LD, builds relative links for nested pages, and keeps the
original page/course navigation in a separate menu. It can be rerun safely.
Do not manually edit the generated global navigation in individual HTML files.

The animation editor (`veo-crator/index.html`), downloadable local source,
Google verification files and generator templates are deliberately excluded.
The editor has application controls, not a content-site navigation bar.

內容頁共用同一份樣式與選單。新增或重建教材後，請執行上述同步指令，
避免產生器恢復舊版導覽。章節連結保留在「本頁／教材導覽」，
動態圖室編輯器的操作列與本機下載版不套用內容網站選單。
