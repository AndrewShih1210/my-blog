$ErrorActionPreference = 'Stop'

$repo = 'C:\Users\sweet\OneDrive\Desktop\pd\REFERENCES_GITHUB'

function Read-Utf8([string]$Path) {
  [System.IO.File]::ReadAllText($Path, [System.Text.Encoding]::UTF8)
}

function Write-Utf8([string]$Path, [string]$Text) {
  [System.IO.File]::WriteAllText($Path, $Text, [System.Text.Encoding]::UTF8)
}

function Ensure-After([string]$Text, [string]$Anchor, [string]$Insertion) {
  if ($Text.Contains($Insertion)) { return $Text }
  return $Text.Replace($Anchor, $Anchor + "`r`n        " + $Insertion)
}

function Escape-Html([string]$Text) {
  $Text.Replace('&', '&amp;').Replace('<', '&lt;').Replace('>', '&gt;')
}

function Convert-Inline([string]$Text) {
  $Text = Escape-Html $Text
  $Text = [regex]::Replace($Text, '\*\*(.+?)\*\*', '<strong>$1</strong>')
  $Text = [regex]::Replace($Text, '\[(.*?)\]\((.*?)\)', '<a href="$2">$1</a>')
  return $Text
}

function Convert-Markdown([string]$Markdown) {
  $lines = $Markdown -split "`r?`n"
  $parts = New-Object System.Collections.Generic.List[string]
  $inList = $false

  foreach ($raw in $lines) {
    $line = $raw.TrimEnd()
    if ([string]::IsNullOrWhiteSpace($line)) {
      if ($inList) {
        $parts.Add('</ul>')
        $inList = $false
      }
      continue
    }

    if ($line.StartsWith('# ')) {
      if ($inList) { $parts.Add('</ul>'); $inList = $false }
      $parts.Add('<h1>' + (Convert-Inline $line.Substring(2)) + '</h1>')
      continue
    }
    if ($line.StartsWith('## ')) {
      if ($inList) { $parts.Add('</ul>'); $inList = $false }
      $parts.Add('<h2>' + (Convert-Inline $line.Substring(3)) + '</h2>')
      continue
    }
    if ($line.StartsWith('### ')) {
      if ($inList) { $parts.Add('</ul>'); $inList = $false }
      $parts.Add('<h3>' + (Convert-Inline $line.Substring(4)) + '</h3>')
      continue
    }

    $img = [regex]::Match($line, '^!\[(.*?)\]\((.*?)\)$')
    if ($img.Success) {
      if ($inList) { $parts.Add('</ul>'); $inList = $false }
      $parts.Add('<figure><img src="' + $img.Groups[2].Value + '" alt="' + $img.Groups[1].Value + '" /></figure>')
      continue
    }

    if ($line.StartsWith('- ') -or $line.StartsWith('* ')) {
      if (-not $inList) {
        $parts.Add('<ul>')
        $inList = $true
      }
      $parts.Add('<li>' + (Convert-Inline $line.Substring(2)) + '</li>')
      continue
    }

    if ($inList) {
      $parts.Add('</ul>')
      $inList = $false
    }

    $parts.Add('<p>' + (Convert-Inline $line) + '</p>')
  }

  if ($inList) { $parts.Add('</ul>') }
  return ($parts -join "`r`n")
}

function Write-WrappedPage(
  [string]$InputPath,
  [string]$OutputPath,
  [string]$Lang,
  [string]$TitleSuffix,
  [string]$HomeHref,
  [string]$WorksHref,
  [string]$MapHref
) {
  $md = Read-Utf8 $InputPath
  $titleMatch = [regex]::Match($md, '^#\s+(.+)$', [System.Text.RegularExpressions.RegexOptions]::Multiline)
  $title = if ($titleMatch.Success) { $titleMatch.Groups[1].Value } else { [System.IO.Path]::GetFileNameWithoutExtension($InputPath) }
  $body = Convert-Markdown $md

  $html = @"
<!doctype html>
<html lang="$Lang">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>$title | $TitleSuffix</title>
  <style>
    :root { --paper:#fffdf8; --ink:#203231; --muted:#5c6d69; --line:#d9d0c2; --accent:#0f766e; }
    * { box-sizing:border-box; }
    body { margin:0; background:linear-gradient(180deg,#efe7da 0%,#f7f3ec 42%,#f5f1e8 100%); color:var(--ink); font-family:"Noto Sans TC","Segoe UI",sans-serif; line-height:1.8; }
    a { color:var(--accent); }
    .wrap { width:min(920px, calc(100vw - 32px)); margin:0 auto; }
    header { padding:24px 0 8px; }
    nav { display:flex; flex-wrap:wrap; gap:12px; }
    nav a { text-decoration:none; padding:9px 14px; border-radius:999px; background:rgba(255,255,255,.76); border:1px solid rgba(32,50,49,.08); color:var(--ink); }
    main { background:var(--paper); border:1px solid var(--line); border-radius:28px; padding:32px; margin:12px auto 40px; box-shadow:0 18px 40px rgba(32,50,49,.08); }
    h1 { font-size:clamp(30px, 4vw, 48px); line-height:1.15; margin:0 0 18px; }
    h2 { margin:28px 0 12px; font-size:28px; }
    h3 { margin:22px 0 8px; font-size:21px; }
    p { margin:0 0 14px; }
    ul { margin:0 0 16px 20px; }
    li { margin-bottom:8px; }
    figure { margin:24px 0; }
    img { max-width:100%; display:block; border-radius:18px; border:1px solid var(--line); background:#fff; }
  </style>
</head>
<body>
  <header class="wrap">
    <nav>
      <a href="$HomeHref">Home</a>
      <a href="$WorksHref">Works</a>
      <a href="$MapHref">Sitemap</a>
    </nav>
  </header>
  <main class="wrap">
    $body
  </main>
</body>
</html>
"@

  Write-Utf8 $OutputPath $html
}

# Root homepages
$rootZh = Join-Path $repo 'index.html'
$text = Read-Utf8 $rootZh
$text = $text.Replace('href="https://github.com/AndrewShih1210/my-blog">研究成果</a>', 'href="./author-works/index.html">研究成果</a>')
$text = $text.Replace('href="https://github.com/AndrewShih1210/my-blog">瀏覽研究成果</a>', 'href="./author-works/index.html">瀏覽研究成果</a>')
$text = Ensure-After $text '<a href="./author-works/index.html">著作專區</a>' '<a href="./sitemap.html">Sitemap</a>'
Write-Utf8 $rootZh $text

$rootEn = Join-Path $repo 'index_en.html'
$text = Read-Utf8 $rootEn
$text = $text.Replace('href="https://github.com/AndrewShih1210/my-blog">Research</a>', 'href="./author-works/index_en.html">Research</a>')
$text = $text.Replace('href="https://github.com/AndrewShih1210/my-blog">Browse Research Outputs</a>', 'href="./author-works/index_en.html">Browse Research Outputs</a>')
$text = Ensure-After $text '<a href="./author-works/index_en.html">Works</a>' '<a href="./sitemap_en.html">Sitemap</a>'
Write-Utf8 $rootEn $text

# Course guide pages from README
$courseReadme = Join-Path $repo 'ai-course-site\README.md'
Write-WrappedPage -InputPath $courseReadme -OutputPath (Join-Path $repo 'ai-course-site\guide.html') -Lang 'zh-Hant' -TitleSuffix 'Course Guide' -HomeHref '../index.html' -WorksHref '../author-works/index.html' -MapHref '../sitemap.html'
Write-WrappedPage -InputPath $courseReadme -OutputPath (Join-Path $repo 'ai-course-site\guide_en.html') -Lang 'en' -TitleSuffix 'Course Guide' -HomeHref '../index_en.html' -WorksHref '../author-works/index_en.html' -MapHref '../sitemap_en.html'

# Course main pages
foreach ($file in @('index.html', 'teaching-plan.html', 'projects.html')) {
  $path = Join-Path $repo ('ai-course-site\' + $file)
  $text = Read-Utf8 $path
  $text = $text.Replace('href="README.md"', 'href="guide.html"')
  if ($file -eq 'projects.html') {
    $text = Ensure-After $text '<a href="teaching-plan.html">教學計畫</a>' '<a href="../index.html">Home</a>'
  } else {
    $text = Ensure-After $text '<a href="projects.html">專題任務</a>' '<a href="../index.html">Home</a>'
  }
  $text = Ensure-After $text '<a href="../index.html">Home</a>' '<a href="../sitemap.html">Sitemap</a>'
  Write-Utf8 $path $text
}

foreach ($file in @('index_en.html', 'teaching-plan_en.html', 'projects_en.html')) {
  $path = Join-Path $repo ('ai-course-site\' + $file)
  $text = Read-Utf8 $path
  $text = $text.Replace('href="README.md"', 'href="guide_en.html"')
  if ($file -eq 'projects_en.html') {
    $text = Ensure-After $text '<a href="teaching-plan_en.html">Teaching Plan</a>' '<a href="../index_en.html">Home</a>'
  } else {
    $text = Ensure-After $text '<a href="projects_en.html">Projects</a>' '<a href="../index_en.html">Home</a>'
  }
  $text = Ensure-After $text '<a href="../index_en.html">Home</a>' '<a href="../sitemap_en.html">Sitemap</a>'
  Write-Utf8 $path $text
}

Get-ChildItem -LiteralPath (Join-Path $repo 'ai-course-site\units') -Filter 'unit*.html' | ForEach-Object {
  $text = Read-Utf8 $_.FullName
  if ($_.Name -like '*_en.html') {
    $text = Ensure-After $text '<a href="../projects_en.html">Projects</a>' '<a href="../../index_en.html">Home</a>'
    $text = Ensure-After $text '<a href="../../index_en.html">Home</a>' '<a href="../../sitemap_en.html">Sitemap</a>'
  } else {
    $text = Ensure-After $text '<a href="../projects.html">專題任務</a>' '<a href="../../index.html">Home</a>'
    $text = Ensure-After $text '<a href="../../index.html">Home</a>' '<a href="../../sitemap.html">Sitemap</a>'
  }
  Write-Utf8 $_.FullName $text
}

# Author works pages
foreach ($file in @('index.html', 'index_en.html')) {
  $path = Join-Path $repo ('author-works\' + $file)
  $text = Read-Utf8 $path
  $text = [regex]::Replace($text, '/article\.md"', '/index.html"')
  $text = [regex]::Replace($text, '/article_en\.md"', '/index_en.html"')
  if ($file -eq 'index.html') {
    $text = Ensure-After $text '<a href="../ai-course-site/index.html">AI 教材</a>' '<a href="../sitemap.html">Sitemap</a>'
  } else {
    $text = Ensure-After $text '<a href="../ai-course-site/index_en.html">AI Course Site</a>' '<a href="../sitemap_en.html">Sitemap</a>'
  }
  Write-Utf8 $path $text
}

# Markdown links inside repository docs
$mdFiles = @(
  (Join-Path $repo 'README.md'),
  (Join-Path $repo 'README_en.md')
) + (Get-ChildItem -LiteralPath $repo -Recurse -Filter 'README*.md' | Select-Object -ExpandProperty FullName)

foreach ($path in ($mdFiles | Select-Object -Unique)) {
  $text = Read-Utf8 $path
  $text = $text.Replace('./article.md)', './index.html)')
  $text = $text.Replace('./article_en.md)', './index_en.html)')
  $text = $text.Replace('./article.md"', './index.html"')
  $text = $text.Replace('./article_en.md"', './index_en.html"')
  Write-Utf8 $path $text
}

# Research article pages
$dirs = Get-ChildItem -LiteralPath $repo -Directory | Where-Object { $_.Name -match '^[0-9]{2}-' }
foreach ($dir in $dirs) {
  $article = Join-Path $dir.FullName 'article.md'
  if (Test-Path -LiteralPath $article) {
    Write-WrappedPage -InputPath $article -OutputPath (Join-Path $dir.FullName 'index.html') -Lang 'zh-Hant' -TitleSuffix 'Research Page' -HomeHref '../index.html' -WorksHref '../author-works/index.html' -MapHref '../sitemap.html'
  }
  $articleEn = Join-Path $dir.FullName 'article_en.md'
  if (Test-Path -LiteralPath $articleEn) {
    Write-WrappedPage -InputPath $articleEn -OutputPath (Join-Path $dir.FullName 'index_en.html') -Lang 'en' -TitleSuffix 'Research Page' -HomeHref '../index_en.html' -WorksHref '../author-works/index_en.html' -MapHref '../sitemap_en.html'
  }
}

Write-Output 'repaired'
