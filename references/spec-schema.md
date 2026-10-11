# Spec JSON Schema

The spec is a single JSON file with two keys: `meta` (cover/header info) and
`sections` (ordered content blocks). One spec can render to PDF or DOCX with
identical structure.

## Top level

```json
{
  "meta": { ...cover + header fields... },
  "sections": [ ...ordered blocks... ]
}
```

## meta fields

| Field | Required | Purpose |
|---|---|---|
| `name` | yes | Student full name (cover fields table, PDF metadata author) |
| `prn` | yes | PRN / roll number |
| `assignment` | no | e.g. "Assignment 6" (cover fields table) |
| `badge` | yes | Small navy line above title, e.g. "EXPERIMENT 6" or "ASSIGNMENT 10" |
| `title` | yes | Big cover title, e.g. "Random Forest" |
| `subtitle` | yes | Italic gray subtitle under the title |
| `subtitle2` | no | Optional second subtitle line |
| `course` | no | Course name on cover + header (default "Supervised Machine Learning Lab") |
| `date` | no | Cover date, e.g. "11 October 2026" |
| `dept` | no | Override department line (default: Dept of AI & ML) |
| `ay_line` | no | Override the AY line under course (default "AY 2026-27  \|  Batch 2025-2029") |
| `footer_line` | no | Override bottom line (default "Academic Year 2026-27") |
| `fields` | no | Override the 5 cover field rows entirely: `[["Label","Value"],...]` |
| `header_left` | no | Running header left text (default "course \| AY 2026-27") |
| `header_right` | no | Running header right text (default: title) |
| `logo` | no | Cover logo: path to an image, or `null` to remove. Default: bundled `assets/sit-logo.png` at 8.5 cm wide, top of cover |

Default fields table (used when `fields` is absent) is exactly:
Name / PRN Roll No. / Assignment / Course / Date.

## sections blocks

Text fields accept inline markup: `<b>...</b>`, `<i>...</i>`,
`<super>...</super>`, `<sub>...</sub>`, and `<font face="Math">...`</font>`
(switches to a serif math font for Greek letters like β, η, μ, Σ, ξ — use for
inline formulas; superscript/subscript digits are tags, never unicode ² ³).

| type | fields | renders |
|---|---|---|
| `h1` | `text` | Numbered top-level section heading (navy, sans bold, goes in TOC) |
| `h2` | `text` | Second-level heading (goes in TOC), e.g. "4.1 Random Forest Algorithm" |
| `p` | `text` | Justified serif body paragraph |
| `lead` | `text` | Bold lead-in line (e.g. "Advantages:") |
| `bullets` | `items: [..]` | Left-aligned bullet list (never justified) |
| `numbered` | `items: [..]`, optional `start` | Numbered procedure list |
| `formula` | `text` | Centered serif formula line (Greek/sub/super safe) |
| `code` | `text` | Monospace code block, gray panel, navy left bar, splits across pages |
| `figure` | `path` (relative to spec dir ok), `caption`, optional `width_cm` (default 16) | Centered screenshot + italic caption, kept together |
| `table` | `header: [..]`, `rows: [[..]]`, `widths: [cm..]` (sum ≤ 16.6), `align: ["l"/"c"/"b"..]` (b=bold, e.g. row labels), optional `summary_rows: [idx]` (0-based data rows shaded blue), optional `math_cols: [idx]` (serif-math cells) | Navy header zebra table |
| `kv_table` | `rows: [["Key","Value"]..]`, optional `w1`, `w2` | Label/value table with striped background |
| `spacer` | optional `cm` (default 0.4) | Vertical gap |

## Conventions

- Number H1s manually in text ("1. Aim", "5. Implementation and Results") and
  H2s as "5.1 Importing the Dataset" — TOC picks up whatever text you use.
- Figure captions: "Figure 1: ..." numbered per document, in order of appearance.
- Keep table widths summing to ≤ 16.6 cm (A4 content width).
- Reference screenshots by file path; images are embedded, never linked.
