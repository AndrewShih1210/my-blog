這個資料夾保存 `linebot-course-site` 的 HTML 模板來源。

使用方式：

1. 更新模板後，執行：
   `C:\Users\sweet\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe scripts/build_linebot_course_site.py`
2. 如果先直接修改了 `linebot-course-site` 內的 HTML，想把目前版本回存成模板，執行：
   `C:\Users\sweet\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe scripts/build_linebot_course_site.py --snapshot`

注意事項：

- 模板應維持 UTF-8 無 BOM。
- `linebot-course-site` 為輸出區，`scripts/linebot-course-site-templates` 為來源區。
