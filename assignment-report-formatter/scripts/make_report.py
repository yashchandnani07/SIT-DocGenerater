#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_report.py - one-command report generator.

Usage:
  python make_report.py --spec spec.json --format pdf  --out report.pdf
  python make_report.py --spec spec.json --format docx --out report.docx

Spec format: see references/spec-schema.md in this skill.
"""
import argparse, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    ap = argparse.ArgumentParser(description="Institutional assignment report generator")
    ap.add_argument("--spec", required=True, help="path to spec JSON")
    ap.add_argument("--format", choices=["pdf", "docx"], default="pdf")
    ap.add_argument("--out", required=True, help="output file path")
    args = ap.parse_args()

    with open(args.spec, encoding="utf-8") as f:
        spec = json.load(f)

    # resolve relative image paths against the spec file's directory
    base = os.path.dirname(os.path.abspath(args.spec))
    for blk in spec.get("sections", []):
        if blk.get("type") == "figure" and blk.get("path") and not os.path.isabs(blk["path"]):
            blk["path"] = os.path.join(base, blk["path"])

    if args.format == "pdf":
        import pdf_builder
        out = pdf_builder.build_pdf(spec, args.out)
    else:
        import docx_builder
        out = docx_builder.build_docx(spec, args.out)
    print("OK ->", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
