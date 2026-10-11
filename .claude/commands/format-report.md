---
description: Format an assignment/lab report into the SIT institutional PDF or DOCX format
argument-hint: [file-or-folder] (--docx)
---

Use the **assignment-report-formatter** skill in this repository (see `SKILL.md` at the repo root) to format $ARGUMENTS into a submission-ready academic report.

Follow the skill's full workflow: extract the content from the uploaded/pointed DOCX or PDF, replace the student identity, restructure into the standard sections, write a spec JSON, and generate the output.

- Target format: PDF, unless the user passed `--docx`, in which case DOCX.
- Filename: `<PRN>_<AssignmentN>.<ext>` unless the user says otherwise.
- The SIT logo banner is baked into the cover — do not remove or reposition it.
- Run the skill's QA pass (render pages, check cover/TOC/overflow) before delivering.
