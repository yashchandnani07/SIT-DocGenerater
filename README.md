# SIT-DocGenerater

A [ZCode skill](https://zcode.ai) that formats any assignment, lab report, practical, or experiment submission into a polished, submission-ready academic **PDF or DOCX** — with the signature SIT institutional cover page, auto table of contents, numbered navy sections, zebra tables, code blocks, figure captions, and running headers/footers.

Every report comes out with an **identical cover page** — that consistency is the whole point.

## Cover page

- Double navy border frame
- Centered **SIT logo banner** (`assets/sit-logo.png`, 8.5 cm, top of page 1)
- Department header, course title, academic-year line
- Assignment/experiment badge, big title, subtitle
- Structured student fields table (Name, PRN/Roll No., Assignment, Course, Date)

## Repository layout

```
assignment-report-formatter/     <- the skill (SKILL.md at its root)
├── SKILL.md                     <- skill entry point & rules
├── scripts/
│   ├── make_report.py           <- CLI: --spec spec.json --format pdf|docx --out file
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

## Usage

Ask ZCode to *format / rebuild / professionalize an assignment*, output a report
as PDF or DOCX, or make an uploaded docx/pdf "submission-ready" — the skill
triggers automatically.

Direct CLI use:

```bash
python assignment-report-formatter/scripts/make_report.py \
  --spec spec.json --format pdf --out 26070126510_Assignment6.pdf
```

## Requirements

- Python 3 with `reportlab` + `Pillow` (PDF) or `python-docx` + `Pillow` (DOCX)
- Fonts: Carlito, Noto Serif SC, DejaVu (DOCX uses Word-native Calibri/Cambria/Consolas)

## Installing the skill

Copy or symlink `assignment-report-formatter/` into your ZCode skills directory
(or install the `.skill` bundle directly from the ZCode client).

## License

[MIT](LICENSE)
