---
name: assignment-report-formatter
description: >-
  Formats any assignment, lab report, practical, or experiment submission into a
  polished academic PDF or DOCX with the signature institutional cover page
  (double navy border frame, centered SIT logo banner, department header, big
  title, structured student fields table), auto table of contents, numbered
  sections, navy zebra tables,
  code blocks, figure captions, and running headers/footers. Use this skill
  whenever the user wants to format, rebuild, convert, or professionalize an
  assignment or report for ANY subject, asks for output "like Assignment 6" or
  "same format/cover as before", wants a report as PDF or DOCX, asks to replace
  a student name/PRN on a submission, uploads a docx/pdf lab report to be made
  submission-ready, or mentions report formatting, cover pages, or TOC — even
  if they don't name this skill explicitly.
compatibility: >-
  Requires Python 3 with reportlab + Pillow (PDF) or python-docx + Pillow
  (DOCX). Fonts used: Carlito, Noto Serif SC, DejaVu (present on this system;
  DOCX uses Word-native Calibri/Cambria/Consolas names).
---

# Assignment Report Formatter

Turn raw assignment content (extracted from an uploaded DOCX/PDF, or provided
as notes) into a consistently formatted academic report. The design is fixed
in `references/design-spec.md` and implemented in `scripts/` — your job is to
prepare content, not to restyle. The cover page must come out identical every
time; that consistency is the whole point.

## Workflow

### 1. Gather the content

- If the user uploaded a DOCX: `pandoc input.docx -t markdown -o extracted.md`
  and copy its `media/` folder for the embedded images.
- If the user uploaded a PDF: extract text with PyMuPDF (`page.get_text()`)
  and images with `page.get_images()` (dedupe by xref, skip tiny images).
  Build contact sheets of extracted images with PIL to identify which figure
  is which before placing them.
- Identify: student name + PRN to use, assignment number, all section text,
  all tables (re-type them as real table rows, never as images), all
  screenshots/figures and their captions, and any formulas.

### 2. Replace the student identity everywhere

Swap the original author's name and PRN with the user's current name/PRN in
the cover fields (this happens automatically via spec `meta`) AND in any
text/body mention. Never leave the old name anywhere. Keep every screenshot
exactly as-is — screenshots are evidence and must not be altered.

### 3. Restructure professionally (do not just copy the source layout)

Typical structure — renumber cleanly, merge fragments, expand thin sections
with 3-5 sentence paragraphs:

```
1. Aim
2. Objectives            (bullets)
3. Problem Statement
4. Theory                (h2 subsections; tables for parameters/metrics)
5. Dataset / Preprocessing
6. Algorithm / Stepwise Procedure   (numbered list)
7. Implementation / Source Code     (code blocks or code screenshots)
8. Results and Discussion           (tables + figures + analysis paragraphs)
9. Challenges Encountered
10. Conclusion
(+ Viva / Key Points, Appendix if the source has them)
```

Preserve all facts, numbers, and conclusions from the source. If the source
notes a discrepancy (e.g. notebook implements a different algorithm than the
practical brief asks), keep that note explicit. Never invent results.

### 4. Write the spec JSON

Follow `references/spec-schema.md`. Key rules:

- H1/H2 numbering is written directly in the text ("4. Theory", "4.1 Bagging").
- Inline markup: `<b>`, `<i>`, `<super>`, `<sub>`, `<font face="Math">β</font>`.
  NEVER use unicode superscript digits (² ³) or math escapes — tags only.
- Greek letters and formula lines go in `formula` blocks or
  `<font face="Math">` spans.
- Tables: real `table`/`kv_table` blocks; widths sum ≤ 16.6 cm; use
  `summary_rows` for Accuracy/avg rows and `math_cols` for formula cells.
- Figures: `figure` blocks with captions "Figure N: ..." numbered in order;
  keep original screenshots unchanged; sensible `width_cm` (16 for wide,
  11-13.5 for tall portrait shots).
- Code: `code` blocks (verbatim source, raw strings).
- Content depth: paragraphs of 3-5 sentences; no section left as a bare
  heading with one line.

### 5. Generate

```bash
python <skill-dir>/scripts/make_report.py --spec spec.json --format pdf  --out 26070126510_Assignment6.pdf
python <skill-dir>/scripts/make_report.py --spec spec.json --format docx --out 26070126510_Assignment6.docx
```

Filename convention: `<PRN>_<AssignmentN>.pdf` (Roll_Ass pattern) unless the
user says otherwise. Output to the user-facing download directory.

### 6. QA before delivering (always)

- PDF: render pages `pdftoppm -png -r 50 out.pdf qa/p` and visually check:
  SIT logo centered at the top of the cover, cover fields correct, TOC page
  numbers match, no text overflow, tables fit,
  figures with captions, header/footer on body pages, no stray page breaks
  inside body flow.
- DOCX: `soffice --headless --convert-to pdf out.docx` then render/QA the
  same way (fonts will substitute metric clones; layout is what matters).
  Remind the user: in Word, right-click the TOC → "Update Field" to fill
  page numbers.
- Confirm the correct name/PRN appears on the cover and nowhere the old one.

## Non-negotiables

- The cover page layout is FIXED — see design-spec step list. Don't move
  blocks, don't change fonts/sizes. Fill only: dept, course, AY line, badge,
  title, subtitle, fields, footer.
- The SIT logo is part of the fixed cover: always place the bundled
  `assets/sit-logo.png` centered at the top of page 1, above the department
  line, 8.5 cm wide — nothing else, no other logo file, no other position.
  Only `meta.logo` (path or `null`) may change that, and only if the user
  explicitly asks.
- Page breaks only between cover → TOC → body; body flows continuously.
- Lists are left-aligned; body paragraphs justified.
- No artificial "End of report" markers; end on the last content section.
- If the user asks for a visual change, update it in ONE place
  (`references/design-spec.md` + `scripts/`) so every future report stays
  consistent.

## Files in this skill

- `scripts/make_report.py` — CLI entry (`--spec`, `--format pdf|docx`, `--out`)
- `scripts/pdf_builder.py` — ReportLab implementation (exact signature format)
- `scripts/docx_builder.py` — python-docx implementation (same design, Word-safe fonts)
- `references/spec-schema.md` — every spec field and block type
- `references/design-spec.md` — the visual system, with exact constants
- `assets/sample-spec.json` — a working example covering all block types
- `assets/sit-logo.png` — the official SIT banner baked into the cover page
