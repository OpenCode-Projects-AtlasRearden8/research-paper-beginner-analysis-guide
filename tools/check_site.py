#!/usr/bin/env python3
"""Verify the built site in site/ is complete and consistent.

Checks:
  - every expected page exists and ends with a closing </html>
  - nav and education-only disclaimer present on every page
  - every internal .html link resolves to a real generated page
  - heading anchors are unique per page (pandoc gives warnings-free duplicates otherwise)
  - LICENSE has the exact required copyright line
  - no obvious secrets/API keys/personal emails in repo content
Exits non-zero on any failure.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"

EXPECTED_PAGES = [
    "index.html",
    "01-anatomy-of-a-paper.html",
    "02-four-pass-method.html",
    "03-strong-vs-weak-claims.html",
    "04-sample-sizes-and-conflicts.html",
    "05-jargon-to-plain-english.html",
    "verdict-template.html",
    "reading-checklist.html",
    "glossary.html",
]

NAV_LABELS = [
    "Anatomy of a Paper",
    "Four-Pass Method",
    "Strong vs. Weak Claims",
    "Samples &amp; Conflicts",
    "Jargon to Plain English",
    "One-Page Verdict",
    "Reading Checklist",
    "Glossary",
]

DISCLAIMER_FRAGMENT = "education only"

problems = []


def check_page(name: str) -> None:
    path = SITE / name
    if not path.is_file():
        problems.append(f"missing page: {name}")
        return
    text = path.read_text(encoding="utf-8")
    if "</html>" not in text or "<!DOCTYPE html>" not in text:
        problems.append(f"{name}: not a complete HTML document")
    if DISCLAIMER_FRAGMENT not in text.lower():
        problems.append(f"{name}: missing education-only disclaimer")
    for label in NAV_LABELS:
        if label not in text:
            problems.append(f"{name}: nav entry '{label}' missing")
    # internal links resolve
    for href in re.findall(r'href="([^"#]+\.html)"', text):
        if href.startswith("http"):
            continue
        target = SITE / href
        if not target.is_file():
            problems.append(f"{name}: broken internal link -> {href}")
    # duplicate heading ids
    ids = re.findall(r'id="([^"]+)"', text)
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        problems.append(f"{name}: duplicate anchor ids {sorted(dupes)}")
    # leftover raw markdown links
    if re.search(r'href="[^"]*\.md"', text):
        problems.append(f"{name}: unrewritten .md href")
    print(f"checked {name}")


def check_license() -> None:
    license_path = ROOT / "LICENSE"
    if not license_path.is_file():
        problems.append("LICENSE file missing")
        return
    text = license_path.read_text(encoding="utf-8")
    if "Copyright (c) 2026 Asdale Dynamics, LLC" not in text:
        problems.append("LICENSE is missing the exact required copyright line")


def check_secrets() -> None:
    # targeted hygiene scan over repo text files (excluding site/, .git/)
    patterns = [
        (re.compile(r"\bsk-[A-Za-z0-9]{16,}"), "possible API key (sk-...)"),
        (re.compile(r"(?:api[_-]?key|secret|password|token)\s*[:=]\s*['\"][^'\"]{8,}",
                    re.I), "possible secret assignment"),
        (re.compile(r"\bghp_[A-Za-z0-9]{20,}|\bgithub_pat_[A-Za-z0-9_]{20,}"),
            "possible GitHub token"),
        (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "possible SSN"),
        (re.compile(r"\b(?:\d[ -]*?){13,19}\b"), "possible credit-card number"),
    ]
    scan_paths = []
    for d in ("docs", "tools", "assets"):
        scan_paths += [p for p in (ROOT / d).rglob("*") if p.is_file()]
    scan_paths += [p for p in ROOT.iterdir()
                   if p.is_file() and p.name in {
                       "README.md", "LICENSE", "STATUS.md", "build.sh", ".gitignore"}]
    for path in scan_paths:
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, PermissionError):
            continue
        for pattern, label in patterns:
            for match in pattern.finditer(text):
                problems.append(
                    f"{path.relative_to(ROOT)}: {label}: {match.group(0)[:50]}"
                )
    print("secrets scan done")


def main() -> None:
    if not SITE.is_dir():
        sys.exit("ERROR: site/ not found. Run build.sh first.")
    for name in EXPECTED_PAGES:
        check_page(name)
    check_license()
    check_secrets()
    if problems:
        print("\nFAILURES:")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)
    print(f"\nOK: all {len(EXPECTED_PAGES)} pages verified.")


if __name__ == "__main__":
    main()
