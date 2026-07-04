from __future__ import annotations

import argparse
from pathlib import Path
import shutil


REPO_ROOT = Path(r"C:\Users\sweet\OneDrive\Desktop\pd\REFERENCES_GITHUB")
SITE_ROOT = REPO_ROOT / "linebot-course-site"
TEMPLATE_ROOT = REPO_ROOT / "scripts" / "linebot-course-site-templates"


def ensure_templates() -> None:
    if not TEMPLATE_ROOT.exists():
        raise FileNotFoundError(
            f"Template directory not found: {TEMPLATE_ROOT}\n"
            "Please create it first and place the UTF-8 HTML source files there."
        )


def build_site() -> None:
    ensure_templates()

    template_files = sorted(TEMPLATE_ROOT.glob("*.html"))
    if not template_files:
        raise FileNotFoundError(
            f"No HTML templates found in {TEMPLATE_ROOT}"
        )

    for template in template_files:
        target = SITE_ROOT / template.name
        content = template.read_text(encoding="utf-8")
        target.write_text(content, encoding="utf-8", newline="\n")
        print(f"Wrote {target}")


def snapshot_current_site() -> None:
    TEMPLATE_ROOT.mkdir(parents=True, exist_ok=True)
    for source in sorted(SITE_ROOT.glob("*.html")):
        shutil.copy2(source, TEMPLATE_ROOT / source.name)
        print(f"Snapshotted {source.name}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build or snapshot the LINE Bot course site."
    )
    parser.add_argument(
        "--snapshot",
        action="store_true",
        help="Copy the current site HTML files back into the template folder.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.snapshot:
        snapshot_current_site()
    else:
        build_site()
