#!/usr/bin/env python3
"""Genera la hoja 'Outreach - Copiar y pegar' del CRM y actualiza el Segmento A con los correos preparados.

Uso:  python3 generar_outreach.py
Qué hace (idempotente, se puede ejecutar varias veces):
  1. Calcula el calendario de envíos (email 1, LinkedIn, follow-up 1, follow-up 2, cierre) por club.
  2. Reescribe la hoja 'Outreach - Copiar y pegar' en 01-clients/crm-ventas.xlsx con TODOS los textos finales.
  3. Actualiza en 'Segmento A - Clubes' contacto, email, asunto, cuerpo y próxima acción de los clubes preparados.
  4. Comprueba que ningún texto lleva placeholders sin rellenar ni nombres múltiples en el saludo.
Dependencias: openpyxl. Cerrar el Excel antes de ejecutar.
Para añadir un club: añadir una entrada a PROSPECTS (abajo) y volver a ejecutar.
"""
import datetime as dt
import os
import re
from zoneinfo import ZoneInfo

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

HERE = os.path.dirname(os.path.abspath(__file__))
CRM = os.path.join(HERE, "..", "..", "01-clients", "crm-ventas.xlsx")
SHEET = "Outreach - Copiar y pegar"

SIG = ("Joel Martinez\nFounder, Always Up\n"
       "joel.martinez@alwaysup.es | +1 (814) 329 1929 | alwaysup.es")
D = dt.date
NY = ZoneInfo("America/New_York")

# ---------------------------------------------------------------- prospectos
# tz: zona del destinatario. e1: fecha del email 1 (real o planificada). sent: ya enviado.
PROSPECTS = [
    dict(key="homefarm", club="Home Farm FC (chicas U13-U15)", short="Home Farm FC", tz="Europe/Dublin", sent=True,
         e1=D(2026, 10, 13), to="homefarmfc@gmail.com", greet="Hi all,", person=None,
         subj="Bringing Home Farm FC to train with Atlético de Madrid & Real Sociedad in Spain",
         linkedin=None, extra_dm="Facebook/Instagram de Home Farm FC"),
    dict(key="hastings", club="Hastings United (Girls Academy)", short="Hastings United", tz="Europe/London", sent=True,
         e1=D(2026, 10, 13), to="georgia.townsend@hastingsunited.com", greet="Hi Georgia,", person="Georgia Townsend (Head of Girls Academy)",
         subj="Bringing Hastings United's Girls Academy to train with LaLiga clubs in Spain",
         linkedin=(D(2026, 10, 15), "Georgia Townsend (Head of Girls Academy, Hastings United)"), extra_dm="Instagram de Hastings United"),
    dict(key="soreide", club="Søreide IL", short="Søreide IL", tz="Europe/Oslo", sent=False,
         e1=D(2026, 10, 14), to="fotball@soreideil.no", greet="Hi Marius and Gunn,", person="Marius Engen / Gunn Eklund Breisnes",
         subj="Training week in Spain for Søreide IL's youth teams",
         linkedin=(D(2026, 10, 16), "Marius Engen (Sportslig leder, Søreide IL fotball)"), extra_dm="Facebook/Instagram de Søreide IL",
         e1_body="""{greet}

I'm Joel, founder of Always Up. My first email bounced from your youth committee address, so I'm writing to you directly.

We organise training weeks in Spain for youth clubs: sessions at the facilities of Atlético de Madrid and Real Sociedad, matches against local academy teams, and accommodation and meals included.

I saw Søreide IL was listed for the Costa Daurada Cup in Salou this summer, so Spain may already be on your radar. A longtime partner club of ours won its first-ever league title after training with us.

Would you be open to a short call next week, or would you prefer a one-page overview first?

Best,
{sig}"""),
    dict(key="holbeach", club="Holbeach United", short="Holbeach United", tz="Europe/London", sent=False,
         e1=D(2026, 10, 14), to="callum@holbeachunitedacademy.com", greet="Hi Callum,", person="Callum Lawe (Vice Chairman, Football & Education Academy)",
         subj="Training week in Spain for Holbeach United's academy",
         linkedin=(D(2026, 10, 16), "Callum Lawe (Holbeach United Football & Education Academy)"), extra_dm="Instagram @holbeachunitedcsa",
         e1_body="""{greet}

I'm Joel, founder of Always Up. We organise training weeks in Spain for youth clubs: sessions at the facilities of Atlético de Madrid and Real Sociedad, matches against local academy teams and a stadium tour, with accommodation and meals included.

I saw Holbeach United was listed for the Costa Daurada Cup in Salou this year, and your Football & Education Academy stood out, so I thought a week in Spain could be a good fit for your older squads.

A longtime partner club of ours won its first-ever league title after training with us, and its coaches credit part of it to the experience.

Would you be open to a short call next week, or would you prefer I send a one-page overview first?

Best,
{sig}"""),
    dict(key="whitehaven", club="Whitehaven AFC (Juniors Girls U13-U15)", short="Whitehaven AFC", tz="Europe/London", sent=False,
         e1=D(2026, 10, 15), to="Luke.johnston@whitehavenafc.com", greet="Hi Luke,", person="Luke Johnston (Chairman)",
         subj="Training week in Spain for Whitehaven's girls teams",
         linkedin=(D(2026, 10, 19), "Luke Johnston (Chairman, Whitehaven AFC)"), extra_dm="Facebook de Whitehaven AFC",
         verify="Email obtenido de un buscador: comprobarlo en whitehavenafc.com/contact antes de enviar. Si es otro, usar el de la web.",
         e1_body="""{greet}

I'm Joel, founder of Always Up. We organise training weeks in Spain for youth clubs: sessions at the facilities of Atlético de Madrid and Real Sociedad, matches against local academy teams and a stadium tour, with accommodation and meals included.

I saw Whitehaven AFC was listed for the Costa Daurada Cup in Salou this summer, and the girls pathway (U13-U15) caught my eye. A longtime partner club of ours won its first-ever league title after training with us.

Would a short call next week work, or would you prefer a one-page overview first? And if you're not the right person, could you point me to whoever organises trips for the girls' section?

Best,
{sig}"""),
    dict(key="maidstone", club="Maidstone United (Girls Development Centre)", short="Maidstone United", tz="Europe/London", sent=False,
         e1=D(2026, 10, 15), to="info@maidstoneunited.co.uk", greet="Hi team,", person=None,
         subj="Question about the Girls Development Centre",
         linkedin=None, extra_dm="Facebook/Instagram de Maidstone United",
         e1_body="""{greet}

I'm Joel, founder of Always Up. We organise training weeks in Spain for youth clubs: sessions at the facilities of Atlético de Madrid and Real Sociedad, matches against local academy teams and a stadium tour, with accommodation and meals included.

I saw Maidstone United was in the Costa Daurada Cup line-up in Salou this summer and thought your Girls Development Centre could be a great fit. Could you point me to the right person to speak with about trips for the girls' teams?

A longtime partner club of ours won its first-ever league title after training with us, so I'd be glad to share how it worked for them.

Thanks a lot,
{sig}"""),
    dict(key="akranes", club="IA Akranes", short="ÍA Akranes", tz="Atlantic/Reykjavik", sent=False,
         e1=D(2026, 10, 15), to="kfia@ia.is", greet="Hi ÍA team,", person=None,
         subj="Question about youth trips to Spain",
         linkedin=None, extra_dm="Facebook/Instagram de ÍA Akranes",
         e1_body="""{greet}

I'm Joel, founder of Always Up. We organise training weeks in Spain for youth clubs: sessions at the facilities of Atlético de Madrid and Real Sociedad, matches against local academy teams and a stadium tour, with accommodation and meals included.

I saw ÍA Akranes was listed for the Costa Daurada Cup in Salou this year. Could you point me to the person who organises trips abroad for your youth teams (yngri flokkar)?

A longtime partner club of ours won its first-ever league title after training with us, and its coaches credit part of it to the experience, so I'd be glad to share how it worked for them.

Thanks a lot,
{sig}"""),
]

# -------------------------------------------------------------- plantillas
FU1 = """{greet}

Following up on my note from last week, in case it got buried.

To make it concrete: a typical week with us is 5 days in Madrid, with training sessions, matches against local academy teams, a tour of the Metropolitano stadium and museum, and full accommodation and meals, all organised by us.

If you're considering Easter or summer 2027, it's a good moment to look at dates while there is flexibility.

Would a short call work, or shall I send a one-page overview?

Best,
{sig}"""

FU1_RIGHT_PERSON = """{greet}

Following up on my note from last week, in case it got buried.

I'm trying to reach whoever organises trips and tours for the youth teams. If that's not you, a name or a forward would be very much appreciated.

In short: a 5-day week in Madrid with training sessions, matches against local academy teams, a tour of the Metropolitano stadium and museum, and full accommodation and meals, all organised by us.

Thanks a lot,
{sig}"""

FU2 = """{greet}

I'll keep this short. Most clubs aren't sure at first whether a trip like this is realistic for their families and calendar, and that's fair.

A 15-minute call is enough to tell you whether it fits, with no commitment. If it's not the right time, just let me know and I'll check back in the new year.

Best,
{sig}"""

BREAKUP = """{greet}

I haven't heard back, so I'll assume the timing isn't right and I won't keep writing.

If anything changes, or you'd like the overview for later, just reply to this email.

Wishing {short} a great season.

Best,
{sig}"""

E1_DEFAULT = None  # todos los email 1 pendientes llevan e1_body propio

LI_NOTE = ("Hi {first}, I'm Joel, founder of Always Up. We help youth clubs train in Spain with Atlético de Madrid "
           "and Real Sociedad. I emailed you recently and wanted to connect here too. Best, Joel")

DM_NOTE = ("Hi! I'm Joel from Always Up. We organise training weeks in Spain for youth clubs (Atlético de Madrid, "
           "Real Sociedad). I emailed the club recently. Who is the best person to talk to about trips for the youth teams?")

HOW_EMAIL = ("Outlook > Nuevo correo. Para / Asunto / Cuerpo tal cual (incluye la firma). Sin adjuntos. "
             "Usa 'Programar envío' para la hora indicada. A los 5 min de enviar, mira la bandeja por si hay rebote.")
HOW_FU = ("Responde DENTRO del hilo del email anterior (carpeta Enviados > abrir el correo > Responder), no un correo nuevo. "
          "Sin adjuntos. Comprueba antes en el CRM que no ha contestado por otro canal.")
HOW_LI = ("A mano en LinkedIn (no automatizar): perfil de la persona > Conectar > Añadir nota > pegar. "
          "Máx. 300 caracteres. Si no aparece 'Añadir nota', conecta sin nota y manda este texto al aceptar.")
HOW_DM = ("A mano, desde la cuenta del club en la red social indicada. Solo si NO ha contestado al email 2. Mensaje corto, sin enlaces.")


def local_to_ny(day, tzname, h=9, m=30):
    loc = dt.datetime(day.year, day.month, day.day, h, m, tzinfo=ZoneInfo(tzname))
    return loc.astimezone(NY).strftime("%H:%M")


def next_tue_thu(d):
    return d


def build_rows():
    rows = []
    for p in PROSPECTS:
        base = p["e1"]
        sigs = dict(sig=SIG, greet=p["greet"], short=p["short"])
        right = p["key"] in ("maidstone", "akranes")
        reply_subj = "Re: " + p["subj"]
        if not p["sent"]:
            rows.append(dict(date=base, club=p["club"], kind="Email 1", to=p["to"], subj=p["subj"],
                             body=p["e1_body"].format(**sigs), how=HOW_EMAIL, tz=p["tz"], note=p.get("verify", "")))
        if p["linkedin"]:
            d, who = p["linkedin"]
            first = who.split()[0]
            rows.append(dict(date=d, club=p["club"], kind="LinkedIn: conectar", to=who, subj="(nota de conexión)",
                             body=LI_NOTE.format(first=first), how=HOW_LI, tz=None, note="Joel lo hace a mano."))
        fu1 = base + dt.timedelta(days=7)
        fu2 = base + dt.timedelta(days=14)
        bu = base + dt.timedelta(days=21)
        rows.append(dict(date=fu1, club=p["club"], kind="Follow-up 1", to=p["to"], subj=reply_subj,
                         body=(FU1_RIGHT_PERSON if right else FU1).format(**sigs), how=HOW_FU, tz=p["tz"], note=""))
        rows.append(dict(date=fu2, club=p["club"], kind="Follow-up 2", to=p["to"], subj=reply_subj,
                         body=FU2.format(**sigs), how=HOW_FU, tz=p["tz"], note=""))
        if p.get("extra_dm"):
            rows.append(dict(date=fu2 + dt.timedelta(days=1), club=p["club"], kind="DM en redes (opcional)", to=p["extra_dm"],
                             subj="(mensaje directo)", body=DM_NOTE, how=HOW_DM, tz=None,
                             note="Solo si no hay respuesta al follow-up 2."))
        rows.append(dict(date=bu, club=p["club"], kind="Cierre (último)", to=p["to"], subj=reply_subj,
                         body=BREAKUP.format(**sigs), how=HOW_FU, tz=p["tz"], note="Tras esto, pasar a 'Perdido' / 'Retomar en 2027' en el CRM."))
    rows.sort(key=lambda r: (r["date"], r["club"]))
    return rows


def validate(rows):
    bad = []
    for r in rows:
        t = r["body"]
        if re.search(r"\{[^}]*\}|\[[A-Za-z ]+\]|XXX|TODO", t):
            bad.append((r["club"], r["kind"], "placeholder"))
        if re.search(r"^Hi [A-Za-zÍ]+ ?/ ?", t):
            bad.append((r["club"], r["kind"], "saludo múltiple"))
        if r["kind"] != "LinkedIn: conectar" and r["kind"] != "DM en redes (opcional)":
            if len(t.split()) > 150:
                bad.append((r["club"], r["kind"], "demasiado largo %d" % len(t.split())))
        if r["kind"] == "LinkedIn: conectar" and len(t) > 300:
            bad.append((r["club"], r["kind"], "nota >300 caracteres"))
    return bad


def write_sheet(rows):
    wb = openpyxl.load_workbook(CRM)
    if SHEET in wb.sheetnames:
        del wb[SHEET]
    ws = wb.create_sheet(SHEET, index=1)
    navy = PatternFill("solid", fgColor="0B1F3A")
    ws["A1"] = "Outreach: copiar y pegar (ordenado por fecha)"
    ws["A1"].font = Font(bold=True, size=14, color="0B1F3A")
    ws["A2"] = ("Cada fila es un envío listo. Fecha = día de envío. Hora = 09:30 locales del destinatario "
                "(la columna de Nueva York ya la convierte). Tras enviar: marca 'Hecho' y escribe la fecha real. "
                "Si el club contesta, deja de enviar el resto de sus filas y sigue el guion de respuestas en 02-sales/plan-outreach-30-dias.md.")
    ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A2:K2")
    ws.row_dimensions[2].height = 48
    heads = ["Fecha", "Día", "Hora local (09:30)", "Hora Nueva York", "Club", "Tipo", "Para", "Asunto", "Texto para pegar",
             "Cómo enviarlo", "Hecho (fecha real)"]
    for i, h in enumerate(heads, 1):
        c = ws.cell(row=4, column=i, value=h)
        c.fill = navy
        c.font = Font(bold=True, color="FFFFFF")
        c.alignment = Alignment(wrap_text=True, vertical="center")
    days = ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"]
    col = {"Email 1": "E8F1FB", "Follow-up 1": "FFF6DD", "Follow-up 2": "FDE9D9", "Cierre (último)": "EEEEEE"}
    for n, r in enumerate(rows, 5):
        ny = local_to_ny(r["date"], r["tz"]) if r["tz"] else "cuando puedas"
        vals = [r["date"], days[r["date"].weekday()], "09:30" if r["tz"] else "-", ny, r["club"], r["kind"], r["to"], r["subj"],
                r["body"], r["how"] + ((" ATENCIÓN: " + r["note"]) if r["note"] else ""), None]
        for i, v in enumerate(vals, 1):
            c = ws.cell(row=n, column=i, value=v)
            c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.cell(row=n, column=1).number_format = "DD/MM/YYYY"
        f = col.get(r["kind"])
        if f:
            for i in range(1, 12):
                ws.cell(row=n, column=i).fill = PatternFill("solid", fgColor=f)
        if r["kind"] == "Email 1" or r["kind"].startswith("Follow") or r["kind"].startswith("Cierre"):
            ws.row_dimensions[n].height = max(150, 15 * (r["body"].count("\n") + 4))
        else:
            ws.row_dimensions[n].height = 90
    for i, w in enumerate([11, 6, 10, 11, 26, 16, 30, 34, 78, 46, 14], 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A5"
    # Marcar como hechos los que ya se enviaron (email 1 de Home Farm y Hastings no están en la hoja)
    # ---------------------------------------------------------- Segmento A
    sa = wb["Segmento A - Clubes"]
    by_name = {}
    for r in range(6, 30):
        v = sa.cell(row=r, column=1).value
        if v:
            by_name[v] = r
    for p in PROSPECTS:
        r = by_name.get(p["club"])
        if not r:
            continue
        first = [x for x in rows if x["club"] == p["club"]]
        e1row = next((x for x in first if x["kind"] == "Email 1"), None)
        nxt = next((x for x in first if x["kind"] == "Follow-up 1"), None)
        sa.cell(row=r, column=7, value=p["to"])
        if p.get("person"):
            sa.cell(row=r, column=6, value=p["person"])
        if e1row:
            sa.cell(row=r, column=9, value="Listo para enviar")
            sa.cell(row=r, column=10, value="Enviar el %s a las 09:30 hora local (Outlook: programar envío). Texto en hoja '%s'." % (
                e1row["date"].strftime("%d/%m/%Y"), SHEET))
            sa.cell(row=r, column=11, value=p["subj"])
            sa.cell(row=r, column=12, value=e1row["body"])
            for cc in (13,):
                sa.cell(row=r, column=cc, value=None)
        elif nxt:
            sa.cell(row=r, column=10, value="Follow-up 1 el %s (en el mismo hilo). Textos en hoja '%s'." % (nxt["date"].strftime("%d/%m/%Y"), SHEET))
    # Notas puntuales
    r = by_name.get("Søreide IL")
    if r:
        sa.cell(row=r, column=15, value="13/10/2026: el email 1 REBOTÓ (ungdomsutvalget@soreideil.no reenvía a una cuenta inexistente en bergensskolen.com). "
                "Contactos reales (soreideil.no/fotball/kontaktinformasjon): Gunn Eklund Breisnes (Leder), Marius Engen (Sportslig leder), fotball@soreideil.no. "
                "Reenvío el 14/10 a fotball@soreideil.no.")
    r = by_name.get("Lower Ormond")
    if r:
        sa.cell(row=r, column=15, value=(sa.cell(row=r, column=15).value or "") +
                " | 13/10/2026: costadauradacup.com lo lista como club de Inglaterra en la edición de Semana Santa 2026. Existe: falta encontrar su contacto.")
    r = by_name.get("Excelsior Rotterdam")
    if r:
        sa.cell(row=r, column=15, value="13/10/2026: es un club profesional con academia (Joep Breimer, hoofd voetbalontwikkeling jeugdopleiding). "
                "Perfil distinto al club amateur viajero: prioridad baja, no incluir en la primera tanda.")
    wb.save(CRM)


def write_md(rows):
    out = os.path.join(HERE, "..", "..", "02-sales", "outreach-textos-generados.md")
    L = ["# Textos de outreach (generado)", "",
         "> Generado por `07-automations/outreach/generar_outreach.py`. NO editar a mano: cambiar el script y volver a ejecutarlo. "
         "Los mismos textos están en la hoja `%s` del CRM (más cómodo para copiar y pegar)." % SHEET, ""]
    for r in rows:
        if r["kind"] in ("Email 1",):
            L += ["## %s: %s (enviar %s)" % (r["club"], r["kind"], r["date"].strftime("%d/%m/%Y")), "",
                  "**Para:** %s" % r["to"], "", "**Asunto:** %s" % r["subj"], "", "```", r["body"], "```", ""]
    open(out, "w", encoding="utf-8").write("\n".join(L))


if __name__ == "__main__":
    rows = build_rows()
    problems = validate(rows)
    if problems:
        for p in problems:
            print("PROBLEMA:", p)
        raise SystemExit("Corrige los textos antes de generar.")
    write_sheet(rows)
    write_md(rows)
    print("OK: %d filas en '%s'" % (len(rows), SHEET))
    for r in rows[:8]:
        print(r["date"], r["club"], "|", r["kind"], "|", local_to_ny(r["date"], r["tz"]) if r["tz"] else "-")
