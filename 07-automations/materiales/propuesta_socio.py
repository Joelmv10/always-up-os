#!/usr/bin/env python3
"""Presentación de colaboración para un socio o canal (por ejemplo Gonzalo, Argentina). 16:9, español.

Uso:  python3 propuesta_socio.py            -> genera 01-clients/propuestas/Always-Up-Propuesta-Gonzalo-Lamas-Argentina-2028.pdf
Diseño: estilo Always Up corporativo (azul #254264, granate #922E32, crema #F4F1E8), títulos en Georgia, logo y águila de la marca.
Contenido: mezcla de la presentación de Enrique (v3) y la de Joel. Sin precios. Cambiar NOMBRE, ANIO o los textos en este archivo.
Dependencias: reportlab, pillow, numpy y materiales.py (esta misma carpeta). Fotos de .cache (ejecutar preparar_imagenes.py antes).
"""
import os

from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

import materiales as M

HERE = os.path.dirname(os.path.abspath(__file__))
BRAND = os.path.join(HERE, "brand")
NOMBRE, ANIO = "Gonzalo Lamas", "2028"
OUT = os.path.abspath(os.path.join(HERE, "..", "..", "01-clients", "propuestas", "Always-Up-Propuesta-Gonzalo-Lamas-Argentina-2028.pdf"))

NAVY = colors.HexColor("#254264"); WINE = colors.HexColor("#922E32"); CREAM = colors.HexColor("#F4F1E8")
INK = colors.HexColor("#1F2937"); GREY = colors.HexColor("#5B6573"); WHITE = colors.white
W, H = 960.0, 540.0
S = 72.0  # puntos por pulgada (diapositiva de 13,333 x 7,5 pulgadas)

pdfmetrics.registerFont(TTFont("GeorgiaB", "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"))
pdfmetrics.registerFont(TTFont("GeorgiaI", "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"))
pdfmetrics.registerFont(TTFont("Georgia", "/System/Library/Fonts/Supplemental/Georgia.ttf"))

NW, IM = M.NW, M.IM
SOC = os.path.join(M.CACHE, "socio")


def img(name):
    return ImageReader(os.path.join(BRAND, name))


def st(name, **kw):
    d = dict(fontName="Helvetica", fontSize=11, leading=15, textColor=INK); d.update(kw)
    return M.sty(name, **d)


def para(c, text, style, x, y_top, w):
    return M.para(c, text, style, x, y_top, w)


class Slide:
    def __init__(self, c, bg=WHITE, n=None):
        self.c = c; self.n = n
        c.setFillColor(bg); c.rect(0, 0, W, H, stroke=0, fill=1)

    # coordenadas en pulgadas desde arriba a la izquierda
    def box(self, x, y, w, h, fill, r=6):
        self.c.setFillColor(fill); self.c.roundRect(x*S, H-(y+h)*S, w*S, h*S, r, stroke=0, fill=1)

    def rect(self, x, y, w, h, fill):
        self.c.setFillColor(fill); self.c.rect(x*S, H-(y+h)*S, w*S, h*S, stroke=0, fill=1)

    def eyebrow(self, text, x=0.75, y=0.60, color=WINE):
        self.c.setFillColor(color); self.c.setFont("Helvetica-Bold", 10.5)
        self.c.drawString(x*S, H-(y+0.20)*S, text.upper())

    def title(self, text, x=0.75, y=0.95, w=10.2, size=30, color=NAVY):
        ps = M.ParagraphStyle("t", fontName="GeorgiaB", fontSize=size, leading=size*1.18, textColor=color)
        h = para(self.c, text, ps, x*S, H-y*S, w*S)
        return y + h/S

    def text(self, text, x, y, w, size=12, color=GREY, leading=None, font="Helvetica"):
        return para(self.c, text, st("p%d" % size, fontSize=size, leading=leading or size*1.38, textColor=color, fontName=font), x*S, H-y*S, w*S)/S

    def logo(self, x=11.98, y=0.30, w=0.95):
        h = w*541/827; self.c.drawImage(img("logo.png"), x*S, H-(y+h)*S, w*S, h*S, mask="auto")

    def icon(self, name, x, y, d=0.6, fill=NAVY):
        self.c.setFillColor(fill); self.c.circle((x+d/2)*S, H-(y+d/2)*S, d/2*S, stroke=0, fill=1)
        g = d*0.52; self.c.drawImage(img("ic_%s.png" % name), (x+(d-g)/2)*S, H-(y+(d+g)/2)*S, g*S, g*S, mask="auto")

    def photo(self, path, x, y, w, h, focus=(0.5, 0.5), cap=None):
        self.c.drawImage(M.fit(path, w*S, h*S, focus, scale=2.2), x*S, H-(y+h)*S, w*S, h*S)
        if cap:
            self.c.setFillColor(colors.Color(0.145, 0.259, 0.392, alpha=0.88)); self.c.rect(x*S, H-(y+h)*S, w*S, 0.28*S, stroke=0, fill=1)
            self.c.setFillColor(WHITE); self.c.setFont("Helvetica-Bold", 7.6); self.c.drawString(x*S+8, H-(y+h)*S+8.5, cap.upper())

    def num(self, color=GREY):
        if self.n:
            self.c.setFillColor(color); self.c.setFont("Helvetica", 8.5); self.c.drawRightString(W-0.45*S, 14, str(self.n))

    def done(self):
        self.num(); self.c.showPage()


def item(s, name, x, y, head, body, w=6.2, fill=NAVY, d=0.52, hs=13.5):
    """Fila con icono en círculo, título y texto (estilo Enrique)."""
    s.icon(name, x, y, d, fill)
    ps = M.ParagraphStyle("ih", fontName="Helvetica-Bold", fontSize=hs, leading=hs*1.25, textColor=INK)
    h1 = para(s.c, head, ps, (x+d+0.2)*S, H-(y-0.02)*S, w*S)
    h2 = para(s.c, body, st("ib", fontSize=11.4, leading=15.2, textColor=GREY), (x+d+0.2)*S, H-(y-0.02)*S-h1-2, w*S)
    return h1 + h2


def card_icon(s, name, x, y, w, h, head, body, num=None, fill=NAVY, bg=WHITE, hs=16, dark=False):
    s.box(x, y, w, h, NAVY if dark else bg)
    s.icon(name, x+0.30, y+0.28, 0.58, WINE if dark else fill)
    ps = M.ParagraphStyle("ch", fontName="GeorgiaB", fontSize=hs, leading=hs*1.2, textColor=WHITE if dark else NAVY)
    h1 = para(s.c, head, ps, (x+0.30)*S, H-(y+1.10)*S, (w-0.6)*S)
    para(s.c, body, st("cb", fontSize=11.2, leading=15, textColor=colors.HexColor("#DCE3EC") if dark else GREY), (x+0.30)*S, H-(y+1.10)*S-h1-5, (w-0.6)*S)
    if num:
        s.c.setFillColor(WINE); s.c.setFont("GeorgiaB", 24); s.c.drawRightString((x+w-0.3)*S, H-(y+0.78)*S, num)


def build():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    c = canvas.Canvas(OUT, pagesize=(W, H)); c.setTitle(f"Always Up - Propuesta de colaboración {ANIO} para {NOMBRE}"); c.setAuthor("Always Up")
    n = [0]

    def new(bg=WHITE):
        n[0] += 1; return Slide(c, bg, n[0])

    # 1 portada ------------------------------------------------------------
    s = new(CREAM)
    s.rect(4.4, 0, 9.0, 7.5, NAVY)
    s.photo(f"{NW}/au_p01_0.png", 4.75, 0.8, 8.1, 5.9, (0.5, 0.55))
    c.drawImage(img("logo.png"), 0.6*S, H-(0.55+1.45)*S, 2.2*S, 1.45*S, mask="auto")
    s.eyebrow(f"Propuesta de colaboración {ANIO}", 0.6, 2.45)
    s.title("Tu socio en España para experiencias de fútbol de élite", 0.6, 2.8, 3.6, 25)
    s.text("Programas a medida para los clubes, colegios y academias con los que trabajas en Argentina.", 0.6, 4.5, 3.5, 12.5)
    s.rect(0.6, 6.2, 0.6, 0.06, WINE)
    c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 12); c.drawString(0.6*S, H-6.62*S, f"Preparado para {NOMBRE} · Argentina")
    c.showPage()

    # 2 punto de partida ---------------------------------------------------
    s = new(WHITE); s.eyebrow("Punto de partida"); s.logo(); y = s.title("Sumar, no sustituir", w=7.4)
    s.text("Lo que hablamos en nuestra reunión y lo que queremos construir juntos.", 0.75, y+0.15, 7.2, 14)
    yy = 2.75
    for ic, h_, b_ in [("group", "Tu red", "Familias, niños y clubes en Argentina, con grupos que ya viajan a España."),
                       ("flag", "Tu objetivo", f"Ver qué más podemos ofrecer a tu comunidad y cómo trabajar juntos a partir de {ANIO}."),
                       ("handshake", "Nuestro punto de partida", "Tu 2027 ya está organizado. No venimos a cambiar nada de lo que funciona: venimos a sumar opciones.")]:
        item(s, ic, 0.75, yy, h_, b_, w=6.2, fill=NAVY if ic != "flag" else WINE); yy += 1.3
    s.photo(f"{IM}/tebro_p12_2.png", 8.7, 1.6, 4.0, 5.2, (0.5, 0.5), "Ciudad Deportiva · Atlético de Madrid"); s.done()

    # 3 lo que cambia para tu negocio -------------------------------------
    s = new(CREAM); s.eyebrow("Por qué trabajar con nosotros"); s.logo(); s.title("Lo que cambia para tu negocio", w=10)
    s.text("Más opciones para tus clientes, un solo interlocutor en España y la relación con tu cliente siempre en tus manos.", 0.75, 1.75, 11, 13)
    ben = [("stadium", "Nuevos destinos", "Madrid, San Sebastián y Gijón, con el Atlético, la Real Sociedad y el Sporting.", NAVY),
           ("chart", "Nuevas líneas de negocio", "Jugadores a entrenar y probar en España, campus en Argentina, Coach Experience, torneos y becas amplían lo que puedes vender.", WINE),
           ("handshake", "Tú mantienes la relación", "Trabajamos como tu equipo en España. Tu cliente sigue siendo tuyo.", NAVY),
           ("group", "Grupos grandes", "Combinamos clubes, sedes, categorías y fechas sin perder calidad.", WINE),
           ("bed", "Todo resuelto", "Residencias de los clubes, traslados, entradas y un único interlocutor antes, durante y después del viaje.", NAVY),
           ("shield", "Tranquilidad", "Los clubes anfitriones cubren la estancia, Always Up tiene responsabilidad civil propia y cada grupo viaja con sus adultos.", WINE)]
    for i, (ic, h_, b_, col) in enumerate(ben):
        card_icon(s, ic, 0.75+(i % 3)*4.0, 2.35+(i//3)*2.4, 3.75, 2.3, h_, b_, fill=col, bg=WHITE, hs=15)
    s.done()

    # 4 quiénes somos ------------------------------------------------------
    s = new(WHITE); s.eyebrow("Quiénes somos"); s.logo(); s.title("La puerta al fútbol español", w=7.4)
    s.text("Always Up es la marca comercial de una compañía española creada en 2024 para organizar experiencias de fútbol de alto nivel en España para clubes, academias, jugadores y entrenadores de todo el mundo.", 0.75, 1.95, 7.2, 13.5, INK)
    s.text("Trabajamos de la mano de clubes de LaLiga y de partners educativos para que cada programa combine fútbol de élite, formación y una experiencia que se recuerde toda la vida.", 0.75, 3.15, 7.2, 13.5, INK)
    yy = 4.3
    for ic, h_, b_ in [("handshake", "Acuerdos con clubes de LaLiga", "Atlético de Madrid, Real Sociedad y Real Sporting de Gijón, y conversaciones con el Deportivo de La Coruña."),
                       ("globe", "Experiencia internacional", "Programas para clubes, academias y entrenadores de Europa y América."),
                       ("grad", "Conocimiento del sistema universitario de EE. UU.", "Experiencia propia como jugador NCAA y partners especializados en becas.")]:
        item(s, ic, 0.75, yy, h_, b_, w=6.6, d=0.46, hs=12.5); yy += 0.95
    s.photo(f"{NW}/au_p02_0.png", 8.55, 1.5, 4.2, 2.55, (0.5, 0.6), "Amistoso contra la academia del Atlético")
    s.photo(f"{NW}/au_p13_5.png", 8.55, 4.2, 4.2, 2.6, (0.5, 0.5), "Día de partido · Metropolitano")
    s.done()

    # 5 valores ------------------------------------------------------------
    s = new(CREAM); s.eyebrow("Nuestros valores"); s.logo(); s.title("Lo que el deporte nos enseña", w=10)
    vals = [("flag", "Perseverancia", "La constancia y la tenacidad como señas de identidad.", NAVY), ("chart", "Superación", "Nada es imposible cuando se trabaja para conseguirlo.", WINE),
            ("book", "Disciplina", "Quien siembra, recoge: invertir tiempo en la pasión.", NAVY), ("runner", "Esfuerzo", "Cada día, una oportunidad de ser mejor.", WINE),
            ("group", "Comunidad", "El orgullo de pertenecer a un equipo.", NAVY), ("heart", "Salud", "Equilibrio físico y mental como base del rendimiento.", WINE)]
    for i, (ic, h_, b_, col) in enumerate(vals):
        card_icon(s, ic, 0.75+(i % 3)*4.0, 2.15+(i//3)*2.35, 3.75, 2.1, h_, b_, fill=col, hs=17)
    s.done()

    # 6 acuerdos con los clubes + prueba social -----------------------------
    s = new(CREAM); s.eyebrow("Nuestros acuerdos"); s.logo(); s.title("Los clubes que hacen posible cada programa", w=10.8)
    cw = 3.85
    clubs = [(f"{NW}/au_p03_0.png", 1, "Real Sociedad", "Zubieta, San Sebastián. Una de las canteras más reconocidas de Europa."),
             (f"{IM}/tebro_p12_2.png", 0, "Atlético de Madrid", "Ciudad Deportiva de Alcalá de Henares y Majadahonda, y residencia del club."),
             (f"{NW}/au_p03_7.png", 2, "Real Sporting de Gijón", "Mareo, Gijón. Cantera y residencia del club.")]
    for i, (ph, ci, name, desc) in enumerate(clubs):
        x = 0.75+i*(cw+0.2); s.box(x, 1.9, cw, 3.35, WHITE)
        c.drawImage(M.fit(ph, cw*S, 1.5*S, (0.5, 0.5), scale=2.2), x*S, H-(1.9+1.5)*S, cw*S, 1.5*S)
        iw, ih = M.CREST_SZ[ci]; chh = 0.6; cww = chh*iw/ih
        c.drawImage(M.CRESTS[ci], (x+0.3)*S, H-(1.9+1.5+0.2+chh)*S, cww*S, chh*S, mask="auto")
        c.setFillColor(NAVY); c.setFont("GeorgiaB", 14.5); c.drawString((x+0.3+cww+0.2)*S, H-(1.9+1.5+0.55)*S, name)
        para(c, desc, st("cd", fontSize=11, leading=15, textColor=GREY), (x+0.3)*S, H-(1.9+1.5+0.95)*S, (cw-0.6)*S)
    s.box(0.75, 5.5, 11.75, 1.55, NAVY); c.setFillColor(WINE); c.setFont("Times-Bold", 64); c.drawString(1.0*S, H-6.45*S, "“")
    para(c, "Sin duda, nuestra experiencia en el Atlético de Madrid nos ayudó a ganar la liga… les da a los jugadores la confianza de sentirse especiales.", M.ParagraphStyle("pq", fontName="GeorgiaI", fontSize=15, leading=21, textColor=WHITE), 1.85*S, H-5.78*S, 10.2*S)
    c.setFillColor(colors.HexColor("#E8C9A7")); c.setFont("Helvetica-Bold", 9.5); c.drawString(1.85*S, H-6.78*S, "CLUB PARTNER EN IRLANDA · PRIMERA LIGA DE SU HISTORIA, TRAS TRES AÑOS CON ALWAYS UP")
    s.done()

    # 7 forma de trabajar --------------------------------------------------
    s = new(CREAM); s.eyebrow("Nuestra forma de trabajar"); s.logo(); s.title("Programas a medida, no paquetes cerrados", w=10.8)
    s.text("Un club, un colegio y una academia tienen edades, niveles, objetivos, fechas y presupuestos distintos. Gracias a nuestros acuerdos con los clubes y al uso de sus instalaciones y residencias, diseñamos cada programa partiendo de lo que necesita tu cliente, no de un catálogo.", 0.75, 1.9, 11.5, 13.5)
    steps = [("chat", "Escuchamos", "Conocemos a cada grupo: perfil, edades, nivel, objetivos deportivos y formativos, fechas y presupuesto."),
             ("compass", "Diseñamos", "Proponemos el programa ideal: club, duración, contenidos, partidos, torneos y actividades."),
             ("handshake", "Coordinamos", "Cerramos todo con los clubes y proveedores: instalaciones, entrenadores, alojamiento y transporte."),
             ("person", "Acompañamos", "Un único interlocutor antes, durante y después del viaje, y seguimiento de resultados.")]
    for i, (ic, h_, b_) in enumerate(steps):
        x = 0.75+i*3.0; s.box(x, 3.2, 2.75, 3.0, WHITE)
        c.setFillColor(WINE); c.setFont("GeorgiaB", 24); c.drawString((x+0.3)*S, H-3.75*S, "0%d" % (i+1)); s.icon(ic, x+1.85, 3.38, 0.58, NAVY)
        c.setFillColor(NAVY); c.setFont("GeorgiaB", 17); c.drawString((x+0.3)*S, H-4.45*S, h_)
        para(c, b_, st("sw", fontSize=11.2, leading=15, textColor=GREY), (x+0.3)*S, H-4.62*S, 2.2*S)
    s.box(0.75, 6.4, 11.75, 0.65, NAVY)
    c.setFillColor(WHITE); c.setFont("GeorgiaB", 14.5); c.drawString(1.1*S, H-6.83*S, "Si lo que imaginas no está en esta propuesta, lo estudiamos con los clubes.")
    s.done()

    # 8 un programa para cada cliente --------------------------------------
    s = new(WHITE); s.eyebrow("Un programa para cada cliente"); s.logo(); s.title("Para cada uno de tus clientes", w=10.4)
    kinds = [("trophy_w", "Clubes", "Team Experience, pretemporadas, torneos internacionales y amistosos con academias españolas.", NAVY),
             ("book", "Colegios", "Viajes deportivos y culturales: entrenamientos con entrenadores de LaLiga, partidos, estadios y visitas, para todos los niveles.", WINE),
             ("runner", "Academias", "Team Experience de alto nivel, campus en Argentina con entrenadores de LaLiga y Coach Experience para su staff.", NAVY),
             ("board", "Entrenadores", "Coach Experience: ponencias, observación de entrenamientos y partidos en la academia del club.", WINE),
             ("grad", "Jugadores que quieren probar", "Venir a España a entrenar, jugar y probar con clubes, o seguir su camino con becas en EE. UU.", NAVY)]
    for i, (ic, h_, b_, col) in enumerate(kinds):
        x = 0.75+(i % 3)*4.0 if i < 3 else 0.75+(i-3)*4.0+2.0
        y0 = 2.05 if i < 3 else 4.65
        card_icon(s, ic, x, y0, 3.75, 2.4, h_, b_, fill=col, bg=CREAM, hs=15, dark=(i == 4))
    s.done()

    # 8b jugadores a España ------------------------------------------------
    s = new(WHITE); s.photo(os.path.join(SOC, "atm_entrenamiento.png"), 0, 0, 5.0, 7.5, (0.5, 0.5)); s.logo()
    s.eyebrow("Servicio · Jugadores en España", 5.6); s.title("Que tus jugadores vivan el fútbol español", 5.6, 0.95, 7.1, 26)
    s.text("Entrenar, jugar y probar: una forma de que tus jugadores vean de cerca cómo se trabaja en un club de LaLiga.", 5.6, 2.25, 7.0, 12.5, INK)
    yy = 3.15
    for ic, h_, b_ in [("runner", "Entrenar en la cantera", "De una semana a un mes entrenando con la metodología de un club de LaLiga, con alojamiento y comidas en la residencia."),
                       ("trophy", "Jugar partidos", "Amistosos contra equipos de la zona y de academias, con informe individual de cada jugador al terminar."),
                       ("binoc", "Probar con clubes españoles", "Organizamos pruebas en clubes para jugadores mayores de edad. Con menores, experiencias de entrenamiento, siempre cumpliendo la normativa FIFA."),
                       ("globe", "Quedarse más tiempo", "Programa Internacional con la Real Sociedad: 1, 5 o 10 meses, con apoyo académico y clases de español.")]:
        hh = item(s, ic, 5.6, yy, h_, b_, w=7.0, d=0.46, hs=12.5); yy += max(0.9, hh/S+0.3)
    c.setFillColor(GREY); c.setFont("Helvetica-Oblique", 9.5); c.drawString(5.6*S, H-7.05*S, "Las pruebas no garantizan un fichaje: dependen del nivel del jugador y del interés de cada club.")
    s.done()

    # 9 team experience -----------------------------------------------------
    s = new(WHITE); s.photo(f"{NW}/au_p12_0.png", 0, 0, 4.9, 7.5, (0.5, 0.45)); s.logo()
    s.eyebrow("Servicio · Team Experience", 5.5); s.title("El sueño de cualquier jugador", 5.5, 0.95, 6.4)
    yy = 2.05
    for ic, h_, b_ in [("runner", "Entrenamientos con la academia del club", "Dirigidos por entrenadores del club, adaptados a cada categoría y etapa formativa."),
                       ("trophy", "Partidos amistosos", "Contra equipos de la academia y de la zona, ajustados al nivel del equipo."),
                       ("book", "Sesiones formativas", "Metodología, nutrición, psicología deportiva y valores."),
                       ("stadium", "Estadio, museo y partidos", "Visita al estadio y posibilidad de asistir a partidos del primer equipo."),
                       ("bed", "Residencia del club u hotel", "Pensión completa, traslados desde el aeropuerto y acompañamiento durante toda la estancia.")]:
        item(s, ic, 5.5, yy, h_, b_, w=6.4, d=0.5, hs=13); yy += 0.92
    c.setFillColor(NAVY); c.setFont("GeorgiaI", 12.5); c.drawString(5.5*S, H-6.9*S, "Duración a medida: habitualmente de 5 a 10 días.")
    s.done()

    # 10 semana tipo --------------------------------------------------------
    s = new(CREAM); s.eyebrow("Un ejemplo real"); s.logo(); s.title("Una semana tipo en la residencia del Atlético", w=10.6)
    s.text("Cinco días con pensión completa, todos los traslados y sesiones de hora y media cada día. Cada programa se construye a medida de cada grupo.", 0.75, 1.9, 7.6, 12.5)
    days = [("LUNES", "Llegada a Madrid, traslado a la residencia y charla de valores del club."), ("MARTES", "Entrenamiento colectivo por la mañana y partido contra un equipo de cantera por la tarde."),
            ("MIÉRCOLES", "Visionado de un entrenamiento, visita al estadio y museo del Metropolitano y partido."), ("JUEVES", "Entrenamiento por la mañana y partido; visionado del primer equipo si el calendario lo permite."),
            ("VIERNES", "Última sesión y salida.")]
    yy = 3.0
    for d_, t_ in days:
        s.box(0.75, yy, 1.35, 0.4, WINE, 4); c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 9.5); c.drawCentredString((0.75+0.675)*S, H-(yy+0.26)*S, d_)
        para(c, t_, st("dy", fontSize=12, leading=16, textColor=INK), 2.3*S, H-(yy-0.02)*S, 5.7*S); yy += 0.82
    s.photo(f"{IM}/tebro_p06_2.png", 8.7, 1.8, 4.0, 1.95, (0.5, 0.5), "Academia · Atlético de Madrid")
    s.photo(f"{IM}/tebro_p07_3.png", 8.7, 3.9, 4.0, 1.4, (0.5, 0.5), "Residencia del club")
    s.photo(f"{IM}/tebro_p16_2.png", 8.7, 5.45, 4.0, 1.4, (0.5, 0.5), "Gimnasio de alto rendimiento")
    s.done()

    # 11 campus -------------------------------------------------------------
    s = new(WHITE); s.photo(f"{NW}/au_p13_2.png", 0, 0, 5.7, 7.5, (0.5, 0.5)); s.logo()
    s.eyebrow("Servicio · Campus internacional", 6.3); s.title("Llevamos LaLiga a Argentina", 6.3, 0.95, 6.3)
    s.text("Entrenadores oficiales de la academia de un club de LaLiga viajan a Argentina para dirigir campus con su metodología en los clubes, colegios y academias con los que trabajas.", 6.3, 2.0, 6.2, 12.5, INK)
    yy = 3.4
    for ic, h_, b_ in [("board", "Entrenadores oficiales del club", "El número de entrenadores se ajusta a la cantidad de participantes."), ("group", "Los entrenadores locales, parte del proyecto", "Trabajan junto a los técnicos del club y se forman en su metodología."),
                       ("shield", "Imagen oficial del club", "Equipación oficial, diplomas y promoción con la imagen del club, siempre con su aprobación."), ("globe", "Un producto nuevo para tu cartera", "Sin que tus clientes tengan que viajar, y como puerta de entrada a un viaje a España.")]:
        item(s, ic, 6.3, yy, h_, b_, w=6.0, d=0.46, hs=12.5); yy += 0.86
    s.box(6.3, 6.85, 6.4, 0.42, CREAM, 4); c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 10); c.drawString(6.5*S, H-7.12*S, "Funciona a partir de un número mínimo de participantes: lo estudiamos con tu volumen.")
    s.done()

    # 12 más servicios ------------------------------------------------------
    s = new(CREAM); s.eyebrow("Más servicios para tus clientes"); s.logo(); s.title("Servicios que se combinan entre sí", w=10.4)
    cols = [("runner", "Jugadores en España", WINE, ["Entrenar y jugar en la cantera de un club de LaLiga", "Pruebas en clubes para mayores de edad", "De una semana a una temporada completa"]),
            ("board", "Coach Experience", NAVY, ["Ponencias con los departamentos del club", "Observación de entrenamientos de U12 a U19", "Metodología, preparación física, porteros y análisis"]),
            ("trophy", "Torneos y stages", WINE, ["MadCup (Madrid, finales de junio) y DonostiCup (San Sebastián, julio)", "Torneos de academias en invierno y Semana Santa", "Pretemporadas y stages a medida"]),
            ("grad", "Becas en EE. UU.", NAVY, ["Evaluación, perfil y vídeo de presentación", "Contacto con universidades y high schools", "Trámites, visado y acompañamiento. Las becas no se pueden garantizar"])]
    cw4 = 2.85
    for i, (ic, h_, col, items_) in enumerate(cols):
        x = 0.75+i*(cw4+0.12); s.box(x, 2.05, cw4, 4.4, WHITE); s.icon(ic, x+0.25, 2.3, 0.58, col)
        c.setFillColor(NAVY); c.setFont("GeorgiaB", 15); c.drawString((x+0.25)*S, H-3.35*S, h_)
        yy = 3.7
        for t_ in items_:
            c.setFillColor(WINE); c.rect((x+0.25)*S, H-(yy+0.14)*S, 5, 5, stroke=0, fill=1)
            hh = para(c, t_, st("ms", fontSize=11, leading=15, textColor=INK), (x+0.45)*S, H-yy*S, (cw4-0.65)*S); yy += max(0.55, hh/S+0.2)
    s.done()

    # 13 año 2028 -----------------------------------------------------------
    s = new(WHITE); s.eyebrow("Ejemplo ilustrativo"); s.logo(); s.title(f"Un año {ANIO} de trabajo conjunto", w=10)
    s.text("Así podría organizarse la oferta para tus clientes a lo largo del año, aprovechando el calendario argentino.", 0.75, 1.75, 11, 13)
    s.rect(0.75, 3.35, 11.75, 0.06, NAVY)
    tl = [("ENE – FEB", "Grupos a España y campus", "Tu verano coincide con la temporada española en plena competición. O campus en Argentina.", NAVY),
          ("MAR – ABR", "Coach Experience", "Formación en España para entrenadores de clubes y academias.", WINE),
          ("JUL", "Vacaciones de invierno", "Grupos de colegios y clubes: MadCup, DonostiCup y experiencias en clubes de LaLiga.", NAVY),
          ("TODO EL AÑO", "Jugadores en España", "Una semana, un mes o una temporada entrenando y probando con clubes.", WINE),
          ("TODO EL AÑO", "Becas en EE. UU.", "Acompañamiento a jugadores con proyección universitaria.", NAVY)]
    for i, (when, h_, b_, col) in enumerate(tl):
        x = 0.75+i*2.38; c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 10.5); c.drawString(x*S, H-2.85*S, when)
        c.setFillColor(col); c.circle((x+0.2)*S, H-3.38*S, 0.2*S, stroke=0, fill=1)
        s.box(x, 3.9, 2.25, 2.7, CREAM)
        para(c, h_, M.ParagraphStyle("th", fontName="GeorgiaB", fontSize=14, leading=17, textColor=NAVY), (x+0.2)*S, H-4.1*S, 1.9*S)
        para(c, b_, st("tb", fontSize=10.5, leading=14.5, textColor=GREY), (x+0.2)*S, H-4.85*S, 1.9*S)
    s.done()

    # 14 formas de trabajar juntos -----------------------------------------
    s = new(CREAM); s.eyebrow("Colaboración"); s.logo(); s.title("Tres formas de trabajar juntos", w=10)
    s.text("No hay un solo modelo. Elegimos contigo el que mejor encaje con tu comunidad y tus clientes.", 0.75, 1.75, 11, 13)
    for i, (l_, h_, b_) in enumerate([("A", "Tú traes, nosotros operamos", "Presentas grupos, familias o clubes de tu red y nosotros nos encargamos de todo: programa, clubes, alojamiento, traslados y seguimiento. Tú mantienes la relación con tu cliente."),
                                      ("B", "Programas con tu marca", "Programas diseñados para tu comunidad, con fechas y plazas por temporada, que presentas como propios con el respaldo de los clubes."),
                                      ("C", "Alianza anual", f"Un calendario compartido para {ANIO} con varios servicios: equipos, entrenadores, jugadores y becas, planificado con tiempo.")]):
        x = 0.75+i*4.0; dark = i == 1
        s.box(x, 2.5, 3.75, 3.4, NAVY if dark else WHITE)
        c.setFillColor(CREAM if dark else WINE); c.circle((x+0.55)*S, H-3.0*S, 0.3*S, stroke=0, fill=1)
        c.setFillColor(NAVY if dark else WHITE); c.setFont("GeorgiaB", 17); c.drawCentredString((x+0.55)*S, H-3.08*S, l_)
        para(c, h_, M.ParagraphStyle("fh", fontName="GeorgiaB", fontSize=17, leading=21, textColor=WHITE if dark else NAVY), (x+1.0)*S, H-2.78*S, 2.5*S)
        para(c, b_, st("fb", fontSize=12, leading=17, textColor=WHITE if dark else GREY), (x+0.35)*S, H-3.65*S, 3.1*S)
    s.box(0.75, 6.1, 11.75, 0.95, WHITE); s.rect(0.75, 6.1, 0.07, 0.95, WINE)
    para(c, "<b>Condiciones claras y por escrito antes de cualquier reserva.</b> Se definen juntos según el volumen, los servicios y las fechas. Empezar con un primer grupo piloto nos permite probar el modelo sin riesgo antes de ampliarlo.", st("cn", fontSize=12, leading=17, textColor=INK), 1.1*S, H-6.25*S, 11.2*S)
    s.done()

    # 15 preguntas ----------------------------------------------------------
    s = new(WHITE); s.eyebrow("Para preparar tu propuesta"); s.logo(); s.title("Lo que nos ayudaría saber", w=10)
    s.text("Con tus respuestas preparamos una propuesta concreta, no genérica.", 0.75, 1.75, 11, 13)
    qs = [("group", "Tus grupos", "¿Qué edades, niveles y tipos de grupo mueves (equipos, colegios, familias)?"), ("chart", f"Volumen para {ANIO}", "¿Cuántas personas te gustaría mover y en qué ventanas del año?"),
          ("heart", "Lo que valoran", "¿Qué buscan hoy tus clientes: competir, formarse, vivir la experiencia?"), ("plane", "Cómo viajan hoy", "¿Cómo organizas los viajes actuales y qué te gustaría mejorar?"),
          ("ticket", "Presupuesto", "¿Qué rango por persona maneja tu comunidad?"), ("grad", "Otros servicios", "¿Te interesan también jugadores que quieran probar en España, entrenadores o becas en EE. UU.?")]
    for i, (ic, h_, b_) in enumerate(qs):
        card_icon(s, ic, 0.75+(i % 3)*4.0, 2.3+(i//3)*2.35, 3.75, 2.15, h_, b_, fill=NAVY if i % 2 == 0 else WINE, bg=CREAM, hs=16)
    s.done()

    # 16 próximos pasos -----------------------------------------------------
    s = new(NAVY); s.photo(os.path.join(SOC, "reale_arena.png"), 0, 0, 5.0, 7.5, (0.5, 0.5))
    s.eyebrow("Próximos pasos", 5.7, 0.8, colors.HexColor("#E8C9A7")); s.title("Empecemos a trabajar juntos", 5.7, 1.15, 7.0, 30, WHITE)
    yy = 2.4
    for i, (h_, b_) in enumerate([("Llamada de planificación", f"30 minutos esta semana o la próxima: tu cartera de clientes, tipos de grupos, volúmenes y fechas habituales. Mi idea es salir con un plan claro para {ANIO}."),
                                  ("Modelo de colaboración", f"Definimos juntos cómo trabajamos y las condiciones para la temporada {ANIO}, y te enviamos una propuesta por escrito."),
                                  ("Validación con los clubes", "Confirmamos disponibilidad de instalaciones, entrenadores y fechas."),
                                  ("Primer grupo piloto", "Empezamos con un primer grupo y ampliamos juntos: reserva, planificación deportiva y acompañamiento hasta el último día.")]):
        c.setFillColor(WINE); c.circle(5.98*S, H-(yy+0.28)*S, 0.28*S, stroke=0, fill=1); c.setFillColor(WHITE); c.setFont("GeorgiaB", 15); c.drawCentredString(5.98*S, H-(yy+0.34)*S, str(i+1))
        c.setFillColor(WHITE); c.setFont("GeorgiaB", 15.5); c.drawString(6.5*S, H-(yy+0.22)*S, h_)
        hh = para(c, b_, st("ns", fontSize=11.5, leading=15.5, textColor=colors.HexColor("#DCE3EC")), 6.5*S, H-(yy+0.35)*S, 6.2*S)
        yy += max(1.0, 0.5+hh/S)
    s.done()

    # 17 cierre -------------------------------------------------------------
    s = new(CREAM)
    c.drawImage(img("aguila.png"), 7.0*S, H-(0.9+4.98)*S, 5.9*S, 4.98*S, mask="auto")
    c.drawImage(img("logo.png"), 0.85*S, H-(1.1+1.7)*S, 2.6*S, 1.7*S, mask="auto")
    para(c, "Siempre arriba. Siempre a medida.", M.ParagraphStyle("end", fontName="GeorgiaB", fontSize=32, leading=38, textColor=NAVY), 0.85*S, H-3.15*S, 6.0*S)
    yy = 4.85
    for k, v in [("Correo", "joel.martinez@alwaysup.es"), ("Teléfono", "+1 (814) 329 1929")]:
        c.setFillColor(WINE); c.setFont("Helvetica-Bold", 10); c.drawString(0.85*S, H-yy*S, k.upper()); c.setFillColor(INK); c.setFont("Helvetica", 15); c.drawString(0.85*S, H-(yy+0.34)*S, v); yy += 0.85
    c.showPage()
    c.save()
    return OUT


if __name__ == "__main__":
    print(build())
