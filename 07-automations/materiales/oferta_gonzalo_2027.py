#!/usr/bin/env python3
"""Oferta 2027 para Gonzalo Lamas (Argentina): productos cerrados con precio para socio. 16:9, español.

Uso:  python3 oferta_gonzalo_2027.py   -> 01-clients/propuestas/Always-Up-Oferta-2027-Argentina-Gonzalo.pdf
Contenido y números: 01-clients/propuestas/gonzalo-2027-opciones.md (20/11/2026). Precios del Atlético 2026-2027.
Los precios para el socio salen del modelo A (precio socio neto, margen del 25 %): si Enrique decide otro modelo
el lunes 23/11, se cambian las constantes de abajo y se regenera (1 minuto). No se envía sin el OK de Joel y Enrique.
Reutiliza el diseño de propuesta_socio.py (misma carpeta).
"""
import os

import propuesta_socio as P
from propuesta_socio import (M, NAVY, WINE, CREAM, INK, GREY, WHITE, W, H, S, Slide, item, card_icon, para, st, img, colors, canvas)

OUT = os.path.abspath(os.path.join(P.HERE, "..", "..", "01-clients", "propuestas", "Always-Up-Oferta-2027-Argentina-Gonzalo.pdf"))
NW, IM, SOC = P.NW, P.IM, P.SOC

# Precios para el socio (modelo A). Cambiar aquí si Enrique decide otra cosa.
CAMPUS_70 = "14.130 €"      # 8.000 / 0,75 = 10.700 + 70 kits a 49 €
CAMPUS_140 = "20.210 €"     # 10.000 / 0,75 = 13.350 + 140 kits a 49 €
CAMPUS_140_NINO = "unos 160 €"
COACH_SOCIO = "2.450 €"
TEAM_REF = "unos 1.500 €"
PROG12 = "2.300 €"
BECAS = "2.500 €"
SAND = colors.HexColor("#E8C9A7")


def build():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    c = canvas.Canvas(OUT, pagesize=(W, H)); c.setTitle("Always Up - Oferta 2027 para Argentina"); c.setAuthor("Always Up")
    n = [0]

    def new(bg=WHITE):
        n[0] += 1; return Slide(c, bg, n[0])

    def bullets(x, y, w, rows, size=11.5, gap=0.16):
        for t_ in rows:
            c.setFillColor(WINE); c.rect(x*S, H-(y+0.15)*S, 5, 5, stroke=0, fill=1)
            hh = para(c, t_, st("bl", fontSize=size, leading=size*1.36, textColor=INK), (x+0.22)*S, H-y*S, (w-0.22)*S)
            y += hh/S + gap
        return y

    def pricebox(x, y, w, h, label, value, note, dark=True):
        s.box(x, y, w, h, NAVY if dark else WHITE)
        c.setFillColor(SAND if dark else WINE); c.setFont("Helvetica-Bold", 9.5); c.drawString((x+0.25)*S, H-(y+0.38)*S, label.upper())
        c.setFillColor(WHITE if dark else NAVY); c.setFont("GeorgiaB", 24); c.drawString((x+0.25)*S, H-(y+0.95)*S, value)
        para(c, note, st("pn", fontSize=10.5, leading=14, textColor=colors.HexColor("#DCE3EC") if dark else GREY), (x+0.25)*S, H-(y+1.12)*S, (w-0.5)*S)

    # 1 portada ------------------------------------------------------------
    s = new(CREAM)
    s.rect(4.4, 0, 9.0, 7.5, NAVY)
    s.photo(f"{NW}/au_p13_2.png", 4.75, 0.8, 8.1, 5.9, (0.5, 0.5))
    c.drawImage(img("logo.png"), 0.6*S, H-(0.55+1.45)*S, 2.2*S, 1.45*S, mask="auto")
    s.eyebrow("Oferta 2027", 0.6, 2.45)
    s.title("Lo que podemos hacer juntos en 2027", 0.6, 2.8, 3.6, 25)
    s.text("Productos cerrados, con precio para ti, para tus colegios, clubes y jugadores en Argentina.", 0.6, 4.5, 3.5, 12.5)
    s.rect(0.6, 6.2, 0.6, 0.06, WINE)
    c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 12); c.drawString(0.6*S, H-6.62*S, "Preparado para Gonzalo Lamas · Argentina")
    c.showPage()

    # 2 resumen -------------------------------------------------------------
    s = new(WHITE); s.eyebrow("Resumen"); s.logo(); s.title("Cinco productos listos para 2027", w=10)
    s.text("Tú vendes a tu comunidad; nosotros lo organizamos todo en España y con los clubes. Precios por persona, sin vuelos.", 0.75, 1.75, 11, 13)
    rows = [("stadium", "Campus del Atlético en Argentina", f"Julio de 2027. Técnicos del Atlético en tu ciudad. Desde {CAMPUS_140_NINO} por niño para ti.", WINE),
            ("board", "Coach Experience en el Atlético", f"5 días en Madrid, grupo de 5 o más, en español. {COACH_SOCIO} por entrenador.", NAVY),
            ("runner", "12 días en el Real Unión", f"Jugadores de 18 años o más, cuando quieran empezar. {PROG12}.", WINE),
            ("grad", "Becas en EE. UU.", f"Jugadores de 16 a 22 para la temporada 2027/28. {BECAS}.", NAVY),
            ("trophy", "Team Experience en el Atlético", f"Equipos y colegios, 5 días en la residencia del club. {TEAM_REF[0].upper()+TEAM_REF[1:]} por jugador.", WINE)]
    for i, (ic, h_, b_, col) in enumerate(rows):
        x = 0.75+(i % 3)*4.0 if i < 3 else 0.75+(i-3)*4.0+2.0
        y0 = 2.3 if i < 3 else 4.8
        card_icon(s, ic, x, y0, 3.75, 2.35, h_, b_, fill=col, bg=CREAM, hs=15)
    s.done()

    # 3 campus: qué es ------------------------------------------------------
    s = new(WHITE); s.photo(f"{IM}/tebro_p06_2.png", 0, 0, 5.0, 7.5, (0.5, 0.5)); s.logo()
    s.eyebrow("1 · Campus del Atlético de Madrid en Argentina", 5.6); s.title("El Atlético, en tus colegios y clubes", 5.6, 0.95, 7.1, 26)
    s.text("Técnicos oficiales de la academia del Atlético viajan a Argentina y dirigen durante 5 días un campus con su metodología, junto a tus entrenadores.", 5.6, 2.25, 7.0, 12.5, INK)
    yy = 3.25
    for ic, h_, b_ in [("board", "Técnicos oficiales del club", "1 técnico del Atlético por cada 35 niños, con 2 entrenadores tuyos por técnico."),
                       ("shield", "Kit oficial Nike del club", "Camiseta, pantalón y medias, fabricados por Nike España, y diploma del club."),
                       ("group", "Tus entrenadores aprenden", "Trabajan toda la semana con los técnicos del Atlético y se quedan con su forma de entrenar."),
                       ("calendar" if False else "flag", "Cuándo", "Julio de 2027, en las vacaciones de invierno (la semana se ajusta a tu provincia).")]:
        hh = item(s, ic, 5.6, yy, h_, b_, w=7.0, d=0.46, hs=12.5); yy += max(0.9, hh/S+0.28)
    s.done()

    # 4 campus: formatos y precio ------------------------------------------
    s = new(CREAM); s.eyebrow("1 · Campus: formatos y precio"); s.logo(); s.title("Dos formatos, con precio cerrado", w=10)
    s.text("Precio fijo por campus para ti, con los kits incluidos. Tú pones el precio a las familias.", 0.75, 1.75, 11, 13)
    pricebox(0.75, 2.45, 5.7, 1.75, "70 niños · 2 técnicos · jornada completa", CAMPUS_70, "5 días. Unos 230 € por niño contando los gastos de viaje de los técnicos.", dark=False)
    pricebox(6.8, 2.45, 5.7, 1.75, "140 niños · 2 técnicos · doble turno (70 + 70)", CAMPUS_140, f"5 días, mañana y tarde. {CAMPUS_140_NINO[0].upper()+CAMPUS_140_NINO[1:]} por niño contando los gastos de viaje. Es el que más te deja.")
    s.box(0.75, 4.45, 11.75, 2.65, WHITE)
    c.setFillColor(NAVY); c.setFont("GeorgiaB", 15); c.drawString(1.05*S, H-4.9*S, "Un día del campus (doble turno)")
    days = [("9:00", "Turno de mañana: activación, técnica individual y trabajo por puestos con la metodología del Atlético."),
            ("11:00", "Juego reducido y partido. Al terminar, un mensaje de valores del club."),
            ("14:30", "Turno de tarde: el mismo programa para el segundo grupo de 70."),
            ("Viernes", "Último partido, entrega de diplomas y foto con los técnicos del club.")]
    yy = 5.15
    for d_, t_ in days:
        s.box(1.05, yy, 1.05, 0.34, WINE, 4); c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 9.5); c.drawCentredString(1.575*S, H-(yy+0.23)*S, d_)
        para(c, t_, st("cd", fontSize=11, leading=14.5, textColor=INK), 2.3*S, H-(yy+0.02)*S, 9.9*S); yy += 0.46
    s.done()

    # 5 campus: quién hace qué ---------------------------------------------
    s = new(WHITE); s.eyebrow("1 · Campus: cómo lo hacemos"); s.logo(); s.title("Quién hace qué", w=10)
    s.box(0.75, 1.85, 5.75, 3.6, CREAM)
    s.icon("handshake", 1.0, 2.05, 0.55, NAVY); c.setFillColor(NAVY); c.setFont("GeorgiaB", 16); c.drawString(1.75*S, H-2.42*S, "Always Up")
    bullets(1.0, 2.85, 5.25, ["El contrato con el Atlético y toda la relación con el club.",
                              "El plan del campus, las fechas y los técnicos.",
                              "El pedido de los kits Nike y la aprobación del material de promoción por el club.",
                              "Un interlocutor contigo antes, durante y después."])
    s.box(6.75, 1.85, 5.75, 3.6, NAVY)
    s.icon("group", 7.0, 2.05, 0.55, WINE); c.setFillColor(WHITE); c.setFont("GeorgiaB", 16); c.drawString(7.75*S, H-2.42*S, "Tú")
    yy = 2.85
    for t_ in ["Las instalaciones (2 o 3 campos) y 2 entrenadores por cada técnico del Atlético.",
               "Vuelos, hotel, comidas, transporte y seguro de los 2 técnicos (unos 2.100 €).",
               "La inscripción y el cobro a las familias, y la promoción.",
               "El envío de los kits a Argentina."]:
        c.setFillColor(SAND); c.rect(7.0*S, H-(yy+0.15)*S, 5, 5, stroke=0, fill=1)
        hh = para(c, t_, st("bw", fontSize=11.5, leading=15.6, textColor=WHITE), 7.22*S, H-yy*S, 5.0*S); yy += hh/S+0.16
    s.box(0.75, 5.7, 11.75, 1.4, CREAM); s.rect(0.75, 5.7, 0.07, 1.4, WINE)
    c.setFillColor(NAVY); c.setFont("GeorgiaB", 14); c.drawString(1.1*S, H-6.08*S, "Plazos para julio de 2027")
    para(c, "Firma y 50 % del campus: en abril (90 días antes). Pedido de los kits: a finales de mayo (45 días antes). Resto del pago: 30 días antes. "
            "El club aprueba la promoción y no se puede prometer el paso a la academia del Atlético.", st("pz", fontSize=11.3, leading=15.5, textColor=INK), 1.1*S, H-6.25*S, 11.2*S)
    s.done()

    # 6 coach experience ----------------------------------------------------
    s = new(WHITE); s.photo(os.path.join(SOC, "atm_entrenamiento.png"), 0, 0, 5.0, 7.5, (0.5, 0.5)); s.logo()
    s.eyebrow("2 · Coach Experience", 5.6); s.title("Una semana dentro de la academia del Atlético", 5.6, 0.95, 7.1, 24)
    s.text("Para un grupo de 5 o más entrenadores de tus clubes o colegios. Todo en español. La fecha la elige el grupo, de septiembre a junio.", 5.6, 2.25, 7.0, 12.5, INK)
    yy = bullets(5.6, 3.15, 7.0, ["<b>Mañanas:</b> entrenamiento de un equipo U17, U19 o U20 y charla de un departamento del club (Metodología, Preparación Física, Desarrollo Individual, Análisis de Juego, Valores).",
                                  "<b>Tardes:</b> entrenamientos del alto rendimiento (U12 a U16) en Majadahonda.",
                                  "<b>Fin de semana:</b> partido de la cantera y, si coincide, del primer equipo (entradas aparte).",
                                  "<b>Incluye:</b> alojamiento y comidas, traslados en Madrid, visita al estadio y museo, y certificado del club."], size=11.2)
    pricebox(5.6, 6.0, 4.0, 1.2, "Precio para ti, por entrenador", COACH_SOCIO, "")
    c.setFillColor(GREY); c.setFont("Helvetica-Oblique", 10); c.drawString(9.85*S, H-6.55*S, "Grupo mínimo: 5 entrenadores."); c.drawString(9.85*S, H-6.8*S, "Mejores meses: febrero a mayo.")
    s.done()

    # 7 jugadores 12 dias ---------------------------------------------------
    s = new(CREAM); s.eyebrow("3 · Jugadores de 18 años o más"); s.logo(); s.title("12 días entrenando en el Real Unión de Irún", w=10.6)
    s.text("Un programa de entrenamiento para jugadores que quieren vivir el día a día de un club español. Empiezan cuando quieran, según el calendario del club.", 0.75, 1.9, 7.4, 12.5)
    bullets(0.75, 3.0, 7.3, ["Entrenamiento diario con el grupo que fije el club, según el nivel del jugador.",
                             "Piso del club, pensión completa y kit de entrenamiento del club.",
                             "Recogida en el aeropuerto y una persona de contacto en Irún.",
                             "Dos sesiones grabadas, vídeo resumen e informe final del cuerpo técnico.",
                             "Es un programa de entrenamiento, no una prueba: no se promete ningún fichaje."], size=11.5)
    pricebox(8.6, 2.0, 3.9, 1.6, "Precio por jugador", PROG12, "12 días, sin vuelos. El jugador trae su seguro médico internacional.")
    s.box(8.6, 3.85, 3.9, 3.15, WHITE)
    c.setFillColor(NAVY); c.setFont("GeorgiaB", 14); c.drawString(8.85*S, H-4.25*S, "Cómo se apunta")
    yy = 4.5
    for i, t_ in enumerate(["Rellena la solicitud con su vídeo y su trayectoria.", "El club la revisa y contesta en 5 días como máximo.",
                            "Reserva su plaza con el 30 %.", "Le enviamos la guía de llegada antes de viajar."]):
        c.setFillColor(WINE); c.setFont("GeorgiaB", 12); c.drawString(8.85*S, H-(yy+0.13)*S, str(i+1))
        hh = para(c, t_, st("ap", fontSize=10.8, leading=14, textColor=INK), 9.15*S, H-yy*S, 3.15*S); yy += hh/S+0.16
    s.done()

    # 8 becas ---------------------------------------------------------------
    s = new(WHITE); s.eyebrow("4 · Becas en EE. UU."); s.logo(); s.title("Fútbol y universidad en Estados Unidos", w=10)
    s.text("Ahora es el momento: las universidades están cerrando sus plantillas para agosto de 2027.", 0.75, 1.75, 11, 13)
    steps = [("binoc", "Evaluación", "Con vídeo y notas, vemos qué nivel de universidad tiene sentido real para cada jugador."),
             ("person", "Perfil", "Preparamos su perfil deportivo y académico para los entrenadores."),
             ("chat", "Universidades", "Contacto con entrenadores de universidades y negociación de la oferta."),
             ("plane", "Trámites", "Admisión, visado y acompañamiento hasta que empieza.")]
    for i, (ic, h_, b_) in enumerate(steps):
        card_icon(s, ic, 0.75+i*2.97, 2.45, 2.82, 2.6, h_, b_, num="0%d" % (i+1), fill=NAVY if i % 2 == 0 else WINE, bg=CREAM, hs=15)
    pricebox(0.75, 5.35, 5.0, 1.65, "Precio por jugador", BECAS, "O en plazos: una parte al empezar y el resto al aceptar una oferta.")
    s.box(6.0, 5.35, 6.5, 1.65, CREAM)
    para(c, "<b>Para quién:</b> jugadores de 16 a 22 años con nivel y notas para jugar y estudiar en una universidad. No se puede garantizar una beca: depende del nivel del jugador y del interés de cada universidad.",
         st("bc", fontSize=11.3, leading=15.5, textColor=INK), 6.3*S, H-5.6*S, 6.0*S)
    s.done()

    # 9 team experience -----------------------------------------------------
    s = new(WHITE); s.photo(f"{NW}/au_p12_0.png", 0, 0, 4.9, 7.5, (0.5, 0.45)); s.logo()
    s.eyebrow("5 · Team Experience", 5.5); s.title("Tus equipos, en la residencia del Atlético", 5.5, 0.95, 6.9, 25)
    s.text("Para equipos y colegios. La fecha la elige el grupo; lo habitual es julio para Argentina.", 5.5, 2.25, 6.9, 12.5, INK)
    bullets(5.5, 3.0, 6.9, ["Residencia oficial del club, pensión completa, lavandería y traslados en Madrid.",
                            "Entrenamientos con técnicos del Atlético y partido contra su academia (si el club acepta el nivel del rival).",
                            "Charla de historia y valores, estadio y museo, certificado del club y seguro de accidentes deportivos."], size=11.5)
    pricebox(5.5, 5.35, 3.6, 1.65, "Referencia por jugador", TEAM_REF, "5 días, sin vuelos. Grupo desde 15.")
    s.box(9.3, 5.35, 3.2, 1.65, CREAM)
    para(c, "Para 2027 o 2028. Los precios de la temporada siguiente están pendientes de actualizar con el club.", st("tr", fontSize=11, leading=15, textColor=INK), 9.5*S, H-5.6*S, 2.85*S)
    s.done()

    # 10 cómo trabajamos ----------------------------------------------------
    s = new(CREAM); s.eyebrow("Cómo trabajamos juntos"); s.logo(); s.title("Simple y por escrito", w=10)
    blocks = [("handshake", "Grupos: precio para ti", "Campus, entrenadores y equipos. Te damos un precio cerrado; tú pones el precio final y cobras a tus clientes en Argentina."),
              ("person", "Jugadores: los traes tú", "12 días y becas. El jugador firma y paga con nosotros, y tú cobras tu parte por cada jugador que traes."),
              ("ticket", "Pagos", "30 % al reservar y el resto 30 días antes. En el campus, 50 % al firmar."),
              ("shield", "Sin sorpresas", "Condiciones por escrito antes de cualquier reserva. Empezamos con un primer grupo y ampliamos.")]
    for i, (ic, h_, b_) in enumerate(blocks):
        card_icon(s, ic, 0.75+(i % 2)*6.0, 2.0+(i//2)*2.6, 5.75, 2.4, h_, b_, fill=NAVY if i % 2 == 0 else WINE, bg=WHITE, hs=16)
    s.done()

    # 11 próximos pasos -----------------------------------------------------
    s = new(NAVY); s.photo(os.path.join(SOC, "reale_arena.png"), 0, 0, 5.0, 7.5, (0.5, 0.5))
    s.eyebrow("Próximos pasos", 5.7, 0.8, SAND); s.title("Empecemos por uno", 5.7, 1.15, 7.0, 30, WHITE)
    yy = 2.4
    for i, (h_, b_) in enumerate([("Elige", "Uno o dos productos para 2027, con número de personas y mes."),
                                  ("Propuesta en 48 horas", "Te enviamos la propuesta por escrito con fechas, precio y condiciones."),
                                  ("Confirmamos con el club", "Fechas, técnicos e instalaciones."),
                                  ("Y 2028", "Con tu volumen, reservamos con tiempo los equipos y colegios del año siguiente.")]):
        c.setFillColor(WINE); c.circle(5.98*S, H-(yy+0.28)*S, 0.28*S, stroke=0, fill=1); c.setFillColor(WHITE); c.setFont("GeorgiaB", 15); c.drawCentredString(5.98*S, H-(yy+0.34)*S, str(i+1))
        c.setFillColor(WHITE); c.setFont("GeorgiaB", 15.5); c.drawString(6.5*S, H-(yy+0.22)*S, h_)
        hh = para(c, b_, st("ns", fontSize=11.5, leading=15.5, textColor=colors.HexColor("#DCE3EC")), 6.5*S, H-(yy+0.35)*S, 6.2*S)
        yy += max(1.0, 0.5+hh/S)
    c.setFillColor(SAND); c.setFont("Helvetica-Bold", 10); c.drawString(5.7*S, H-6.75*S, "JOEL MARTINEZ · joel.martinez@alwaysup.es · +1 (814) 329 1929")
    c.setFillColor(colors.HexColor("#DCE3EC")); c.setFont("Helvetica", 9); c.drawString(5.7*S, H-7.05*S, "Precios de la temporada 2026-2027 de los clubes, por persona y sin vuelos.")
    s.done()

    c.save()
    return OUT


if __name__ == "__main__":
    print(build())
