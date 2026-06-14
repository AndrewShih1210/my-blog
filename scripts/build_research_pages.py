from __future__ import annotations

import json
import re
from dataclasses import dataclass
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://andrewshih1210.github.io/my-blog"
DIR_PATTERN = re.compile(r"^(0[1-9]|1[0-3])-")


@dataclass
class Block:
    kind: str
    value: object


@dataclass
class Section:
    heading: str
    blocks: list[Block]


def truncate_text(text: str, limit: int = 150) -> str:
    clean = re.sub(r"\s+", " ", text).strip()
    return clean if len(clean) <= limit else clean[: limit - 1].rstrip() + "…"


def normalize_asset_path(path: str) -> str:
    normalized = path.replace("\\", "/")
    if normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_paragraph(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def parse_markdown(path: Path) -> dict:
    lines = path.read_text(encoding="utf-8").splitlines()
    title = ""
    preamble: list[str] = []
    sections: list[Section] = []
    current_heading: str | None = None
    current_blocks: list[Block] = []
    paragraph_lines: list[str] = []
    list_items: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph_lines
        if paragraph_lines:
            text = normalize_paragraph(" ".join(paragraph_lines))
            if text:
                current_blocks.append(Block("paragraph", text))
            paragraph_lines = []

    def flush_list() -> None:
        nonlocal list_items
        if list_items:
            current_blocks.append(Block("list", list_items[:]))
            list_items = []

    def flush_section() -> None:
        nonlocal current_heading, current_blocks
        flush_paragraph()
        flush_list()
        if current_heading is not None:
            sections.append(Section(current_heading, current_blocks[:]))
        current_heading = None
        current_blocks = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            title = stripped[2:].strip()
            continue
        if stripped.startswith("## "):
            flush_section()
            current_heading = stripped[3:].strip()
            continue
        if not stripped:
            if current_heading is None:
                continue
            flush_paragraph()
            flush_list()
            continue
        image_match = re.match(r"^!\[(.*?)\]\((.*?)\)$", stripped)
        if image_match:
            flush_paragraph()
            flush_list()
            current_blocks.append(
                Block(
                    "image",
                    {
                        "alt": image_match.group(1).strip(),
                        "src": normalize_asset_path(image_match.group(2).strip()),
                    },
                )
            )
            continue
        if stripped.startswith("- "):
            flush_paragraph()
            list_items.append(stripped[2:].strip())
            continue
        if current_heading is None:
            preamble.append(stripped)
        else:
            paragraph_lines.append(stripped)

    flush_section()
    return {"title": title, "preamble": preamble, "sections": sections}


def find_preamble_value(preamble: list[str], prefixes: list[str]) -> str:
    for line in preamble:
        for prefix in prefixes:
            if line.startswith(prefix):
                return line[len(prefix) :].strip()
    return ""


def parse_keywords(text: str) -> list[str]:
    if not text:
        return []
    parts = re.split(r"[、,，;；]\s*", text)
    return [part.strip() for part in parts if part.strip()]


def section_text(section: Section | None) -> str:
    if not section:
        return ""
    chunks: list[str] = []
    for block in section.blocks:
        if block.kind == "paragraph":
            chunks.append(str(block.value))
        elif block.kind == "list":
            chunks.extend(str(item) for item in block.value)
    return " ".join(chunks).strip()


def section_by_heading(sections: list[Section], headings: list[str]) -> Section | None:
    for heading in headings:
        for section in sections:
            if section.heading == heading:
                return section
    return None


def parse_authors(author_line: str, lang: str) -> list[str]:
    if not author_line:
        return []
    if lang == "zh":
        return [part.strip() for part in author_line.split("、") if part.strip()]
    normalized = author_line.replace(" and ", ", ").replace("&", ",")
    return [part.strip() for part in normalized.split(",") if part.strip()]


def render_list(items: list[str]) -> str:
    rendered = "\n".join(f"              <li>{escape(item)}</li>" for item in items)
    return f"            <ul>\n{rendered}\n            </ul>"


def render_paragraphs(blocks: list[Block]) -> str:
    rendered: list[str] = []
    for block in blocks:
        if block.kind == "paragraph":
            rendered.append(f"            <p>{escape(str(block.value))}</p>")
        elif block.kind == "list":
            rendered.append(render_list(list(block.value)))
    return "\n".join(rendered)


def render_generic_sections(sections: list[Section]) -> str:
    chunks: list[str] = []
    for section in sections:
        body = render_paragraphs(section.blocks)
        if not body:
            continue
        chunks.append(
            "\n".join(
                [
                    "  <section class=\"section\">",
                    "    <div class=\"wrap card\">",
                    f"      <h2>{escape(section.heading)}</h2>",
                    body,
                    "    </div>",
                    "  </section>",
                ]
            )
        )
    return "\n".join(chunks)


def render_figures(images: list[dict[str, str]], lang: str) -> str:
    if not images:
        return ""
    heading = "圖像摘錄" if lang == "zh" else "Extracted Figures"
    eyebrow = "Figures"
    description = (
        "保留原始研究圖像，供閱讀時對照研究脈絡與視覺資訊。"
        if lang == "zh"
        else "Original extracted figures are retained for visual reference and contextual reading."
    )
    cards = "\n".join(
        [
            "\n".join(
                [
                    "      <article class=\"figure-card\">",
                    f"        <img src=\"{escape(img['src'], quote=True)}\" alt=\"{escape(img['alt'])}\" />",
                    "      </article>",
                ]
            )
            for img in images
        ]
    )
    return "\n".join(
        [
            "  <section class=\"section\">",
            "    <div class=\"wrap section-head\">",
            "      <div>",
            f"        <p class=\"eyebrow\">{eyebrow}</p>",
            f"        <h2>{heading}</h2>",
            "      </div>",
            f"      <p>{escape(description)}</p>",
            "    </div>",
            "    <div class=\"wrap figure-grid\">",
            cards,
            "    </div>",
            "  </section>",
        ]
    )


def build_tags(author: str, keywords: list[str], page_count: int, image_count: int, lang: str) -> list[str]:
    if lang == "zh":
        tags = [f"作者：{author}"]
        tags.append(f"{page_count} 頁內容")
        if image_count:
            tags.append(f"{image_count} 張圖像")
    else:
        tags = [f"Author: {author}"]
        tags.append(f"{page_count} page" if page_count == 1 else f"{page_count} pages")
        if image_count:
            tags.append(f"{image_count} figure" if image_count == 1 else f"{image_count} figures")
    tags.extend(keywords[:2])
    return tags[:5]


def build_page(folder: Path, lang: str) -> str:
    metadata = read_json(folder / "metadata.json")
    markdown = parse_markdown(folder / ("article.md" if lang == "zh" else "article_en.md"))
    title = metadata["title"] if lang == "zh" else metadata["title_en"]
    preamble = markdown["preamble"]
    sections = markdown["sections"]

    author_prefixes = ["作者："] if lang == "zh" else ["Author:", "Authors:"]
    detail_prefixes = ["發表資訊："] if lang == "zh" else ["Presentation details:"]
    author = find_preamble_value(preamble, author_prefixes) or (
        metadata["author"] if lang == "zh" else metadata["author_en"]
    )
    presentation_details = find_preamble_value(preamble, detail_prefixes)

    intro_section = section_by_heading(sections, ["文章簡述", "Overview"])
    key_points_section = section_by_heading(sections, ["研究重點", "Key Points"])
    keywords_section = section_by_heading(sections, ["關鍵主題", "Keywords"])
    summary_section = section_by_heading(sections, ["內容摘述", "Summary"])
    figures_section = section_by_heading(sections, ["圖像摘錄", "Extracted Figures"])

    intro_text = section_text(intro_section)
    summary_text = section_text(summary_section)
    description = truncate_text(intro_text or summary_text or title)

    keywords = metadata.get("keywords" if lang == "zh" else "keywords_en", []) or parse_keywords(
        section_text(keywords_section)
    )
    images = [
        block.value
        for block in (figures_section.blocks if figures_section else [])
        if block.kind == "image"
    ]
    if not images:
        images = [
            {
                "src": normalize_asset_path(path),
                "alt": f"{title} - {Path(path).name}",
            }
            for path in metadata["files"].get("images", [])
        ]

    is_zh = lang == "zh"
    page_name = "index.html" if is_zh else "index_en.html"
    alt_page_name = "index_en.html" if is_zh else "index.html"
    page_url = f"{BASE_URL}/{folder.name}/{page_name}"
    alt_url = f"{BASE_URL}/{folder.name}/{alt_page_name}"
    home_url = "../index.html" if is_zh else "../index_en.html"
    works_url = "../author-works/index.html" if is_zh else "../author-works/index_en.html"
    apa_url = "../author-works/apa.html" if is_zh else "../author-works/apa_en.html"
    sitemap_url = "../sitemap.html" if is_zh else "../sitemap_en.html"
    switch_label = "EN" if is_zh else "中文"
    switch_href = f"./{alt_page_name}"

    page_title = f"{title} | Research Page"
    og_image = f"{BASE_URL}/{folder.name}/{images[0]['src']}" if images else ""
    site_lang = "zh-Hant" if is_zh else "en"
    authors = parse_authors(author, lang)
    json_ld = {
        "@context": "https://schema.org",
        "@type": "ScholarlyArticle",
        "headline": title,
        "inLanguage": site_lang,
        "author": [{"@type": "Person", "name": name} for name in authors] or [{"@type": "Person", "name": author}],
        "url": page_url,
    }
    if keywords:
        json_ld["about"] = keywords
    if images:
        json_ld["image"] = [f"{BASE_URL}/{folder.name}/{img['src']}" for img in images]

    tags = build_tags(author, keywords, metadata.get("page_count", 0), metadata.get("image_count", 0), lang)
    tag_html = "\n".join(f"          <span class=\"tag\">{escape(tag)}</span>" for tag in tags)
    keywords_text = "、".join(keywords) if is_zh else ", ".join(keywords)

    hero_eyebrow = "Research Page"
    info_heading = "發表資訊" if is_zh else "Publication Info"
    keywords_heading = "關鍵主題" if is_zh else "Keywords"
    source_label = "來源檔案" if is_zh else "Source file"
    content_note = (
        "本頁由研究資料與文章摘述自動整理，統一採用站內共用版型。"
        if is_zh
        else "This page is generated from the shared research-page structure and uses the site-wide template."
    )
    back_works = "回到著作專區" if is_zh else "Back to Works Page"
    view_apa = "查看 APA 清單" if is_zh else "View APA List"
    overview_heading = intro_section.heading if intro_section else ("研究概述" if is_zh else "Overview")

    info_body: list[str] = []
    if presentation_details:
        info_body.append(f"        <p class=\"muted\">{escape(presentation_details)}</p>")
    else:
        separator = "：" if is_zh else ": "
        info_body.append(
            f"        <p class=\"muted\">{escape(source_label)}{separator}{escape(metadata.get('source_name', ''))}</p>"
        )
    if keywords_text:
        info_body.extend(
            [
                f"        <h3>{keywords_heading}</h3>",
                f"        <p class=\"muted\">{escape(keywords_text)}</p>",
            ]
        )
    info_body.append(f"        <p class=\"note\">{escape(content_note)}</p>")

    body_sections: list[Section] = []
    for section in sections:
        if section in [intro_section, key_points_section, keywords_section, summary_section, figures_section]:
            continue
        body_sections.append(section)

    key_points_html = ""
    if key_points_section:
        list_block = next((block for block in key_points_section.blocks if block.kind == "list"), None)
        if list_block:
            key_points_html = render_list(list(list_block.value))
        else:
            key_points_html = render_paragraphs(key_points_section.blocks)

    summary_html = render_paragraphs(summary_section.blocks) if summary_section else ""
    intro_html = render_paragraphs(intro_section.blocks) if intro_section else ""
    figures_html = render_figures(images, lang)
    generic_html = render_generic_sections(body_sections)
    summary_section_html = ""
    if summary_section and summary_html:
        summary_section_html = "\n".join(
            [
                "  <section class=\"section\">",
                "    <div class=\"wrap card\">",
                f"      <h2>{escape(summary_section.heading)}</h2>",
                summary_html,
                "    </div>",
                "  </section>",
            ]
        )

    return f"""<!doctype html>
<html lang="{site_lang}">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="description" content="{escape(description, quote=True)}" />
  <meta name="robots" content="index,follow,max-image-preview:large" />
  <meta name="author" content="{escape(author, quote=True)}" />
  <link rel="canonical" href="{page_url}" />
  <link rel="alternate" hreflang="{site_lang}" href="{page_url}" />
  <link rel="alternate" hreflang="{'en' if is_zh else 'zh-Hant'}" href="{alt_url}" />
  <meta property="og:type" content="article" />
  <meta property="og:title" content="{escape(title, quote=True)}" />
  <meta property="og:description" content="{escape(description, quote=True)}" />
  <meta property="og:url" content="{page_url}" />
  {"<meta property=\"og:image\" content=\"" + escape(og_image, quote=True) + "\" />" if og_image else ""}
  <meta name="twitter:card" content="summary_large_image" />
  <title>{escape(page_title)}</title>
  <style>
    :root {{ --bg:#f4f7fb; --paper:rgba(255,255,255,.94); --paper-strong:#fff; --ink:#0f172a; --muted:#475569; --line:#dbe3ee; --accent:#1d4ed8; --accent-soft:rgba(37,99,235,.08); --shadow:0 18px 42px rgba(15,23,42,.08); --radius-card:18px; --radius-button:8px; }}
    *{{box-sizing:border-box}} html{{scroll-behavior:smooth}}
    body{{margin:0;color:var(--ink);font-family:"Inter","Noto Sans TC","Microsoft JhengHei",sans-serif;line-height:1.8;background:radial-gradient(circle at top left, rgba(59,130,246,.14), transparent 28%),radial-gradient(circle at top right, rgba(15,23,42,.08), transparent 24%),linear-gradient(180deg,#eef4fb 0%,#f8fbff 44%,#f4f7fb 100%);padding-top:92px}}
    a{{color:inherit}} .wrap{{width:min(1100px,calc(100vw - 32px));margin:0 auto}}
    .site-header{{position:fixed;inset:0 0 auto 0;z-index:50;border-bottom:1px solid rgba(148,163,184,.18);background:rgba(248,251,255,.84);backdrop-filter:blur(18px);box-shadow:0 6px 22px rgba(15,23,42,.04)}}
    .topbar,.section-head{{display:flex;justify-content:space-between;gap:18px;align-items:end}} .topbar{{padding:16px 0;align-items:center}}
    .nav{{display:flex;flex-wrap:nowrap;gap:12px;overflow-x:auto;scrollbar-width:none}} .nav::-webkit-scrollbar{{display:none}}
    .nav a,.button{{min-height:44px;display:inline-flex;align-items:center;padding:10px 16px;border-radius:var(--radius-button);border:1px solid rgba(148,163,184,.22);background:rgba(255,255,255,.74);text-decoration:none;font-weight:700;white-space:nowrap}}
    .button.primary{{background:linear-gradient(135deg,#1d4ed8,#2563eb);border-color:#1d4ed8;color:#fff}}
    .hero,.section{{padding:24px 0}}
    .eyebrow,.tag{{display:inline-flex;align-items:center}}
    .eyebrow{{padding:6px 12px;border-radius:999px;background:var(--accent-soft);color:var(--accent);font-size:13px;font-weight:800;letter-spacing:.04em;text-transform:uppercase}}
    h1,h2,h3,p{{margin-top:0}} h1{{font-size:clamp(36px,5vw,58px);line-height:1.06;margin:14px 0;letter-spacing:-.03em}} h2{{font-size:clamp(28px,3vw,38px);margin-bottom:14px;letter-spacing:-.02em}} h3{{font-size:22px;line-height:1.25;margin-bottom:10px}}
    .lead,.muted,.section-head p,.note{{color:var(--muted)}}
    .card,.figure-card,.info-card{{background:var(--paper);border:1px solid var(--line);border-radius:var(--radius-card);box-shadow:var(--shadow);padding:26px}}
    .hero-grid,.grid-2,.figure-grid{{display:grid;gap:18px}} .hero-grid{{grid-template-columns:1.2fr .8fr}} .grid-2{{grid-template-columns:repeat(2,minmax(0,1fr))}} .figure-grid{{grid-template-columns:repeat(2,minmax(0,1fr))}}
    .meta,.actions{{display:flex;flex-wrap:wrap;gap:10px}} .meta{{margin:14px 0 0}} .actions{{margin-top:20px}}
    .tag{{padding:6px 12px;border-radius:999px;background:var(--accent-soft);color:var(--accent);font-size:14px;font-weight:700}}
    .section-head{{margin-bottom:18px}} .section-head p{{max-width:620px}}
    ul{{margin:0;padding-left:20px}} li{{margin-bottom:10px}}
    .figure-card img{{display:block;width:100%;height:auto;border-radius:14px;border:1px solid var(--line);background:#fff}}
    .footer{{padding:20px 0 48px;color:var(--muted);font-size:15px}}
    @media (max-width:980px){{body{{padding-top:108px}}.topbar,.section-head{{display:block}}.nav{{margin-top:12px}}.hero-grid,.grid-2,.figure-grid{{grid-template-columns:1fr}}}}
  </style>
  <script type="application/ld+json">
{json.dumps(json_ld, ensure_ascii=False, indent=2)}
  </script>
</head>
<body>
  <header class="site-header">
    <div class="wrap topbar">
      <a href="{home_url}"><strong>Yu-Ting Shih Academic Site</strong></a>
      <nav class="nav" aria-label="{'主要導覽' if is_zh else 'Primary navigation'}">
        <a href="{home_url}">{'首頁' if is_zh else 'Home'}</a>
        <a href="{works_url}">{'著作專區' if is_zh else 'Author Works'}</a>
        <a href="{apa_url}">{'APA 清單' if is_zh else 'APA List'}</a>
        <a href="{sitemap_url}">{'網站導覽' if is_zh else 'Sitemap'}</a>
        <a href="{switch_href}">{switch_label}</a>
      </nav>
    </div>
  </header>

  <section class="hero">
    <div class="wrap hero-grid">
      <article class="card">
        <p class="eyebrow">{hero_eyebrow}</p>
        <h1>{escape(title)}</h1>
        <p class="lead">{escape(truncate_text(intro_text or description, 240))}</p>
        <div class="meta">
{tag_html}
        </div>
        <div class="actions">
          <a class="button primary" href="{works_url}">{back_works}</a>
          <a class="button" href="{apa_url}">{view_apa}</a>
        </div>
      </article>
      <article class="info-card">
        <h2>{info_heading}</h2>
{chr(10).join(info_body)}
      </article>
    </div>
  </section>

  <section class="section">
    <div class="wrap grid-2">
      <article class="card">
        <h2>{escape(overview_heading)}</h2>
{intro_html}
      </article>
      <article class="card">
        <h2>{escape(key_points_section.heading if key_points_section else ('研究重點' if is_zh else 'Key Points'))}</h2>
{key_points_html}
      </article>
    </div>
  </section>

  {summary_section_html}
  {generic_html}
  {figures_html}

  <footer class="wrap footer">
    <p>{escape(content_note)} {'本頁與著作專區、APA 清單及網站導覽頁互相連結。' if is_zh else 'This page links back to the works page, APA list, and sitemap.'}</p>
  </footer>
</body>
</html>
"""


def write_pages() -> None:
    for folder in sorted([path for path in ROOT.iterdir() if path.is_dir() and DIR_PATTERN.match(path.name)]):
        (folder / "index.html").write_text(build_page(folder, "zh"), encoding="utf-8", newline="\n")
        (folder / "index_en.html").write_text(build_page(folder, "en"), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    write_pages()
