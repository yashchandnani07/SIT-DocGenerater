# SIT-DocGenerater

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Skill](https://img.shields.io/badge/format-agentskills.io-purple)](https://agentskills.io)

A **universal agent skill** that formats any assignment, lab report, practical, or experiment submission into a polished, submission-ready academic **PDF or DOCX** — the signature SIT institutional format: double navy cover frame with the official SIT logo banner, auto table of contents, numbered navy sections, zebra tables, code blocks, figure captions, running headers/footers.

Every report comes out with an **identical cover page** — that consistency is the whole point.

Works three ways: **as a skill for any AI agent** (SKILL.md at repo root, open [agentskills](https://agentskills.io) format), **as a slash command** (`/format-report`), or **as a plain CLI** (`sitfmt`) with no agent at all.

## Install

### Any agent (Claude Code, ZCode, Codex, Cursor, opencode, …)

```bash
git clone https://github.com/yashchandnani07/SIT-DocGenerater.git
cp -r SIT-DocGenerater ~/.claude/skills/        # Claude Code
# or ~/.zcode/skills/  (ZCode) · ~/.codex/skills/ · ~/.cursor/skills/ …
```

Any agent that reads `SKILL.md` files picks it up automatically — the entry point is at the repo root.

### Claude Code — slash command

Drop this repo (or copy `.claude/commands/`) into your project, then:

```
/format-report "Assignment 6 yash.pdf"
/format-report ./labs --docx
```

### Standalone CLI (no agent)

```bash
git clone https://github.com/yashchandnani07/SIT-DocGenerater.git
cd SIT-DocGenerater
pipx install .                # or: pip install .

sitfmt --spec spec.json --format pdf  --out 26070126510_Assignment6.pdf
sitfmt --spec spec.json --format docx --out 26070126510_Assignment6.docx
```

## What you get

| Part | Detail |
|---|---|
| Cover page | Double navy border frame, centered SIT logo banner (8.5 cm, top of page 1), department header, course title, AY line, assignment badge, big title, subtitle, student fields table |
| TOC | Auto-generated with dot leaders (PDF: multiBuild · DOCX: real Word TOC field) |
| Body | Numbered navy headings, justified serif body, zebra tables, mono code blocks with navy bar, italic figure captions |
| Chrome | Running header/footer with page numbers on body pages |

## The spec

Content is described by a single JSON file (`meta` + `sections` blocks — headings, paragraphs, bullets, formulas, code, figures, tables). See [`references/spec-schema.md`](references/spec-schema.md) and the working example in [`assets/sample-spec.json`](assets/sample-spec.json). The exact visual system is pinned in [`references/design-spec.md`](references/design-spec.md).

When used through an agent, the agent builds this spec for you from an uploaded DOCX/PDF or raw notes — you never touch the JSON.

## Repository layout

```
├── SKILL.md                     <- skill entry point (open agentskills format)
├── sitfmt.py                    <- CLI shim (pipx install .)
├── pyproject.toml
├── .claude/commands/
│   └── format-report.md         <- /format-report slash command
├── scripts/
│   ├── make_report.py           <- core CLI (--spec, --format pdf|docx, --out)
│   ├── pdf_builder.py           <- ReportLab implementation
│   └── docx_builder.py          <- python-docx implementation (Word-native fonts)
├── references/
│   ├── design-spec.md           <- the exact visual system (constants)
│   └── spec-schema.md           <- every spec field and block type
└── assets/
    ├── sit-logo.png             <- official SIT banner, baked into the cover
    ├── sample-spec.json         <- working example covering all block types
    └── sample-figure.png
```

## Requirements

- Python ≥ 3.9 with `reportlab`, `python-docx`, `Pillow` (installed automatically via pip/pipx)
- Fonts: Carlito, Noto Serif SC, DejaVu (DOCX uses Word-native Calibri/Cambria/Consolas)

## License

[MIT](LICENSE)
