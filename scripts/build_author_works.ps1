$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$python = "C:\Users\sweet\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
$script = Join-Path $PSScriptRoot "build_author_works.py"

if (-not (Test-Path -LiteralPath $python)) {
  throw "找不到 Python runtime：$python"
}

& $python $script

if ($LASTEXITCODE -ne 0) {
  throw "build_author_works.py 執行失敗，exit code: $LASTEXITCODE"
}

Write-Host "author-works pages regenerated from works-data.json"
