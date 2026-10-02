#!/usr/bin/env python3
"""Genera una propuesta escrita de Always Up (PDF con marca) a partir de una ficha JSON.

Uso:
    python3 generar_propuesta.py ejemplos/team_experience_ejemplo.json
    python3 generar_propuesta.py mi_cliente.json -o ../../01-clients/propuestas/mi_cliente.pdf

Servicios (campo "servicio"): team | coach | camp | becas | programa
Dependencias: pip install reportlab pillow numpy
Los presets (qué incluye, qué no incluye, términos) están en PRESETS: revisarlos antes del primer uso real.
"""
import argparse, io, json, os, sys
import numpy as np
from PIL import Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table,
                                TableStyle, KeepTogether)

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(HERE, "..", "..", "02-sales", "assets", "brand", "always-up-logo-fondo-blanco.jpg")
NAVY = colors.HexColor("#003399"); RED = colors.HexColor("#C6272F"); CREAM = colors.HexColor("#F6E9C7")
INK = colors.HexColor("#1F2430"); GREY = colors.HexColor("#5B6270"); LIGHT = colors.HexColor("#EEF2FA")
W, H = A4; M = 40

PRESETS = {
    "team": {
        "titulo": "Team Experience",
        "includes": [
            "Daily training sessions led by official academy coaches, adapted to your age stage and level",
            "Friendly matches against academy teams and local sides, with official referees",
            "Formative sessions (methodology, nutrition, player psychology)",
            "Stadium and club museum visit; first-team or academy match viewing when the calendar allows",
            "Full-board accommodation in the club residence or a hotel near the facilities",
            "All local transfers in authorised buses and assistance in your language throughout",
            "A single Always Up point of contact before, during and after the trip",
        ],
        "not_included": ["International flights", "Personal health and travel insurance of each participant", "Visas, where applicable", "Optional international tournament fees"],
        "steps": [("Confirmation", "You confirm dates and group size in writing."), ("Club agenda", "We close the programme with the host club."),
                  ("Logistics", "Residence, transfers and schedule confirmed."), ("Experience", "We are with you on site, and review the trip afterwards.")],
    },
    "coach": {
        "titulo": "Coach Experience",
        "includes": [
            "Observation of academy training sessions across age groups, accompanied by a club representative who speaks your language",
            "Masterclasses with the club's departments (methodology, physical preparation, game analysis, individual development, club values)",
            "Academy match viewing and, when dates coincide, a first-team match",
            "Stadium and museum tour",
            "Accommodation, meals, private transport and assistance in your language",
            "Certificate of participation",
        ],
        "not_included": ["International flights", "Personal health and travel insurance", "Visas, where applicable"],
        "steps": [("Confirmation", "You confirm dates and staff list."), ("Club agenda", "We close sessions and masterclasses with the club."),
                  ("Logistics", "Accommodation, transport and schedule confirmed."), ("Experience", "We accompany your staff and review the trip afterwards.")],
    },
    "camp": {
        "titulo": "International Camp",
        "includes": [
            "Official academy coaches travelling to your facilities (number according to the option selected)",
            "5-6 day camp following the club's methodology, up to 8 hours of activity per day",
            "Official participation diploma for every player and an official first-team shirt for the camp week",
            "Club micro-site with a link to your registration page; official graphic templates for promotion",
            "Coordination of the programme and the relationship with the club from Always Up",
        ],
        "not_included": ["Flights, hotel (3-star minimum, full board), transfers, travel insurance and visas of the club's staff (borne by the promoter)",
                         "Official Nike kit for participants (priced per player)", "Local coaches, venue, promotion, registrations and player insurance (borne by the promoter)"],
        "steps": [("Due diligence", "Company, venue and child-protection documentation reviewed by the club."), ("Approval & contract", "The Academy and its Compliance department approve; contract and 50% payment."),
                  ("Promotion", "Registrations open with club-approved material; kit order 45+ days before."), ("Camp", "Final payment before the start; the club's coaches run the camp.")],
        "terms": ["The project is subject to the approval of the club's Academy management and Compliance department.",
                  "All promotional material must be approved by the club before publication.",
                  "The camp is promoted as a formative and recreational programme, never as an access route to the Academy."],
    },
    "becas": {
        "titulo": "USA Scholarship Pathway",
        "includes": [
            "Athletic evaluation of the player's profile and video",
            "Personalised athletic resume",
            "Direct communication with college and high-school coaches matched to the player's profile",
            "Management of academic and administrative requirements",
            "Visa and admission support",
            "Identification of scholarship opportunities that fit the player's level, academics and budget",
        ],
        "not_included": ["Tuition, accommodation and living costs at the US institution (they depend on the scholarship obtained)", "Flights and visa fees", "Language and admission exam fees"],
        "steps": [("Evaluation", "We review video, level and academic record."), ("Profile", "We build the athletic resume and target list."),
                  ("Coach contact", "We communicate directly with coaches."), ("Offers & admission", "We support the decision, admission and visa.")],
        "terms": ["No scholarship, placement or admission is guaranteed: the outcome depends on the player's level, academic record and coaches' interest."],
    },
    "programa": {
        "titulo": "Real Sociedad International Residential Programme",
        "includes": [
            "Training with the same methodology as Real Sociedad's academy at the Zubieta complex (4-5 sessions per week, around 12 hours)",
            "Weekly individual video analysis and periodic progress reports",
            "Accommodation and meals at the Olarain residence in San Sebastian",
            "Academic support and Spanish language classes",
            "Cultural and city orientation programme",
        ],
        "not_included": ["International flights", "Personal health and travel insurance unless stated", "Visa fees, where applicable"],
        "steps": [("Application", "Football CV, academic history and motivation."), ("Evaluation", "Review of the player's profile and video."),
                  ("Confirmation", "Format and dates agreed in writing."), ("Arrival", "Welcome, residence and first week orientation.")],
        "terms": ["Admission to the programme is subject to evaluation of the player's profile."],
    },
}

def S(name, **kw):
    d = dict(fontName="Helvetica", fontSize=10, leading=14.2, textColor=INK); d.update(kw); return ParagraphStyle(name, **d)
BODY = S("b"); SMALL = S("s", fontSize=8.5, leading=11.6, textColor=GREY)
H2 = S("h2", fontName="Helvetica-Bold", fontSize=13.5, leading=17, textColor=NAVY, spaceBefore=14, spaceAfter=6)
BUL = S("bul", leftIndent=14, bulletIndent=0, spaceAfter=3)

def logo_reader():
    im = Image.open(LOGO_PATH).convert("RGB"); a = np.array(im); m = (a.sum(axis=2) < 255*3-15); ys, xs = np.where(m)
    im = im.crop((max(xs.min()-15, 0), max(ys.min()-15, 0), min(xs.max()+15, im.width), min(ys.max()+15, im.height)))
    b = io.BytesIO(); im.save(b, "PNG"); b.seek(0); return ImageReader(b), im.height/im.width

def bullets(items, color=RED):
    return [Paragraph(f"<font color='{color.hexval()}'>&#9632;</font>&nbsp;&nbsp;{t}", BUL) for t in items]

def money(v, cur):
    return f"{cur}{v:,.0f}".replace(",", ".") if cur == "€" else f"{cur}{v:,.0f}"

def build(spec, out):
    key = spec["servicio"]; pre = PRESETS[key]
    cur = spec.get("moneda", "€"); logo, lr = logo_reader()
    titulo = spec.get("titulo_programa") or pre["titulo"]
    includes = spec.get("incluye") or pre["includes"]
    not_inc = spec.get("no_incluye") or pre["not_included"]
    steps = spec.get("pasos") or pre["steps"]
    terms = (pre.get("terms") or []) + spec.get("terminos_extra", [])

    def page(c, doc):
        c.saveState()
        c.drawImage(logo, M, H-M-44, 62, 62*lr, mask="auto")
        c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 9.5); c.drawRightString(W-M, H-M-8, "PROPOSAL")
        c.setFillColor(GREY); c.setFont("Helvetica", 8.5); c.drawRightString(W-M, H-M-20, f"{titulo}  |  {spec['cliente']}")
        c.setStrokeColor(NAVY); c.setLineWidth(1); c.line(M, H-M-48, W-M, H-M-48)
        c.setFillColor(NAVY); c.rect(0, 0, W, 30, stroke=0, fill=1); c.setFillColor(RED); c.rect(0, 30, W, 2.4, stroke=0, fill=1)
        c.setFillColor(colors.white); c.setFont("Helvetica", 8.2)
        c.drawString(M, 11, "Always Up  |  joel.martinez@alwaysup.es  |  +1 (814) 329 1929  |  alwaysup.es")
        c.drawRightString(W-M, 11, f"Page {doc.page}")
        c.restoreState()

    doc = BaseDocTemplate(out, pagesize=A4, leftMargin=M, rightMargin=M, topMargin=M+60, bottomMargin=48,
                          title=f"Always Up - Proposal - {spec['cliente']}", author="Always Up")
    doc.addPageTemplates([PageTemplate(id="p", frames=[Frame(M, 48, W-2*M, H-48-(M+60), id="f", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)], onPage=page)])
    st = []
    st.append(Paragraph(titulo, S("t", fontName="Helvetica-Bold", fontSize=26, leading=30, textColor=NAVY)))
    st.append(Paragraph(f"Prepared for <b>{spec['cliente']}</b>", S("t2", fontSize=12, leading=17, textColor=RED, fontName="Helvetica-Bold", spaceBefore=4)))
    meta = [["Date", spec["fecha"]], ["Valid until", spec.get("validez", "30 days from the date above")], ["Prepared by", "Joel Martinez, Always Up"]]
    mt = Table(meta, colWidths=[70, 200]); mt.setStyle(TableStyle([("FONT", (0, 0), (0, -1), "Helvetica-Bold", 8.8), ("FONT", (1, 0), (1, -1), "Helvetica", 8.8),
                                                               ("TEXTCOLOR", (0, 0), (0, -1), GREY), ("TOPPADDING", (0, 0), (-1, -1), 1), ("BOTTOMPADDING", (0, 0), (-1, -1), 1), ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
    st += [Spacer(1, 6), mt]
    st.append(Paragraph("Your objective", H2)); st.append(Paragraph(spec["objetivo"], BODY))
    st.append(Paragraph("What we propose", H2)); st.append(Paragraph(spec["propuesta"], BODY))
    ficha = spec.get("datos", [])
    if ficha:
        t = Table([[k, v] for k, v in ficha], colWidths=[110, W-2*M-110])
        t.setStyle(TableStyle([("FONT", (0, 0), (0, -1), "Helvetica-Bold", 9), ("FONT", (1, 0), (1, -1), "Helvetica", 9), ("TEXTCOLOR", (0, 0), (0, -1), NAVY),
                               ("BACKGROUND", (0, 0), (-1, -1), LIGHT), ("LINEBELOW", (0, 0), (-1, -2), 0.4, colors.white),
                               ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5), ("LEFTPADDING", (0, 0), (-1, -1), 8)]))
        st += [Spacer(1, 6), t]
    st.append(Paragraph("What is included", H2)); st += bullets(includes)
    st.append(Paragraph("Not included", H2)); st += bullets(not_inc, GREY)
    if spec.get("programa_detalle"):
        st.append(Paragraph("Programme", H2)); st += bullets(spec["programa_detalle"])
    # investment
    inv = [[Paragraph("<b>Item</b>", S("th", fontSize=9, textColor=colors.white)), Paragraph("<b>Detail</b>", S("th2", fontSize=9, textColor=colors.white)),
            Paragraph("<b>Amount</b>", S("th3", fontSize=9, textColor=colors.white, alignment=2))]]
    total = 0
    for it in spec["precio"]["lineas"]:
        amt = it["importe"]; total += amt if it.get("suma", True) else 0
        inv.append([Paragraph(it["concepto"], S("c1", fontSize=9.2)), Paragraph(it.get("detalle", ""), S("c2", fontSize=8.6, textColor=GREY)),
                    Paragraph(money(amt, cur), S("c3", fontSize=9.2, alignment=2))])
    if spec["precio"].get("mostrar_total", True):
        inv.append([Paragraph("<b>Total</b>", S("tt", fontSize=10)), "", Paragraph(f"<b>{money(total, cur)}</b>", S("tt2", fontSize=10.5, alignment=2, textColor=RED))])
    it_ = Table(inv, colWidths=[170, W-2*M-170-90, 90], repeatRows=1)
    it_.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), NAVY), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
                             ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6), ("LEFTPADDING", (0, 0), (-1, -1), 8),
                             ("LINEBELOW", (0, -1), (-1, -1), 1, NAVY)]))
    blk = [Paragraph("Investment", H2), it_]
    if spec["precio"].get("nota"): blk += [Spacer(1, 4), Paragraph(spec["precio"]["nota"], SMALL)]
    if spec["precio"].get("pago"): blk += [Spacer(1, 4), Paragraph(f"<b>Payment:</b> {spec['precio']['pago']}", S("pg", fontSize=9.2))]
    st.append(KeepTogether(blk))
    st.append(Paragraph("How it works from here", H2))
    sw = (W-2*M-3*8)/4; cells = []
    for i, (t, b) in enumerate(steps):
        cells.append(Paragraph(f"<font color='{RED.hexval()}'><b>{i+1}</b></font>&nbsp;<b>{t}</b><br/><font size=8.4 color='#5B6270'>{b}</font>", S("sp", fontSize=9.4, leading=12.6)))
    stt = Table([cells], colWidths=[sw]*4, hAlign="LEFT"); stt.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
                                                                                  ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 6), ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                                                                                  ("LINEAFTER", (0, 0), (-2, -1), 3, colors.white)]))
    st.append(stt)
    if terms:
        st.append(Paragraph("Conditions", H2)); st += bullets(terms, GREY)
    nxt = Table([[Paragraph(f"<font color='white'><b>Next step:</b> {spec['siguiente_paso']}</font>", S("n", fontSize=10.8, leading=15, textColor=colors.white))]], colWidths=[W-2*M])
    nxt.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), RED), ("TOPPADDING", (0, 0), (-1, -1), 11), ("BOTTOMPADDING", (0, 0), (-1, -1), 11), ("LEFTPADDING", (0, 0), (-1, -1), 14)]))
    st += [Spacer(1, 16), KeepTogether([nxt]), Spacer(1, 8),
           Paragraph("Any question before then, just reply to this message. <b>Joel Martinez</b> · Always Up · joel.martinez@alwaysup.es · +1 (814) 329 1929", SMALL)]
    doc.build(st); return out

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("spec"); ap.add_argument("-o", "--out")
    a = ap.parse_args(); spec = json.load(open(a.spec, encoding="utf-8"))
    out = a.out or os.path.join(HERE, "..", "..", "01-clients", "propuestas", f"propuesta_{spec['cliente'].lower().replace(' ', '_')}.pdf")
    os.makedirs(os.path.dirname(out), exist_ok=True); print(build(spec, out))
