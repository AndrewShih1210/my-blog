$ErrorActionPreference = "Stop"
$projectDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host ""
Write-Host "Motion Studio is starting..." -ForegroundColor Cyan
Write-Host "Open: http://127.0.0.1:8765" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server." -ForegroundColor DarkGray
Write-Host ""

Push-Location $projectDir
try {
    node ".\server.js"
}
finally {
    Pop-Location
}
