[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function U([int[]]$codes) {
  return (-join ($codes | ForEach-Object { [char]$_ }))
}

$repoRoot = Split-Path -Parent $PSScriptRoot
$sourceDir = [System.IO.Path]::GetFullPath((Join-Path $repoRoot "..\classfile\My_Certificate"))
$outputDir = Join-Path $repoRoot "certificates-site"
$itemsDir = Join-Path $outputDir "items"
$dataPath = Join-Path $outputDir "data.js"

if (-not (Test-Path -LiteralPath $sourceDir)) {
  throw "Source directory not found: $sourceDir"
}

New-Item -ItemType Directory -Force -Path $outputDir | Out-Null
New-Item -ItemType Directory -Force -Path $itemsDir | Out-Null
Get-ChildItem -LiteralPath $itemsDir -File -Force | Remove-Item -Force

$lb = [char]0x3010
$rb = [char]0x3011

$prefixGoogle = "$lb" + "Google" + "$rb"
$prefixLicense = "$lb" + (U @(0x8B49, 0x7167)) + "$rb"
$prefixTraining = "$lb" + (U @(0x7814, 0x7FD2, 0x8B49, 0x660E)) + "$rb"
$prefixPresentation = "$lb" + (U @(0x767C, 0x8868)) + "$rb"
$prefixAppointment = "$lb" + (U @(0x8058, 0x66F8)) + "$rb"
$prefixAppreciation = "$lb" + (U @(0x611F, 0x8B1D, 0x72C0)) + "$rb"
$prefixPatent = "$lb" + (U @(0x5C08, 0x5229, 0x8B49, 0x66F8)) + "$rb"
$prefixStatus = "$lb" + (U @(0x8B49, 0x660E)) + "$rb"

$ntcuZh = U @(0x570B, 0x7ACB, 0x81FA, 0x4E2D, 0x6559, 0x80B2, 0x5927, 0x5B78)
$ntcuZhAlt = U @(0x570B, 0x7ACB, 0x53F0, 0x4E2D, 0x6559, 0x80B2, 0x5927, 0x5B78)
$ntcuShortZh = U @(0x81FA, 0x4E2D, 0x6559, 0x80B2, 0x5927, 0x5B78)
$ntcuShortZhAlt = U @(0x53F0, 0x4E2D, 0x6559, 0x80B2, 0x5927, 0x5B78)
$tunghaiZh = U @(0x6771, 0x6D77, 0x5927, 0x5B78)
$yudaZh = U @(0x80B2, 0x9054, 0x79D1, 0x6280, 0x5927, 0x5B78)
$shinMinZh = U @(0x65B0, 0x6C11, 0x9AD8, 0x4E2D)
$daMingZh = U @(0x5927, 0x660E, 0x9AD8, 0x4E2D)
$csmuZh = U @(0x4E2D, 0x5C71, 0x91AB, 0x5B78, 0x5927, 0x5B78)
$chongLunZh = U @(0x5D07, 0x502B, 0x570B, 0x4E2D)
$onlineZh = U @(0x7DDA, 0x4E0A, 0x5206, 0x4EAB)

function Get-CategoryKey([string]$name) {
  if ($name.StartsWith($prefixGoogle)) { return "google" }
  if ($name.StartsWith($prefixLicense)) { return "license" }
  if ($name.StartsWith($prefixTraining)) { return "training" }
  if ($name.StartsWith($prefixPresentation)) { return "presentation" }
  if ($name.StartsWith($prefixAppointment)) { return "appointment" }
  if ($name.StartsWith($prefixAppreciation)) { return "appreciation" }
  if ($name.StartsWith($prefixPatent)) { return "patent" }
  if ($name.StartsWith($prefixStatus)) { return "status" }
  return "status"
}

function Clean-Title([string]$name) {
  $base = [System.IO.Path]::GetFileNameWithoutExtension($name)
  foreach ($prefix in @($prefixGoogle, $prefixLicense, $prefixTraining, $prefixPresentation, $prefixAppointment, $prefixAppreciation, $prefixPatent, $prefixStatus)) {
    if ($base.StartsWith($prefix)) {
      $base = $base.Substring($prefix.Length)
    }
  }
  $base = $base -replace '_1$', ''
  $base = $base -replace '\.PDF$', ''
  $base = $base -replace '\s+', ' '
  return $base.Trim()
}

function Get-Issuer([string]$name, [string]$categoryKey) {
  if ($categoryKey -eq "google") { return @{ zh = "Google / Google Cloud"; en = "Google / Google Cloud" } }
  if ($categoryKey -eq "appointment") { return @{ zh = $ntcuZh; en = "National Taichung University of Education" } }
  if ($categoryKey -eq "patent") { return @{ zh = "智慧財產局"; en = "Intellectual Property Authority" } }
  if ($categoryKey -eq "status") { return @{ zh = "學術身分文件"; en = "Academic Documentation" } }

  $ntcuPattern = [regex]::Escape($ntcuZh) + '|' + [regex]::Escape($ntcuZhAlt) + '|' + [regex]::Escape($ntcuShortZh) + '|' + [regex]::Escape($ntcuShortZhAlt) + '|NTCU'
  if ($name -match $ntcuPattern) { return @{ zh = $ntcuShortZh; en = "National Taichung University of Education" } }
  if ($name -match [regex]::Escape($tunghaiZh)) { return @{ zh = $tunghaiZh; en = "Tunghai University" } }
  if ($name -match [regex]::Escape($yudaZh)) { return @{ zh = $yudaZh; en = "Yuda University of Science and Technology" } }
  if ($name -match [regex]::Escape($shinMinZh)) { return @{ zh = $shinMinZh; en = "Shin Min High School" } }
  if ($name -match [regex]::Escape($daMingZh)) { return @{ zh = $daMingZh; en = "Da Ming High School" } }
  if ($name -match [regex]::Escape($csmuZh)) { return @{ zh = $csmuZh; en = "Chung Shan Medical University" } }
  if ($name -match [regex]::Escape($chongLunZh)) { return @{ zh = $chongLunZh; en = "Chong Lun Junior High School" } }
  if ($name -match [regex]::Escape($onlineZh)) { return @{ zh = $onlineZh; en = "Online Sharing" } }
  if ($name -match 'Oracle') { return @{ zh = "Oracle"; en = "Oracle" } }
  if ($name -match 'Microsoft') { return @{ zh = "Microsoft"; en = "Microsoft" } }
  if ($name -match 'Google') { return @{ zh = "Google"; en = "Google" } }
  if ($name -match 'TaiwanCALL') { return @{ zh = "TaiwanCALL"; en = "TaiwanCALL" } }
  if ($name -match 'ICEET') { return @{ zh = "ICEET"; en = "ICEET" } }
  if ($name -match 'TWELF') { return @{ zh = "TWELF"; en = "TWELF" } }
  if ($name -match 'TANET') { return @{ zh = "TANET"; en = "TANET" } }
  if ($name -match 'Education Sciences') { return @{ zh = "Education Sciences"; en = "Education Sciences" } }

  return @{ zh = "相關單位"; en = "Relevant issuing or hosting body" }
}

function Get-EnglishTitle([string]$titleZh, [string]$categoryKey) {
  switch ($categoryKey) {
    "patent" { return "Patent Record: $titleZh" }
    "appointment" { return "Appointment Letter: $titleZh" }
    "appreciation" { return "Letter of Appreciation: $titleZh" }
    "training" { return "Training Certificate: $titleZh" }
    "presentation" { return "Presentation Record: $titleZh" }
    "lecture" { return "Lecture Record: $titleZh" }
    "license" { return "Certification: $titleZh" }
    "status" { return "Academic Proof: $titleZh" }
    default { return $titleZh }
  }
}

function Get-Year([string]$title, [string]$fileName) {
  foreach ($candidate in @($title, $fileName)) {
    if ($candidate -match '(20\d{2})') { return $Matches[1] }
    if ($candidate -match '^(1\d{2})') { return "$($Matches[1])" }
  }
  return ""
}

function Normalize-LectureTitle([string]$titleZh) {
  return $titleZh
}

function Get-EffectiveCategoryKey([string]$fileName, [string]$titleZh, [string]$categoryKey) {
  if ($titleZh -like '2024-11-19*') { return 'lecture' }
  if ($titleZh -like '2024-11-21*') { return 'lecture' }
  if ($titleZh -like '2025-09-04*') { return 'lecture' }
  if ($titleZh -like '2025-09-12*') { return 'lecture' }
  if ($titleZh -like '2026-02-11*') { return 'lecture' }
  if ($titleZh -like '2026-04-12*') { return 'lecture' }
  if ($titleZh -like '2026-04-16*') { return 'lecture' }
  if ($titleZh -like '2026-04-29*') { return 'lecture' }
  if ($titleZh -like '2026-05-22*') { return 'lecture' }
  if ($titleZh -like '2026-06-01*') { return 'lecture' }
  if ($titleZh -like '2026-06-02*') { return 'lecture' }
  if ($titleZh -like '2026-07-13*') { return 'lecture' }
  return $categoryKey
}

function Get-Overrides([string]$fileName) {
  $appreciationDaming = [string]::Concat($prefixAppreciation, (U @(0x904B,0x7528,0x0041,0x0049,0x8F14,0x52A9,0x5B78,0x7FD2,0x8B1B,0x5EA7,0x8B1B,0x5E2B)), '.jpg')
  $appreciationYuda = [string]::Concat($prefixAppreciation, $yudaZh, '.jpg')
  $appreciationCsmu = [string]::Concat($prefixAppreciation, 'AI', (U @(0x5DE5,0x5177,0x61C9,0x7528)), ',', (U @(0x95DC,0x65BC,0x91AB,0x7642,0x8207,0x653E,0x5C04,0x79D1,0x8F14,0x52A9,0x5DE5,0x4F5C)), ',Gemini ', (U @(0x96F2,0x7AEF,0x6574,0x5408,0x8207,0x63D0,0x793A,0x8A5E,0x5DE5,0x7A0B)), ' (1).jpg')

  if ($fileName -eq $appreciationDaming) {
    return @{
      titleZh = '114 12 07 大明高中 如何運用AI輔助學習 講座講師'
      titleEn = 'Letter of Appreciation: December 7, 2025, Da Ming High School, How to Use AI to Support Learning'
      issuerZh = $daMingZh
      issuerEn = 'Da Ming High School'
      year = '2025'
      categoryKey = 'appreciation'
    }
  }

  if ($fileName -eq $appreciationYuda) {
    return @{
      titleZh = [string]::Concat('2026-04-16 ', $yudaZh, ' ', $lb, (U @(0x8B93,0x0041,0x0049,0x6210,0x70BA,0x795E,0x968A,0x53CB)), $rb, (U @(0x6559,0x5B78,0x73FE,0x5834,0x7684,0x61C9,0x7528,0x8207,0x5275,0x65B0,0x5BE6,0x9304)))
      titleEn = 'Lecture Record: 2026-04-16 Yuda University of Science and Technology - Let AI Become Your Teammate'
      issuerZh = $yudaZh
      issuerEn = 'Yuda University of Science and Technology'
      year = '2026'
      categoryKey = 'lecture'
    }
  }

  if ($fileName -eq $appreciationCsmu) {
    return @{
      titleZh = [string]::Concat('2026-02-11 ', $csmuZh, ' ', (U @(0x95DC,0x65BC,0x91AB,0x7642,0x8207,0x653E,0x5C04,0x79D1,0x8F14,0x52A9,0x5DE5,0x4F5C)), ',Gemini ', (U @(0x96F2,0x7AEF,0x6574,0x5408,0x8207,0x63D0,0x793A,0x8A5E,0x5DE5,0x7A0B)))
      titleEn = 'Lecture Record: 2026-02-11 Chung Shan Medical University - Gemini Cloud Integration and Prompt Engineering for Medical and Radiology Support Work'
      issuerZh = $csmuZh
      issuerEn = 'Chung Shan Medical University'
      year = '2026'
      categoryKey = 'lecture'
    }
  }

  return $null
}

$files = Get-ChildItem -LiteralPath $sourceDir -File | Sort-Object Name
$items = @()
$index = 1

foreach ($file in $files) {
  $categoryKey = Get-CategoryKey $file.Name
  $titleZh = Clean-Title $file.Name
  $titleEn = Get-EnglishTitle $titleZh $categoryKey
  $issuer = Get-Issuer $file.Name $categoryKey
  $year = Get-Year $titleZh $file.Name
  $override = Get-Overrides $file.Name

  if ($null -ne $override) {
    if ($override.categoryKey) { $categoryKey = $override.categoryKey }
    if ($override.titleZh) { $titleZh = $override.titleZh }
    if ($override.titleEn) { $titleEn = $override.titleEn }
    if ($override.issuerZh -or $override.issuerEn) {
      $issuer = @{ zh = $override.issuerZh; en = $override.issuerEn }
    }
    if ($override.year) { $year = $override.year }
  }

  $categoryKey = Get-EffectiveCategoryKey $file.Name $titleZh $categoryKey
  if ($categoryKey -eq 'lecture') {
    $titleZh = Normalize-LectureTitle $titleZh
  }
  $titleEn = Get-EnglishTitle $titleZh $categoryKey

  $slug = ('item-{0:d3}{1}' -f $index, $file.Extension.ToLowerInvariant())
  Copy-Item -LiteralPath $file.FullName -Destination (Join-Path $itemsDir $slug) -Force

  $items += [ordered]@{
    id = ('cert-{0:d3}' -f $index)
    sort = $index
    image = "./items/$slug"
    originalFile = $file.Name
    titleZh = $titleZh
    titleEn = $titleEn
    categoryKey = $categoryKey
    issuerZh = $issuer.zh
    issuerEn = $issuer.en
    year = $year
  }

  $index++
}

$json = $items | ConvertTo-Json -Depth 4
$dataJs = @"
window.CERTIFICATE_ITEMS = $json;
"@
[System.IO.File]::WriteAllText($dataPath, $dataJs, [System.Text.UTF8Encoding]::new($false))

Write-Host "Built certificate site data for $($items.Count) items."
