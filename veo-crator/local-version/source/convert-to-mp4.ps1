param(
    [Parameter(Mandatory = $false)]
    [string]$InputWebM,

    [Parameter(Mandatory = $false)]
    [string]$OutputMp4
)

$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($InputWebM)) {
    $InputWebM = Read-Host "Enter the full path to the WebM file"
}

$resolvedInput = (Resolve-Path -LiteralPath $InputWebM).Path
if ([string]::IsNullOrWhiteSpace($OutputMp4)) {
    $OutputMp4 = [System.IO.Path]::ChangeExtension($resolvedInput, ".mp4")
}

$ffmpegCommand = Get-Command "ffmpeg.exe" -ErrorAction SilentlyContinue

if ($ffmpegCommand) {
    $ffmpeg = $ffmpegCommand.Source
}
else {
    throw "ffmpeg.exe was not found. Install ffmpeg or add ffmpeg.exe to PATH."
}

Write-Host "Converting WebM to MP4..." -ForegroundColor Cyan
& $ffmpeg -y -i $resolvedInput -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart $OutputMp4

if ($LASTEXITCODE -ne 0) {
    throw "ffmpeg conversion failed with exit code $LASTEXITCODE"
}

$outputResolved = (Resolve-Path -LiteralPath $OutputMp4).Path
Write-Host "Completed: $outputResolved" -ForegroundColor Green
