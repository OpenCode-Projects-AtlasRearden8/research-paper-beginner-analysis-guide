# Reading Research Papers — A Beginner's Guide

**A non-student, never-condescending guide to reading formal research papers —
anatomy of a paywalled PDF, a four-pass reading method, strong vs. weak claims,
sample-size and conflict-of-interest literacy, jargon translation, and a one-page
verdict template.**

Warm plain English, education-only disclaimers throughout, built to complement
**ai-for-nurse-educators-guide** and **patient-teaching-with-ai-guide** with the
deeper source-reading skill underneath them both.

## What's inside

- `docs/` — the full guide as plain markdown:
  - Start Here (overview and how to use the guide)
  - Chapter 1: Anatomy of a Paywalled PDF (+ legal free routes to papers)
  - Chapter 2: The Four-Pass Reading Method
  - Chapter 3: Strong Claims vs. Weak Claims
  - Chapter 4: Sample Sizes and Conflicts of Interest
  - Chapter 5: Translating Jargon to Plain English
  - The One-Page Verdict Template
  - Quick Reading Checklist
  - Glossary
- `build.sh` — builds the static HTML site into `site/` then verifies it
- `tools/build.py` — pandoc-powered markdown → standalone-HTML site builder
- `tools/check_site.py` — site verifier (pages complete, nav/disclaimer present,
  internal links resolve, LICENSE line exact, secrets scan)

## Run it locally

Requirements: Python 3.9+ and [pandoc](https://pandoc.org). No network needed to
build or read the site.

```sh
./build.sh          # build + verify
./build.sh --quick  # build only
```

Then open `site/index.html` in any browser — pages are self-contained (inline CSS,
no fonts fetched, no tracking, no cookies). The guide's rendered nav, checklists,
tables, and verdict template all work from `file://`.

## Design notes

- **Local-first**: plain markdown source, plain HTML output, no accounts, no
  analytics, nothing leaves your machine.
- **Tested build**: `build.sh` refuses to finish until the verifier passes —
  every page complete and consistent, all internal links resolve, no leftover
  `.md` links, LICENSE line exact, and a targeted secrets scan.
- **Voice**: like a friend would explain it — warm, step-by-step, never assuming
  background you don't have and never talking down.
- **Education only**: every page carries the disclaimer; the guide never claims to
  replace medical, legal, or financial professionals.

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Asdale Dynamics, LLC.

Built and maintained by **Asdale Dynamics, LLC** — beginner-friendly AI education,
books, guides, and practical tools. Learn more at
[dylanasdale.github.io](https://dylanasdale.github.io).
