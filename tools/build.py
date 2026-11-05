#!/usr/bin/env python3
"""Build the static HTML site from docs/ markdown.

Local-first: converts every markdown file in docs/ to a standalone HTML page
(no external assets, no fonts fetched, works from file:// after the build).
Requires pandoc on PATH.
"""

import html
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SITE = ROOT / "site"

# Display order for the nav sidebar.
PAGE_ORDER = [
    "README.md",
    "01-anatomy-of-a-paper.md",
    "02-four-pass-method.md",
    "03-strong-vs-weak-claims.md",
    "04-sample-sizes-and-conflicts.md",
    "05-jargon-to-plain-english.md",
    "verdict-template.md",
    "reading-checklist.md",
    "glossary.md",
]

NAV_LABELS = {
    "README.md": "Start Here",
    "01-anatomy-of-a-paper.md": "1. Anatomy of a Paper",
    "02-four-pass-method.md": "2. Four-Pass Method",
    "03-strong-vs-weak-claims.md": "3. Strong vs. Weak Claims",
    "04-sample-sizes-and-conflicts.md": "4. Samples & Conflicts",
    "05-jargon-to-plain-english.md": "5. Jargon to Plain English",
    "verdict-template.md": "6. One-Page Verdict",
    "reading-checklist.md": "7. Reading Checklist",
    "glossary.md": "8. Glossary",
}

OUTPUT_NAMES = {
    "README.md": "index.html",
}

DISCLAIMER = (
    "This guide is for education only. It is not medical, legal, or financial "
    "advice, and it does not replace professionals who can see your whole "
    "picture. Take your questions and verdicts to the right person."
)

STYLE = (ROOT / "assets" / "style.css").read_text(encoding="utf-8")

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Reading Research Papers, Beginner's Guide</title>
<meta name="description" content="A warm, plain-English beginner's guide to reading formal research papers: anatomy of a paywalled PDF, the four-pass reading method, strong vs. weak claims, sample sizes, conflicts of interest, and a one-page verdict template.">
<style>
{style}
</style>
</head>
<body>
<a class="skip" href="#content">Skip to content</a>
<div class="layout">
<nav aria-label="Guide chapters">
<p class="brand"><a href="index.html">Reading Research Papers</a><span class="brand-sub">a beginner's guide by Asdale Dynamics, LLC</span></p>
<ul>
{nav}
</ul>
<p class="nav-note">Education only — not medical, legal, or financial advice.</p>
</nav>
<main id="content">
{body}
<footer class="page-footer">
<p>{disclaimer}</p>
<p class="fine">Local-first static site, built from plain markdown. No tracking, no accounts, no cookies.</p>
</footer>
</main>
</div>
</body>
</html>
"""


def slug(md_name: str) -> str:
    name = OUTPUT_NAMES.get(md_name, md_name.rsplit(".", 1)[0] + ".html")
    return name


def run_pandoc(md_path: Path) -> str:
    result = subprocess.run(
        ["pandoc", "-f", "gfm+smart", "-t", "html5", str(md_path)],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def extract_title(body: str, fallback: str) -> str:
    match = re.search(r"<h1[^>]*>(.*?)</h1>", body, flags=re.S)
    if match:
        return re.sub(r"<[^>]+>", "", html.unescape(match.group(1))).strip()
    return fallback


def rewrite_links(body: str) -> str:
    # docs-style .md links become .html links in the built site
    return re.sub(r'(href=")([^"#]+)\.md(["#])', r"\1\2.html\3", body)


def build() -> None:
    docs = sorted(p for p in DOCS.glob("*.md"))
    names = {p.name for p in docs}
    missing = [n for n in PAGE_ORDER if n not in names]
    if missing:
        sys.exit(f"ERROR: nav lists pages missing from docs/: {missing}")
    unordered = names - set(PAGE_ORDER)
    if unordered:
        sys.exit(f"ERROR: docs/ contains pages not listed in PAGE_ORDER: {sorted(unordered)}")

    nav_items = []
    for name in PAGE_ORDER:
        href = slug(name)
        current = ' class="current"' if name == "README.md" else ""
        nav_items.append(
            f'<li{current}><a href="{href}">{html.escape(NAV_LABELS[name])}</a></li>'
        )
    nav = "\n".join(nav_items)

    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True)

    for name in PAGE_ORDER:
        raw = run_pandoc(DOCS / name)
        body = rewrite_links(raw)
        title = extract_title(body, NAV_LABELS[name])
        page = PAGE_TEMPLATE.format(
            title=html.escape(title),
            style=STYLE,
            nav=nav,
            body=body,
            disclaimer=DISCLAIMER,
        )
        out = SITE / slug(name)
        out.write_text(page, encoding="utf-8")
        print(f"built {out.relative_to(ROOT)}")

    print(f"OK: {len(PAGE_ORDER)} pages -> site/")


def main() -> None:
    try:
        build()
    except FileNotFoundError:
        sys.exit(
            "ERROR: pandoc was not found on PATH. "
            "Install it (https://pandoc.org) and re-run."
        )
    except subprocess.CalledProcessError as exc:
        sys.exit(f"ERROR: pandoc failed: {exc.stderr}")


if __name__ == "__main__":
    main()
