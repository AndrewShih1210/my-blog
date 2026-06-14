from __future__ import annotations

import json
import re
from pathlib import Path
from html import escape


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "author-works" / "works-data.json"


def load_data() -> dict:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def ordered_works(data: dict) -> list[dict]:
    return sorted(data["works"], key=lambda item: (-item["year"], item["sort"]))


def link_or_text(text: str, href: str | None) -> str:
    safe_text = escape(text)
    if href:
        return f'<a href="{escape(href, quote=True)}">{safe_text}</a>'
    return safe_text


def build_works_grid(data: dict, lang: str) -> str:
    button_text = "開啟成果頁" if lang == "zh" else "Open research page"
    parts: list[str] = []
    for item in ordered_works(data):
        payload = item[lang]
        page = item["pageZh"] if lang == "zh" else item["pageEn"]
        pieces = [
            "      <article class=\"work-card\">",
            f"        <h3>{escape(payload['cardTitle'])}</h3>",
            f"        <p class=\"muted\">{escape(payload['meta'])}</p>",
            f"        <p>{escape(payload['summary'])}</p>",
        ]
        if page:
            pieces.append(
                f"        <a class=\"button\" href=\"{escape(page, quote=True)}\">{button_text}</a>"
            )
        pieces.append("      </article>")
        parts.append("\n".join(pieces))
    return "\n".join(parts)


def build_apa_groups(data: dict, lang: str) -> str:
    notes = data["yearNotes"][lang]
    works_by_year: dict[int, list[dict]] = {}
    for item in ordered_works(data):
        works_by_year.setdefault(item["year"], []).append(item)

    patent = data["patent"]
    works_by_year.setdefault(patent["year"], [])

    year_order = sorted(works_by_year.keys(), reverse=True)
    chunks: list[str] = []
    for year in year_order:
        chunks.append("      <div class=\"year-block\">")
        chunks.append("        <div class=\"year-head\">")
        chunks.append(f"          <h3>{year}</h3>")
        chunks.append(f"          <span class=\"year-note\">{escape(notes[str(year)])}</span>")
        chunks.append("        </div>")
        chunks.append("        <ol>")

        if year == patent["year"]:
            if lang == "zh":
                patent_line = (
                    f"{escape('施育廷（2026）。')}"
                    f"{link_or_text(patent['zh']['title'], patent['url'])}"
                    f"{escape('。中華民國經濟部智慧財產局。')}"
                )
            else:
                patent_line = (
                    f"{escape('Shih, Y.-T. (2026). ')}"
                    f"{link_or_text(patent['en']['title'], patent['url'])}"
                    f"{escape('. Taiwan Intellectual Property Office, Ministry of Economic Affairs.')}"
                )
            chunks.append(f"          <li>{patent_line}</li>")

        for item in works_by_year[year]:
            payload = item[lang]
            page = item["pageZh"] if lang == "zh" else item["pageEn"]
            if lang == "zh":
                if re.search(r"[A-Za-z]", payload["apaAuthors"]):
                    line = (
                        f"{escape(payload['apaAuthors'])} ({escape(payload['apaDate'])}). "
                        f"{link_or_text(payload['title'], page)} {escape(payload['apaLabel'])}. "
                        f"{escape(payload['apaVenue'])}"
                    )
                else:
                    line = (
                        f"{escape(payload['apaAuthors'])}（{escape(payload['apaDate'])}）。"
                        f"{link_or_text(payload['title'], page)}"
                        f"{escape(payload['apaLabel'])}。{escape(payload['apaVenue'])}"
                    )
            else:
                line = (
                    f"{escape(payload['apaAuthors'])} ({escape(payload['apaDate'])}). "
                    f"{link_or_text(payload['title'], page)} {escape(payload['apaLabel'])}. "
                    f"{escape(payload['apaVenue'])}"
                )
            chunks.append(f"          <li>{line}</li>")

        chunks.append("        </ol>")
        chunks.append("      </div>")
    return "\n".join(chunks)


def replace_between_markers(text: str, start_marker: str, end_marker: str, replacement: str) -> str:
    start = text.index(start_marker) + len(start_marker)
    end = text.index(end_marker)
    return text[:start] + "\n" + replacement + "\n    " + text[end:]


def update_file(path: Path, start_marker: str, end_marker: str, replacement: str) -> None:
    text = path.read_text(encoding="utf-8")
    updated = replace_between_markers(text, start_marker, end_marker, replacement)
    path.write_text(updated, encoding="utf-8", newline="\n")


def main() -> None:
    data = load_data()
    update_file(
        ROOT / "author-works" / "index.html",
        "<!-- GENERATED_WORKS_GRID_ZH_START -->",
        "<!-- GENERATED_WORKS_GRID_ZH_END -->",
        build_works_grid(data, "zh"),
    )
    update_file(
        ROOT / "author-works" / "index_en.html",
        "<!-- GENERATED_WORKS_GRID_EN_START -->",
        "<!-- GENERATED_WORKS_GRID_EN_END -->",
        build_works_grid(data, "en"),
    )
    update_file(
        ROOT / "author-works" / "apa.html",
        "<!-- GENERATED_APA_ZH_START -->",
        "<!-- GENERATED_APA_ZH_END -->",
        build_apa_groups(data, "zh"),
    )
    update_file(
        ROOT / "author-works" / "apa_en.html",
        "<!-- GENERATED_APA_EN_START -->",
        "<!-- GENERATED_APA_EN_END -->",
        build_apa_groups(data, "en"),
    )


if __name__ == "__main__":
    main()
