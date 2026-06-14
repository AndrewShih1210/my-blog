$ErrorActionPreference = "Stop"

$python = "C:\Users\sweet\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
$script = Join-Path $PSScriptRoot "build_research_pages.py"

if (-not (Test-Path -LiteralPath $python)) {
  throw "找不到 Python runtime：$python"
}

& $python $script

if ($LASTEXITCODE -ne 0) {
  throw "build_research_pages.py 執行失敗，exit code: $LASTEXITCODE"
}

Write-Host "research pages regenerated from metadata.json and article.md files"
