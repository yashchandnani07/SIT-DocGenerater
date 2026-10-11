# -*- coding: utf-8 -*-
"""PDF builder - institutional assignment report (signature format).

Faithful port of the format used for 26070126510_Assignment6/7/9/10/11.pdf:
double navy cover frame, TOC with dot leaders, numbered navy headings,
zebra tables, mono code blocks, figure captions, running header/footer.
"""
import os, re
from PIL import Image as PILImage
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Image, Table, TableStyle, PageBreak,
                                NextPageTemplate, KeepTogether, HRFlowable)
from reportlab.platypus.tableofcontents import TableOfContents

FD = "/usr/share/fonts/truetype"
_FALLBACKS = {
    "Sans":    [f"{FD}/english/Carlito-Regular.ttf", f"{FD}/dejavu/DejaVuSans.ttf"],
    "Sans-B":  [f"{FD}/english/Carlito-Bold.ttf", f"{FD}/dejavu/DejaVuSans-Bold.ttf"],
    "Sans-I":  [f"{FD}/english/Carlito-Italic.ttf", f"{FD}/dejavu/DejaVuSans-Oblique.ttf"],
    "Serif":   [f"{FD}/noto-serif-sc/NotoSerifSC-Regular.ttf", f"{FD}/dejavu/DejaVuSerif.ttf"],
    "Serif-B": [f"{FD}/noto-serif-sc/NotoSerifSC-Bold.ttf", f"{FD}/dejavu/DejaVuSerif-Bold.ttf"],
    "Math":    [f"{FD}/dejavu/DejaVuSerif.ttf"],
    "Mono":    [f"{FD}/dejavu/DejaVuSansMono.ttf"],
}
for n, cands in _FALLBACKS.items():
    for p in cands:
        if os.path.exists(p):
            pdfmetrics.registerFont(TTFont(n, p)); break

NAVY = HexColor("#1F3A5F"); INK = HexColor("#1A1A1A"); GRAY = HexColor("#5B6472")
RULE = HexColor("#C9CFD8"); ROWBG = HexColor("#F2F5F9"); SUMBG = HexColor("#E4EAF2")
CODEBG = HexColor("#F5F6F8")
W, H = A4
ML = MR = 2.2 * cm

def PS(name, **kw): return ParagraphStyle(name, **kw)

H1 = PS("H1", fontName="Sans-B", fontSize=14.5, leading=18, textColor=NAVY,
        spaceBefore=18, spaceAfter=7, keepWithNext=1)
H2 = PS("H2", fontName="Sans-B", fontSize=11.5, leading=15, textColor=INK,
        spaceBefore=13, spaceAfter=5, keepWithNext=1)
Body = PS("Body", fontName="Serif", fontSize=10.5, leading=16, textColor=INK,
          alignment=TA_JUSTIFY, spaceAfter=8)
Bullet = PS("Bullet", fontName="Serif", fontSize=10.5, leading=15.5, textColor=INK,
            alignment=TA_LEFT, leftIndent=18, bulletIndent=6, spaceAfter=3.5)
NumIt = PS("NumIt", fontName="Serif", fontSize=10.5, leading=15.5, textColor=INK,
           alignment=TA_LEFT, leftIndent=24, bulletIndent=6, spaceAfter=3.5)
Lead = PS("Lead", fontName="Serif-B", fontSize=10.5, leading=16, textColor=INK,
          alignment=TA_LEFT, spaceBefore=4, spaceAfter=4)
Formula = PS("Formula", fontName="Math", fontSize=10.5, leading=17, textColor=INK,
             alignment=TA_CENTER, spaceBefore=3, spaceAfter=9)
Caption = PS("Caption", fontName="Sans-I", fontSize=9, leading=12.5, textColor=GRAY,
             alignment=TA_CENTER, spaceBefore=5, spaceAfter=14)
Code = PS("Code", fontName="Mono", fontSize=7.9, leading=10.6, textColor=INK, alignment=TA_LEFT)
TOCTitle = PS("TOCTitle", fontName="Sans-B", fontSize=16, leading=20, textColor=NAVY, spaceAfter=6)
TH  = PS("TH", fontName="Sans-B", fontSize=9, leading=12, textColor=white, alignment=TA_CENTER)
TCc = PS("TCc", fontName="Serif", fontSize=9.5, leading=13, textColor=INK, alignment=TA_CENTER)
TCl = PS("TCl", fontName="Serif", fontSize=9.5, leading=13.5, textColor=INK, alignment=TA_LEFT)
TCb = PS("TCb", fontName="Serif-B", fontSize=9.5, leading=13, textColor=INK, alignment=TA_LEFT)
TCp = PS("TCp", fontName="Sans-B", fontSize=9, leading=13, textColor=NAVY, alignment=TA_LEFT)
TCm = PS("TCm", fontName="Math", fontSize=9.5, leading=13, textColor=INK, alignment=TA_CENTER)


class LabDoc(BaseDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            s = flowable.style.name
            if s in ("H1", "H2"):
                self.notify("TOCEntry", (0 if s == "H1" else 1,
                                         flowable.getPlainText(), self.page))


def _on_cover(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(NAVY)
    canvas.setLineWidth(1.6)
    canvas.rect(1.1 * cm, 1.1 * cm, W - 2.2 * cm, H - 2.2 * cm)
    canvas.setLineWidth(0.5)
    canvas.rect(1.32 * cm, 1.32 * cm, W - 2.64 * cm, H - 2.64 * cm)
    canvas.restoreState()


def _make_on_body(header_left, header_right):
    def on_body(canvas, doc):
        canvas.saveState()
        canvas.setFont("Sans", 8.5); canvas.setFillColor(GRAY)
        canvas.drawString(ML, H - 1.55 * cm, header_left)
        canvas.drawRightString(W - MR, H - 1.55 * cm, header_right)
        canvas.setStrokeColor(RULE); canvas.setLineWidth(0.6)
        canvas.line(ML, H - 1.78 * cm, W - MR, H - 1.78 * cm)
        canvas.line(ML, 1.55 * cm, W - MR, 1.55 * cm)
        canvas.setFont("Sans", 8.5)
        canvas.drawCentredString(W / 2.0, 1.12 * cm, "Page %d" % doc.page)
        canvas.restoreState()
    return on_body


def _default_logo():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        os.pardir, "assets", "sit-logo.png")


def cover_flowables(meta):
    dept = meta.get("dept", "DEPARTMENT OF ARTIFICIAL INTELLIGENCE &amp; MACHINE LEARNING")
    ay = meta.get("ay_line", "AY 2026-27  |  Batch 2025-2029")
    footer = meta.get("footer_line", "Academic Year 2026-27")
    logo = meta.get("logo", _default_logo())
    c = PS("c", fontName="Sans-B", fontSize=10.5, leading=14, textColor=GRAY, alignment=TA_CENTER)
    s = []
    s.append(Spacer(1, 0.55 * cm))
    if logo:
        s.append(_img(logo, 8.5))
        s.append(Spacer(1, 0.5 * cm))
    s.append(Paragraph(dept, c))
    s.append(Spacer(1, 0.35 * cm))
    s.append(HRFlowable(width="38%", thickness=1.1, color=NAVY))
    s.append(Spacer(1, 1.5 * cm))
    s.append(Paragraph(meta.get("course", "Supervised Machine Learning Lab"),
             PS("c2", fontName="Sans-B", fontSize=21, leading=26, textColor=INK, alignment=TA_CENTER)))
    s.append(Spacer(1, 0.28 * cm))
    s.append(Paragraph(ay, PS("c3", fontName="Sans", fontSize=11, leading=14,
                              textColor=GRAY, alignment=TA_CENTER)))
    s.append(Spacer(1, 2.0 * cm))
    s.append(Paragraph(meta["badge"], PS("c4", fontName="Sans-B", fontSize=12.5, leading=16,
                                         textColor=NAVY, alignment=TA_CENTER)))
    s.append(Spacer(1, 0.3 * cm))
    s.append(Paragraph(meta["title"], PS("c5", fontName="Sans-B", fontSize=28, leading=34,
                                         textColor=INK, alignment=TA_CENTER)))
    s.append(Spacer(1, 0.42 * cm))
    s.append(Paragraph(meta["subtitle"], PS("c6", fontName="Sans-I", fontSize=12, leading=16,
                                            textColor=GRAY, alignment=TA_CENTER)))
    if meta.get("subtitle2"):
        s.append(Spacer(1, 0.35 * cm))
        s.append(Paragraph(meta["subtitle2"], PS("c6b", fontName="Sans-I", fontSize=10.5,
                                                 leading=14, textColor=GRAY, alignment=TA_CENTER)))
    s.append(Spacer(1, 2.0 * cm))
    fld = PS("fld", fontName="Sans-B", fontSize=10.5, leading=15, textColor=NAVY)
    fval = PS("fval", fontName="Serif", fontSize=11, leading=15, textColor=INK)
    fields = meta.get("fields") or [
        ("Name", meta["name"]), ("PRN / Roll No.", meta["prn"]),
        ("Assignment", meta.get("assignment", "")),
        ("Course", meta.get("course", "Supervised Machine Learning Lab")),
        ("Date", meta.get("date", "")),
    ]
    rows = [[Paragraph(k, fld), Paragraph(v, fval)] for k, v in fields]
    ft = Table(rows, colWidths=[4.6 * cm, 8.6 * cm])
    ft.setStyle(TableStyle([
        ("LINEABOVE", (0, 0), (-1, 0), 1.0, NAVY),
        ("LINEBELOW", (0, 0), (-1, -2), 0.4, RULE),
        ("LINEBELOW", (0, -1), (-1, -1), 1.0, NAVY),
        ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ]))
    s.append(ft)
    s.append(Spacer(1, 1.5 * cm))
    s.append(Paragraph(footer, PS("c7", fontName="Sans", fontSize=9.5, leading=13,
                                  textColor=GRAY, alignment=TA_CENTER)))
    s.append(NextPageTemplate("body"))
    s.append(PageBreak())
    return s


def toc_block():
    toc = TableOfContents()
    toc.levelStyles = [
        PS("TOC0", fontName="Sans-B", fontSize=10.5, leading=17, textColor=INK, leftIndent=2),
        PS("TOC1", fontName="Serif", fontSize=10, leading=15, textColor=INK, leftIndent=18),
    ]
    toc.dotsMinLevel = 0
    return [Paragraph("Table of Contents", TOCTitle),
            HRFlowable(width="100%", thickness=1.0, color=NAVY, spaceAfter=14), toc, PageBreak()]


def _img(path, width_cm):
    pw, ph = PILImage.open(path).size
    wd = width_cm * cm
    return Image(path, width=wd, height=wd * ph / pw)


def _code_block(code_text):
    lines = code_text.rstrip().split("\n")
    rows = []
    for ln in lines:
        esc = ln.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        esc = re.sub(r"^ +", lambda m: "\u00a0" * len(m.group()), esc)
        rows.append([Paragraph(esc if esc.strip() else "\u00a0", Code)])
    t = Table(rows, colWidths=[16.6 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CODEBG),
        ("BOX", (0, 0), (-1, -1), 0.5, RULE),
        ("LINEBEFORE", (0, 0), (0, -1), 2.2, NAVY),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 0.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 0.4),
    ]))
    return t


def _data_table(header, rows, widths_cm, aligns, summary_rows=None, math_cols=None):
    math_cols = math_cols or []
    summary_rows = set(summary_rows or [])
    data = [[Paragraph(h, TH) for h in header]]
    for ri, r in enumerate(rows):
        line = []
        for ci, cell in enumerate(r):
            if ri in summary_rows:
                sty = TCb
            elif ci in math_cols:
                sty = TCm
            else:
                sty = TCc if aligns[ci] == "c" else (TCb if aligns[ci] == "b" else TCl)
            line.append(Paragraph(str(cell), sty))
        data.append(line)
    t = Table(data, colWidths=[w * cm for w in widths_cm], repeatRows=1)
    st = [("BACKGROUND", (0, 0), (-1, 0), NAVY),
          ("GRID", (0, 0), (-1, -1), 0.4, RULE),
          ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
          ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
          ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7)]
    if summary_rows:
        st.append(("ROWBACKGROUNDS", (0, 1), (-1, max(1, min(summary_rows) - 1)), [white, ROWBG]))
        for ri in sorted(summary_rows):
            st.append(("BACKGROUND", (0, ri + 1), (-1, ri + 1), SUMBG))
    else:
        st.append(("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, ROWBG]))
    t.setStyle(TableStyle(st))
    return t


def _kv_table(pairs, w1, w2):
    rows = [[Paragraph(k, TCp), Paragraph(str(v), TCb)] for k, v in pairs]
    t = Table(rows, colWidths=[w1 * cm, w2 * cm])
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, RULE),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [ROWBG, white]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8)]))
    return t


def render_blocks(blocks):
    """Convert spec blocks into ReportLab flowables."""
    out = []
    for b in blocks:
        ty = b["type"]
        if ty == "h1":
            out.append(Paragraph(b["text"], H1))
        elif ty == "h2":
            out.append(Paragraph(b["text"], H2))
        elif ty == "p":
            out.append(Paragraph(b["text"], Body))
        elif ty == "lead":
            out.append(Paragraph(b["text"], Lead))
        elif ty == "bullets":
            out.extend(Paragraph(x, Bullet, bulletText="\u2022") for x in b["items"])
            out.append(Spacer(1, 4))
        elif ty == "numbered":
            start = b.get("start", 1)
            out.extend(Paragraph(x, NumIt, bulletText="%d." % i)
                       for i, x in enumerate(b["items"], start))
            out.append(Spacer(1, 4))
        elif ty == "formula":
            out.append(Paragraph(b["text"], Formula))
        elif ty == "spacer":
            out.append(Spacer(1, b.get("cm", 0.4) * cm))
        elif ty == "code":
            out.append(_code_block(b["text"])); out.append(Spacer(1, 10))
        elif ty == "figure":
            out.append(KeepTogether([_img(b["path"], b.get("width_cm", 16.0)),
                                     Paragraph(b["caption"], Caption)]))
        elif ty == "table":
            out.append(_data_table(b["header"], b["rows"], b.get("widths", []),
                                   b.get("align", ["l"] * len(b["header"])),
                                   b.get("summary_rows"), b.get("math_cols")))
            out.append(Spacer(1, 10))
        elif ty == "kv_table":
            w1 = b.get("w1", 6.0); w2 = b.get("w2", 10.6)
            out.append(_kv_table(b["rows"], w1, w2)); out.append(Spacer(1, 10))
        else:
            raise ValueError("unknown block type: %s" % ty)
    return out


def build_pdf(spec, out_path):
    meta = spec["meta"]
    doc = LabDoc(out_path, pagesize=A4, leftMargin=ML, rightMargin=MR,
                 topMargin=2.3 * cm, bottomMargin=2.0 * cm,
                 title=meta["title"], author="%s (%s)" % (meta["name"], meta["prn"]))
    cover_frame = Frame(2.6 * cm, 2.4 * cm, W - 5.2 * cm, H - 4.8 * cm, id="cover")
    body_frame = Frame(ML, 2.0 * cm, W - ML - MR, H - 2.3 * cm - 2.0 * cm, id="body")
    hl = meta.get("header_left", "%s  |  %s" % (meta.get("course", ""), "AY 2026-27"))
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_frame], onPage=_on_cover),
        PageTemplate(id="body", frames=[body_frame],
                     onPage=_make_on_body(hl, meta.get("header_right", meta["title"]))),
    ])
    story = cover_flowables(meta) + toc_block() + render_blocks(spec["sections"])
    doc.multiBuild(story)
    return out_path
