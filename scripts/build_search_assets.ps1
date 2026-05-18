[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$repoRoot = Split-Path -Parent $PSScriptRoot
$baseUrl = "https://andrewshih1210.github.io/my-blog"

function Convert-ToPublicUrl([string]$fullPath) {
  $rootWithSlash = $repoRoot.TrimEnd('\') + '\'
  $relative = $fullPath.Substring($rootWithSlash.Length)
  $segments = $relative -split '[\\/]'
  $encoded = $segments | ForEach-Object { [System.Uri]::EscapeDataString($_) }
  return "$baseUrl/" + ($encoded -join "/")
}

$htmlFiles = Get-ChildItem -Path $repoRoot -Recurse -Filter *.html |
  Where-Object { $_.FullName -notmatch '\\\.git\\' } |
  Sort-Object FullName

$urlEntries = foreach ($file in $htmlFiles) {
  [PSCustomObject]@{
    Url = Convert-ToPublicUrl $file.FullName
    LastMod = $file.LastWriteTime.ToString("yyyy-MM-dd")
  }
}

$sitemapBody = ($urlEntries | ForEach-Object {
@"
  <url>
    <loc>$($_.Url)</loc>
    <lastmod>$($_.LastMod)</lastmod>
  </url>
"@
}) -join "`n"

$sitemapXml = @"
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
$sitemapBody
</urlset>
"@

[System.IO.File]::WriteAllText((Join-Path $repoRoot "sitemap.xml"), $sitemapXml, [System.Text.UTF8Encoding]::new($false))

$robotsTxt = @"
User-agent: *
Allow: /

Sitemap: $baseUrl/sitemap.xml
"@

[System.IO.File]::WriteAllText((Join-Path $repoRoot "robots.txt"), $robotsTxt, [System.Text.UTF8Encoding]::new($false))

Write-Host "Generated sitemap.xml and robots.txt for $($urlEntries.Count) HTML pages."
