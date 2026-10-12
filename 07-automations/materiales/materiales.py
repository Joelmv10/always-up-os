#!/usr/bin/env python3
"""Genera los materiales de venta de Always Up (PDF con marca).

Uso:
    python3 preparar_imagenes.py        # una vez (o cuando cambien los PDFs fuente)
    python3 materiales.py fichas        # Team y Coach Experience
    python3 materiales.py deck          # deck de empresa: versión completa (envío 1 a 1) y pública (LinkedIn)
    python3 materiales.py todo

Salida: 02-sales/assets/. La versión pública del deck no lleva fotos de equipos con menores identificables.
Dependencias: pip install reportlab pillow numpy
"""
import io, os, sys
import numpy as np
from PIL import Image, ImageOps
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, ".cache"); IM = os.path.join(CACHE, "imgs"); NW = os.path.join(CACHE, "new")
OUTDIR = os.path.abspath(os.path.join(HERE, "..", "..", "02-sales", "assets"))
LOGO_PATH = os.path.abspath(os.path.join(OUTDIR, "brand", "always-up-logo-fondo-blanco.jpg"))
CAL = "calendly.com/joel-martinez-alwaysup/always-up-assessment-call"

NAVY = colors.HexColor("#003399"); RED = colors.HexColor("#C6272F"); CREAM = colors.HexColor("#F6E9C7")
INK = colors.HexColor("#1F2430"); GREY = colors.HexColor("#5B6270"); LIGHT = colors.HexColor("#EEF2FA")
T_TRAIN = colors.HexColor("#DCE6F8"); T_MATCH = colors.HexColor("#FADCDD"); T_CLUB = colors.HexColor("#F6E9C7")
T_MEAL = colors.HexColor("#EFEFEF"); T_TRAVEL = colors.HexColor("#E6E6E6")
TCOL = {"train": T_TRAIN, "match": T_MATCH, "club": T_CLUB, "meal": T_MEAL, "travel": T_TRAVEL}

# ------------------------------------------------------------------ utilidades comunes
def fit(path, w, h, focus=(0.5, 0.5), scale=3):
    im = Image.open(path).convert("RGB"); im = ImageOps.exif_transpose(im)
    im = ImageOps.fit(im, (int(w*scale), int(h*scale)), Image.LANCZOS, centering=focus)
    b = io.BytesIO(); im.save(b, "JPEG", quality=88); b.seek(0); return ImageReader(b)

def _logo():
    im = Image.open(LOGO_PATH).convert("RGB"); a = np.array(im); mk = a.sum(axis=2) < 255*3-15; ys, xs = np.where(mk)
    im = im.crop((max(xs.min()-15, 0), max(ys.min()-15, 0), min(xs.max()+15, im.width), min(ys.max()+15, im.height)))
    b = io.BytesIO(); im.save(b, "PNG"); b.seek(0); return ImageReader(b), im.height/im.width
LOGO, LOGO_R = _logo()
CREST_FILES = [f"{CACHE}/crest_atm_t.png", f"{CACHE}/crest_rs_t.png", f"{CACHE}/crest_sporting.png"]
CRESTS = [ImageReader(p) for p in CREST_FILES]; CREST_SZ = [Image.open(p).size for p in CREST_FILES]

def sty(name, **kw):
    d = dict(fontName="Helvetica", fontSize=10, leading=14, textColor=INK, alignment=TA_LEFT); d.update(kw); return ParagraphStyle(name, **d)

def para(c, text, style, x, y_top, w):
    p = Paragraph(text, style); _, h = p.wrap(w, 3000); p.drawOn(c, x, y_top-h); return h

def gradient_photo(path, w, h, focus, g0, g1, scale=3, strength=0.95):
    base = Image.open(path).convert("RGB"); base = ImageOps.exif_transpose(base)
    base = ImageOps.fit(base, (int(w*scale), int(h*scale)), Image.LANCZOS, centering=focus)
    arr = np.array(base).astype(float); t = np.linspace(0, 1, arr.shape[0])[:, None]
    al = (np.clip((t-g0)/(g1-g0), 0, 1)**1.15)*strength; navy = np.array([0, 20, 78.])
    arr = arr*(1-al[..., None]) + navy*al[..., None]
    o = Image.fromarray(arr.astype("uint8")); bb = io.BytesIO(); o.save(bb, "JPEG", quality=90); bb.seek(0); return ImageReader(bb)

# ================================================================== FICHAS (A4 vertical)
W, H = A4; M = 36
BODY = sty("b", fontSize=9.9, leading=14.2); SMALL = sty("s", fontSize=8.3, leading=11.4, textColor=GREY)
CARD_T = sty("ct", fontName="Helvetica-Bold", fontSize=10.3, leading=13, textColor=NAVY); CARD_B = sty("cb", fontSize=8.9, leading=12.3)

def f_h2(c, text, y_top):
    c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 13.5); c.drawString(M, y_top-14, text); return y_top-26

def f_logo(c, x, y_top, w):
    h = w*LOGO_R; c.drawImage(LOGO, x, y_top-h, w, h, mask="auto")

def f_crest_row(c, y_top, label):
    c.setFont("Helvetica-Bold", 7.8); c.setFillColor(GREY); c.drawString(M, y_top-8, label)
    x = M; hh = 34
    for img, (iw, ih) in zip(CRESTS, CREST_SZ):
        w = hh*iw/ih; c.drawImage(img, x, y_top-14-hh, w, hh, mask="auto"); x += w+16
    return y_top-14-hh

def f_chips(c, y_top, labels):
    x = M; y = y_top-18; c.setFont("Helvetica-Bold", 8.2)
    for lb in labels:
        w = c.stringWidth(lb, "Helvetica-Bold", 8.2)+18
        c.setFillColor(LIGHT); c.setStrokeColor(NAVY); c.setLineWidth(0.7); c.roundRect(x, y, w, 18, 9, stroke=1, fill=1)
        c.setFillColor(NAVY); c.drawString(x+9, y+5.6, lb); x += w+7
    return y-6

def f_footer(c):
    c.setFillColor(NAVY); c.rect(0, 0, W, 32, stroke=0, fill=1); c.setFillColor(RED); c.rect(0, 32, W, 2.4, stroke=0, fill=1)
    c.setFillColor(colors.white); c.setFont("Helvetica", 8.3)
    c.drawString(M, 12, "Always Up  |  joel.martinez@alwaysup.es  |  +1 (814) 329 1929  |  alwaysup.es")

def f_hero(c, img, title, tagline, focus, hh=300, g0=0.30, g1=1.0, tb=84):
    c.drawImage(gradient_photo(img, W, hh, focus, g0, g1), 0, H-hh, W, hh)
    c.setFillColor(colors.white); c.roundRect(M-8, H-90, 116, 72, 6, stroke=0, fill=1); f_logo(c, M-2, H-23, 104)
    c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 31); c.drawString(M, H-hh+tb, title)
    p = Paragraph(tagline, sty("tg", fontSize=11.8, leading=16, textColor=CREAM)); _, ph = p.wrap(W-2*M-30, 100); p.drawOn(c, M, H-hh+tb-12-ph)
    return H-hh

def f_bullets(c, items, y_top, gap=5):
    y = y_top
    for head, body in items:
        c.setFillColor(RED); c.rect(M, y-10, 5.5, 5.5, stroke=0, fill=1)
        h = para(c, f"<b>{head}</b> {body}" if head else body, BODY, M+15, y, W-2*M-15); y -= h+gap
    return y

def f_card(c, x, y_top, w, h, title, body):
    c.setFillColor(LIGHT); c.roundRect(x, y_top-h, w, h, 5, stroke=0, fill=1); c.setFillColor(RED); c.rect(x, y_top-h, 3.5, h, stroke=0, fill=1)
    ht = para(c, title, CARD_T, x+13, y_top-10, w-22); para(c, body, CARD_B, x+13, y_top-13-ht, w-22)

def f_photo_row(c, items, y_top, h, label=None, gap=6):
    n = len(items); w = (W-2*M-gap*(n-1))/n
    if label:
        c.setFont("Helvetica-Bold", 7.8); c.setFillColor(GREY); c.drawString(M, y_top-8, label); y_top -= 12
    for i, (path, cap, focus) in enumerate(items):
        x = M+i*(w+gap); c.drawImage(fit(path, w, h, focus), x, y_top-h, w, h)
        if cap:
            c.setFillColor(colors.Color(0, 0.08, 0.3, alpha=0.78)); c.rect(x, y_top-h, w, 15, stroke=0, fill=1)
            c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 7); c.drawString(x+5, y_top-h+4.6, cap)
    return y_top-h

def f_quote(c, y_top, h, q, src):
    c.setFillColor(NAVY); c.roundRect(M, y_top-h, W-2*M, h, 6, stroke=0, fill=1)
    c.setFillColor(RED); c.setFont("Times-Bold", 46); c.drawString(M+12, y_top-38, "“")
    para(c, q, sty("q", fontName="Helvetica-Oblique", fontSize=11.2, leading=15.5, textColor=colors.white), M+50, y_top-12, W-2*M-66)
    para(c, src, sty("qs", fontSize=8.2, textColor=CREAM), M+50, y_top-h+19, W-2*M-66)

def f_steps(c, y_top, items):
    n = len(items); gap = 8; w = (W-2*M-gap*(n-1))/n
    for i, (t, bd) in enumerate(items):
        x = M+i*(w+gap); c.setFillColor(RED); c.circle(x+10, y_top-10, 10, stroke=0, fill=1)
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 10.5); c.drawCentredString(x+10, y_top-13.6, str(i+1))
        h = para(c, f"<b>{t}</b>", sty("st", fontName="Helvetica-Bold", fontSize=9.2, leading=11.6, textColor=NAVY), x+25, y_top-1, w-27)
        para(c, bd, sty("sb", fontSize=8.3, leading=11), x+25, y_top-3-h, w-27)

def f_cta(c, y_top, h, l1, l2):
    c.setFillColor(RED); c.roundRect(M, y_top-h, W-2*M, h, 6, stroke=0, fill=1)
    para(c, l1, sty("c1", fontName="Helvetica-Bold", fontSize=13, leading=16, textColor=colors.white), M+16, y_top-11, W-2*M-32)
    para(c, l2, sty("c2", fontSize=9.2, leading=12.6, textColor=colors.white), M+16, y_top-33, W-2*M-32)

def f_mini_header(c, title):
    f_logo(c, M, H-16, 64); c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 10.5); c.drawRightString(W-M, H-32, title)
    c.setStrokeColor(NAVY); c.setLineWidth(1); c.line(M, H-56, W-M, H-56); return H-68

def f_legend(c, y_top, items):
    x = M
    for col, lb in items:
        c.setFillColor(col); c.roundRect(x, y_top-9, 12, 9, 2, stroke=0, fill=1)
        c.setFillColor(GREY); c.setFont("Helvetica", 7.6); c.drawString(x+16, y_top-7.4, lb); x += 16+c.stringWidth(lb, "Helvetica", 7.6)+14

def f_timetable(c, y_top, days, rows, grid, row_h, font=7.6, lead=9.6):
    lw = 52; gap = 3; cw = (W-2*M-lw-gap*len(days))/len(days); x0 = M+lw+gap
    for i, d in enumerate(days):
        x = x0+i*(cw+gap); c.setFillColor(NAVY); c.rect(x, y_top-20, cw, 20, stroke=0, fill=1)
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 9); c.drawCentredString(x+cw/2, y_top-13.5, d)
    y = y_top-23
    for r, rn in enumerate(rows):
        c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 7.8); c.drawString(M, y-row_h/2-2.5, rn)
        for i in range(len(days)):
            txt, typ = grid[r][i]; x = x0+i*(cw+gap)
            c.setFillColor(TCOL[typ]); c.roundRect(x, y-row_h, cw, row_h, 3, stroke=0, fill=1)
            para(c, txt, sty("tt", fontSize=font, leading=lead), x+5, y-5, cw-10)
        y -= row_h+gap
    return y

def f_timeline_cols(c, y_top, cols, row_h):
    n = len(cols); gap = 8; cw = (W-2*M-gap*(n-1))/n
    for i, (d, items) in enumerate(cols):
        x = M+i*(cw+gap); c.setFillColor(NAVY); c.roundRect(x, y_top-20, cw, 20, 4, stroke=0, fill=1); c.rect(x, y_top-20, cw, 8, stroke=0, fill=1)
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 9.5); c.drawCentredString(x+cw/2, y_top-14, d)
        y = y_top-24
        for tm, tx, typ in items:
            c.setFillColor(TCOL[typ]); c.roundRect(x, y-row_h, cw, row_h, 3, stroke=0, fill=1)
            c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 8.4); c.drawString(x+7, y-12, tm)
            para(c, tx, sty("tl", fontSize=8, leading=10.2), x+7, y-17, cw-14); y -= row_h+3
    return y_top-24-(row_h+3)*max(len(i[1]) for i in cols)

STEPS = [("Planning call", "20 minutes to understand your group, dates and goals."), ("Tailored proposal", "A written programme and proposal built for you."),
         ("We handle everything", "Club agenda, accommodation, transfers and logistics."), ("Experience + follow-up", "We are on site, and review the trip with your staff after.")]

def build_team():
    out = f"{OUTDIR}/Always-Up-Team-Experience.pdf"; c = canvas.Canvas(out, pagesize=A4)
    c.setTitle("Always Up - Team Experience"); c.setAuthor("Always Up")
    y = f_hero(c, f"{NW}/au_p02_0.png", "TEAM EXPERIENCE",
               "A professional football experience inside Atlético de Madrid, Real Sociedad and Real Sporting de Gijón — for team trips and pre-seasons.",
               (0.5, 0.85), hh=318, g0=0.55, g1=0.92, tb=74)
    y -= 10; y = f_crest_row(c, y, "TRAINING INSIDE THE FACILITIES OF"); y -= 10
    h = para(c, "Not a camp or a tour. Your team trains where professional LaLiga academies train: official club coaches, "
                "their methodology, their pitches and residences, and matches against academy sides — a programme built "
                "around your level, your dates and your objectives.", BODY, M, y, W-2*M); y -= h+6
    y = f_chips(c, y, ["Team trips", "Pre-seasons", "Tournament preparation", "Boys’ and girls’ teams", "U7 to amateur"]); y -= 8
    y = f_h2(c, "Why teams choose Always Up", y); cw = (W-2*M-16)/3
    f_card(c, M, y, cw, 76, "Real professional access", "Your players train in the same facilities and with the same methodology as the clubs’ own academy teams.")
    f_card(c, M+cw+8, y, cw, 76, "Official club coaches", "Sessions led by Academy coaches who work with your group by age stage, in your language.")
    f_card(c, M+2*(cw+8), y, cw, 76, "Everything handled", "One point of contact for residence, meals, transfers, matches and schedule.")
    y -= 76+10; y = f_h2(c, "What your team lives", y)
    items = [("Professional training", "with official academy coaches, adapted to your age stage (U7 to U19 and amateur)."),
             ("Official and friendly matches", "against academy teams and local sides with official referees, matched to your level (minimum 2 in a 5-day stay)."),
             ("Tactical and video analysis,", "plus formative sessions on methodology, nutrition and player psychology."),
             ("Professional high-performance facilities:", "your team trains and plays in the clubs’ own facilities, with stadium and museum visits and first-team or academy match viewing when the calendar allows."),
             ("Full accommodation and logistics:", "full board in the club residence (or a hotel next to the facilities), all transfers in authorised buses, assistance in your language."),
             ("Cultural experience", "of professional football and life in Spain. Optional DonostiCup and MadCup tournaments (30+ countries).")]
    f_bullets(c, items, y, gap=4); f_footer(c); c.showPage()

    y = f_mini_header(c, "TEAM EXPERIENCE")
    y = f_h2(c, "Example of a Team Experience hired for five days", y)
    days = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"]; rows = ["MORNING", "AFTERNOON", "EVENING"]
    grid = [
        [("09:55 Arrival in Madrid, airport transfer · 11:30 Club values talk at the residence", "club"), ("10:00–11:30 Collective training session, Alcalá", "train"), ("11:00 Training viewing, Majadahonda", "club"), ("10:00–11:30 Collective training session, Alcalá", "train"), ("10:00–11:30 Collective training session, Alcalá", "train")],
        [("16:00 Collective training session, Alcalá", "train"), ("17:30–21:00 Match vs Academy team, Alcalá", "match"), ("16:30 Stadium and museum tour, Metropolitano · 18:30 Match vs Academy team", "match"), ("17:30 Match vs Academy team, Alcalá", "match"), ("16:25 Departure from Madrid", "travel")],
        [("Dinner at the residence", "meal"), ("Dinner at the residence", "meal"), ("Dinner at the residence", "meal"), ("First-team match viewing at the Metropolitano (calendar permitting)", "club"), ("Dinner at the residence", "meal")],
    ]
    y = f_timetable(c, y, days, rows, grid, 52, 7.5, 9.4)
    f_legend(c, y-4, [(T_TRAIN, "Training"), (T_MATCH, "Matches"), (T_CLUB, "Club experience"), (T_MEAL, "Meals"), (T_TRAVEL, "Travel")]); y -= 18
    para(c, "Real example: full board in the club residence, all transfers in authorised buses, 1.5-hour training sessions every day, stadium and museum visit and free time for any activity. "
            "<b>Every programme is built to measure for each club.</b>", SMALL, M, y, W-2*M); y -= 36
    y = f_photo_row(c, [(f"{NW}/au_p01_0.png", "REAL TEAMS WITH ALWAYS UP", (0.5, 0.6)), (f"{NW}/au_p05_0.png", "ZUBIETA · REAL SOCIEDAD", (0.5, 0.55)),
                        (f"{NW}/au_p13_4.png", "PRESS ROOM · ATLÉTICO", (0.5, 0.55)), (f"{NW}/au_p13_0.png", "WOMEN’S TEAM · ZUBIETA", (0.5, 0.55))], y, 84, "REAL EXPERIENCES"); y -= 8
    y = f_photo_row(c, [(f"{IM}/tebro_p12_2.png", "SPORTS CITY · ATLÉTICO", (0.5, 0.5)), (f"{IM}/qs_p05_0.png", "ZUBIETA · REAL SOCIEDAD", (0.5, 0.5)),
                        (f"{NW}/au_p03_7.png", "MAREO · REAL SPORTING", (0.5, 0.5)), (f"{NW}/spor__DSC4194.png", "CLUB RESIDENCE · MAREO", (0.5, 0.5))], y, 80, "WHERE YOU TRAIN AND STAY"); y -= 10
    f_quote(c, y, 66, "No doubt our Atlético de Madrid Experience helped us win our league title... it gives players the belief they are special.",
            "Long-term partner club, Ireland — after three years training with Always Up"); y -= 76
    f_steps(c, y, STEPS); y -= 66
    f_cta(c, y, 50, "Ready to plan your trip?", f"Book a 20-minute planning call: {CAL}  ·  or reply to this email.")
    f_footer(c); c.showPage(); c.save(); return out

def build_coach():
    out = f"{OUTDIR}/Always-Up-Coach-Experience.pdf"; c = canvas.Canvas(out, pagesize=A4)
    c.setTitle("Always Up - Coach Experience"); c.setAuthor("Always Up")
    y = f_hero(c, f"{NW}/au_p13_3.png", "COACH EXPERIENCE",
               "See how professional LaLiga academies build players — from the inside. Observe, learn and take it back to your club.",
               (0.5, 0.27), hh=316, g0=0.40, g1=0.68, tb=72)
    y -= 12; y = f_crest_row(c, y, "OBSERVING INSIDE THE ACADEMIES OF"); y -= 12
    h = para(c, "A professional programme for coaches and technical staff: watch official academy sessions, attend masterclasses with the clubs’ own departments and "
                "understand the methodology behind Atlético de Madrid, Real Sociedad and Real Sporting. Duration and content are tailored to your staff.", BODY, M, y, W-2*M); y -= h+6
    y = f_chips(c, y, ["Technical staff", "Academy directors", "Pre-season planning", "Coach education"]); y -= 10
    y = f_h2(c, "What your staff gets", y)
    items = [("Observation of professional training sessions", "of the academies across age groups, always accompanied by a club representative who speaks your language."),
             ("Masterclasses with the club’s departments:", "methodology, physical preparation, individual development, game analysis, club values, scouting, goalkeeping, psychology and nutrition."),
             ("High-performance exposure:", "sessions of the academy’s top age groups and, depending on the calendar, first-team or second-team sessions."),
             ("Match viewing:", "an academy match and, when dates coincide, a LaLiga or European first-team match."),
             ("Stadium and museum tour", "to see how the club works beyond the pitch."),
             ("Full logistics:", "accommodation, meals, private transport and assistance in your language throughout."),
             ("Network and certificate:", "direct contact with academy staff and coaches from other countries; certificate of participation.")]
    y = f_bullets(c, items, y, gap=5); y -= 6
    c.setFillColor(LIGHT); c.roundRect(M, y-52, W-2*M, 52, 6, stroke=0, fill=1); c.setFillColor(RED); c.rect(M, y-52, 3.5, 52, stroke=0, fill=1)
    para(c, "<b>Two clubs, one trip.</b> Combine San Sebastián (Real Sociedad) and Madrid (Atlético de Madrid) in a single week: masterclasses and training observation at Zubieta, "
            "followed by a Madrid extension with academy and first-team matches.", sty("two", fontSize=9.2, leading=12.6), M+14, y-10, W-2*M-28)
    f_footer(c); c.showPage()

    y = f_mini_header(c, "COACH EXPERIENCE"); y = f_h2(c, "A real 3-day programme at Atlético de Madrid", y)
    cols = [("DAY 1", [("11:15", "Arrival in Madrid", "travel"), ("13:00", "Formative session: Methodology (1.5 h)", "club"), ("17:00", "Observe Academy training U15–U17", "train"), ("19:00", "Observe Academy training U12–U14", "train")]),
            ("DAY 2", [("09:30", "Observe Academy training U19", "train"), ("11:30", "Observe Academy training U18", "train"), ("16:00", "Formative session: Methodology 2", "club"), ("17:00", "Academy match at Alcalá", "match")]),
            ("DAY 3", [("10:00", "Formative session: Physical preparation (2 h)", "club"), ("12:30", "Observe Academy training U18", "train"), ("Optional", "Stadium & museum tour · first-team match when dates coincide", "match"), ("16:40", "Departure", "travel")])]
    y = f_timeline_cols(c, y, cols, 46); y -= 4
    f_legend(c, y, [(T_TRAIN, "Observed training"), (T_CLUB, "Masterclasses"), (T_MATCH, "Matches"), (T_TRAVEL, "Travel")]); y -= 16
    para(c, "Sample from a real 3-day programme. Programmes run from 3 days to a full week, built around your staff’s interests.", SMALL, M, y, W-2*M); y -= 24
    y = f_photo_row(c, [(f"{NW}/au_p13_3.png", "CLUB PRESS ROOM", (0.5, 0.62)), (f"{IM}/tebro_p15_2.png", "ACADEMY GYM", (0.5, 0.5)),
                        (f"{NW}/au_p05_0.png", "ZUBIETA · REAL SOCIEDAD", (0.5, 0.5)), (f"{NW}/spor__DSC4176.png", "MEETING ROOMS · MAREO", (0.5, 0.5))], y, 84, "INSIDE THE CLUBS"); y -= 8
    y = f_photo_row(c, [(f"{IM}/tebro_p12_2.png", "SPORTS CITY · ATLÉTICO", (0.5, 0.5)), (f"{IM}/tebro_p10_3.png", "CENTRO DEPORTIVO ALCALÁ", (0.5, 0.5)),
                        (f"{NW}/au_p03_7.png", "MAREO · REAL SPORTING", (0.5, 0.5))], y, 76, "FACILITIES"); y -= 12
    f_quote(c, y, 56, "Watching these teams train was a dream for our coaches.", "International club coach — Coach Experience in Madrid"); y -= 66
    f_steps(c, y, STEPS); y -= 66
    f_cta(c, y, 54, "Want to bring your staff to Spain?", f"Book a 20-minute planning call: {CAL}  ·  or reply to this email.")
    f_footer(c); c.showPage(); c.save(); return out

# ================================================================== DECK (16:9 horizontal)
DW, DH = 960, 540; DM = 54

def d_fit(path, w, h, focus=(0.5, 0.5)): return fit(path, w, h, focus, scale=2.5)

def d_logo(c, x, y_top, w):
    h = w*LOGO_R; c.drawImage(LOGO, x, y_top-h, w, h, mask="auto")

def d_crests(c, x, y, hh, gap=18, white_card=False):
    for img, (iw, ih) in zip(CRESTS, CREST_SZ):
        w = hh*iw/ih
        if white_card: c.setFillColor(colors.white); c.roundRect(x-8, y-6, w+16, hh+12, 6, stroke=0, fill=1)
        c.drawImage(img, x, y, w, hh, mask="auto"); x += w+gap+(16 if white_card else 0)

def build_deck(public):
    out = f"{OUTDIR}/Always-Up-Company-Deck-Public.pdf" if public else f"{OUTDIR}/Always-Up-Company-Deck.pdf"
    c = canvas.Canvas(out, pagesize=(DW, DH)); c.setTitle("Always Up - Company presentation"); c.setAuthor("Always Up")
    page = [0]

    def chrome(section):
        page[0] += 1; d_logo(c, DM, DH-24, 58)
        c.setFillColor(GREY); c.setFont("Helvetica-Bold", 8.5); c.drawRightString(DW-DM, DH-38, section.upper())
        c.setStrokeColor(colors.HexColor("#D5DAE5")); c.setLineWidth(0.8); c.line(DM, 36, DW-DM, 36)
        c.setFillColor(GREY); c.setFont("Helvetica", 8.5); c.drawString(DM, 20, "Always Up  ·  alwaysup.es  ·  joel.martinez@alwaysup.es"); c.drawRightString(DW-DM, 20, str(page[0]))

    def title(text, y=None, sub=None, sub_w=None):
        y = y or DH-92
        c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 28 if len(text) > 38 else 30); c.drawString(DM, y, text)
        c.setFillColor(RED); c.rect(DM, y-12, 46, 3.5, stroke=0, fill=1)
        if sub: para(c, sub, sty("sub", fontSize=12.5, leading=17, textColor=GREY), DM, y-24, sub_w or (DW-2*DM-30))

    def bullets(items, x, y_top, w, gap=8, size=12.0):
        y = y_top
        for head, body in items:
            c.setFillColor(RED); c.rect(x, y-10, 6, 6, stroke=0, fill=1)
            h = para(c, f"<b>{head}</b> {body}" if head else body, sty("bl", fontSize=size, leading=size+4.6), x+16, y, w-16); y -= h+gap
        return y

    def panel(path, x, y, w, h, focus=(0.5, 0.5), cap=None):
        c.drawImage(d_fit(path, w, h, focus), x, y, w, h)
        if cap:
            c.setFillColor(colors.Color(0, 0.08, 0.3, alpha=0.8)); c.rect(x, y, w, 20, stroke=0, fill=1)
            c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 8); c.drawString(x+8, y+6.5, cap)

    def card(x, y_top, w, h, head, body, tag):
        c.setFillColor(LIGHT); c.roundRect(x, y_top-h, w, h, 6, stroke=0, fill=1); c.setFillColor(RED); c.rect(x, y_top-h, 4, h, stroke=0, fill=1)
        c.setFillColor(GREY); c.setFont("Helvetica-Bold", 7.6); c.drawString(x+16, y_top-17, tag.upper())
        c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 14); c.drawString(x+16, y_top-36, head)
        para(c, body, sty("cb", fontSize=10.2, leading=14), x+16, y_top-46, w-28)

    def service(section, ttl, sub, items, imgs):
        chrome(section); title(ttl, sub=sub, sub_w=450); bullets(items, DM, DH-176 if len(sub) > 70 else DH-168, 440, gap=8, size=11.8)
        c.setFillColor(LIGHT); c.roundRect(DM, 62, 440, 44, 6, stroke=0, fill=1); c.setFillColor(RED); c.rect(DM, 62, 4, 44, stroke=0, fill=1)
        para(c, f"<b>Want the full details?</b> Ask us for the detailed {ttl} overview.", sty("cta", fontSize=11, leading=15), DM+16, 98, 410)
        panel(imgs[0][0], 530, 232, 376, 210, imgs[0][2], imgs[0][1]); panel(imgs[1][0], 530, 62, 376, 160, imgs[1][2], imgs[1][1]); c.showPage()

    # 1 portada (panel navy + foto)
    page[0] += 1
    cover = f"{IM}/qs_p04_0.png" if public else f"{NW}/au_p01_0.png"
    c.drawImage(d_fit(cover, DW-430, DH, (0.5, 0.5)), 430, 0, DW-430, DH)
    c.setFillColor(NAVY); c.rect(0, 0, 430, DH, stroke=0, fill=1); c.setFillColor(RED); c.rect(430, 0, 5, DH, stroke=0, fill=1)
    c.setFillColor(colors.white); c.roundRect(DM-10, DH-124, 150, 96, 8, stroke=0, fill=1); d_logo(c, DM-2, DH-34, 134)
    c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 36); c.drawString(DM, 300, "Elite football"); c.drawString(DM, 258, "experiences in Spain")
    c.setFillColor(CREAM); c.setFont("Helvetica-Oblique", 15); c.drawString(DM, 222, "“Train like the greats, live like a pro.”")
    c.setFillColor(colors.white); c.setFont("Helvetica", 11.5); c.drawString(DM, 192, "For international teams, players and coaches")
    d_crests(c, DM, 86, 44, 18, white_card=True)
    c.setFillColor(colors.white); c.setFont("Helvetica", 8.8); c.drawString(DM, 56, "Atlético de Madrid  ·  Real Sociedad  ·  Real Sporting de Gijón"); c.showPage()

    # 2 problema
    chrome("Why Always Up"); title("Most teams never experience"); c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 30); c.drawString(DM, DH-128, "real European football")
    c.setFillColor(RED); c.rect(DM, DH-141, 46, 3.5, stroke=0, fill=1); y = DH-176
    para(c, "Many teams travel abroad. But very few experience real professional football environments.", sty("p", fontSize=16, leading=23), DM, y, 400)
    para(c, "<b>They train… They play…</b><br/><font color='#C6272F'><b>But they don’t live the game.</b></font>", sty("p2", fontSize=19, leading=28), DM, y-84, 400)
    para(c, "At Always Up we create professional football experiences in Spain that go beyond training — inside the facilities of professional clubs, with their coaches and their methodology.", sty("p3", fontSize=12.5, leading=18, textColor=GREY), DM, y-170, 400)
    if public: panel(f"{IM}/qs_p05_0.png", 500, 62, 406, 372, (0.5, 0.5), "ZUBIETA · REAL SOCIEDAD")
    else: panel(f"{NW}/au_p02_0.png", 500, 62, 406, 372, (0.5, 0.6), "FRIENDLY MATCH VS ATLÉTICO DE MADRID ACADEMY")
    c.showPage()

    # 3 quiénes somos (3 instalaciones)
    chrome("Who we are"); title("We bring you inside Spanish football")
    para(c, "Always Up connects international clubs, coaches and players with real professional environments in Spain and the USA, through direct partnerships with professional clubs.", sty("x", fontSize=13.5, leading=19, textColor=GREY), DM, DH-128, 800)
    cw = (DW-2*DM-40)/3
    for i, (img, n, d) in enumerate([(f"{IM}/tebro_p12_2.png", "Atlético de Madrid", "Sports City Alcalá · Academy methodology"), (f"{NW}/au_p03_0.png", "Real Sociedad", "Zubieta · One of Europe’s top academies"), (f"{NW}/au_p03_7.png", "Real Sporting de Gijón", "Mareo · Academy and residence")]):
        xx = DM+i*(cw+20); c.drawImage(d_fit(img, cw, 128), xx, 236, cw, 128)
        iw, ih = CREST_SZ[i]; chh = 38; cww = chh*iw/ih; c.drawImage(CRESTS[i], xx, 190, cww, chh, mask="auto")
        c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 13); c.drawString(xx+cww+12, 212, n); para(c, d, sty("d", fontSize=10, leading=13, textColor=GREY), xx+cww+12, 204, cw-cww-14)
    for i, (h_, b_) in enumerate([("Direct access", "Training inside the facilities of professional LaLiga clubs."), ("Official coaches", "Sessions led by the clubs’ own academy coaches and methodology."), ("Spain + USA", "We understand both worlds: European football culture and the American athletic system.")]):
        card(DM+i*(cw+20), 150, cw, 96, h_, b_, "")
    c.showPage()

    # 4 qué hacemos
    chrome("What we do"); title("Five ways to experience it", sub="Each programme is tailored to your group — accommodation, meals, transport and personalised attention included.")
    cw = (DW-2*DM-32)/3; ch = 150
    for i, (h_, b_, t_) in enumerate([("Team Experience", "Your team trains and plays inside professional academies in Spain: sessions, matches, tactical analysis, stadium visits.", "Clubs & academies"),
                                      ("Coach Experience", "Observe professional sessions, attend masterclasses and learn the methodology of professional clubs.", "Coaches & staff"),
                                      ("International Camps", "Official academy coaches travel to your facilities and run a certified training camp in your country.", "Academies"),
                                      ("International Programme", "Months of full immersion training and living at Real Sociedad’s academy: 1, 5 or 10 months.", "Players"),
                                      ("Study & Play USA", "Athletic evaluation, resume and direct communication with US college coaches, with admission support.", "Players & families")]):
        card(DM+(i % 3)*(cw+16), DH-190-(i//3)*(ch+14), cw, ch, h_, b_, t_)
    c.setFillColor(NAVY); c.roundRect(DM+2*(cw+16), DH-190-(ch+14)-ch, cw, ch, 6, stroke=0, fill=1)
    para(c, "<b>Not sure which fits?</b><br/><br/>Book a short call and we will point you to the right programme.", sty("q", fontSize=12.5, leading=18, textColor=colors.white), DM+2*(cw+16)+18, DH-190-(ch+14)-18, cw-36); c.showPage()

    # 5 team + ejemplo 5 días
    service("Team Experience", "Team Experience", "Bring your team to train where professionals train.",
            [("Professional training", "with official academy coaches, adapted to your age stage and level."), ("Official / friendly matches", "against academy teams with official referees."),
             ("Tactical & video analysis", "to understand and improve your team’s game."), ("Professional high-performance facilities:", "your team trains and plays in the clubs’ own facilities, plus stadium and museum visits."),
             ("Full accommodation & logistics:", "residence or hotel, meals, transfers, one point of contact."), ("Cultural experience:", "professional football and life in Spain."),
             ("Built for", "team trips and pre-seasons, one to two weeks. Optional DonostiCup / MadCup.")],
            [(f"{IM}/tebro_p12_2.png", "SPORTS CITY · ATLÉTICO DE MADRID", (0.5, 0.5)), (f"{NW}/au_p05_0.png", "TRAINING AT ZUBIETA · REAL SOCIEDAD", (0.5, 0.5))])
    chrome("Team Experience"); title("Example of a Team Experience hired for five days", sub="Every programme is built to measure for each club: dates, level, age group and objectives.")
    days = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"]
    grid = [[("09:55 Arrival in Madrid, airport transfer<br/>11:30 Club values talk at the residence", "club"), ("10:00–11:30 Collective training session, CD Alcalá", "train"), ("11:00 Training viewing, CD Majadahonda", "club"), ("10:00–11:30 Collective training session, CD Alcalá", "train"), ("10:00–11:30 Collective training session, CD Alcalá", "train")],
            [("16:00 Collective training session, CD Alcalá", "train"), ("17:30–21:00 Match vs Academy team, CD Alcalá", "match"), ("16:30 Stadium and museum tour, Riyadh Air Metropolitano<br/>18:30 Match vs Academy team, CD Alcalá", "match"), ("17:30 Match vs Academy team, CD Alcalá<br/>Evening: first-team match viewing, Metropolitano (calendar permitting)", "match"), ("16:25 Departure from Madrid", "travel")]]
    lw = 62; gap = 4; cwid = (DW-2*DM-lw-gap*5)/5; x0 = DM+lw+gap; yy = DH-170
    for i, d in enumerate(days):
        x = x0+i*(cwid+gap); c.setFillColor(NAVY); c.rect(x, yy-22, cwid, 22, stroke=0, fill=1); c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 10); c.drawCentredString(x+cwid/2, yy-15, d)
    y = yy-26
    for r, rn in enumerate(["MORNING", "AFTERNOON"]):
        rh = 92; c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 9); c.drawString(DM, y-rh/2-3, rn)
        for i in range(5):
            txt, typ = grid[r][i]; x = x0+i*(cwid+gap); c.setFillColor(TCOL[typ]); c.roundRect(x, y-rh, cwid, rh, 4, stroke=0, fill=1); para(c, txt, sty("tt", fontSize=9.3, leading=12.2), x+8, y-8, cwid-16)
        y -= rh+gap
    c.setFillColor(T_MEAL); c.roundRect(x0, y-34, 5*cwid+4*gap, 34, 4, stroke=0, fill=1); c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 9); c.drawString(DM, y-21, "MEALS")
    para(c, "Breakfast, lunch and dinner at the club residence every day (or at a hotel next to the facilities).", sty("ml", fontSize=9.6, leading=12), x0+10, y-9, 5*cwid-10); y -= 34+gap
    bullets([("Full board", "in the club residence · <b>all transfers</b> in authorised buses · <b>1.5-hour</b> training sessions every day · stadium and museum visit · free time for any activity of the team.")], DM, y-12, DW-2*DM, gap=4, size=10.5); c.showPage()

    # 6 coach
    service("Coach Experience", "Coach Experience", "Learn the methodology from inside the clubs.",
            [("Observe professional", "training sessions of the academies, across age groups."), ("Masterclasses", "with the clubs’ departments: methodology, physical preparation, analysis, scouting, goalkeeping."),
             ("Match viewing", "and stadium tour; first-team sessions when the calendar allows."), ("Tailored duration,", "from 3 days to a full week, with one or two clubs."),
             ("Network", "with academy staff and coaches from other countries."), ("Certificate", "of participation.")],
            [(f"{NW}/au_p13_3.png", "CLUB PRESS ROOM · ATLÉTICO DE MADRID", (0.5, 0.35)), (f"{IM}/tebro_p15_2.png", "ACADEMY HIGH-PERFORMANCE GYM", (0.5, 0.5))])
    # 7 camps
    service("International Camps", "International Camps", "The clubs’ coaches, in your facilities.",
            [("Official academy coaches", "from Atlético de Madrid and Real Sociedad travel to your country."), ("5–6 day camps", "following the club’s methodology, with up to 8 hours of activity per day."),
             ("Your academy promotes", "and registers players; we manage the relationship and the programme with the club."), ("Official club material:", "participation diploma for every player and official kit."),
             ("A professional programme", "for your players without travelling to Spain.")],
            [(f"{IM}/tebro_p13_2.png", "ACADEMY STADIUM · ATLÉTICO DE MADRID", (0.5, 0.5)), (f"{IM}/tebro_p10_3.png", "CENTRO DEPORTIVO ALCALÁ", (0.5, 0.5))])
    # 8 international programme
    chrome("International Programme"); title("Become part of Real Sociedad International Club", sub="A full immersion football programme in San Sebastián: from a short-term experience to full season development. Train daily, compete weekly, live the experience.")
    pw = (DW-2*DM-28)/3
    for i, (t_, h_, b_) in enumerate([("1 MONTH", "Discovery", "Available all year · 24+ training sessions · matches vs local teams · individual progress report"),
                                      ("5 MONTHS", "Development", "Jan–May or Feb–Jun · integration with RS youth teams · 60+ sessions · Spanish classes · academic support"),
                                      ("10 MONTHS", "Full Immersion", "September–June · full season with the Academy · 120+ sessions · bilingual education · end-of-year report")]):
        x = DM+i*(pw+14); y = DH-196; c.setFillColor(NAVY if i == 1 else LIGHT); c.roundRect(x, y-158, pw, 158, 6, stroke=0, fill=1); tc = colors.white if i == 1 else NAVY
        c.setFillColor(CREAM if i == 1 else RED); c.setFont("Helvetica-Bold", 9.5); c.drawString(x+16, y-24, t_+("  ·  MOST POPULAR" if i == 1 else ""))
        c.setFillColor(tc); c.setFont("Helvetica-Bold", 20); c.drawString(x+16, y-52, h_); para(c, b_, sty("pb", fontSize=10.8, leading=15, textColor=(colors.white if i == 1 else INK)), x+16, y-66, pw-32)
    panel(f"{NW}/au_p08_2.png", DM, 62, 400, 96, (0.5, 0.55), "REAL SOCIEDAD TRAINING SESSION · ZUBIETA"); panel(f"{IM}/rsstage_p07_0.png", DM+410, 62, 240, 96, (0.5, 0.5), "REALE ARENA")
    panel(f"{IM}/rsstage_p04_1.png", DM+660, 62, DW-2*DM-660, 96, (0.5, 0.5), "SAN SEBASTIÁN"); c.showPage()
    # 9 usa
    service("Study & Play USA", "Study & Play USA", "We connect international talent with academic and athletic opportunities in the USA. Turn your talent into an opportunity.",
            [("Athletic evaluation", "and a personalised athletic resume."), ("Direct communication", "with US college and high school coaches."), ("Academic and administrative", "requirements managed with you."),
             ("Visa and admission", "support."), ("Scholarship opportunities", "matched to your profile and goals."), ("We understand both worlds:", "European football culture and the American athletic system.")],
            [(f"{NW}/au_p09_1.png", "SPANISH PLAYERS IN US COLLEGE SOCCER", (0.5, 0.45)), (f"{NW}/au_p09_0.png", "COMPETING IN THE USA", (0.5, 0.5))])
    # 10 por qué
    chrome("Why Always Up"); title("Why clubs and families choose us"); pw = (DW-2*DM-32)/3
    for i, (a_, b_) in enumerate([("Exclusive access", "to professional clubs"), ("Experience in Spain", "and the USA"), ("Direct connection", "with Spanish football"), ("100% personalised", "programmes"), ("Real professional", "environment"), ("International", "network")]):
        x = DM+(i % 3)*(pw+16); y = DH-130-(i//3)*108; c.setFillColor(LIGHT); c.roundRect(x, y-92, pw, 92, 6, stroke=0, fill=1); c.setFillColor(RED); c.rect(x, y-92, 4, 92, stroke=0, fill=1)
        c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 15); c.drawString(x+18, y-38, a_); c.setFillColor(GREY); c.setFont("Helvetica", 12.5); c.drawString(x+18, y-58, b_)
    c.setFillColor(NAVY); c.roundRect(DM, 62, DW-2*DM, 66, 8, stroke=0, fill=1); c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 17); c.drawString(DM+24, 102, "We don’t organise trips.")
    c.setFillColor(CREAM); c.drawString(DM+24, 78, "We create real football experiences."); c.showPage()
    # 11 resultados
    chrome("Results"); title("International teams and players have already trusted us")
    para(c, "Experiences in elite environments  ·  Players from multiple countries  ·  Ongoing collaborations with clubs and coaches", sty("cl", fontSize=11.5, leading=16, textColor=GREY), DM, DH-128, DW-2*DM)
    qw = (DW-2*DM-32)/3
    for i, (q, s_) in enumerate([("No doubt our Atlético de Madrid Experience helped us win our league title… it gives players the belief they are special.", "Long-term partner club, Ireland — after three years with Always Up"),
                                 ("Watching these teams train was a dream for our coaches.", "International club coach"), ("Everything perfectly organised, we will definitely come back.", "International club")]):
        x = DM+i*(qw+16); c.setFillColor(NAVY if i == 0 else LIGHT); c.roundRect(x, 190, qw, 200, 8, stroke=0, fill=1); c.setFillColor(RED); c.setFont("Times-Bold", 60); c.drawString(x+16, 354, "“")
        para(c, q, sty("qq", fontName="Helvetica-Oblique", fontSize=13, leading=18.5, textColor=(colors.white if i == 0 else INK)), x+20, 342, qw-40)
        para(c, s_, sty("qs", fontSize=9.5, leading=13, textColor=(CREAM if i == 0 else GREY)), x+20, 232, qw-40)
    sw = (DW-2*DM-42)/4
    for i, (t_, b_) in enumerate([("Planning call", "20 minutes: your group, dates, goals."), ("Tailored proposal", "A written programme built for you."), ("We handle everything", "Club agenda and logistics."), ("Follow-up", "We review the experience with you.")]):
        x = DM+i*(sw+14); c.setFillColor(RED); c.circle(x+11, 160, 11, stroke=0, fill=1); c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 12); c.drawCentredString(x+11, 155.5, str(i+1))
        c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 11.5); c.drawString(x+30, 156, t_); para(c, b_, sty("sb", fontSize=10, leading=13.5, textColor=GREY), x+30, 148, sw-32)
    c.showPage()
    # 11b galería real (solo versión completa)
    if not public:
        chrome("Real experiences"); title("Real experiences with Always Up", sub="International teams and players on the pitch with professional clubs.")
        gl = [(f"{NW}/au_p01_0.png", "WITH ATLÉTICO DE MADRID FIRST-TEAM PLAYERS", (0.5, 0.55)), (f"{NW}/au_p13_4.png", "PRESS ROOM · ATLÉTICO DE MADRID", (0.5, 0.55)), (f"{NW}/au_p13_5.png", "MATCH DAY · METROPOLITANO", (0.5, 0.5)),
              (f"{NW}/au_p05_0.png", "ZUBIETA · REAL SOCIEDAD", (0.5, 0.5)), (f"{NW}/au_p13_0.png", "WOMEN’S TEAM · ZUBIETA", (0.5, 0.5)), (f"{NW}/au_p02_0.png", "FRIENDLY VS ATLÉTICO DE MADRID ACADEMY", (0.5, 0.6))]
        gw = (DW-2*DM-24)/3; gh = 150
        for i, (pth, cap, fc) in enumerate(gl): panel(pth, DM+(i % 3)*(gw+12), 242-(i//3)*(gh+12), gw, gh, fc, cap)
        c.showPage()
    # 12 cta
    page[0] += 1
    c.drawImage(gradient_photo(f"{IM}/qs_p16_0.png", DW, DH, (0.5, 0.45), 0.0, 1.0, scale=2.5), 0, 0, DW, DH)  # gradiente vertical suave
    c.setFillColor(colors.Color(0, 0.08, 0.3, alpha=0.55)); c.rect(0, 0, DW, DH, stroke=0, fill=1)
    c.setFillColor(colors.white); c.roundRect(DM-10, DH-124, 150, 96, 8, stroke=0, fill=1); d_logo(c, DM-2, DH-34, 134)
    c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 38); c.drawString(DM, 300, "Let’s plan your"); c.drawString(DM, 252, "experience in Spain")
    c.setFillColor(CREAM); c.setFont("Helvetica", 15); c.drawString(DM, 214, "Book a 20-minute call and tell us about your group.")
    y = 170
    for k, v in [("Book a call", CAL), ("Email", "joel.martinez@alwaysup.es"), ("Phone", "+1 (814) 329 1929"), ("Web", "alwaysup.es")]:
        c.setFillColor(CREAM); c.setFont("Helvetica-Bold", 10); c.drawString(DM, y, k.upper()); c.setFillColor(colors.white); c.setFont("Helvetica", 13); c.drawString(DM+90, y, v); y -= 26
    c.showPage(); c.save(); return out

if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "todo"
    if what in ("fichas", "todo"): print(build_team()); print(build_coach())
    if what in ("deck", "todo"): print(build_deck(False)); print(build_deck(True))
