$ErrorActionPreference = 'Stop'

$repo = 'C:\Users\sweet\OneDrive\Desktop\pd\REFERENCES_GITHUB'

function Read-Text([string]$Path) {
  return [System.IO.File]::ReadAllText($Path, [System.Text.Encoding]::UTF8)
}

function Write-Text([string]$Path, [string]$Text) {
  [System.IO.File]::WriteAllText($Path, $Text, [System.Text.Encoding]::UTF8)
}

function Ensure-After([string]$Text, [string]$Anchor, [string]$Insertion) {
  if ($Text.Contains($Insertion)) { return $Text }
  return $Text.Replace($Anchor, $Anchor + "`r`n        " + $Insertion)
}

function Escape-Html([string]$Text) {
  return $Text.Replace('&', '&amp;').Replace('<', '&lt;').Replace('>', '&gt;')
}

function Convert-InlineMarkdown([string]$Text) {
  $Text = Escape-Html $Text
  $Text = [regex]::Replace($Text, '\*\*(.+?)\*\*', '<strong>$1</strong>')
  $Text = [regex]::Replace($Text, '\[(.*?)\]\((.*?)\)', '<a href="$2">$1</a>')
  return $Text
}

function Convert-MarkdownToHtml([string]$Markdown) {
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
      $parts.Add('<h1>' + (Convert-InlineMarkdown $line.Substring(2)) + '</h1>')
      continue
    }
    if ($line.StartsWith('## ')) {
      if ($inList) { $parts.Add('</ul>'); $inList = $false }
      $parts.Add('<h2>' + (Convert-InlineMarkdown $line.Substring(3)) + '</h2>')
      continue
    }
    if ($line.StartsWith('### ')) {
      if ($inList) { $parts.Add('</ul>'); $inList = $false }
      $parts.Add('<h3>' + (Convert-InlineMarkdown $line.Substring(4)) + '</h3>')
      continue
    }

    $match = [regex]::Match($line, '^!\[(.*?)\]\((.*?)\)$')
    if ($match.Success) {
      if ($inList) { $parts.Add('</ul>'); $inList = $false }
      $parts.Add('<figure><img src="' + $match.Groups[2].Value + '" alt="' + $match.Groups[1].Value + '" /></figure>')
      continue
    }

    if ($line.StartsWith('- ') -or $line.StartsWith('* ')) {
      if (-not $inList) {
        $parts.Add('<ul>')
        $inList = $true
      }
      $parts.Add('<li>' + (Convert-InlineMarkdown $line.Substring(2)) + '</li>')
      continue
    }

    if ($inList) {
      $parts.Add('</ul>')
      $inList = $false
    }

    $parts.Add('<p>' + (Convert-InlineMarkdown $line) + '</p>')
  }

  if ($inList) { $parts.Add('</ul>') }
  return ($parts -join "`r`n")
}

# Root homepages
$rootZh = Join-Path $repo 'index.html'
$text = Read-Text $rootZh
$text = $text.Replace('href="https://github.com/AndrewShih1210/my-blog">研究成果</a>', 'href="./author-works/index.html">研究成果</a>')
$text = $text.Replace('href="https://github.com/AndrewShih1210/my-blog">瀏覽研究成果</a>', 'href="./author-works/index.html">瀏覽研究成果</a>')
$text = Ensure-After $text '<a href="./author-works/index.html">著作專區</a>' '<a href="./sitemap.html">網站導覽</a>'
Write-Text $rootZh $text

$rootEn = Join-Path $repo 'index_en.html'
$text = Read-Text $rootEn
$text = $text.Replace('href="https://github.com/AndrewShih1210/my-blog">Research</a>', 'href="./author-works/index_en.html">Research</a>')
$text = $text.Replace('href="https://github.com/AndrewShih1210/my-blog">Browse Research Outputs</a>', 'href="./author-works/index_en.html">Browse Research Outputs</a>')
$text = Ensure-After $text '<a href="./author-works/index_en.html">Works</a>' '<a href="./sitemap_en.html">Sitemap</a>'
Write-Text $rootEn $text

# Course root pages
$coursePages = @(
  @{ File='index.html'; Anchor='<a href="projects.html">專題任務</a>'; Insert='<a href="../index.html">學術首頁</a>'; Map='<a href="../sitemap.html">網站導覽</a>' },
  @{ File='teaching-plan.html'; Anchor='<a href="projects.html">專題任務</a>'; Insert='<a href="../index.html">學術首頁</a>'; Map='<a href="../sitemap.html">網站導覽</a>' },
  @{ File='projects.html'; Anchor='<a href="teaching-plan.html">教學計畫</a>'; Insert='<a href="../index.html">學術首頁</a>'; Map='<a href="../sitemap.html">網站導覽</a>' },
  @{ File='index_en.html'; Anchor='<a href="projects_en.html">Projects</a>'; Insert='<a href="../index_en.html">Academic Home</a>'; Map='<a href="../sitemap_en.html">Sitemap</a>' },
  @{ File='teaching-plan_en.html'; Anchor='<a href="projects_en.html">Projects</a>'; Insert='<a href="../index_en.html">Academic Home</a>'; Map='<a href="../sitemap_en.html">Sitemap</a>' },
  @{ File='projects_en.html'; Anchor='<a href="teaching-plan_en.html">Teaching Plan</a>'; Insert='<a href="../index_en.html">Academic Home</a>'; Map='<a href="../sitemap_en.html">Sitemap</a>' }
)

foreach ($item in $coursePages) {
  $path = Join-Path $repo ('ai-course-site\' + $item.File)
  $text = Read-Text $path
  $text = Ensure-After $text $item.Anchor $item.Insert
  $text = Ensure-After $text $item.Insert $item.Map
  Write-Text $path $text
}

# Course unit pages
Get-ChildItem -LiteralPath (Join-Path $repo 'ai-course-site\units') -Filter 'unit*.html' | ForEach-Object {
  $path = $_.FullName
  $text = Read-Text $path
  if ($_.Name -like '*_en.html') {
    $text = Ensure-After $text '<a href="../projects_en.html">Projects</a>' '<a href="../../index_en.html">Academic Home</a>'
    $text = Ensure-After $text '<a href="../../index_en.html">Academic Home</a>' '<a href="../../sitemap_en.html">Sitemap</a>'
  }
  else {
    $text = Ensure-After $text '<a href="../projects.html">專題任務</a>' '<a href="../../index.html">學術首頁</a>'
    $text = Ensure-After $text '<a href="../../index.html">學術首頁</a>' '<a href="../../sitemap.html">網站導覽</a>'
  }
  Write-Text $path $text
}

# Author works pages
Get-ChildItem -LiteralPath (Join-Path $repo 'author-works') -Filter '*.html' | ForEach-Object {
  $path = $_.FullName
  $text = Read-Text $path
  $text = [regex]::Replace($text, '/article\.md"', '/index.html"')
  $text = [regex]::Replace($text, '/article_en\.md"', '/index_en.html"')

  if ($_.Name -eq 'index.html') {
    $text = Ensure-After $text '<a href="../ai-course-site/index.html">AI 教材</a>' '<a href="../sitemap.html">網站導覽</a>'
    $text = $text.Replace('<section class="section">' + "`r`n" + '    <div class="wrap section-head">' + "`r`n" + '      <div>' + "`r`n" + '        <p class="eyebrow">Featured Output</p>', '<section class="section" id="featured">' + "`r`n" + '    <div class="wrap section-head">' + "`r`n" + '      <div>' + "`r`n" + '        <p class="eyebrow">Featured Output</p>')
    $text = $text.Replace('<section class="section">' + "`r`n" + '    <div class="wrap grid-2">', '<section class="section" id="visuals">' + "`r`n" + '    <div class="wrap grid-2">')
  }

  if ($_.Name -eq 'index_en.html') {
    $text = Ensure-After $text '<a href="../ai-course-site/index_en.html">AI Course Site</a>' '<a href="../sitemap_en.html">Sitemap</a>'
    $text = $text.Replace('<section class="section"><div class="wrap section-head"><div><p class="eyebrow">Featured Output</p>', '<section class="section" id="featured"><div class="wrap section-head"><div><p class="eyebrow">Featured Output</p>')
    $text = $text.Replace('<section class="section"><div class="wrap grid-2">', '<section class="section" id="visuals"><div class="wrap grid-2">')
  }

  Write-Text $path $text
}

# Generate HTML wrappers for article pages
$dirs = Get-ChildItem -LiteralPath $repo -Directory | Where-Object { $_.Name -match '^[0-9]{2}-' }
foreach ($dir in $dirs) {
  foreach ($spec in @(
    @{ Md='article.md'; Out='index.html'; Lang='zh-Hant'; Home='../index.html'; Works='../author-works/index.html'; WorksLabel='研究成果專區'; Map='../sitemap.html'; MapLabel='網站導覽'; HomeLabel='學術首頁'; Suffix='研究成果' },
    @{ Md='article_en.md'; Out='index_en.html'; Lang='en'; Home='../index_en.html'; Works='../author-works/index_en.html'; WorksLabel='Research Works'; Map='../sitemap_en.html'; MapLabel='Sitemap'; HomeLabel='Academic Home'; Suffix='Research Page' }
  )) {
    $mdPath = Join-Path $dir.FullName $spec.Md
    if (-not (Test-Path -LiteralPath $mdPath)) { continue }

    $md = Read-Text $mdPath
    $titleMatch = [regex]::Match($md, '^#\s+(.+)$', [System.Text.RegularExpressions.RegexOptions]::Multiline)
    $title = if ($titleMatch.Success) { $titleMatch.Groups[1].Value } else { $dir.Name }
    $body = Convert-MarkdownToHtml $md

    $html = @"
<!doctype html>
<html lang="$($spec.Lang)">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>$title | $($spec.Suffix)</title>
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
    .meta { color:var(--muted); margin-bottom:20px; }
  </style>
</head>
<body>
  <header class="wrap">
    <nav>
      <a href="$($spec.Home)">$($spec.HomeLabel)</a>
      <a href="$($spec.Works)">$($spec.WorksLabel)</a>
      <a href="$($spec.Map)">$($spec.MapLabel)</a>
    </nav>
  </header>
  <main class="wrap">
    <p class="meta">$($dir.Name)</p>
    $body
  </main>
</body>
</html>
"@

    Write-Text (Join-Path $dir.FullName $spec.Out) $html
  }
}

Write-Output 'updated'
