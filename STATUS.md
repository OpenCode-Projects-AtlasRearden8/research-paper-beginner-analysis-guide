# STATUS.md

**Project:** Reading Research Papers — A Non-Student Beginner's Guide
**Owner:** Asdale Dynamics, LLC
**State:** Complete and verified (as of Nov 5, 2026)

## What was built

A local-first, education-only guide teaching non-students how to read formal
research papers, in the warm "like a friend would explain it" house style used
across the Dylan Asdale guides. It complements ai-for-nurse-educators-guide and
patient-teaching-with-ai-guide by supplying the deeper source-reading skill
underneath them.

Content (all in `docs/`, plain markdown):

1. **01-anatomy-of-a-paper.md** — anatomy of a paywalled PDF, section by section,
   plus six legal free routes to full-text papers (libraries, PMC, preprints,
   author copies, polite emails, open access journals).
2. **02-four-pass-method.md** — Skim / Map / Read / Verdict passes, adapted from
   Keshav's three-pass system for beginners.
3. **03-strong-vs-weak-claims.md** — hedge-word wall vs. sturdy-evidence markers,
   relative-vs-absolute risk, correlation dressed as cause, claim-to-data matching.
4. **04-sample-sizes-and-conflicts.md** — four size-of-n intuitions, significance
   vs. importance, funding/affiliation/COI places to look, publication bias.
5. **05-jargon-to-plain-english.md** — 3-step translation method, 21-entry
   starter table, safe AI-as-translation-helper protocol.
6. **verdict-template.md** — the one-page verdict fill-in sheet.
7. **reading-checklist.md** — the whole method as checkboxes, plus sanity habits.
8. **glossary.md** — ~35 paper-reading terms in plain English.
9. **README.md (docs)** — Start Here page with a friendly promise and the
   education-only framing.

Infrastructure:

- `build.sh` — one-command build + verify; `--quick` skips verification.
- `tools/build.py` — converts every `docs/*.md` page via pandoc (gfm+smart →
  html5) into standalone HTML pages with shared nav, inline CSS, title,
  description, and per-page education-only footer. Rewrites `.md` links to
  `.html`. Maps `docs/README.md` to `site/index.html`. Fails loudly if the
  nav list and docs/ files disagree or if pandoc is missing.
- `tools/check_site.py` — verifier: all 9 pages complete and well-formed, nav
  and disclaimer on every page, every internal `.html` link resolves, no
  duplicate anchors, no leftover `.md` hrefs, LICENSE contains the exact line
  "Copyright (c) 2026 Asdale Dynamics, LLC", and a targeted secrets scan
  (API keys, GitHub tokens, SSN/credit-card patterns, secret-style assignments)
  over repo text files.
- `assets/style.css` — one stylesheet, inlined into each page; no webfonts,
  no external requests, responsive down to phone width.
- `README.md` — project intro, contents, run instructions, design notes,
  MIT license, credit to Asdale Dynamics, LLC.
- `LICENSE` — MIT, copyright line exactly `Copyright (c) 2026 Asdale Dynamics, LLC`.

## How to run it

Requirements: Python 3.9+ and pandoc on PATH. No network needed to build or read.

```sh
./build.sh          # build + verify
./build.sh --quick  # build only
```

Then open `site/index.html` in any browser. Pages are self-contained and work
from `file://` — no server, no accounts, no tracking, no cookies.

## Verification results

- `./build.sh` — PASS. All 9 pages built; verifier reports
  `OK: all 9 pages verified.`
- `./build.sh --quick` — PASS (build only path exercised).
- `python3 -m py_compile tools/build.py tools/check_site.py` — PASS.
- Secrets scan — PASS (no API keys, tokens, or personal data in repo files).
- Markdown inspected for stray non-English characters — clean.
- Spot checks — tables render (`<table>` present in ch. 3 and ch. 5), task-list
  checkboxes render as real inputs, 12 `<hr>` fill-in separators on the verdict
  page, nav highlights the current page.

## Known gaps / honest limits

- `site/` is generated output and intentionally gitignored; rebuild after
  checkout before browsing. (A checkout without running `./build.sh` first has
  no HTML.)
- The secrets scan is a targeted pattern check, not a forensic audit.
- The build depends on pandoc being installed; there is no fallback converter.
- The verdict template is proof-friendly markdown; if someone later wants a
  fillable PDF, that's new work.
- Content coverage is deliberately beginner-scoped: no deeper statistics
  (beyond significance vs. effect size), no review of specific journals'
  quirks, and no citation-manager tooling.
- Cross-guide links to ai-for-nurse-educators-guide and
  patient-teaching-with-ai-guide are textual references, not hyperlinks, since
  those repos' URLs weren't known to this build.

Disclaimers: the guide is education only and is not medical, legal, or financial
advice; every page repeats this.
