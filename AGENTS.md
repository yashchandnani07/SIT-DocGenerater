# Agent instructions

This repository is a universal agent skill: **assignment-report-formatter**.

- The skill entry point is [`SKILL.md`](SKILL.md) at the repo root (open
  [agentskills](https://agentskills.io) format — compatible with Claude Code,
  ZCode, Codex, Cursor, opencode, and any agent that reads SKILL.md files).
- Slash command (Claude Code & compatible): `/format-report <file-or-folder>`
  defined in [`.claude/commands/format-report.md`](.claude/commands/format-report.md).
- Standalone CLI (no agent needed): `pipx install .` then
  `sitfmt --spec spec.json --format pdf --out report.pdf`.

When the user asks to format, rebuild, professionalize, or make
"submission-ready" any assignment/lab report (docx or pdf), read `SKILL.md`
and follow its workflow exactly.
