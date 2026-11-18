"""Convierte un documento .md del repo en PDF con la marca de Always Up y en Word editable.

Creado el 18/11/2026 para el catálogo 2027 y el manual de producto y venta.

Uso:
    python3 documento_marca.py origen.md salida_sin_extension [--subtitulo "texto"] [--etiqueta "texto del pie"]

Genera salida.pdf (Google Chrome sin interfaz, con portada, colores y logo) y salida.docx
(python-docx, con estilos editables en Word o Pages).

Admite el Markdown que usamos en el repo: títulos #, ##, ###, párrafos, citas >, listas con - y
1. (con sangría de 2 espacios), tablas, líneas --- y negrita **...**.
"""
import argparse
import datetime as dt
import html
import os
import re
import subprocess
import tempfile

import fitz
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
LOGO = os.path.join(REPO, "02-sales", "assets", "brand", "always-up-logo-fondo-blanco.jpg")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

NAVY, RED, CREAM, INK, GREY, LIGHT = "003399", "C6272F", "F6E9C7", "1F2430", "5B6270", "EEF2FA"
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "octubre", "noviembre", "diciembre"]


# ---------- lectura del Markdown ----------
def parse(md):
    """Devuelve una lista de bloques: (tipo, datos)."""
    lines = md.splitlines()
    blocks, i = [], 0
    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if not s:
            i += 1
            continue
        if s.startswith("#"):
            n = len(s) - len(s.lstrip("#"))
            blocks.append(("h%d" % n, s[n:].strip()))
            i += 1
        elif s == "---":
            blocks.append(("hr", None))
            i += 1
        elif s.startswith(">"):
            paras, cur = [], []
            while i < len(lines) and lines[i].strip().startswith(">"):
                t = lines[i].strip()[1:].strip()
                if t:
                    cur.append(t)
                elif cur:
                    paras.append(" ".join(cur))
                    cur = []
                i += 1
            if cur:
                paras.append(" ".join(cur))
            blocks.append(("quote", paras))
        elif s.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            blocks.append(("table", rows))
        elif re.match(r"^\s*(- |\d+\. )", ln):
            items = []
            while i < len(lines) and re.match(r"^\s*(- |\d+\. )", lines[i]):
                m = re.match(r"^(\s*)(- |\d+\. )(.*)$", lines[i])
                items.append((len(m.group(1)) // 2, m.group(2) != "- ", m.group(3)))
                i += 1
            blocks.append(("list", items))
        else:
            cur = []
            while i < len(lines) and lines[i].strip() and not re.match(r"^\s*(#|>|\||- |\d+\. |---$)", lines[i]):
                cur.append(lines[i].strip())
                i += 1
            blocks.append(("p", " ".join(cur)))
    return blocks


def runs(text):
    """Trocea un texto en (fragmento, negrita)."""
    out = []
    for k, part in enumerate(re.split(r"\*\*", text)):
        if part:
            out.append((re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", part), k % 2 == 1))
    return out


def inline_html(text):
    t = html.escape(text)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
    return t


# ---------- PDF ----------
CSS = """
@page { size: A4; margin: 20mm 18mm 20mm 18mm; }
* { box-sizing: border-box; }
body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #%(INK)s; font-size: 10.2pt; line-height: 1.45; margin: 0; }
.cover { height: 252mm; display: flex; flex-direction: column; justify-content: space-between; page-break-after: always; }
.cover .top img { width: 52mm; }
.cover .band { background: #%(NAVY)s; color: white; padding: 18mm 14mm; border-radius: 4mm; border-bottom: 3mm solid #%(RED)s; }
.cover h1 { font-size: 26pt; line-height: 1.15; margin: 0 0 6mm 0; color: white; border: 0; padding: 0; }
.cover .sub { font-size: 12pt; opacity: .92; }
.cover .meta { color: #%(GREY)s; font-size: 9.5pt; border-top: 1px solid #D5DAE5; padding-top: 4mm; }
.cover .lead { background: #%(LIGHT)s; border-left: 1.6mm solid #%(NAVY)s; padding: 5mm 6mm; border-radius: 2mm; font-size: 10pt; }
.cover .lead p { margin: 0 0 2.5mm 0; } .cover .lead p:last-child { margin: 0; }
h1 { font-size: 18pt; color: #%(NAVY)s; }
h2 { font-size: 15pt; color: #%(NAVY)s; margin: 9mm 0 3mm 0; padding-bottom: 1.6mm; border-bottom: 0.7mm solid #%(RED)s; page-break-after: avoid; }
h3 { font-size: 12pt; color: #%(NAVY)s; margin: 6mm 0 2mm 0; page-break-after: avoid; }
h2.anexo { page-break-before: always; }
h3.ficha { background: #%(NAVY)s; color: white; padding: 2.2mm 3.5mm; border-radius: 1.5mm; margin-top: 7mm; }
p { margin: 0 0 2.6mm 0; }
strong { color: #%(INK)s; }
ul, ol { margin: 0 0 3mm 0; padding-left: 6mm; }
li { margin: 0 0 1.2mm 0; }
li::marker { color: #%(RED)s; }
blockquote { margin: 0 0 4mm 0; background: #%(LIGHT)s; border-left: 1.4mm solid #%(NAVY)s; padding: 3mm 5mm; border-radius: 1.5mm; }
blockquote p { margin: 0 0 1.8mm 0; } blockquote p:last-child { margin: 0; }
table { width: 100%%; border-collapse: collapse; margin: 1mm 0 4mm 0; font-size: 8.9pt; page-break-inside: auto; }
tr { page-break-inside: avoid; }
th { background: #%(NAVY)s; color: white; text-align: left; padding: 2mm 2.2mm; font-weight: 600; vertical-align: bottom; }
td { padding: 1.8mm 2.2mm; border-bottom: 0.3mm solid #D5DAE5; vertical-align: top; }
tbody tr:nth-child(even) td { background: #F7F9FD; }
table.kv td:first-child { width: 32%%; background: #%(CREAM)s; font-weight: 600; color: #%(NAVY)s; }
table.kv tr:nth-child(even) td:first-child { background: #%(CREAM)s; }
hr { border: 0; border-top: 0.3mm solid #D5DAE5; margin: 6mm 0; }
a { color: #%(NAVY)s; }
""" % dict(INK=INK, NAVY=NAVY, RED=RED, CREAM=CREAM, GREY=GREY, LIGHT=LIGHT)


def to_html(blocks, title, subtitle, fecha):
    out = []
    # portada: el título (h1) y la primera cita van en la portada
    lead = ""
    rest = list(blocks)
    if rest and rest[0][0] == "h1":
        rest = rest[1:]
    if rest and rest[0][0] == "quote":
        lead = "".join("<p>%s</p>" % inline_html(p) for p in rest[0][1])
        rest = rest[1:]
    out.append('<section class="cover"><div class="top"><img src="file://%s"></div>'
               '<div class="band"><h1>%s</h1><div class="sub">%s</div></div>'
               '<div class="lead">%s</div><div class="meta">Always Up · Quality Servix Premium SL · %s</div></section>'
               % (LOGO, inline_html(title), inline_html(subtitle), lead, fecha))
    en_anexo = False
    for kind, data in rest:
        if kind == "h2":
            cls = ""
            if data.lower().startswith("anexo"):
                cls = ' class="anexo"'
                en_anexo = True
            out.append("<h2%s>%s</h2>" % (cls, inline_html(data)))
        elif kind == "h3":
            cls = ' class="ficha"' if en_anexo and re.match(r"^[A-Z]\d+\.", data) else ""
            out.append("<h3%s>%s</h3>" % (cls, inline_html(data)))
        elif kind in ("h1", "h4"):
            out.append("<h3>%s</h3>" % inline_html(data))
        elif kind == "hr":
            continue
        elif kind == "p":
            out.append("<p>%s</p>" % inline_html(data))
        elif kind == "quote":
            out.append("<blockquote>%s</blockquote>" % "".join("<p>%s</p>" % inline_html(p) for p in data))
        elif kind == "list":
            out.append(list_html(data))
        elif kind == "table":
            head, body = data[0], data[1:]
            kv = all(not c for c in head)
            h = ['<table class="kv">' if kv else "<table>"]
            if not kv:
                h.append("<thead><tr>%s</tr></thead>" % "".join("<th>%s</th>" % inline_html(c) for c in head))
            h.append("<tbody>")
            for r in body:
                h.append("<tr>%s</tr>" % "".join("<td>%s</td>" % inline_html(c) for c in r))
            h.append("</tbody></table>")
            out.append("".join(h))
    return "<!doctype html><html lang='es'><head><meta charset='utf-8'><title>%s</title><style>%s</style></head><body>%s</body></html>" % (
        html.escape(title), CSS, "\n".join(out))


def list_html(items):
    out, stack = [], []
    for lvl, ordered, text in items:
        while len(stack) > lvl + 1:
            out.append("</li></%s>" % stack.pop())
        if len(stack) == lvl + 1:
            out.append("</li>")
        while len(stack) < lvl + 1:
            tag = "ol" if ordered else "ul"
            out.append("<%s>" % tag)
            stack.append(tag)
        out.append("<li>%s" % inline_html(text))
    while stack:
        out.append("</li></%s>" % stack.pop())
    return "".join(out)


def make_pdf(blocks, title, subtitle, fecha, etiqueta, salida):
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, "doc.html")
        open(src, "w", encoding="utf-8").write(to_html(blocks, title, subtitle, fecha))
        raw = os.path.join(tmp, "raw.pdf")
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                        "--allow-file-access-from-files", "--print-to-pdf=" + raw, "file://" + src],
                       check=True, capture_output=True, timeout=180)
        d = fitz.open(raw)
        n = d.page_count
        for k, p in enumerate(d):
            if k == 0:
                continue
            r = p.rect
            p.draw_line(fitz.Point(51, r.height - 40), fitz.Point(r.width - 51, r.height - 40), color=(0.84, 0.85, 0.9), width=0.6)
            p.insert_text(fitz.Point(51, r.height - 28), "Always Up · " + etiqueta, fontsize=7.5, color=(0.36, 0.38, 0.44))
            txt = "%d / %d" % (k + 1, n)
            w = fitz.get_text_length(txt, fontsize=7.5)
            p.insert_text(fitz.Point(r.width - 51 - w, r.height - 28), txt, fontsize=7.5, color=(0.36, 0.38, 0.44))
        d.set_metadata({"title": title, "author": "Always Up", "subject": subtitle})
        d.save(salida, garbage=4, deflate=True)
    return n


# ---------- Word ----------
def rgb(h):
    return RGBColor.from_string(h)


def shade(cell, color):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear")
    sh.set(qn("w:color"), "auto")
    sh.set(qn("w:fill"), color)
    tcPr.append(sh)


def cell_borders(table, color="D5DAE5"):
    tblPr = table._tbl.tblPr
    b = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement("w:" + edge)
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), "4")
        e.set(qn("w:color"), color)
        b.append(e)
    tblPr.append(b)


def add_runs(par, text, size=None, color=None, bold_all=False):
    for frag, bold in runs(text):
        r = par.add_run(frag)
        r.bold = bold or bold_all
        if size:
            r.font.size = Pt(size)
        if color:
            r.font.color.rgb = rgb(color)
    return par


def page_field(par):
    r = par.add_run()
    for tag, txt in (("begin", None), (None, "PAGE"), ("end", None)):
        if tag:
            f = OxmlElement("w:fldChar")
            f.set(qn("w:fldCharType"), tag)
            r._r.append(f)
        else:
            it = OxmlElement("w:instrText")
            it.set(qn("xml:space"), "preserve")
            it.text = txt
            r._r.append(it)


def make_docx(blocks, title, subtitle, fecha, etiqueta, salida):
    doc = Document()
    sec = doc.sections[0]
    sec.page_height, sec.page_width = Cm(29.7), Cm(21.0)
    for m in ("left_margin", "right_margin"):
        setattr(sec, m, Cm(1.9))
    sec.top_margin, sec.bottom_margin = Cm(1.8), Cm(1.8)

    st = doc.styles
    st["Normal"].font.name = "Arial"
    st["Normal"].font.size = Pt(10)
    st["Normal"].font.color.rgb = rgb(INK)
    st["Normal"].paragraph_format.space_after = Pt(4)
    st["Normal"].paragraph_format.line_spacing = 1.15
    for name, size, color in (("Title", 26, NAVY), ("Heading 1", 16, NAVY), ("Heading 2", 12.5, NAVY), ("Heading 3", 11, NAVY)):
        s = st[name]
        s.font.name = "Arial"
        s.font.size = Pt(size)
        s.font.bold = True
        s.font.color.rgb = rgb(color)
        rpr = s.element.get_or_add_rPr()
        fonts = rpr.find(qn("w:rFonts"))
        if fonts is None:
            fonts = OxmlElement("w:rFonts")
            rpr.append(fonts)
        for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
            fonts.set(qn(a), "Arial")
        s.paragraph_format.space_before = Pt(14 if name == "Heading 1" else 10)
        s.paragraph_format.space_after = Pt(4)
        s.paragraph_format.keep_with_next = True

    # portada
    rest = list(blocks)
    if rest and rest[0][0] == "h1":
        rest = rest[1:]
    lead = []
    if rest and rest[0][0] == "quote":
        lead = rest[0][1]
        rest = rest[1:]
    doc.add_picture(LOGO, width=Cm(5.2))
    doc.add_paragraph().paragraph_format.space_after = Pt(60)
    t = doc.add_paragraph(style="Title")
    add_runs(t, title, color=NAVY)
    sp = doc.add_paragraph()
    add_runs(sp, subtitle, size=12, color=RED)
    doc.add_paragraph().paragraph_format.space_after = Pt(30)
    for p in lead:
        q = doc.add_paragraph()
        q.paragraph_format.left_indent = Cm(0.4)
        add_runs(q, p, size=10)
    doc.add_paragraph().paragraph_format.space_after = Pt(40)
    meta = doc.add_paragraph()
    add_runs(meta, "Always Up · Quality Servix Premium SL · " + fecha, size=9, color=GREY)
    meta.runs[-1].add_break(WD_BREAK.PAGE)

    # pie con número de página
    fp = sec.footer.paragraphs[0]
    add_runs(fp, "Always Up · %s · página " % etiqueta, size=8, color=GREY)
    page_field(fp)
    sec.different_first_page_header_footer = True

    usable = sec.page_width - sec.left_margin - sec.right_margin
    for kind, data in rest:
        if kind == "h2":
            if data.lower().startswith("anexo"):
                doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
            add_runs(doc.add_paragraph(style="Heading 1"), data, color=NAVY)
        elif kind == "h3":
            add_runs(doc.add_paragraph(style="Heading 2"), data, color=NAVY)
        elif kind in ("h1", "h4"):
            add_runs(doc.add_paragraph(style="Heading 3"), data, color=NAVY)
        elif kind == "hr":
            continue
        elif kind == "p":
            add_runs(doc.add_paragraph(), data)
        elif kind == "quote":
            for p in data:
                q = doc.add_paragraph()
                q.paragraph_format.left_indent = Cm(0.5)
                add_runs(q, p, color=GREY)
        elif kind == "list":
            counters = {}
            for lvl, ordered, text in data:
                lvl = min(lvl, 2)
                if ordered:
                    counters[lvl] = counters.get(lvl, 0) + 1
                    for k in list(counters):
                        if k > lvl:
                            del counters[k]
                    p = doc.add_paragraph()
                    p.paragraph_format.left_indent = Cm(0.6 + 0.6 * lvl)
                    p.paragraph_format.first_line_indent = Cm(-0.5)
                    r = p.add_run("%d.  " % counters[lvl])
                    r.bold = True
                    r.font.color.rgb = rgb(NAVY)
                    add_runs(p, text)
                else:
                    style = "List Bullet" if lvl == 0 else "List Bullet %d" % (lvl + 1)
                    add_runs(doc.add_paragraph(style=style), text)
                p_last = doc.paragraphs[-1]
                p_last.paragraph_format.space_after = Pt(2)
        elif kind == "table":
            head, body = data[0], data[1:]
            kv = all(not c for c in head)
            rows = body if kv else [head] + body
            ncol = max(len(r) for r in rows)
            tb = doc.add_table(rows=len(rows), cols=ncol)
            tb.alignment = WD_TABLE_ALIGNMENT.CENTER
            tb.autofit = False
            cell_borders(tb)
            if kv:
                widths = [int(usable * 0.3), int(usable * 0.7)]
            else:
                lens = [max(len(r[c]) if c < len(r) else 0 for r in rows) for c in range(ncol)]
                lens = [min(max(l, 8), 60) for l in lens]
                widths = [int(usable * l / sum(lens)) for l in lens]
            for ri, r in enumerate(rows):
                for ci in range(ncol):
                    cell = tb.cell(ri, ci)
                    cell.width = widths[ci]
                    txt = r[ci] if ci < len(r) else ""
                    par = cell.paragraphs[0]
                    par.paragraph_format.space_after = Pt(1)
                    if not kv and ri == 0:
                        add_runs(par, txt, size=8.5, color="FFFFFF", bold_all=True)
                        shade(cell, NAVY)
                    elif kv and ci == 0:
                        add_runs(par, txt, size=8.5, color=NAVY, bold_all=True)
                        shade(cell, CREAM)
                    else:
                        add_runs(par, txt, size=8.5)
            if not kv:
                trPr = tb.rows[0]._tr.get_or_add_trPr()
                h = OxmlElement("w:tblHeader")
                h.set(qn("w:val"), "true")
                trPr.append(h)
            doc.add_paragraph().paragraph_format.space_after = Pt(2)
    doc.core_properties.title = title
    doc.core_properties.author = "Always Up"
    doc.save(salida)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("origen")
    ap.add_argument("salida")
    ap.add_argument("--subtitulo", default="")
    ap.add_argument("--etiqueta", default="Documento interno")
    a = ap.parse_args()
    md = open(a.origen, encoding="utf-8").read()
    blocks = parse(md)
    title = blocks[0][1] if blocks and blocks[0][0] == "h1" else os.path.basename(a.origen)
    hoy = dt.date.today()
    fecha = "%d de %s de %d" % (hoy.day, MESES[hoy.month - 1], hoy.year)
    n = make_pdf(blocks, title, a.subtitulo, fecha, a.etiqueta, a.salida + ".pdf")
    make_docx(blocks, title, a.subtitulo, fecha, a.etiqueta, a.salida + ".docx")
    print("PDF: %s.pdf (%d páginas)\nWord: %s.docx" % (a.salida, n, a.salida))


if __name__ == "__main__":
    main()
