"""Build llms-full.txt from reviewed public excerpts, using only the stdlib.

Run from any directory: python scripts/build_public_summary.py
Use --check to detect stale output without writing. No recursive discovery,
network requests, inferred summaries, or timestamps are used.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://andrewshih1210.github.io/my-blog/"
RESEARCH_DIRS = (
    "01-探討學習者對AI教育應用之科技認知與態度、整合性科技接受度及使用意願之分析",
    "02-AI-輔助程式設計與數據分析學習中的人機互動行為分析",
    "03-Enhancing-learning-outcomes-and-reducing-anxiety-in-programming-courses-through-AI-integration",
    "04-From-Traditional-Semantic-Analysis-to-Generative-AI-Research-on-Cybersecurity-and-Privacy-Challenges-in-Cloud-Based-Educational-Task-Automation",
    "05-優化學習工作流輕量級無伺服器AI代理人之開發與成效分析",
    "06-優化教學場域與學習效率之輕量級無伺服器AI代理人應用",
    "07-探討-GenAI人機協作評量之信度與差異分析",
    "08-數位閱讀策略工具「英語閱讀小舵手」對學生英語閱讀素養影響之準實驗研究企劃",
    "09-從心盲到心流-運算思維在生成式AI互動中的認知補償與效益",
    "10-生成式AI自動評分與回饋系統之滿意度與需求分析",
    "11-生成式AI於資料科學課程的導入時長效應-比較不同介入週數對非資訊背景大學生學習成效之影響",
    "12-生成式AI於霸凌情境模擬多重虛擬學生進行正向反思活動",
    "13-運用智慧對話系統於心理與社會情緒評量之應用",
)
RESEARCH = tuple(f"{name}/index.html" for name in RESEARCH_DIRS)
UNITS = tuple(f"ai-course-site/units/unit{n:02d}.html" for n in range(1, 9))
PATENT = "author-works/index.html"
TALKS = ("talks/index.html", "talks/index_en.html")
ALLOWLIST = RESEARCH + UNITS + (PATENT,) + TALKS
VOID = frozenset("area base br col embed hr img input link meta param source track wbr".split())
EXCERPT_LIMIT = 700
RESEARCH_CONTEXT = 'section.section > div.wrap.card:has(> h2[text="內容摘述"]) > p'
UNIT_CONTEXT = 'section.page-hero > div.wrap > p.lead; article.article > section#goals.panel > ul.clean-list > li'


@dataclass
class Element:
    tag: str
    attrs: dict = field(default_factory=dict)
    children: list = field(default_factory=list)

    def matches(self, tag, classes=(), element_id=None):
        return (self.tag == tag
                and set(classes) <= set((self.attrs.get("class") or "").split())
                and (element_id is None or self.attrs.get("id") == element_id))

    def elements(self):
        return [child for child in self.children if isinstance(child, Element)]

    def walk(self):
        yield self
        for child in self.elements():
            yield from child.walk()

    def text(self):
        if self.tag in {"script", "style", "template", "noscript", "nav", "aside", "footer", "header"}:
            return ""
        if "hidden" in self.attrs or self.attrs.get("aria-hidden") == "true":
            return ""
        return "".join(child.text() if isinstance(child, Element) else child
                       for child in self.children)


class ExcerptTree(HTMLParser):
    """Minimal tree for the explicit direct-child selectors above."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Element("document")
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = Element(tag, dict(attrs))
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def source_excerpt(relative, source):
    tree = ExcerptTree()
    tree.feed(source)
    tree.close()
    paragraphs = []
    if relative in RESEARCH:
        context = RESEARCH_CONTEXT
        for section in tree.root.walk():
            if not section.matches("section", ("section",)):
                continue
            for card in section.elements():
                if not card.matches("div", ("wrap", "card")):
                    continue
                if any(c.tag == "h2" and clean(c.text()) == "內容摘述" for c in card.elements()):
                    paragraphs.extend(c.text() for c in card.elements() if c.tag == "p")
    else:
        context = UNIT_CONTEXT
        for node in tree.root.walk():
            if node.matches("section", ("page-hero",)):
                for wrap in node.elements():
                    if wrap.matches("div", ("wrap",)):
                        paragraphs.extend(c.text() for c in wrap.elements() if c.matches("p", ("lead",)))
            if node.matches("article", ("article",)):
                for section in node.elements():
                    if section.matches("section", ("panel",), "goals"):
                        for goals in section.elements():
                            if goals.matches("ul", ("clean-list",)):
                                paragraphs.extend(c.text() for c in goals.elements() if c.tag == "li")
    text = clean(" ".join(paragraphs))
    note = ""
    if relative == RESEARCH[11]:
        # This source embeds a byline and email addresses before its introduction.
        parts = re.split(r"1\s*、\s*緒\s*論\s*", text, maxsplit=1)
        if len(parts) != 2:
            raise ValueError("Research 12 introduction boundary changed; review before publishing.")
        text = parts[1]
        context += '; text after "1 、 緒 論" only'
        note = "Source introduction is incomplete; author/contact preamble omitted."
    if not text:
        raise ValueError(f"Missing allowlisted excerpt: {relative}")
    # Fail closed rather than silently publishing contacts or unrelated project data.
    compact = re.sub(r"\s+", "", text).lower()
    if "@" in text or any(term in compact for term in (
        "研究參與", "參與研究計畫", "任職計畫", "受聘計畫", "researchparticipation",
        "employmentproject", "mailto:", "電話:", "手機:",
    )):
        raise ValueError(f"Excerpt requires privacy/scope review: {relative}")
    text = normalize_excerpt_spacing(text)
    if len(text) > EXCERPT_LIMIT:
        text = text[:EXCERPT_LIMIT - 3].rstrip() + "..."
        note = (note + " Excerpt truncated to 700 characters.").strip()
    return context, text, note


class PublicMetadata(HTMLParser):
    """Read head metadata and only h3 / citation text in a patent card."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.title = []
        self.description = ""
        self.patent_title = []
        self.patent_citation = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = (attrs.get("class") or "").split()
        blocked = tag in {"script", "style", "template", "noscript"} or any(
            frame[2] for frame in self.stack
        )
        if tag == "meta" and not blocked and any(f[0] == "head" for f in self.stack):
            if (attrs.get("name") or "").lower() == "description":
                self.description = attrs.get("content") or ""
        if tag not in VOID:
            self.stack.append((tag, classes, blocked))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        if any(f[2] for f in self.stack):
            return
        tags = [f[0] for f in self.stack]
        if "head" in tags and "title" in tags:
            self.title.append(data)
        if any("patent" in f[1] for f in self.stack):
            if "h3" in tags:
                self.patent_title.append(data)
            if any(f[0] == "p" and "muted" in f[1] for f in self.stack):
                self.patent_citation.append(data)


def clean(value):
    return " ".join(value.split())


def normalize_excerpt_spacing(text):
    """Remove only whitespace between Han characters in exported excerpts."""
    han = r"\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\U00020000-\U0002fa1f\U00030000-\U000323af"
    return re.sub(rf"(?<=[{han}])\s+(?=[{han}])", "", text)


def read_page(relative):
    if relative not in ALLOWLIST:
        raise ValueError(f"Not allowlisted: {relative}")
    path = ROOT / relative
    if path.resolve() != path.absolute():
        raise ValueError(f"Symlink or redirected source: {relative}")
    parser = PublicMetadata()
    source = path.read_text(encoding="utf-8-sig")
    parser.feed(source)
    parser.close()
    if not clean("".join(parser.title)):
        raise ValueError(f"Missing title: {relative}")
    parser.excerpt = source_excerpt(relative, source) if relative in RESEARCH + UNITS else None
    return parser


def build():
    lines = [
        "# Public source summary: Yu-Ting Shih (Andrew Shih)", "",
        "Generated by scripts/build_public_summary.py from an explicit local allowlist.",
        "This digest includes metadata and source-authored research/course excerpts (up to 700 characters per page).",
        "Selectors identify the source context; whitespace is normalized and truncation is marked.",
        "Only excerpt output removes whitespace between Han characters; English/numeric spacing is retained.",
        "Excerpts preserve source claims, not independent verification. They do not establish publication status,",
        "research findings, effectiveness, or patent validity. Consult each source.",
        "Research participation, employment projects, private records, test pages,",
        "scripts, navigation, and non-allowlisted body sections are outside this digest's scope.", "",
    ]
    groups = (("Research pages", RESEARCH), ("AI course units", UNITS),
              ("Patent section", (PATENT,)),
              ("Talks", tuple(p for p in TALKS if (ROOT / p).is_file())))
    for heading, paths in groups:
        lines.extend([f"## {heading}", ""])
        if not paths:
            lines.extend(["No allowlisted talks pages present at build time.", ""])
        for relative in paths:
            page = read_page(relative)
            if relative == PATENT:
                title = clean("".join(page.patent_title))
                citation = clean("".join(page.patent_citation))
                if not title or not citation:
                    raise ValueError("Patent card title/citation missing; review source markup.")
                lines.extend([f"### {title}",
                              f"Source: {BASE_URL}{PATENT}",
                              "Extraction context: div.patent h3; div.patent p.muted (patent only)",
                              f"Patent title (source): {title}",
                              f"Patent citation (source): {citation}"])
            else:
                lines.extend([
                    f"### {clean(''.join(page.title))}",
                    f"Source: {BASE_URL}{quote(relative, safe='/')}",
                    f"Meta description: {clean(page.description) or 'Not provided in source.'}",
                ])
                if page.excerpt:
                    context, excerpt, note = page.excerpt
                    lines.extend([f"Extraction context: {context}", f"Source excerpt: {excerpt}"])
                    if note:
                        lines.append(f"Excerpt note: {note}")
            lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    content = build().encode("utf-8")
    output = ROOT / "llms-full.txt"
    if args.check:
        if not output.is_file() or output.read_bytes() != content:
            parser.exit(1, "llms-full.txt is missing or stale; run the generator.\n")
        print("OK: llms-full.txt matches allowlisted sources.")
    else:
        output.write_bytes(content)
        print(f"Generated llms-full.txt ({len(content)} bytes).")


if __name__ == "__main__":
    main()
