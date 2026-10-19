#!/usr/bin/env python3
"""Construye las pestañas de trabajo del CRM (01-clients/crm-ventas.xlsx) a partir de datos versionados en este archivo.

Uso:  python3 generar_outreach.py        (cerrar el Excel antes)
Genera / reescribe (idempotente):
  LEEME, Calendario diario, Textos para copiar, Plan por servicio, Verificación
  + actualiza 'Segmento A - Clubes' (contactos, emails, estados) y las metas de 'Hoy'.
Validaciones automáticas: sin placeholders, sin guiones largos ni palabras de "tono IA", longitud, saludo de una sola persona.
Para añadir un club: añadir una entrada a PROSPECTS y ejecutar de nuevo.
"""
import datetime as dt
from copy import copy as copy_style
import math
import os
import re
import subprocess
from zoneinfo import ZoneInfo

import openpyxl
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

HERE = os.path.dirname(os.path.abspath(__file__))
CRM = os.path.join(HERE, "..", "..", "01-clients", "crm-ventas.xlsx")
D = dt.date
NY = ZoneInfo("America/New_York")
TODAY_BUILD = D(2026, 10, 13)

NAVY = "0B1F3A"; RED = "C8102E"; GREY = "F2F2F2"; LBLUE = "E8F1FB"; LYEL = "FFF6DD"; LORG = "FDE9D9"; LGRN = "E7F4EA"
thin = Side(style="thin", color="D0D0D0")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)

SIG = ("Joel Martinez\nFounder, Always Up\n"
       "joel.martinez@alwaysup.es | +1 (814) 329 1929 | alwaysup.es")
SIG_FR = SIG

# ------------------------------------------------------------------ prospectos
PROSPECTS = [
    dict(key="homefarm", club="Home Farm FC (chicas U13-U15)", short="Home Farm FC", tz="Europe/Dublin", lang="en", sent=True,
         e1=D(2026, 10, 13), to="homefarmfc@gmail.com", greet="Hi all,", person=None,
         subj="Bringing Home Farm FC to train with Atlético de Madrid & Real Sociedad in Spain", linkedin=None,
         dm="Facebook o Instagram de Home Farm FC"),
    dict(key="hastings", club="Hastings United (Girls Academy)", short="Hastings United", tz="Europe/London", lang="en", sent=True,
         e1=D(2026, 10, 13), to="georgia.townsend@hastingsunited.com", greet="Hi Georgia,", person="Georgia Townsend (Head of Girls Academy)",
         subj="Bringing Hastings United's Girls Academy to train with LaLiga clubs in Spain",
         linkedin=(D(2026, 10, 20), "Georgia Townsend", "https://www.linkedin.com/in/georgia-townsend-5b17321a4/", "Media: figura en East Sussex College Group, que patrocina la academia. Antes de conectar, comprueba que su perfil habla de fútbol, Hastings o la academia; si no, no conectes."), dm="Instagram de Hastings United"),
    dict(key="soreide", club="Søreide IL", short="Søreide IL", tz="Europe/Oslo", lang="en", sent=False,
         e1=D(2026, 10, 14), to="fotball@soreideil.no", greet="Hi Marius and Gunn,", person="Marius Engen (sportslig leder) / Gunn Eklund Breisnes (leder)",
         subj="A week in Spain for Søreide's youth teams", linkedin=None, dm="Facebook o Instagram de Søreide IL",
         e1_body="""{greet}

I'm Joel, I run Always Up. My first email bounced from your youth committee address, so I'm writing to you directly.

We take youth teams to Spain for a week of training at Atlético de Madrid and Real Sociedad facilities, with matches against local academy sides and accommodation and meals all sorted.

I saw Søreide was down for the Costa Daurada Cup this summer, so Spain may already be on your radar. One of our partner clubs in Ireland won their first ever league title after a few years with us.

Would you be up for a quick call next week? Or I can send a short overview first if that's easier.

Best,
{sig}"""),
    dict(key="holbeach", club="Holbeach United", short="Holbeach United", tz="Europe/London", lang="en", sent=False,
         e1=D(2026, 10, 14), to="callum@holbeachunitedacademy.com", greet="Hi Callum,", person="Callum Lawe (Vice Chairman, Football & Education Academy)",
         subj="A week in Spain for Holbeach's academy squads", linkedin=None, dm="Instagram @holbeachunitedcsa", stop_after_e1=True,
         e1_body="""{greet}

I'm Joel, I run Always Up. We take youth teams to Spain for a week of training at Atlético de Madrid and Real Sociedad facilities, with matches against local academy sides, a stadium tour, and accommodation and meals all sorted.

I saw Holbeach was down for the Costa Daurada Cup this year, and your Football & Education Academy made me think a week like this could suit your older squads.

One of our partner clubs in Ireland won their first ever league title after a few years of coming out with us, and their coaches said the trip helped.

Would you be up for a quick call next week? If you'd rather see the details first, I'm happy to send a short overview.

Best,
{sig}"""),
    dict(key="holbeach_dan", club="Holbeach United (Dan Lester)", short="Holbeach United", tz="Europe/London", lang="en", sent=False,
         e1=D(2026, 10, 21), to="dan@holbeachunitedacademy.com", greet="Hi Dan,", person="Dan Lester (director y responsable de educación de la Football & Education Academy)",
         subj="A week in Spain for Holbeach's academy squads",
         linkedin=[(D(2026, 10, 22), "Dan Lester", "Pega en el buscador de LinkedIn: Dan Lester Holbeach United", "Sin enlace directo (no sale en buscadores). Comprueba que el perfil dice Holbeach United."),
                   (D(2026, 10, 22), "Callum Lawe", "Pega en el buscador de LinkedIn: Callum Lawe Masar Athletic", "Sin enlace directo. Se ha ido a Abu Dhabi a montar Masar Athletic (fútbol y educación). Comprueba que menciona Holbeach o Masar.",
                    "Hi Callum, I'm Joel, I run Always Up. I emailed you at Holbeach before realising you'd moved on to Masar Athletic, congratulations. If you ever want players to train in Spain with Atlético de Madrid or Real Sociedad facilities, I'd be glad to help. Joel")],
         dm="Instagram @holbeachunitedcsa",
         e1_body="""{greet}

I'm Joel, I run Always Up. I wrote last week to Callum Lawe, but I understand he has moved to Abu Dhabi, so I'm writing to you as the person leading the Football & Education Academy.

We take youth teams to Spain for a week of training at Atlético de Madrid and Real Sociedad facilities, with matches against local academy sides, a stadium tour, and accommodation and meals all sorted.

I saw Holbeach was down for the Costa Daurada Cup this year, and a week like this could suit your older squads. One of our partner clubs in Ireland won their first ever league title after a few years of coming out with us, and their coaches said the trip helped.

Would you be up for a quick call? If you'd rather see the details first, I'm happy to send a short overview.

Best,
{sig}"""),
    dict(key="whitehaven", club="Whitehaven AFC (Juniors Girls U13-U15)", short="Whitehaven", tz="Europe/London", lang="en", sent=False,
         e1=D(2026, 10, 15), to="Luke.johnston@whitehavenafc.com", greet="Hi Luke,", person="Luke Johnston (Chairman)",
         subj="A week in Spain for Whitehaven's girls teams", linkedin=(D(2026, 10, 20), "Luke Johnston", "https://www.linkedin.com/in/lukerobertjohnston/", "Media baja: perfil de Luke Johnston en Whitehaven. Comprueba que menciona Whitehaven AFC (presidente) antes de conectar."), dm="Facebook de Whitehaven AFC (plan B si el email rebota)",
         e1_body="""{greet}

I'm Joel, I run Always Up. We take youth teams to Spain for a week of training at Atlético de Madrid and Real Sociedad facilities, with matches against local academy sides, a stadium tour, and accommodation and meals all sorted.

I saw Whitehaven was down for the Costa Daurada Cup this summer, and that the club has girls teams from under 9 up to under 16, so I thought this could be a good fit.

Would you be up for a quick call next week, or would you like a short overview first? And if you're not the right person, could you point me to whoever organises trips for the girls section?

Best,
{sig}"""),
    dict(key="maidstone", club="Maidstone United (Girls Development Centre)", short="Maidstone United", tz="Europe/London", lang="en", sent=False,
         e1=D(2026, 10, 15), to="info@maidstoneunited.co.uk", greet="Hi team,", person=None,
         subj="A question about the Girls Development Centre", linkedin=None, dm="Facebook o Instagram de Maidstone United", right=True,
         e1_body="""{greet}

I'm Joel, I run Always Up. We take youth teams to Spain for a week of training at Atlético de Madrid and Real Sociedad facilities, with matches against local academy sides, a stadium tour, and accommodation and meals all sorted.

I saw Maidstone United was down for the Costa Daurada Cup this summer and thought your Girls Development Centre could be a great fit. Could you point me to the right person to talk to about trips for the girls teams?

One of our partner clubs in Ireland won their first ever league title after a few years with us, so I'd be glad to share how it went for them.

Thanks a lot,
{sig}"""),
    dict(key="akranes", club="IA Akranes", short="ÍA Akranes", tz="Atlantic/Reykjavik", lang="en", sent=False,
         e1=D(2026, 10, 15), to="kfia@ia.is", greet="Hi ÍA team,", person=None,
         subj="A question about youth trips to Spain", linkedin=None, dm="Facebook o Instagram de ÍA Akranes", right=True,
         e1_body="""{greet}

I'm Joel, I run Always Up. We take youth teams to Spain for a week of training at Atlético de Madrid and Real Sociedad facilities, with matches against local academy sides, a stadium tour, and accommodation and meals all sorted.

I saw ÍA Akranes was down for the Costa Daurada Cup this year. Could you point me to the person who looks after trips abroad for your youth teams?

One of our partner clubs in Ireland won their first ever league title after a few years with us, so I'd be glad to share how it went for them.

Thanks a lot,
{sig}"""),
    dict(key="virtu", club="Virtu Academy", short="Virtu Academy", tz="Europe/London", lang="en", sent=False,
         e1=D(2026, 10, 20), to="info@virtuacademy.co.uk", greet="Hi team,", person="Mohammed Ayoub (director, según directorio; sin confirmar)",
         subj="A question about trips to Spain for Virtu", linkedin=None, dm="Instagram de Virtu Academy", right=True,
         pais="Reino Unido (Reading)", cat="Academia 5 a 16 años", motivo="En la lista de la Costa Daurada Cup (edición de Semana Santa 2026)", fuente="costadauradacup.com / virtuacademy.co.uk",
         e1_body="""{greet}

I'm Joel, I run Always Up. We take youth teams to Spain for a week of training at Atlético de Madrid and Real Sociedad facilities, with matches against local academy sides, a stadium tour, and accommodation and meals all sorted.

I saw Virtu Academy was down for the Costa Daurada Cup this year. Could you point me to the person who organises trips abroad for your teams?

One of our partner clubs in Ireland won their first ever league title after a few years with us, so I'd be glad to share how it went for them.

Thanks a lot,
{sig}"""),
    dict(key="porte", club="FC Porte d'Aquitaine", short="le FC Porte d'Aquitaine", tz="Europe/Paris", lang="fr", sent=False,
         e1=D(2026, 10, 20), to="math.bachowski.mb@gmail.com", greet="Bonjour Mathieu,", person="Mathieu Bachowski (responsable technique jeunes)",
         subj="Une semaine en Espagne pour les jeunes du FC Porte d'Aquitaine", linkedin=None, dm="Facebook du FC Porte d'Aquitaine", right=False,
         pais="Francia", cat="U15 y U17", motivo="En la lista de la Costa Daurada Cup (edición de verano 2026)", fuente="costadauradacup.com / fff.fr",
         e1_body="""{greet}

Je m'appelle Joel et je dirige Always Up. Nous emmenons des équipes de jeunes en Espagne pour une semaine d'entraînement dans les installations de l'Atlético de Madrid et de la Real Sociedad, avec des matchs contre des équipes de centres de formation locaux, la visite d'un stade, l'hébergement et les repas.

J'ai vu que le FC Porte d'Aquitaine était inscrit à la Costa Daurada Cup cet été, et je me suis dit que cela pourrait intéresser vos U15 ou U17. Un de nos clubs partenaires en Irlande a remporté son premier titre de champion après quelques années avec nous.

Auriez-vous quelques minutes pour un appel la semaine prochaine ? Sinon, je peux d'abord vous envoyer une courte présentation.

Cordialement,
{sig}"""),
]

# ----------------------------------------------------------- prospectos de EEUU
# Los emails a EEUU exigen (CAN-SPAM) dirección postal del remitente y forma de darse de baja.
# Mientras ADDRESS esté vacío, estos envíos NO se generan. Rellenar con la dirección fiscal de Quality Servix Premium SL.
ADDRESS = ""
SIG_US = SIG + "\nQuality Servix Premium SL | %s\nIf you'd rather not hear from me, just reply and I won't email you again." % ADDRESS

US_E1 = """{greet}

I'm Joel, I run Always Up. We take youth teams to Spain for a week of training at Atlético de Madrid and Real Sociedad facilities, with matches against local academy sides, a stadium tour, and accommodation and meals all sorted.

I saw {short} {hook}, and thought a week in Spain could be a great fit for your older age groups. One of our partner clubs in Ireland won their first ever league title after a few years of coming out with us, and their coaches said the trip helped.

Would you be up for a quick call? If you'd rather see the details first, I'm happy to send a short overview.

Best,
{sig}"""

US_E1_RIGHT = """{greet}

I'm Joel, I run Always Up. We take youth teams to Spain for a week of training at Atlético de Madrid and Real Sociedad facilities, with matches against local academy sides, a stadium tour, and accommodation and meals all sorted.

I saw {short} {hook}, and understand {who} leads the program. Could you point me to them, or to whoever organises trips abroad for your older teams?

One of our partner clubs in Ireland won their first ever league title after a few years of coming out with us, so I'd be glad to share how it went for them.

Thanks a lot,
{sig}"""


def _us(key, club, short, tz, to, greet, person, estado, e1, right=None, hook="is part of MLS NEXT", li=None):
    d = dict(key=key, club=club, short=short, tz=tz, lang="en", sent=False, e1=e1, to=to, greet=greet, person=person,
             subj=("A week in Spain for %s's academy teams" % short) if not right else "A question about trips abroad for %s" % short,
             linkedin=None, dm="Instagram de %s" % short, us=True, estado=estado, pais="EEUU (%s)" % estado, cat="Club MLS NEXT",
             motivo="Miembro del directorio oficial de MLS NEXT; club independiente (no academia de franquicia MLS)", fuente="mlssoccer.com/mlsnext (lista de Joel) + web del club")
    if right:
        d["right"] = True
        d["e1_body"] = US_E1_RIGHT.replace("{who}", right).replace("{hook}", hook)
    else:
        d["e1_body"] = US_E1.replace("{hook}", hook)
    if li:
        d["linkedin"] = (e1 + dt.timedelta(days=2), li[0], li[1], li[2])
    return d


PROSPECTS_US = [
    _us("seacoast", "Seacoast United", "Seacoast United", "America/New_York", "iscott@seacoastunited.com", "Hi Iain,", "Iain Scott (Director of Coaching)", "New Hampshire", D(2026, 11, 3), hook="was down for the Donosti Cup in San Sebastián this summer", li=("Iain Scott", "Pega en el buscador de LinkedIn: Iain Scott Seacoast United", "Sin enlace directo. Comprueba que el perfil dice Seacoast United.")),
    _us("cedar", "Cedar Stars Academy", "Cedar Stars Academy", "America/New_York", "phil.swenda@cedarstars.com", "Hi Phil,", "Phil Swenda (Academy Director, Monmouth)", "Nueva Jersey", D(2026, 11, 3), li=("Phil Swenda", "Pega en el buscador de LinkedIn: Phil Swenda Cedar Stars Academy", "Sin enlace directo. Comprueba que dice Cedar Stars.")),
    _us("ifa", "Intercontinental Football Academy of New England", "IFA New England", "America/New_York", "mhardiman@ifanewengland.com", "Hi Matt,", "Matt Hardiman (consultas de chicos)", "Massachusetts", D(2026, 11, 3), li=("Matt Hardiman", "https://www.linkedin.com/in/matt-hardiman-3639a459/", "Alta: aparece como IFA New England (Boston).")),
    _us("ballistic", "Ballistic United", "Ballistic United", "America/Los_Angeles", "jerrylosson@busc.org", "Hi Jerry,", "Jerry Losson (MLS NEXT Director of Coaching)", "California", D(2026, 11, 4), li=("Jerry Losson", "Pega en el buscador de LinkedIn: Jerry Losson Ballistic United", "Sin enlace directo. Comprueba que dice Ballistic United.")),
    _us("delco", "FC Delco", "FC Delco", "America/New_York", "info@fcdelco.org", "Hi team,", "Jeff Zaun (Director de MLS NEXT; email personal sin confirmar)", "Pensilvania", D(2026, 11, 4), right="Jeff Zaun", li=("Jeff Zaun", "Pega en el buscador de LinkedIn: Jeff Zaun FC Delco", "Sin enlace directo. Comprueba que dice FC Delco.")),
    _us("jaguars", "Michigan Jaguars FC", "Michigan Jaguars", "America/New_York", "mo.hijazi@michiganjaguarsfc.com", "Hi Mo,", "Mo Hijazi (Director of Coaching, Dearborn; hay varias sedes)", "Míchigan", D(2026, 11, 4), li=("Mo Hijazi", "https://www.linkedin.com/in/mo-hijazi-757b3829/", "Media-alta: Dearborn, Míchigan; entrenador y director de coaching. Comprueba que menciona Michigan Jaguars.")),
    _us("loufusz", "Lou Fusz Athletic", "Lou Fusz Athletic", "America/Chicago", "matt.mueller@loufuszathletic.com", "Hi Matt,", "Matt Mueller (Director of Coaching and Competition)", "Misuri", D(2026, 11, 10), li=("Matt Mueller", "Pega en el buscador de LinkedIn: Matt Mueller Lou Fusz Athletic", "Nombre muy común: el perfil que sale en buscadores es de otra empresa. Comprueba que dice Lou Fusz Athletic.")),
    _us("slsg", "St. Louis Scott Gallagher", "St. Louis Scott Gallagher", "America/Chicago", "strittschuh@slsgsoccer.com", "Hi Steve,", "Steve Trittschuh (MLS NEXT Director)", "Misuri", D(2026, 11, 10), li=("Steve Trittschuh", "Pega en el buscador de LinkedIn: Steve Trittschuh St. Louis Scott Gallagher", "Sin enlace directo. Comprueba que dice Scott Gallagher.")),
    _us("cincyunited", "Cincinnati United Premier", "Cincinnati United", "America/New_York", "rhands@cincinnatiunitedsc.com", "Hi Reece,", "Reece Hands (Technical Director y MLS NEXT Director)", "Ohio", D(2026, 11, 10), li=("Reece Hands", "https://www.linkedin.com/in/reece-hands-39547419b/", "Alta: Boys Technical Director, Cincinnati United.")),
    _us("tbu", "Tampa Bay United", "Tampa Bay United", "America/New_York", "fgonzalez@tbusc.com", "Hi Fernando,", "Fernando Gonzalez (MLS NEXT Director)", "Florida", D(2026, 11, 11), li=("Fernando Gonzalez", "Pega en el buscador de LinkedIn: Fernando Gonzalez Tampa Bay United", "Nombre muy común: comprueba que dice Tampa Bay United.")),
    _us("bethesda", "Bethesda Soccer Club", "Bethesda SC", "America/New_York", "dbiss@bethesdasoccer.org", "Hi Derek,", "Derek Biss (Academy Director, MLS NEXT)", "Maryland", D(2026, 11, 11), li=("Derek Biss", "https://www.linkedin.com/in/derek-biss-8b518b11/", "Alta: MLSNext Academy Director, Bethesda Soccer Club.")),
    _us("walnut", "Walnut Creek Surf", "Walnut Creek Surf", "America/Los_Angeles", "mani@wcsc.org", "Hi Mani,", "Mani Salimpour (Director of Coaching)", "California", D(2026, 11, 17), hook="was down for the Donosti Cup in San Sebastián this summer", li=("Mani Salimpour", "Pega en el buscador de LinkedIn: Mani Salimpour Walnut Creek Surf", "Sin enlace directo. Comprueba que dice Walnut Creek Surf.")),
    _us("chicagofcu", "Chicago FC United", "Chicago FC United", "America/Chicago", "info@chicagofcunited.com", "Hi team,", "Jeff DeGroot (MLS NEXT Academy Director; email personal sin confirmar)", "Illinois", D(2026, 11, 17), right="Jeff DeGroot"),
    _us("sockers", "Sockers FC Chicago", "Sockers FC Chicago", "America/Chicago", "admin@sockersfcchicago.com", "Hi team,", "Oleg Vatchev (Director de Metodología MLS NEXT; email personal sin confirmar)", "Illinois", D(2026, 11, 11), right="Oleg Vatchev"),
]


# ---------------------------------------------------------------- plantillas
T = {
"en": dict(
FU1="""{greet}

Just following up on my email from last week in case it got buried.

To give you an idea, a typical week is five days in Madrid. Training sessions, matches against local academy teams, a tour of the Metropolitano and the stadium museum, and accommodation and meals all sorted by us.

If you're thinking about Easter or summer 2027, now is a good time to look at dates.

Happy to jump on a quick call, or send the details by email if that's easier.

Best,
{sig}""",
FU1_RIGHT="""{greet}

Just following up on my email from last week in case it got buried.

I'm trying to reach whoever organises trips for the youth teams. If that's not you, a name or a quick forward would be really appreciated.

In short, it's five days in Madrid with training sessions, matches against local academy teams, a tour of the Metropolitano, and accommodation and meals all sorted by us.

Thanks a lot,
{sig}""",
FU2="""{greet}

I'll keep this short. A lot of clubs aren't sure at first whether a trip like this would work for their families and their calendar, which is completely fair.

A 15 minute call is usually enough to see if it makes sense, with no commitment. And if now isn't the right time, just tell me and I'll check back in the new year.

Best,
{sig}""",
BU="""{greet}

I haven't heard back, so I'll assume the timing isn't right and I won't keep emailing.

If anything changes, or you'd like the details for later, just reply here.

Wishing {short} a great season.

Best,
{sig}""",
LI="Hi {first}, I'm Joel, I run Always Up. We take youth teams to Spain to train with Atlético de Madrid and Real Sociedad. I emailed you this week and thought I'd connect here too. Joel",
DM="Hi! I'm Joel from Always Up. We take youth teams to Spain for training weeks (Atlético de Madrid, Real Sociedad). I emailed the club recently. Who would be the best person to speak to about trips for your youth teams?"),
"fr": dict(
FU1="""{greet}

Je me permets de revenir vers vous au cas où mon message de la semaine dernière se serait perdu.

Pour vous donner une idée, une semaine type dure cinq jours à Madrid : séances d'entraînement, matchs contre des équipes de centres de formation locaux, visite du Metropolitano et de son musée, hébergement et repas pris en charge par nos soins.

Si vous pensez à Pâques ou à l'été 2027, c'est le bon moment pour regarder les dates.

Je suis disponible pour un court appel, ou je peux vous envoyer les détails par email si c'est plus simple.

Cordialement,
{sig}""",
FU1_RIGHT=None,
FU2="""{greet}

Je serai bref. Beaucoup de clubs ne savent pas au début si un voyage comme celui-ci est réaliste pour leurs familles et leur calendrier, et c'est tout à fait normal.

Un appel de 15 minutes suffit généralement pour voir si cela a du sens, sans engagement. Et si ce n'est pas le bon moment, dites-le-moi et je reviendrai vers vous en début d'année.

Cordialement,
{sig}""",
BU="""{greet}

Je n'ai pas eu de retour, je suppose donc que le moment n'est pas le bon et je ne vous écrirai plus.

Si les choses changent, ou si vous souhaitez recevoir les détails pour plus tard, répondez simplement à ce message.

Je souhaite à {short} une très belle saison.

Cordialement,
{sig}""",
LI="Bonjour {first}, je suis Joel, je dirige Always Up. Nous emmenons des équipes de jeunes en Espagne pour s'entraîner avec l'Atlético de Madrid et la Real Sociedad. Je vous ai écrit cette semaine et je me connecte aussi ici. Joel",
DM="Bonjour ! Je suis Joel d'Always Up. Nous emmenons des équipes de jeunes en Espagne pour des semaines d'entraînement (Atlético de Madrid, Real Sociedad). J'ai écrit au club récemment. Qui serait la bonne personne pour parler des déplacements des équipes de jeunes ?"),
}

HOW_EMAIL = ("En Mail: correo nuevo desde joel.martinez@alwaysup.es. Pega Para, Asunto y Texto tal cual (la firma ya va dentro). Sin adjuntos. "
             "Flecha junto a Enviar > Enviar más tarde > fecha y la hora de la columna C. Una vez programado, no lo envíes a mano.")
HOW_FU = ("Busca el correo original por destinatario (Outlook buscador > All folders, o Mail > Enviados) y pulsa Responder para que quede en el mismo hilo. Pega el texto. Sin adjuntos. "
          "Envíalo más tarde a la hora de la columna C. Antes, mira en el CRM que no haya contestado por otro canal.")
HOW_LI = ("A mano en LinkedIn: perfil de la persona > Conectar > Añadir nota > pegar el texto (máx. 300 caracteres). "
          "Si no deja añadir nota, conecta sin nota y manda el texto cuando acepte.")
HOW_DM = "A mano desde la cuenta de la red indicada. Solo si no ha contestado al follow-up 2. Sin enlaces."


def label(club):
    return re.sub(r"\s*\(.*?\)", "", club)


def local_to_ny(day, tzname, h=9, m=30):
    loc = dt.datetime(day.year, day.month, day.day, h, m, tzinfo=ZoneInfo(tzname))
    return loc.astimezone(NY).strftime("%H:%M")


def spanish_day(d):
    return ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"][d.weekday()]


def build_sends():
    rows = []
    for p in PROSPECTS + (PROSPECTS_US if ADDRESS else []):
        t = T[p["lang"]]
        sg = dict(sig=(SIG_US if p.get("us") else SIG), greet=p["greet"], short=p["short"])
        base = p["e1"]
        right = p.get("right", False)
        subj_re = "Re: " + p["subj"]
        if not p["sent"]:
            rows.append(dict(date=base, club=p["club"], kind="Email 1", to=p["to"], subj=p["subj"], body=p["e1_body"].format(**sg),
                             how=HOW_EMAIL, tz=p["tz"], key=p["key"]))
        lis = p["linkedin"]
        if lis:
            lis = lis if isinstance(lis, list) else [lis]
            for item in lis:
                d, who, how_, conf_ = item[0], item[1], item[2], item[3]
                note_ = item[4] if len(item) > 4 else t["LI"].format(first=who.split()[0])
                rows.append(dict(date=d, club=p["club"], kind="LinkedIn conectar", to=who, subj="(nota de conexión)",
                                 body=note_, how=HOW_LI, tz=None, key=p["key"], li_link=how_, li_conf=conf_))
        if p.get("stop_after_e1"):
            continue
        fu1 = (t["FU1_RIGHT"] if right and t["FU1_RIGHT"] else t["FU1"]).format(**sg)
        rows.append(dict(date=base + dt.timedelta(days=7), club=p["club"], kind="Follow-up 1", to=p["to"], subj=subj_re, body=fu1,
                         how=HOW_FU, tz=p["tz"], key=p["key"]))
        rows.append(dict(date=base + dt.timedelta(days=14), club=p["club"], kind="Follow-up 2", to=p["to"], subj=subj_re,
                         body=t["FU2"].format(**sg), how=HOW_FU, tz=p["tz"], key=p["key"]))
        rows.append(dict(date=base + dt.timedelta(days=15), club=p["club"], kind="DM en redes", to=p["dm"], subj="(mensaje directo)",
                         body=t["DM"], how=HOW_DM, tz=None, key=p["key"], optional=True))
        rows.append(dict(date=base + dt.timedelta(days=21), club=p["club"], kind="Cierre", to=p["to"], subj=subj_re,
                         body=t["BU"].format(**sg), how=HOW_FU, tz=p["tz"], key=p["key"]))
    rows.sort(key=lambda r: (r["date"], r["club"]))
    return rows


# ------------------------------------------------------- plantillas de respuesta
REPLIES = [
    ("Responde: quiere hablar", "Great, thanks for getting back to me. Would {A} or {B} work for a call? Those are your local times. If neither suits, tell me what does and I'll adapt. I'll send an invite as soon as we pick one.\n\nBest,\n" + SIG,
     "Menos de 4 horas. Sustituye {A} y {B} por dos horarios de la tabla de LEEME convertidos a su hora. Si prefiere elegir él: ofrece el enlace de Calendly."),
    ("Responde: pide información", "Of course. I've attached our company overview and the programme sheet for Team Experience. If it's easier to talk it through, I'm happy to jump on a quick call as well, just tell me what time suits you.\n\nBest,\n" + SIG,
     "Adjunta Always-Up-Company-Deck.pdf y Always-Up-Team-Experience.pdf (02-sales/assets). Menos de 4 horas."),
    ("Responde: pregunta el precio", "It depends on the dates and the size of the group. As a reference, the five day programme starts at around $1,500 per player. A 15 minute call would let me give you an exact figure for your squad.\n\nBest,\n" + SIG,
     "Decisión tuya: dar la referencia (recomendado) o dejar el precio para la llamada."),
    ("Responde: ahora no", "No problem at all, and thanks for letting me know. Would it be okay if I check back in January, when most clubs start planning Easter and summer 2027?\n\nBest,\n" + SIG,
     "Apunta en el CRM: Retomar enero 2027, con fecha."),
    ("Responde: no soy la persona", "Thanks, that's really helpful. Could you share their name and email? I'll mention that you pointed me their way.\n\nBest,\n" + SIG,
     "Luego escribe al nombre que te den (usa un email 1 con su nombre) y menciona a quien te derivó."),
    ("Daniel (MLS NEXT): follow-up por Instagram", "Hola Daniel, ¿qué tal? Hace unas semanas hablamos de tu duda entre 1º y 2º de Bachillerato y de cómo encajaría con el proceso universitario en EEUU. Te escribo solo para saber si sigues con ganas de explorarlo.\n\nSi es así, mándame tu posición y, si tienes, un vídeo o enlace de algún partido de la MLS NEXT, y te cuento con calma qué opciones reales habría en tu caso. Cuanto antes lo veamos, más margen hay para decidir bien lo del curso.\n\nY si ahora no es el momento, no pasa nada, dímelo y lo dejamos aquí.",
     "Instagram. Un solo follow-up. Si no contesta en 7 días, pasa a Frío en el CRM. No pidas más datos en este mensaje."),
    ("Club irlandés: permiso para su testimonio y presentaciones (WhatsApp)", "Hi [nombre], hope you and the squad are doing well, and congratulations again on the league title.\n\nI have two small favours to ask, only if you're comfortable with them. First, would you be happy for us to quote what your coach said about the Atlético trip helping the team? Even better, if one of the coaches could send two or three lines, or a 30 second video message, in their own words. Second, if you know other clubs who might enjoy a trip like yours, an introduction from you would help us a lot.\n\nThanks so much either way, and I hope we see you in Spain again soon.\n\nJoel",
     "WhatsApp. Lo manda quien tenga la relación con el club (Joel o Enrique). Cambia [nombre] por el nombre del contacto. Si acepta, guarda su respuesta en 08-knowledge-base y pásamela para usarla en el deck, la web y los emails."),
]

BANNED = [r"—", r"–", r" - ", r"\bdelve\b", r"\bleverage\b", r"\bseamless", r"\btailored\b", r"\bjourney\b", r"\bunlock\b", r"I hope this email finds you",
          r"\bsynerg", r"\bcutting-edge\b", r"\bworld-class\b", r"\belevate\b", r"\bgame-changer\b"]


def validate(rows):
    bad = []
    for r in rows:
        if r["kind"] in ("LinkedIn conectar", "DM en redes", "Plantilla"):
            texts = [r["body"]]
        else:
            texts = [r["body"], r["subj"]]
        for tx in texts:
            for pat in BANNED:
                if re.search(pat, tx, flags=re.I):
                    bad.append((r["club"], r["kind"], "patrón no permitido: %s" % pat))
            if r["kind"] != "Plantilla" and re.search(r"\{[^}]*\}|\[[A-Za-z ]+\]", tx):
                bad.append((r["club"], r["kind"], "placeholder sin rellenar"))
        if re.search(r"^(Hi|Hello) [^\n,]+ ?(/|&) ", r["body"], flags=re.M):
            bad.append((r["club"], r["kind"], "saludo múltiple"))
        if r["kind"] == "Email 1" and len(r["body"].split()) > 170:
            bad.append((r["club"], r["kind"], "email 1 demasiado largo: %d palabras" % len(r["body"].split())))
        if r["kind"] == "LinkedIn conectar" and len(r["body"]) > 300:
            bad.append((r["club"], r["kind"], "nota de LinkedIn >300 caracteres"))
        if r["kind"] != "Plantilla" and r["kind"] not in ("LinkedIn conectar", "DM en redes") and "Joel Martinez\nFounder" not in r["body"]:
            bad.append((r["club"], r["kind"], "falta la firma"))
    return bad


# ---------------------------------------------------------------- calendario
def build_calendar(sends):
    """Devuelve lista de dicts: date, time (HH:MM NY o texto), sortkey, svc, task, how, where, mins."""
    C = []

    def add(d, t, sk, svc, task, how, where="", mins=10):
        C.append(dict(date=d, time=t, sk=sk, svc=svc, task=task, how=how, where=where, mins=mins))

    start, end = D(2026, 10, 13), D(2026, 11, 27)
    d = start
    while d <= end:
        wd = d.weekday()
        if wd < 5:
            add(d, "8:00", 480, "Todos", "Revisión diaria: bandeja, Instagram, WhatsApp",
                "1) Outlook: mira Recibidos y busca rebotes (correos del sistema que dicen 'Undeliverable' o 'permanent fatal errors'). 2) Instagram y WhatsApp: responde a todo lo que haya entrado, máximo 12 h de espera. 3) Si un club ha contestado: para su cadencia y usa 'Respuestas tipo' en la hoja Textos para copiar.",
                "Textos para copiar (final de la hoja)", 15)
        d += dt.timedelta(days=1)

    # --- envíos por fecha: se programan la víspera en Apple Mail; se confirman a las 08:00
    by_date = {}
    for s in sends:
        if s["tz"] and s["date"] >= TODAY_BUILD:
            by_date.setdefault(s["date"], []).append(s)
    for dd, items in sorted(by_date.items()):
        if dd > end:
            continue
        lines = ["• %s | %s | programar para las %s hora Nueva York (09:30 allí)" % (label(x["club"]), x["kind"], local_to_ny(x["date"], x["tz"])) for x in items]
        prev = max(dd - dt.timedelta(days=1), D(2026, 10, 14))
        if dd > D(2026, 10, 14):
            add(prev, "Tarde", 1200, "Team/Coach", "Programar en Apple Mail los envíos del %s %s" % (spanish_day(dd), dd.strftime("%d/%m")),
                "Para cada correo: copia Para, Asunto y Texto de la hoja 'Textos para copiar' (filtra por la fecha %s). Revisa en 30 segundos: saludo, nombre del club, firma, sin adjuntos. En Mail: flecha junto a Enviar > Enviar más tarde > fecha y hora indicadas.\n%s\nRegla: una vez programado, NO lo envíes a mano (se duplicaría). Si a las 08:00 no aparece enviado, entonces sí." % (dd.strftime("%d/%m"), "\n".join(lines)),
                "Textos para copiar", 15 + 5 * len(items))
        add(dd, "8:00", 481, "Team/Coach", "Confirmar que salieron los correos de hoy y mirar rebotes",
            "Para cada correo: en Outlook, buscador > escribe el destinatario > 'All folders' (el correo puede estar en 'INBOX.Sent' o 'Sent Messages', no solo en 'Sent'); o en Mail, mira el buzón Enviados. Si aparece: marca Hecho en 'Textos para copiar'. Si NO aparece: envíalo ya a mano. Después mira Recibidos por si hay rebote ('Undeliverable' o 'permanent fatal errors'); si lo hay, anótalo y avísame.",
            "Outlook buscador / Mail Enviados", 10)
    for s in sends:
        if s["date"] < TODAY_BUILD or s["date"] > end:
            continue
        if s["kind"] == "LinkedIn conectar":
            add(s["date"], "Libre", 700, "Team/Coach", "LinkedIn: conectar con %s (%s)" % (s["to"], label(s["club"])),
                "Perfil: %s  |  Fiabilidad: %s  |  %s  Texto de la nota: «%s»" % (s["li_link"], s["li_conf"], s["how"], s["body"]), "LinkedIn - Conexiones", 5)
        if s["kind"] == "DM en redes":
            add(s["date"], "Libre", 710, "Team/Coach", "Opcional: DM a %s (%s)" % (s["to"], label(s["club"])),
                "Solo si el club no ha respondido a nada. " + s["how"] + " Texto: «%s»" % s["body"], "Textos para copiar", 5)
        if s["kind"] in ("Email 1", "Follow-up 1", "Follow-up 2", "Cierre"):
            who = label(s["club"])
            loc = dt.datetime(s["date"].year, s["date"].month, s["date"].day, 7, 30, tzinfo=NY).astimezone(ZoneInfo(s["tz"])).strftime("%H:%M")
            nyt = local_to_ny(s["date"], s["tz"])
            add(s["date"], nyt, int(nyt[:2]) * 60 + int(nyt[3:]), "Team/Coach", "ENVIAR %s a %s" % (s["kind"].lower(), who),
                "Sale a las %s hora Nueva York (09:30 allí) si lo programaste la víspera. No hace falta hacer nada a esta hora. Si es follow-up, se envía respondiendo al correo original (búscalo por destinatario en Outlook o Mail y pulsa Responder)." % nyt,
                "Textos para copiar", 0)

    # --- tareas puntuales
    A = add
    A(D(2026, 10, 13), "Tarde", 1000, "Becas", "Omar: anotado el follow-up enviado hoy", "Nada que hacer. Si responde, pásame su mensaje. Si no, el 20/10 envías el último mensaje (ver ese día).", "Segmento C - Becas, fila Omar", 0)
    A(D(2026, 10, 13), "21:00", 1260, "Transversal", "Prueba de entregabilidad (por qué tus correos caen en spam)",
      "1) Desde joel.martinez@alwaysup.es manda a tu Gmail personal un correo con texto normal (pega el de Holbeach) y asunto normal. 2) Ábrelo en Gmail > tres puntos > Mostrar original: copia lo que ponga en SPF, DKIM y DMARC (deben decir PASS). 3) Entra en mail-tester.com, copia la dirección que te da, mándale desde alwaysup.es el mismo texto y pulsa 'Then check your score'. Pásame la nota y el resultado de SPF, DKIM y DMARC. No pegues nada más.", "Chat con Claude", 15)
    A(D(2026, 10, 14), "Libre", 650, "Transversal", "Opcional: pruebas de envío programado en Apple Mail (máx. 15 min)", "Programa un correo a ti mismo a 10 minutos con (1) Mail abierto y el Mac despierto, (2) Mail cerrado, (3) Mac en reposo. Anota cuál sale. Si ninguno funciona con el Mac apagado, no se programa: se envía a mano a las 07:30.", "Mail de Apple", 15)
    A(D(2026, 10, 14), "Libre", 640, "Team/Coach", "Comprobar si Søreide y Holbeach recibieron el correo una o dos veces", "En Outlook: buscador > 'fotball@soreideil.no' y luego 'callum@holbeachunitedacademy.com' > All folders. Cuenta cuántas copias hay y a qué hora salió cada una. Dime el resultado: si hay duplicado, no escribas nada al club (disculparse llama más la atención); solo se responde con naturalidad si ellos lo mencionan.", "Outlook buscador", 5)
    A(D(2026, 10, 14), "Libre", 655, "Transversal", "Prueba de spam con Microsoft (antes del lote del jueves)",
      "Tres de los cinco clubes del jueves y Hastings usan correo Microsoft 365, que es el filtro más estricto con dominios nuevos. Manda el correo de Whitehaven (texto normal) a una cuenta Outlook o Hotmail (la tuya, de un amigo o una gratuita que crees tú) y mira si cae en Recibidos o en Correo no deseado. Cuéntame el resultado. Si cae en spam, lo marcas 'No es spam' y repetimos mañana.", "Chat con Claude", 10)
    A(D(2026, 10, 15), "Libre", 655, "Transversal", "Calentar el dominio: 2 o 3 correos reales más a gente de confianza (ya hiciste 3)",
      "Escribe desde alwaysup.es a 2 o 3 personas más (familia, amigos, conocidos con Gmail, Outlook o iCloud) un correo normal con una pregunta, y pídeles que respondan. Si caen en spam, que lo marquen como 'No es spam'. Es la forma más rápida de mejorar la reputación de un dominio nuevo.", "", 15)
    A(D(2026, 10, 14), "12:00", 720, "Becas", "Daniel (MLS NEXT): enviar el follow-up por Instagram", "No contestó a tu mensaje del 21/09. Mi consejo: un único follow-up corto con salida fácil, y si no responde en 7 días, pasarlo a 'Frío'. Texto en 'Respuestas tipo' (Daniel). Mejor entre las 12:00 y las 14:00 de Nueva York (18:00 a 20:00 en España, cuando está libre de clase). Después apunta en el CRM la fecha de envío.", "Textos para copiar (Respuestas tipo)", 5)
    A(D(2026, 10, 15), "Libre", 640, "Becas", "Darme tu feedback sobre la ficha de Becas EEUU", "Ábrela (02-sales/assets/Always-Up-Becas-EEUU.pdf) y dime qué cambiarías. Antes de cambiar nada te digo si me parece buena idea.", "02-sales/assets", 15)
    A(D(2026, 11, 2), "Libre", 645, "Team/Coach", "Greystones: preguntar a Enrique si ya pidió el testimonio y las presentaciones", "Decidido el 19/10 con Enrique: se hace sí o sí. Nuestro contacto está de baja por paternidad, así que Enrique le escribirá en unas dos semanas. Esta semana no hay nada que hacer. Hoy solo preguntas a Enrique cómo va; si ya contestó, pásame lo que haya dicho. El texto base está en 'Textos para copiar' (Respuestas tipo).", "Textos para copiar (Respuestas tipo)", 5)
    A(D(2026, 10, 16), "Libre", 640, "Todos", "Revisión semanal 1: qué ha pasado esta semana", "Mira la hoja Hoy y anota respuestas, rebotes y llamadas. Pásame un resumen de tres líneas: yo ajusto el plan.", "Hoy", 20)
    rr = [(D(2026, 10, 21), 45, "Definir la estrategia y los pilares de contenido con la sesión de agentes y decidir qué se publica primero. Objetivo: plan v1 listo el 24/10."),
          (D(2026, 10, 24), 60, "Cerrar el plan v1 y montar el calendario de contenido de las 2 primeras semanas (con los vídeos de 'Joel Content/03_Final')."),
          (D(2026, 10, 28), 30, "Preparar o programar las 2 publicaciones de la semana."),
          (D(2026, 10, 31), 60, "Grabar o editar el contenido nuevo de la semana siguiente."),
          (D(2026, 11, 4), 30, "Preparar o programar las publicaciones de la semana."),
          (D(2026, 11, 7), 60, "Grabar o editar contenido y revisar métricas de las 2 primeras semanas (qué funciona)."),
          (D(2026, 11, 11), 30, "Preparar o programar las publicaciones y ajustar el plan según métricas."),
          (D(2026, 11, 14), 60, "Grabar o editar el contenido de la semana siguiente."), (D(2026, 11, 18), 30, "Preparar o programar las publicaciones."),
          (D(2026, 11, 21), 60, "Grabar o editar contenido y revisar métricas."), (D(2026, 11, 25), 30, "Preparar o programar las publicaciones.")]
    for dd, mins, txt in rr:
        A(dd, "Libre", 600, "Instagram", "Bloque de redes sociales (%d min)" % mins, txt + " La meta sigue siendo 10.000 seguidores a fin de año; partimos de 2.150. Mide cada semana seguidores nuevos y mensajes de familias o clubes.", "Chat con Claude / sesión de agentes", mins)
    for dd in (D(2026, 10, 19), D(2026, 10, 26), D(2026, 11, 2), D(2026, 11, 9), D(2026, 11, 16), D(2026, 11, 23)):
        A(dd, "Libre", 500, "Team/Coach", "Pedirme: «investiga 10 clubes más» (Europa, EEUU o los dos) para la siguiente tanda", "Escríbeme esa frase. Yo verifico decisor y email en la web del club y te dejo los correos listos en esta hoja antes del jueves.", "Chat con Claude", 5)
        A(dd, "Libre", 520, "Becas", "Revisar leads de becas con acción vencida", "Pestaña Segmento C - Becas: ordena por 'Próxima acción'. Contesta o actualiza todo lo atrasado. Aplica las 4 preguntas de cualificación.", "Segmento C - Becas", 20)
    A(D(2026, 10, 19), "Libre", 800, "Team/Coach", "LinkedIn: 10 minutos de actividad", "Acepta conexiones, comenta tres publicaciones de entrenadores o clubes con algo de valor (no publicidad). Eso hace que te vean antes de que llegue el email.", "", 10)
    A(D(2026, 10, 20), "Libre", 650, "Becas", "Omar: último mensaje corto si sigue sin contestar", "«Hola Omar, no quiero atosigarte. Si en este momento no es prioridad, no pasa nada, lo dejamos aquí y lo retomamos cuando te venga bien. Si quieres seguir, mándame lo que tengas del vídeo y empezamos.» Después pásalo a 'Frío' en el CRM.", "Segmento C - Becas", 5)
    A(D(2026, 10, 22), "Libre", 640, "Team/Coach", "Preguntar a Atlético y Real Sociedad por las fechas reales de Semana Santa y verano 2027", "Necesitamos saber qué semanas hay disponibles y hasta cuándo se pueden reservar. Con eso tendremos urgencia real y honesta para los follow-ups (hoy no la tenemos). Puede hacerlo Enrique.", "", 20)
    A(D(2026, 10, 23), "Libre", 640, "Todos", "Sesión con Enrique: Team Experience, International Program y opciones de Bélgica", "Ya decidido el 16/10: Campus Internacional (firma Always Up con el Atlético, precio fijo, sin adelantar dinero, seguros del Atlético). Pendiente de hablar: (1) Team Experience: anticipo para reservar fechas (sugiero 20 a 30 %) y condiciones de cancelación por escrito, más contrato y seguros con menores; (2) International Program: precio por jugador y nuestra comisión; (3) Bélgica: qué opciones ha propuesto el contacto y si pedimos a la Real Sociedad una propuesta más flexible; (4) si se confirmó la tecnificación en Zubieta del 22 al 28 de noviembre. Detalle en 00-company/decisiones-pendientes-enrique.md.", "plan-outreach-30-dias.md sección 7", 45)
    A(D(2026, 10, 23), "Libre", 650, "International Program", "Cerrar el precio y la comisión del International Program con Enrique", "Es lo único que falta para poder preparar una ficha y hablar con SADE: precio por jugador y qué cobra Always Up. Ya sabemos: mínimo 9 o 10 jugadores, se reserva antes de la temporada y Always Up cobra y luego paga a la Real Sociedad.", "", 10)
    A(D(2026, 10, 24), "Libre", 600, "GEE / Fichas", "Revisar las nuevas fichas (GEE, Campus Internacional, International Program)", "Las preparo yo tras tu feedback de la ficha de Becas. Tú revisas y me dices qué cambiar.", "02-sales/assets", 30)
    A(D(2026, 10, 26), "Libre", 640, "Campus Internacional", "Campus Internacional: contarme las opciones que proponga el contacto de Bélgica", "Cuando las tengas, dímelas y vemos si salen las cuentas. No hacemos outreach frío ni ficha de este servicio hasta entonces.", "Oportunidades y notas", 15)
    A(D(2026, 10, 27), "Libre", 640, "Team/Coach", "Enviar la tanda 3 de emails (los textos los tengo listos tras tu petición del 19/10)", "Aparecerán en la hoja Textos para copiar con su hora de programación.", "Textos para copiar", 20)
    A(D(2026, 10, 28), "Libre", 640, "Becas", "Piloto: 5 mensajes a entrenadores de club o instituto que tengan jugadores de 15 a 18 años", "Yo investigo la lista y los textos (se entregan el 26/10). La idea: un entrenador que recomienda la ficha de Becas trae varias familias a la vez. Los textos nunca nombran al partner ni prometen becas.", "Textos para copiar", 25)
    A(D(2026, 11, 3), "Libre", 640, "Team/Coach", "Enviar la tanda 4 de emails", "Mismo proceso. Los textos estarán en la hoja tras tu petición del 26/10.", "Textos para copiar", 20)
    A(D(2026, 11, 6), "Libre", 640, "Todos", "Revisión semanal 4: qué asunto y qué mensaje funcionan mejor", "Con ya 20 o 30 emails enviados se puede empezar a comparar. Pásame respuestas por email para ajustar.", "Hoy", 20)
    A(D(2026, 11, 9), "Libre", 640, "Todos", "Revisión del mes con Claude (45 min)", "Resultados, qué cambiamos, qué dejamos y plan del segundo mes. Comprobamos si llegamos a la primera venta real. Valoramos también la automatización del envío (objetivo de Joel: cientos de correos a la semana): Google Workspace, herramienta de envíos con calentamiento y qué se puede delegar.", "Chat con Claude", 45)
    for dd in (D(2026, 10, 16), D(2026, 10, 23), D(2026, 10, 30), D(2026, 11, 6), D(2026, 11, 13), D(2026, 11, 20), D(2026, 11, 27)):
        A(dd, "Libre", 990, "Todos", "Actualizar el CRM con lo que ha pasado esta semana", "Estado y fecha de último contacto de cada club o lead. Así la hoja Hoy cuenta bien.", "Segmento A, B, C", 15)
    C.sort(key=lambda x: (x["date"], x["sk"]))
    return C


# ----------------------------------------------------------------- utilidades
def est_height(text, width, minh=18, line=14.5):
    if text is None:
        return minh
    lines = 0
    for ln in str(text).split("\n"):
        lines += max(1, math.ceil(len(ln) / max(width * 1.05, 1)))
    return max(minh, lines * line + 4)


def head(ws, row, labels, widths=None):
    for i, h in enumerate(labels, 1):
        c = ws.cell(row=row, column=i, value=h)
        c.fill = PatternFill("solid", fgColor=NAVY)
        c.font = Font(bold=True, color="FFFFFF", size=10)
        c.alignment = Alignment(wrap_text=True, vertical="center")
        c.border = BORDER
    if widths:
        for i, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[row].height = 30


def title(ws, text, sub=None, span=10):
    ws["A1"] = text
    ws["A1"].font = Font(bold=True, size=15, color=NAVY)
    ws.row_dimensions[1].height = 26
    if sub:
        ws["A2"] = sub
        ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
        ws["A2"].font = Font(size=10, color="444444")
        ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=span)
        ws.row_dimensions[2].height = 46


def fresh(wb, name, idx=None):
    if name in wb.sheetnames:
        del wb[name]
    return wb.create_sheet(name, idx) if idx is not None else wb.create_sheet(name)


def dig_mx(domain):
    try:
        out = subprocess.run(["dig", "+short", "MX", domain], capture_output=True, text=True, timeout=8).stdout.strip()
        return "Sí" if out else "No responde (revisar)"
    except Exception:
        return "No comprobado"


# ------------------------------------------------------------------- hojas
def read_saved(wb, sheet, key_cols, val_cols, header_row=4):
    """Lee lo que Joel ha rellenado a mano para conservarlo al regenerar."""
    saved = {}
    if sheet not in wb.sheetnames:
        return saved
    ws = wb[sheet]
    for r in range(header_row + 1, ws.max_row + 1):
        key = tuple(str(ws.cell(row=r, column=c).value) for c in key_cols)
        vals = tuple(ws.cell(row=r, column=c).value for c in val_cols)
        if any(v not in (None, "", "Pendiente", "Automático") for v in vals):
            saved[key] = vals
    return saved


def sheet_calendar(wb, cal):
    saved = read_saved(wb, "Calendario diario", (1, 5), (9, 10))
    ws = fresh(wb, "Calendario diario", 0)
    title(ws, "Calendario diario: 13 de octubre a 13 de noviembre de 2026",
          "Qué haces tú cada día, a qué hora y cómo. Las horas son de Nueva York. Los correos se programan la víspera en Apple Mail (Enviar más tarde) para las 09:30 de cada club; a las 08:00 compruebas que salieron. "
          "Cambia la columna Estado a Hecho al terminar. Hoy se marca en amarillo. Si algo queda Pendiente de un día anterior, sale en rojo.", span=9)
    head(ws, 4, ["Fecha", "Día", "Hora (NY)", "Servicio", "Tarea", "Cómo se hace, paso a paso", "Dónde está el texto", "Min", "Estado"],
         [11, 11, 9, 16, 40, 78, 24, 6, 12])
    ws.cell(row=4, column=10, value="Notas / resultado")
    c = ws.cell(row=4, column=10)
    c.fill = PatternFill("solid", fgColor=NAVY); c.font = Font(bold=True, color="FFFFFF"); c.border = BORDER
    ws.column_dimensions["J"].width = 36
    svc_col = {"Team/Coach": LBLUE, "Becas": LGRN, "Instagram": "F3E8FF", "Brasil/Campus": LYEL, "Campus Internacional": LYEL,
               "International Program": LYEL, "GEE / Fichas": LYEL, "Todos": GREY, "Transversal": GREY}
    r = 5
    last_week = None
    dv = DataValidation(type="list", formula1='"Pendiente,Hecho,Saltado"', allow_blank=True)
    ws.add_data_validation(dv)
    first = r
    for t in cal:
        wk = t["date"].isocalendar()[1]
        if wk != last_week:
            monday = t["date"] - dt.timedelta(days=t["date"].weekday())
            sunday = monday + dt.timedelta(days=6)
            ws.cell(row=r, column=1, value="SEMANA  %s a %s" % (monday.strftime("%d/%m"), sunday.strftime("%d/%m")))
            ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=10)
            ws.cell(row=r, column=1).fill = PatternFill("solid", fgColor=RED)
            ws.cell(row=r, column=1).font = Font(bold=True, color="FFFFFF", size=11)
            ws.row_dimensions[r].height = 22
            r += 1
            last_week = wk
        vals = [t["date"], spanish_day(t["date"]).capitalize(), t["time"], t["svc"], t["task"], t["how"], t["where"], t["mins"] or None, "Pendiente", None]
        informative = False
        for i, v in enumerate(vals, 1):
            cell = ws.cell(row=r, column=i, value=v)
            cell.alignment = Alignment(wrap_text=True, vertical="top")
            cell.border = BORDER
            cell.font = Font(size=10, italic=informative, color=("777777" if informative else "000000"))
            if i == 4:
                cell.fill = PatternFill("solid", fgColor=svc_col.get(t["svc"], GREY))
            if i == 5 and not informative:
                cell.font = Font(size=10, bold=True)
        ws.cell(row=r, column=1).number_format = "DD/MM/YYYY"
        ws.cell(row=r, column=3).alignment = Alignment(horizontal="center", vertical="top")
        key = (str(t["date"]) + " 00:00:00", t["task"])
        if key in saved:
            ws.cell(row=r, column=9, value=saved[key][0] or "Pendiente")
            ws.cell(row=r, column=10, value=saved[key][1])
        if informative:
            ws.cell(row=r, column=9, value="Automático")
        else:
            dv.add(ws.cell(row=r, column=9))
        ws.row_dimensions[r].height = min(max(est_height(t["how"], 78), est_height(t["task"], 40), 30), 330)
        r += 1
    last = r - 1
    rng = "A%d:J%d" % (first, last)
    ws.conditional_formatting.add(rng, FormulaRule(formula=["$I%d=\"Hecho\"" % first], font=Font(color="999999", strike=True), stopIfTrue=True))
    ws.conditional_formatting.add(rng, FormulaRule(formula=["$A%d=TODAY()" % first], fill=PatternFill("solid", bgColor="FFF2CC", fgColor="FFF2CC")))
    ws.conditional_formatting.add("I%d:I%d" % (first, last), FormulaRule(formula=["AND(ISNUMBER($A%d),$A%d<TODAY(),$I%d=\"Pendiente\")" % (first, first, first)],
                                  font=Font(color="C00000", bold=True)))
    ws.freeze_panes = "A5"
    ws.auto_filter.ref = "A4:J%d" % last
    ws.sheet_properties.tabColor = RED


def sheet_texts(wb, sends):
    saved = read_saved(wb, "Textos para copiar", (1, 4, 5), (10,))
    ws = fresh(wb, "Textos para copiar", 1)
    title(ws, "Textos para copiar y pegar",
          "Una fila por envío, ordenada por fecha. Filtra la columna Fecha para ver solo el día que toca. Copia Para, Asunto y Texto sin cambiar nada: la firma ya va incluida. "
          "Hora = a qué hora de Nueva York programar el envío (son las 09:30 en el país del club). Los textos están revisados por Claude: sin guiones largos, sin placeholders, saludo a una sola persona.", span=11)
    head(ws, 4, ["Fecha", "Día", "Programar para (NY)", "Club", "Tipo", "Para", "Asunto", "Texto para pegar", "Cómo enviarlo", "Hecho (fecha real)", "Qué hacer si..."],
         [11, 9, 14, 26, 15, 30, 34, 78, 44, 14, 36])
    col = {"Email 1": LBLUE, "Follow-up 1": LYEL, "Follow-up 2": LORG, "Cierre": "EEEEEE", "LinkedIn conectar": "F3E8FF", "DM en redes": "F3E8FF"}
    ifs = {"Email 1": "Rebota: avísame y busco otra dirección. Contesta: para la cadencia y mira 'Respuestas tipo' abajo.",
           "Follow-up 1": "Si ya contestó por otro canal, no lo envíes.", "Follow-up 2": "Si contestó, no lo envíes.",
           "Cierre": "Tras este correo, pasa el club a 'Retomar en enero 2027' en el CRM.",
           "LinkedIn conectar": "Si acepta, no mandes más mensajes hasta que conteste al email.", "DM en redes": "Solo si no hay respuesta a nada."}
    r = 5
    for s in sends:
        if s["date"] < TODAY_BUILD:
            continue
        ny = ("%s (09:30 allí)" % local_to_ny(s["date"], s["tz"])) if s["tz"] else "Libre"
        vals = [s["date"], spanish_day(s["date"]).capitalize(), ny, s["club"], s["kind"], s["to"], s["subj"], s["body"], s["how"], None, ifs.get(s["kind"], "")]
        for i, v in enumerate(vals, 1):
            c = ws.cell(row=r, column=i, value=v)
            c.alignment = Alignment(wrap_text=True, vertical="top")
            c.border = BORDER
            c.font = Font(size=10)
            c.fill = PatternFill("solid", fgColor=col.get(s["kind"], GREY))
        k = (str(s["date"]) + " 00:00:00", s["club"], s["kind"])
        if k in saved:
            ws.cell(row=r, column=10, value=saved[k][0])
        ws.cell(row=r, column=1).number_format = "DD/MM/YYYY"
        ws.cell(row=r, column=3).alignment = Alignment(horizontal="center", vertical="top")
        ws.row_dimensions[r].height = min(max(est_height(s["body"], 78), est_height(s["how"], 44), 60), 330)
        r += 1
    last = r - 1
    r += 2
    ws.cell(row=r, column=1, value="RESPUESTAS TIPO Y OTROS TEXTOS (para cuando contestan o para casos concretos)")
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=11)
    ws.cell(row=r, column=1).fill = PatternFill("solid", fgColor=RED)
    ws.cell(row=r, column=1).font = Font(bold=True, color="FFFFFF", size=11)
    r += 1
    for name, body, note in REPLIES:
        ws.cell(row=r, column=4, value=name)
        ws.cell(row=r, column=8, value=body)
        ws.cell(row=r, column=9, value=note)
        for i in (4, 8, 9):
            ws.cell(row=r, column=i).alignment = Alignment(wrap_text=True, vertical="top")
            ws.cell(row=r, column=i).border = BORDER
            ws.cell(row=r, column=i).font = Font(size=10, bold=(i == 4))
        ws.row_dimensions[r].height = min(max(est_height(body, 78), est_height(note, 44), 40), 300)
        r += 1
    ws.freeze_panes = "A5"
    ws.auto_filter.ref = "A4:K%d" % last
    ws.sheet_properties.tabColor = NAVY


def sheet_services(wb):
    ws = fresh(wb, "Plan por servicio", 3)
    title(ws, "Plan de captación por servicio",
          "Un único plan para conseguir clientes en todos los servicios, con prioridades. Con 10 a 20 horas semanales no se pueden empujar siete líneas a la vez: "
          "se trabajan a fondo las dos primeras, se cuida el resto con contactos cálidos y se documenta lo demás. Detalle completo en 02-sales/plan-captacion-todos-los-servicios.md.", span=9)
    head(ws, 4, ["Servicio", "Prioridad", "Quién compra", "Dónde lo encontramos (por orden de rendimiento)", "Qué decimos en el primer mensaje",
                 "Qué se hace cada semana", "Objetivo a 30 días", "Material", "Límites y riesgos"],
         [24, 11, 28, 46, 40, 44, 30, 26, 40])
    rows = [
        ("Team Experience", "1 (principal)", "Club o comité de equipos de 12 a 18 años, preferiblemente de los que ya viajan",
         "1) Email con nombre y apellido (Claude investiga).\n2) Referidos del club irlandés.\n3) LinkedIn al decisor.\n4) DM de Instagram o Facebook del club.\n5) Listas de participantes de torneos en España.",
         "Una semana de entrenamiento en las instalaciones de Atlético y Real Sociedad. Pregunta de dos opciones: llamada corta o resumen.",
         "Tanda nueva de 5 a 8 clubes. Follow-ups según calendario. 5 conexiones de LinkedIn. Una petición de referidos.",
         "25 clubes contactados con nombre, 3 a 5 respuestas, 2 llamadas.",
         "Ficha Team Experience y deck de empresa (solo tras respuesta).",
         "Ciclo largo: el cierre probable es de noviembre a enero. Mucha lista de torneos no sirve: clubes ya inactivos o sin contacto."),
        ("Coach Experience", "1 (junto a Team)", "Director técnico o entrenadores de los mismos clubes",
         "Se vende en la misma conversación que Team Experience. Después: asociaciones de entrenadores y cursos.",
         "En la llamada: «¿os interesaría también que vuestros entrenadores se formen con la metodología del club?»",
         "Mencionarlo en el 100 % de las llamadas. Una publicación en LinkedIn sobre formación de entrenadores.",
         "Que salga en todas las propuestas como opción.", "Ficha Coach Experience.",
         "No hace falta outreach propio todavía. No lo dispersemos."),
        ("Becas EEUU (Study & Play USA)", "1 (el que cierra antes)", "Familias de jugadores de 14 a 22 años, y sus entrenadores",
         "1) DMs entrantes de Instagram y WhatsApp.\n2) Contenido de Instagram.\n3) Entrenadores y academias que recomiendan a sus jugadores.\n4) Referidos de familias que ya hablaron con nosotros.",
         "Las 4 preguntas de cualificación (nivel, vídeo, notas, presupuesto del año en EEUU). Nunca prometer beca ni nombrar al partner.",
         "Responder todo en menos de 12 h. Seguimiento a cada lead según etapa. 2 o 3 contenidos. Desde la semana 3: 5 mensajes a entrenadores prescriptores.",
         "10 leads cualificados, 3 llamadas, 1 cierre (Omar, Daniel o el del béisbol son los más avanzados).",
         "Ficha Becas EEUU + vídeo del jugador.",
         "Depende del nivel real del jugador. No descontar como primera respuesta: primero diagnosticar la objeción."),
        ("Campus Internacional (ATM y Real Sociedad fuera de España)", "3 (en pausa)", "Academias o clubes extranjeros con 140 o más niños capaces de pagar unos 130 a 200 € por niño",
         "Solo contactos cálidos: el contacto de Bélgica, SADE Puerto Rico. Sin outreach frío.",
         "No hay primer mensaje: solo conversaciones con contactos cálidos.",
         "Esperar las opciones que proponga el contacto belga. Hipótesis a explorar: pedir a la Real Sociedad una propuesta más flexible (menos entrenadores, formato más ligero).",
         "Ninguno: no hay ficha ni outreach hasta que una versión de la propuesta salga las cuentas.", "Diapositiva del deck.",
         "Bélgica: el contacto dice que no le salen las cuentas (tope de 300 € por niño y los costes de entrenadores, campo, vuelos, alojamiento y comida de los entrenadores del Atlético). Decisiones tomadas el 16/10: firma Always Up con el Atlético, precio fijo a la academia, no se adelanta dinero y los seguros del campus los pone el Atlético."),
        ("International Program (Real Sociedad)", "2", "Un club de origen o academia con un grupo de 9 a 10 jugadores, o varias familias que se agrupen",
         "Academias con volumen (por ejemplo SADE Puerto Rico, que reunió a 140 jugadores en su showcase), clubes de origen con los que ya hablamos y, para llegar a 9 o 10, familias de Instagram.",
         "Una temporada completa de entrenamiento y vida en la Real Sociedad. Siempre se habla de un grupo, no de un jugador suelto.",
         "Recoger interés. Hablar con SADE. Cerrar con Enrique el precio por jugador y nuestra comisión.", "Comisión y precio definidos y una conversación con SADE.", "Diapositiva del deck. Ficha para clubes y academias cuando haya precio.",
         "Mínimo viable: 9 o 10 jugadores. Se reserva antes de la temporada. Nosotros cobramos y luego pagamos a la Real Sociedad, con contrato con el club de origen y con el destino. Devoluciones 0. Con familias consumidoras esa cláusula puede no ser válida: revisar con abogado. Precio y comisión por definir."),
        ("GEE (colegios privados en EEUU)", "3", "Familias de jugadores de 14 a 17 años que buscan high school privado en EEUU",
         "Dentro de la cualificación de Becas, como opción cuando encaja. Es un partner externo.",
         "Se menciona en la conversación de becas, no es un primer mensaje.",
         "Nada propio. Ficha aparte.", "Ficha GEE creada.", "Ficha pendiente.", "Dependemos del partner. Comprador distinto al de becas universitarias: ficha separada."),
        ("Oportunidades profesionales (Alemania y España) y Player Development", "4 (sin estructurar)", "Jugadores 16 a 22 años con nivel profesional posible",
         "No hay outreach. Se recoge interés que llegue por Instagram.", "Ninguno todavía.", "Apuntar interés en 'Oportunidades y notas'.", "Ninguno.", "Ninguno.",
         "Exposición legal con agentes FIFA y menores: usar siempre agente licenciado y abogado. No empezar hasta tener estructura."),
        ("Transversal: marca y canales", "Constante", "Todos",
         "Instagram (10.000 seguidores a fin de 2026), LinkedIn (perfil terminado y deck público subido), web alwaysup.es, Calendly (pendiente de tu horario).",
         "Siempre la misma promesa: experiencias reales con clubes profesionales.", "3 stories o posts por semana. 10 minutos de LinkedIn en días alternos.",
         "Sesión de redes el 17/10 y plan de 4 semanas.", "Perfiles y deck.", "Sin fotos de menores identificables."),
    ]
    for i, row in enumerate(rows, 5):
        for j, v in enumerate(row, 1):
            c = ws.cell(row=i, column=j, value=v)
            c.alignment = Alignment(wrap_text=True, vertical="top")
            c.border = BORDER
            c.font = Font(size=10, bold=(j == 1))
        ws.cell(row=i, column=2).fill = PatternFill("solid", fgColor=(LGRN if row[1].startswith("1") else LYEL if row[1].startswith("2") else GREY))
        ws.row_dimensions[i].height = max(est_height(row[3], 46), est_height(row[5], 44), est_height(row[8], 40), 60)
    ws.freeze_panes = "B5"
    ws.sheet_properties.tabColor = NAVY


VERIF = [
    ("Home Farm FC", "homefarmfc@gmail.com", "Email del club en dbsportstours; enviado 13/10", "Entregado (sin rebote a las 21:30 de España)", "Alta", "Facebook del club"),
    ("Hastings United", "georgia.townsend@hastingsunited.com", "Directorio de la academia; enviado 13/10", "Entregado (sin rebote)", "Alta", "Instagram del club"),
    ("Søreide IL", "fotball@soreideil.no", "soreideil.no/fotball/kontaktinformasjon (publicado por el club)", "Pendiente de enviar", "Alta", "Facebook del club"),
    ("Holbeach United (Callum Lawe)", "callum@holbeachunitedacademy.com", "holbeachunitedcsa.org.uk/contact. ATENCIÓN: Callum Lawe dejó el club (lincsonline, ago 2026) y se fue a Abu Dhabi", "Enviado 14/10, probablemente sin lector", "Baja: persona ya no está", "dan@holbeachunitedacademy.com (Dan Lester)"),
    ("Holbeach United (Dan Lester)", "dan@holbeachunitedacademy.com", "Director y responsable de educación de la academia (búsqueda; coincide con el dominio de la academia)", "Pendiente de enviar el 21/10", "Media", "info@holbeachunitedcsa.org.uk"),
    ("Walnut Creek Surf (EEUU)", "mani@wcsc.org", "Página de staff del club (wcsc.org/club-operations)", "Pendiente: falta dirección postal de la empresa", "Alta", "Contacto del club en wcsc.org"),
    ("Chicago FC United (EEUU)", "info@chicagofcunited.com", "Contacto general del club; Jeff DeGroot es MLS Next Academy Director, sin email personal publicado", "Pendiente: falta dirección postal de la empresa", "Alta (general)", "Teléfono 847-386-6579"),
    ("Whitehaven AFC", "Luke.johnston@whitehavenafc.com", "Aparece como email de contacto del club en dos búsquedas. La web no lo muestra en texto (lo comprobé abriendo la página).", "Pendiente de enviar", "Media", "Facebook de Whitehaven AFC o teléfono +44 1946 692211"),
    ("Maidstone United", "info@maidstoneunited.co.uk", "Contacto general del club (búsqueda)", "Pendiente de enviar", "Media", "Teléfono 078 3585 4704 (Girls Development Centre) o redes"),
    ("IA Akranes", "kfia@ia.is", "Contacto del club (kfia.is y búsqueda)", "Pendiente de enviar", "Media-alta", "Facebook del club"),
    ("Virtu Academy", "info@virtuacademy.co.uk", "virtuacademy.co.uk (búsqueda)", "Pendiente de enviar", "Media", "Instagram del club"),
    ("Seacoast United (EEUU)", "iscott@seacoastunited.com", "Director de coaching según directorios de terceros (búsqueda); la web no lo publica en texto", "Pendiente: falta dirección postal de la empresa", "Media", "questions@seacoastunited.com"),
    ("Cedar Stars Academy (EEUU)", "phil.swenda@cedarstars.com", "Página de staff de Monmouth (cedarstars.com/monmouth-staff)", "Pendiente: falta dirección postal de la empresa", "Media-alta", "contactus@cedarstars.com"),
    ("IFA New England (EEUU)", "mhardiman@ifanewengland.com", "Contacto publicado por el club para consultas de chicos", "Pendiente: falta dirección postal de la empresa", "Media-alta", "Formulario de ifanewengland.com/contact-us"),
    ("Ballistic United (EEUU)", "jerrylosson@busc.org", "Página de staff MLS NEXT (busc.org/mls-next/staff)", "Pendiente: falta dirección postal de la empresa", "Media-alta", "Directorio busc.org/about/directory"),
    ("FC Delco (EEUU)", "info@fcdelco.org", "Contacto general publicado; Jeff Zaun es Director de MLS NEXT, email personal no encontrado", "Pendiente: falta dirección postal de la empresa", "Alta (general)", "Formulario de fcdelco.org/administration/contact-us"),
    ("Michigan Jaguars (EEUU)", "mo.hijazi@michiganjaguarsfc.com", "Página de staff de la sede de Dearborn; el club tiene varias sedes", "Pendiente: falta dirección postal de la empresa", "Media", "michiganjaguarsfc.com/club/staff"),
    ("Lou Fusz Athletic (EEUU)", "matt.mueller@loufuszathletic.com", "Directorio de staff del club (búsqueda)", "Pendiente: falta dirección postal de la empresa", "Media-alta", "loufuszathletic.com/inside-lfa/staff"),
    ("St. Louis Scott Gallagher (EEUU)", "strittschuh@slsgsoccer.com", "Página de MLS NEXT del club (slsgsoccer.com)", "Pendiente: falta dirección postal de la empresa", "Media-alta", "Formulario del club"),
    ("Cincinnati United (EEUU)", "rhands@cincinnatiunitedsc.com", "Directorio de coaching del club (búsqueda)", "Pendiente: falta dirección postal de la empresa", "Media", "cincinnatiunitedsc.com/contact-us"),
    ("Tampa Bay United (EEUU)", "fgonzalez@tbusc.com", "Directorio de staff del club (búsqueda)", "Pendiente: falta dirección postal de la empresa", "Media", "tbusc.com/about/staff"),
    ("Bethesda SC (EEUU)", "dbiss@bethesdasoccer.org", "Página del club (bethesdasoccer.org/derek-biss)", "Pendiente: falta dirección postal de la empresa", "Alta", "Contacto general del club"),
    ("Sockers FC Chicago (EEUU)", "admin@sockersfcchicago.com", "Contacto general publicado; Oleg Vatchev lleva MLS NEXT, email personal no encontrado", "Pendiente: falta dirección postal de la empresa", "Alta (general)", "sockersfcchicago.com/contact-us"),
    ("FC Porte d'Aquitaine", "math.bachowski.mb@gmail.com", "Responsable técnico de jóvenes según directorio (búsqueda). Gmail personal.", "Pendiente de enviar", "Media", "Email oficial del club en la FFF: 560792@lfna.fr"),
]


def sheet_verif(wb):
    ws = fresh(wb, "Verificación", 4)
    title(ws, "Verificación de contactos (control de calidad)",
          "Qué he comprobado de cada dirección y con qué fiabilidad. Importante: ningún método permite saber al 100 % que un buzón existe hasta enviar. "
          "Por eso, tras cada envío miras los rebotes a los pocos minutos (tarea diaria del calendario). «Dominio recibe correo» significa que el dominio tiene servidor de correo activo.", span=7)
    head(ws, 4, ["Club", "Email", "Fuente", "Dominio recibe correo", "Estado", "Fiabilidad", "Plan B si falla"], [24, 36, 56, 18, 28, 12, 46])
    for i, (club, em, src, st, conf, planb) in enumerate(VERIF, 5):
        mx = dig_mx(em.split("@")[1])
        vals = [club, em, src, mx, st, conf, planb]
        for j, v in enumerate(vals, 1):
            c = ws.cell(row=i, column=j, value=v)
            c.alignment = Alignment(wrap_text=True, vertical="top")
            c.border = BORDER
            c.font = Font(size=10)
        ws.cell(row=i, column=6).fill = PatternFill("solid", fgColor=(LGRN if conf == "Alta" else LYEL))
        ws.row_dimensions[i].height = est_height(src, 56, 30)
    r = 5 + len(VERIF) + 1
    notes = ["Descartados tras investigar (13/10): Morecambe Hawks United (equipo local pequeño, no encaja), Team ALTI (sin datos fiables), Lower Ormond (existe en la lista de Semana Santa pero no encuentro contacto).",
             "Excelsior Rotterdam: club profesional con academia (Joep Breimer, jefe de desarrollo de la cantera). Perfil distinto, prioridad baja."]
    for n in notes:
        ws.cell(row=r, column=1, value=n)
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=7)
        ws.cell(row=r, column=1).alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[r].height = 32
        r += 1
    ws.sheet_properties.tabColor = NAVY


def sheet_linkedin(wb, sends):
    saved = read_saved(wb, "LinkedIn - Conexiones", (2, 3), (8, 9))
    ws = fresh(wb, "LinkedIn - Conexiones", 4)
    title(ws, "LinkedIn: conexiones con decisores (se hacen a mano)",
          "Cada fila es una persona. Columna D: enlace directo al perfil o el texto exacto que debes pegar en el buscador de LinkedIn. Antes de conectar, comprueba que el cargo o el club del perfil coincide (columna E te dice cuánta confianza tengo). "
          "Copia la nota de la columna F (máx. 300 caracteres). Si tu cuenta no te deja añadir nota, conecta sin nota y manda el texto cuando acepten. Ritmo: 4 a 8 a la semana, 2 días después del email. No se automatiza.", span=9)
    head(ws, 4, ["Fecha", "Persona", "Club", "Perfil (enlace o qué buscar)", "Fiabilidad", "Nota de conexión (copiar y pegar)", "Cargo / quién es", "Hecho", "Notas"],
         [11, 20, 26, 52, 38, 70, 34, 12, 30])
    people = {}
    for p in PROSPECTS + PROSPECTS_US:
        people[p["key"]] = p
    r = 5
    for x in sends:
        if x["kind"] != "LinkedIn conectar" or x["date"] < D(2026, 10, 19):
            continue
        p = people.get(x["key"], {})
        vals = [x["date"], x["to"], label(x["club"]), x["li_link"], x["li_conf"], x["body"], p.get("person", ""), None, None]
        k = (x["to"], label(x["club"]))
        old = saved.get(k)
        if old:
            vals[7], vals[8] = old
        for i, v in enumerate(vals, 1):
            c = ws.cell(row=r, column=i, value=v)
            c.alignment = Alignment(wrap_text=True, vertical="top"); c.border = BORDER; c.font = Font(size=10)
        ws.cell(row=r, column=1).number_format = "DD/MM/YYYY"
        ws.cell(row=r, column=1).fill = PatternFill("solid", fgColor="F3E8FF")
        ws.row_dimensions[r].height = max(est_height(x["body"], 70), est_height(x["li_link"], 52), est_height(x["li_conf"], 38), 48)
        r += 1
    dv = DataValidation(type="list", formula1='"Pendiente,Hecho,Saltado"', allow_blank=True)
    ws.add_data_validation(dv)
    for rr in range(5, r):
        if ws.cell(row=rr, column=8).value is None:
            ws.cell(row=rr, column=8, value="Pendiente")
        dv.add(ws.cell(row=rr, column=8))
    ws.freeze_panes = "A5"
    ws.sheet_properties.tabColor = "7B3FA0"


def apply_registro(wb):
    """Aplica registro.json (lo que ha pasado de verdad) al Excel: estados de clubes, 'Hecho' en textos y tareas hechas."""
    import json
    path = os.path.join(HERE, "registro.json")
    if not os.path.exists(path):
        return
    reg = json.load(open(path, encoding="utf-8"))
    people = {p["key"]: p for p in PROSPECTS + PROSPECTS_US}
    sa, sb, tx, cal = wb["Segmento A - Clubes"], wb["Segmento B - America"], wb["Textos para copiar"], wb["Calendario diario"]
    for e in reg.get("envios", []):
        p = people.get(e["key"])
        if not p:
            continue
        d = dt.datetime.strptime(e["date"], "%Y-%m-%d")
        for ws, col_estado in ((sa, 9), (sb, 8)):
            for r in range(6, ws.max_row + 1):
                if ws.cell(row=r, column=1).value == p["club"]:
                    ws.cell(row=r, column=col_estado, value="Enviado")
                    cf = 13 if ws is sa else 12
                    ws.cell(row=r, column=cf, value=d); ws.cell(row=r, column=cf + 1, value=d)
                    ws.cell(row=r, column=cf).number_format = "DD/MM/YYYY"; ws.cell(row=r, column=cf + 1).number_format = "DD/MM/YYYY"
        for r in range(5, tx.max_row + 1):
            if tx.cell(row=r, column=4).value == p["club"] and tx.cell(row=r, column=5).value == e["kind"]:
                tx.cell(row=r, column=10, value=d); tx.cell(row=r, column=10).number_format = "DD/MM/YYYY"
    for t in reg.get("tareas", []):
        d = dt.datetime.strptime(t["date"], "%Y-%m-%d").date()
        for r in range(5, cal.max_row + 1):
            a = cal.cell(row=r, column=1).value
            title_ = cal.cell(row=r, column=5).value or ""
            if isinstance(a, dt.datetime) and a.date() == d and title_.startswith(t["task"]):
                cal.cell(row=r, column=9, value="Hecho")
                if not cal.cell(row=r, column=10).value:
                    cal.cell(row=r, column=10, value=t.get("nota"))


def sheet_readme(wb):
    ws = fresh(wb, "LEEME", 0)
    ws.column_dimensions["A"].width = 24
    ws.column_dimensions["B"].width = 110
    ws["A1"] = "Always Up: CRM y plan de captación"
    ws["A1"].font = Font(bold=True, size=16, color=NAVY)
    ws["A2"] = "Actualizado el 13/10/2026. Primero esta página (2 minutos), luego la pestaña Calendario diario."
    ws["A2"].font = Font(italic=True, color="555555")
    blocks = [
        ("TU RUTINA", ""),
        ("Cada mañana (15 min)", "Abre Calendario diario. Hoy sale en amarillo. Haz lo que diga, marca Hecho. Revisa bandeja, Instagram y WhatsApp."),
        ("La víspera (20 min)", "Prepara los correos del día siguiente. Si tu correo permite programar, déjalos programados. Si no, los envías a mano a las 07:30 de Nueva York. El calendario te dice cuáles y de dónde copiar el texto."),
        ("Cada viernes (20 min)", "Revisión semanal: cuéntame respuestas, rebotes y llamadas. Yo actualizo el plan y preparo la siguiente tanda."),
        ("Cada lunes (5 min)", "Escríbeme «investiga 10 clubes más». Yo verifico contactos y dejo los correos listos."),
        ("PESTAÑAS", ""),
        ("Calendario diario", "Tu lista de tareas por día, con hora, pasos y dónde está el texto. Es lo único que necesitas mirar a diario."),
        ("Textos para copiar", "Todos los correos, notas de LinkedIn y mensajes, listos para pegar. Incluye respuestas tipo para cuando contesten."),
        ("LinkedIn - Conexiones", "Las personas con las que conectar en LinkedIn: enlace o qué buscar, nota para copiar y fecha. Se hacen a mano."),
        ("Hoy", "Panel con números (se calculan solos desde las pestañas de segmento)."),
        ("Plan por servicio", "Cómo conseguimos clientes en cada servicio y en qué orden."),
        ("Verificación", "De dónde sale cada email y qué tan fiable es."),
        ("Segmento A / B / C", "Las listas de clubes (A), universidades y clubes de América (B) y leads de becas (C). Actualiza Estado y Fecha de último contacto."),
        ("Dashboard, LinkedIn, Oportunidades", "Fotos del embudo, registro de LinkedIn y notas sueltas."),
        ("COMO Y CUANDO ENVIAR", ""),
        ("Qué se ha comprobado (14/10/2026)", "El envío programado con Mail de Apple SÍ sale: llegó con Mail abierto, con Mail cerrado y con el Mac en reposo. Puede retrasarse unos 10 minutos y no avisa. Los correos programados del 14/10 sí salieron (Holbeach, 04:41)."),
        ("Por qué parecía que no salían", "El correo enviado se guarda en carpetas distintas según el programa: 'Sent' (Outlook), 'INBOX.Sent' (servidor) y 'Sent Messages' (Mail). No lo ves donde miras. Para comprobar: Outlook > buscador > escribe el destinatario > All folders."),
        ("Cómo se programa", "Mail: correo nuevo, pega todo, flecha junto a Enviar > Enviar más tarde > fecha y hora de la columna 'Programar para (NY)'. Se programa la víspera por la tarde."),
        ("Regla para no duplicar", "Una vez programado un correo, no lo envíes a mano. A las 08:00 busca al destinatario en todas las carpetas: si aparece, marca Hecho; solo si no aparece, lo envías a mano."),
        ("Control", "La fuente de verdad es esta hoja: columna 'Hecho (fecha real)' de 'Textos para copiar' y el CRM. No dependas de la carpeta Enviados de ningún programa."),
        ("Truco opcional", "Pon tu Gmail personal en copia oculta (CCO) de cada correo a un club: recibirás una copia como prueba de que salió, y verás en Gmail si entra en bandeja. El club no lo ve."),
        ("TUS FRANJAS DE LLAMADA", ""),
        ("Lo que tienes en Calendly (hora Nueva York)", "Dom 12:00 a 17:00 | Lun 17:30 a 21:00 | Mar 13:00 a 19:00 | Mié 11:00 a 12:30 | Jue 17:00 a 21:00 | Vie 14:00 a 18:00 | Sáb no disponible."),
        ("Clubes de Europa (+5 h en UK e Irlanda, +6 h en Noruega, Francia y Países Bajos; +4 y +5 del 25 al 31/10)", "Sirven: Martes 13:00 a 15:00 (18:00 a 20:00 en UK, buen horario para comités de voluntarios) y Miércoles 11:00 a 12:30 (16:00 a 17:30 en UK). Mal: Lunes y Jueves por la tarde (ya es de madrugada allí), Viernes (noche) y Domingo (tarde de domingo)."),
        ("Familias de América (México, Latinoamérica, EEUU)", "Sirven: Lunes y Jueves por la tarde y Martes 17:00 a 19:00."),
        ("Calendly: no hace falta tocarlo", "Calendly enseña a cada persona los huecos en SU hora, y elige ella. Para familias de becas sirve tal cual. Para clubes, lo normal es proponer tú dos horarios concretos de esta tabla en el email de respuesta (más cómodo para ellos y sin herramienta). El enlace queda como alternativa."),
        ("REGLAS QUE NO SE ROMPEN", ""),
        ("Nunca", "Adjuntos en el primer correo. Nombrar al partner de becas. Prometer becas o fichajes. Inventar urgencia. Discutir precio por escrito sin tu decisión."),
        ("Si contestan", "Paras la cadencia de ese club y abres 'Respuestas tipo' (hoja Textos para copiar). Menos de 4 horas de respuesta en horario del club."),
        ("Si un correo rebota", "Me lo dices; busco otra dirección del club y te la dejo preparada."),
        ("Colores", "Azul claro = email 1, amarillo = follow-up 1, naranja = follow-up 2, gris = cierre, lila = LinkedIn o redes, rojo = pendiente atrasado."),
    ]
    r = 4
    for a, b in blocks:
        if b == "":
            ws.cell(row=r, column=1, value=a)
            ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=2)
            ws.cell(row=r, column=1).fill = PatternFill("solid", fgColor=NAVY)
            ws.cell(row=r, column=1).font = Font(bold=True, color="FFFFFF")
            ws.row_dimensions[r].height = 22
        else:
            ws.cell(row=r, column=1, value=a).font = Font(bold=True, size=10)
            ws.cell(row=r, column=2, value=b).font = Font(size=10)
            for cc in (1, 2):
                ws.cell(row=r, column=cc).alignment = Alignment(wrap_text=True, vertical="top")
                ws.cell(row=r, column=cc).border = BORDER
            ws.row_dimensions[r].height = est_height(b, 110, 20)
        r += 1
    ws.sheet_properties.tabColor = RED


def update_segment_a(wb, sends):
    sa = wb["Segmento A - Clubes"]
    by_name = {sa.cell(row=r, column=1).value: r for r in range(6, 60) if sa.cell(row=r, column=1).value}
    next_row = max(by_name.values()) + 1
    for p in PROSPECTS:
        r = by_name.get(p["club"])
        if r is None:
            r = next_row
            next_row += 1
            for cidx in range(1, 17):
                src, dst = sa.cell(row=16, column=cidx), sa.cell(row=r, column=cidx)
                dst._style = copy_style(src._style)
            sa.cell(row=r, column=1, value=p["club"])
            sa.cell(row=r, column=2, value=p.get("pais"))
            sa.cell(row=r, column=3, value=p.get("cat"))
            sa.cell(row=r, column=4, value=p.get("motivo"))
            sa.cell(row=r, column=5, value=p.get("fuente"))
            sa.cell(row=r, column=16, value="1er email: nada adjunto, solo texto con firma. Si pide información: deck de empresa + ficha Team Experience. Tras la llamada: propuesta escrita.")
        mine = [x for x in sends if x["key"] == p["key"]]
        e1 = next((x for x in mine if x["kind"] == "Email 1"), None)
        fu1 = next((x for x in mine if x["kind"] == "Follow-up 1"), None)
        sa.cell(row=r, column=7, value=p["to"])
        if p.get("person"):
            sa.cell(row=r, column=6, value=p["person"])
        sa.cell(row=r, column=11, value=p["subj"])
        advanced = sa.cell(row=r, column=9).value in ("Enviado", "Respondido", "Llamada agendada", "Llamada realizada", "Cerrado", "Perdido", "En negociación", "Solo info")
        if advanced:
            if sa.cell(row=r, column=9).value == "Enviado" and fu1:
                sa.cell(row=r, column=10, value="Follow-up 1 el %s en el mismo hilo (enviar a las 07:30 hora Nueva York). Textos en la hoja 'Textos para copiar'." % fu1["date"].strftime("%d/%m/%Y"))
        elif e1:
            sa.cell(row=r, column=9, value="Listo para enviar")
            sa.cell(row=r, column=10, value="Enviar el %s a las 07:30 hora Nueva York. Textos en la hoja 'Textos para copiar'." % e1["date"].strftime("%d/%m/%Y"))
            sa.cell(row=r, column=12, value=e1["body"])
        elif fu1:
            sa.cell(row=r, column=10, value="Follow-up 1 el %s en el mismo hilo. Textos en la hoja 'Textos para copiar'." % fu1["date"].strftime("%d/%m/%Y"))
    # notas puntuales
    def setnote(name, text, append=False):
        r = by_name.get(name)
        if r:
            old = sa.cell(row=r, column=15).value or ""
            sa.cell(row=r, column=15, value=(old + " | " + text) if (append and old) else text)
    setnote("Søreide IL", "13/10/2026: el email 1 REBOTÓ (ungdomsutvalget@soreideil.no reenvía a una cuenta inexistente en bergensskolen.com). Contactos reales en soreideil.no/fotball/kontaktinformasjon. Reenvío el 14/10 a fotball@soreideil.no.")
    setnote("Whitehaven AFC (Juniors Girls U13-U15)", "Email de Luke Johnston (presidente) sacado de buscadores; la web no lo muestra. Si rebota: Facebook o teléfono +44 1946 692211.")
    setnote("Lower Ormond", "13/10/2026: aparece como club de Inglaterra en la edición de Semana Santa de la Costa Daurada Cup. No encuentro contacto fiable.", True)
    setnote("Excelsior Rotterdam", "13/10/2026: club profesional con academia. Perfil distinto, prioridad baja.")
    setnote("Morecambe Hawks", "13/10/2026: solo equipo local pequeño de liga amateur. Descartado.")
    r = by_name.get("Leonardo Uren / equipo (Brasil) — posible partner, no solo cliente")
    if r:
        sa.cell(row=r, column=9, value="Perdido")
        sa.cell(row=r, column=10, value="Decisión de Joel (13/10/2026): no insistir. Reabrir solo si él escribe.")
        sa.cell(row=r, column=15, value=(sa.cell(row=r, column=15).value or "") + " | 13/10/2026: Joel decide no reactivar: varios intentos y las dos últimas sin respuesta.")
    # Segmento B: clubes de EEUU preparados
    sb = wb["Segmento B - America"]
    exist = {sb.cell(row=r, column=1).value: r for r in range(6, 80) if sb.cell(row=r, column=1).value}
    nxt = max(exist.values()) + 1 if exist else 6
    for p in PROSPECTS_US:
        r = exist.get(p["club"])
        if r is None:
            r = nxt; nxt += 1
            for cidx in range(1, 16):
                src, dst = sb.cell(row=6, column=cidx), sb.cell(row=r, column=cidx)
                dst._style = copy_style(src._style)
        mine = [x for x in sends if x["key"] == p["key"]]
        e1 = next((x for x in mine if x["kind"] == "Email 1"), None)
        sb.cell(row=r, column=1, value=p["club"]); sb.cell(row=r, column=2, value=p["pais"]); sb.cell(row=r, column=3, value=p["cat"])
        sb.cell(row=r, column=4, value=p["motivo"]); sb.cell(row=r, column=5, value=p["fuente"]); sb.cell(row=r, column=6, value=p["person"]); sb.cell(row=r, column=7, value=p["to"])
        cur = sb.cell(row=r, column=8).value
        if cur not in ("Enviado", "Respondido", "Llamada agendada", "Llamada realizada", "Cerrado", "Perdido"):
            if e1:
                sb.cell(row=r, column=8, value="Listo para enviar")
                sb.cell(row=r, column=9, value="Enviar el %s a las 09:30 hora local (%s). Textos en 'Textos para copiar'." % (p["e1"].strftime("%d/%m/%Y"), local_to_ny(p["e1"], p["tz"]) + " hora Nueva York"))
                sb.cell(row=r, column=10, value=p["subj"]); sb.cell(row=r, column=11, value=e1["body"])
            else:
                sb.cell(row=r, column=8, value="Pendiente investigar")
                sb.cell(row=r, column=9, value="Falta la dirección postal de Quality Servix Premium SL para poder enviar a EEUU (ley CAN-SPAM). Fecha prevista: %s." % p["e1"].strftime("%d/%m/%Y"))
        sb.cell(row=r, column=15, value="1er email: nada adjunto, solo texto. Si pide información: deck de empresa + ficha Team Experience.")
    # Hoy: metas realistas
    h = wb["Hoy"]
    h["A11"].value = "Métrica"; h["B11"].value = "Meta semanal"
    h["A12"].value = "Nuevos clubes/academias investigados con decisor y email verificados"; h["B12"].value = "10"
    h["A13"].value = "Emails de outreach nuevos enviados"; h["B13"].value = "5 a 8"
    h["A14"].value = "Conexiones de LinkedIn con nota personalizada"; h["B14"].value = "5"


def main():
    sends = build_sends()
    rep_rows = [dict(club="-", kind="Plantilla", body=b, subj="") for _, b, _ in REPLIES]
    problems = validate(sends + rep_rows)
    if problems:
        for p in problems:
            print("PROBLEMA:", p)
        raise SystemExit("Corrige los textos antes de generar.")
    cal = build_calendar(sends)
    wb = openpyxl.load_workbook(CRM)
    if "Outreach - Copiar y pegar" in wb.sheetnames:
        del wb["Outreach - Copiar y pegar"]
    update_segment_a(wb, sends)
    sheet_calendar(wb, cal)
    sheet_texts(wb, sends)
    sheet_linkedin(wb, sends)
    sheet_services(wb)
    sheet_verif(wb)
    sheet_readme(wb)
    apply_registro(wb)
    order = ["LEEME", "Calendario diario", "Hoy", "Textos para copiar", "LinkedIn - Conexiones", "Plan por servicio", "Verificación", "Segmento A - Clubes",
             "Segmento B - America", "Segmento C - Becas", "Dashboard", "LinkedIn - Plan diario", "Oportunidades y notas"]
    wb._sheets = [wb[n] for n in order if n in wb.sheetnames] + [s for s in wb._sheets if s.title not in order]
    wb.active = 1
    wb.save(CRM)
    # md resumen
    out = os.path.join(HERE, "..", "..", "02-sales", "outreach-textos-generados.md")
    L = ["# Textos de outreach (generado)", "", "> Generado por `07-automations/outreach/generar_outreach.py`. No editar a mano: cambiar el script y ejecutarlo de nuevo. "
         "Los mismos textos están, ordenados por fecha, en la hoja `Textos para copiar` del CRM.", ""]
    for s in sends:
        if s["kind"] == "Email 1":
            L += ["## %s: email 1 (enviar %s a las %s hora Nueva York)" % (s["club"], s["date"].strftime("%d/%m/%Y"), local_to_ny(s["date"], s["tz"])), "",
                  "**Para:** %s" % s["to"], "", "**Asunto:** %s" % s["subj"], "", "```", s["body"], "```", ""]
    open(out, "w", encoding="utf-8").write("\n".join(L))
    print("OK. Tareas en calendario: %d, envíos: %d" % (len(cal), len(sends)))


if __name__ == "__main__":
    main()
