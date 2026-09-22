# Embudo de ventas — inbound (Instagram, DM, email)

> Diseñado para cubrir los 5 servicios reales, no solo becas — Joel va a publicar contenido de todos los servicios desde agosto 2026. Ver [playbook-ventas.md](playbook-ventas.md) para pricing y manejo de objeciones, [pipeline.md](../01-clients/pipeline.md) para registrar cada lead.

**Por qué esto es la prioridad #1 ahora mismo:** ya hay inbound real (Instagram) que genera interés y videollamadas, pero **0 clientes cerrados hasta ahora**. El problema no es falta de leads, es falta de proceso entre "alguien pregunta" y "alguien firma". Arreglar esto vale más que conseguir más leads nuevos (LinkedIn, EEUU) mientras la fuga siga abierta.

## Decisión sobre el "Always Up Sales System" (revisión externa, 2026-07)

Joel compartió una revisión externa (vía ChatGPT actuando de CRO) que proponía convertir esto en un "Sales System" de 17 módulos con carpeta propia. Decisión tomada: **no se crea ninguna estructura paralela** — este repo (`01-clients`, `02-sales`, `03-operations`) sigue siendo la única fuente de verdad. Se adoptan las ideas buenas y baratas directamente aquí; se descartan o aplazan las que añaden infraestructura sin validar primero:

- **Adoptado ahora:** nombres de llamada tipo diagnóstico (no "sales call"), propuesta escrita tras la llamada, petición explícita de referidos, revisión semanal de métricas, vídeos personalizados de prospección.
- **Aplazado hasta validar el proceso manual con clientes reales:** email marketing/nurturing automático, sistema de puntuación de leads, automatización con ManyChat/HubSpot/n8n.
- **No se construye todavía:** rama de embudo para Player Development (servicio sin programa/precio definido aún).

## Recuperación de backlog (mensajes/comentarios sin contestar tras una ausencia)

> Situación real de agosto 2026: Joel volvió de vacaciones con ~3 semanas de DMs y comentarios sin contestar. Esta gente ya mostró interés real — probablemente más rápido de convertir que el outreach en frío, así que se trabaja primero.

**Proceso:**
1. Bloque de tiempo dedicado (1-2h seguidas), no a ratos sueltos.
2. Comentarios primero (responder "te escribo por privado"), luego DMs de más reciente a más antiguo — pero contestar a **todos**, incluso los de hace semanas.
3. Usar el mensaje de recuperación (no cualificación normal, reconoce el hueco de tiempo sin sobre-disculparse):

```
¡Hola! Perdona la tardanza en contestar — he estado unos días fuera.
¿Sigues interesado/a? Si es así, cuéntame rápido:
[preguntas de cualificación del servicio correspondiente — ver Paso 2 abajo,
o sección 2 de "Las 5 etapas" según el servicio]
```

4. Configurar "Respuestas guardadas" en Instagram (cuenta Profesional/Creador → Ajustes → Mensajes → Respuestas guardadas) con este mensaje + las preguntas por servicio, para no escribir cada uno desde cero.
5. Registrar cada respuesta en [pipeline.md](../01-clients/pipeline.md) según van contestando.

## Caso práctico: comentario en vídeo de becas (el más repetido hoy)

**Diagnóstico de lo que Joel ya hacía:** responder al comentario público con "te escribo por privado" está bien (rápido, personal) — no cambiar. El problema estaba en el DM: *"Cuéntame tu situación"* es una **pregunta abierta**, y las preguntas abiertas bajan la tasa de respuesta porque obligan al lead a pensar qué escribir. Sustituir por preguntas concretas de respuesta rápida.

**Paso 1 — comentario público:** igual que ahora, sin cambios.

**Paso 2 — primer DM (cualificación con preguntas concretas, no abiertas):**
```
Hola! 👋 Vi tu comentario en el vídeo sobre becas deportivas — genial que estés interesado.

Para poder ayudarte de verdad, cuéntame rápido:
1. ¿Qué edad tiene el jugador/a y en qué curso/año está ahora? (¿cuándo se gradúa?)
2. ¿En qué equipo/categoría juega hoy y suele ser titular? (club, academia, selección…)
3. ¿Tenéis un vídeo reciente jugando (últimos ~6 meses)?
4. ¿En qué país estáis ahora?

Con esto te digo exactamente cómo os podemos ayudar 🙌
```

**Por qué estas 4 y no otras** (Joel pidió medir el nivel real, 2026-08):
- **Edad + año de graduación** → sin esto no hay forma de saber si hay un plazo real. Un niño de 10-13 años es "solo info", no una llamada — el proceso serio empieza a los 15-16.
- **Nivel al que juega hoy** → es el dato que más determina si una beca es realista. Alguien que apenas juega en un equipo de nivel bajo no va a conseguir beca universitaria en EEUU, y una llamada ahí es tiempo perdido — mejor decírselo con cariño por texto.
- **Vídeo reciente** → sin vídeo no se puede evaluar, así que no se puede hacer una llamada útil. Si no lo tiene, el siguiente paso es conseguirlo, no agendar.
- **País** → afecta a visado, coste total y realismo del caso.

**Paso 3 — dos caminos según la respuesta (esto es lo que faltaba):**
- **Señal real** (contesta rápido y con detalle: juega a buen nivel, se gradúa en 1-2 años, tiene o puede conseguir vídeo): pasar directo al enlace de reserva de llamada + guía corta de becas. No alargar por texto.
- **Vago / no encaja** (respuesta corta sin datos, jugador muy joven, sin vídeo ni forma de conseguirlo, nivel claramente bajo): mandar info básica async, **no** agendar llamada, marcar "solo info" en el CRM, y dejar la puerta abierta sin perseguir ("cuando tengas un vídeo / cuando estéis más cerca de la graduación, escríbeme y lo vemos").

### Cuando piden videollamada antes de estar cualificados (situación real de agosto 2026)

Pasa a menudo: alguien lee la guía y responde *"el siguiente paso es programar la videollamada"* — sin que sepas todavía su nivel. **Regla: no se agenda la llamada hasta tener respuesta concreta a nivel + vídeo (+ año de graduación en becas).** No es decir que no — es anteponer 3 preguntas, enmarcadas como preparación:

```
¡Perfecto! Antes de la videollamada, para que sea lo más útil posible y poder
evaluar bien el caso, cuéntame 3 cosas rápidas:
1. ¿En qué equipo/categoría juega ahora y suele ser titular?
2. ¿Tenéis un vídeo reciente jugando? (si no, ese es el primer paso antes de la llamada)
3. ¿Cómo va de notas/promedio? (cuenta para la admisión en EEUU)

Con esto preparo la llamada con algo concreto que deciros.
```

Si contesta con señal real → mandas el Calendly. Si contesta con vaguedad o no contesta → se ha autodescartado, marcar "solo info".

**Nota de CRM:** cuando un lead salta de Instagram a WhatsApp, apunta ya el número de teléfono junto a su handle en la pestaña "Segmento C - Becas" de [crm-ventas.xlsx](../01-clients/crm-ventas.xlsx) y pega ahí sus respuestas — así no vuelves a perder el perfil al cambiar de canal (problema real que te ha pasado).

### Dos ejemplos reales resueltos

**Ejemplo A — padre mexicano, gemelos de 17, último año de prepa** (pidió videollamada tras leer la guía):
```
¡Perfecto! Con 17 años y último curso, el momento es ahora — hay que moverse
esta temporada para entrada en otoño 2027. Antes de la videollamada, para
poder evaluar de verdad su caso, cuéntame 3 cosas rápidas:
1. ¿En qué equipo/categoría juegan ahora y suelen ser titulares?
2. ¿Tienen algún vídeo reciente jugando? Si no, es el primer paso antes de la llamada.
3. ¿Cómo van de promedio en la prepa? (cuenta para la admisión en EEUU)

Con esto preparo la llamada con algo concreto para deciros.
```
(Está razonablemente bien de plazo y edad — solo falta nivel, vídeo y notas antes de agendar.)

**Ejemplo B — mensaje de Marruecos: "I love football and want to play in the future, would you accept me and let me join you?"**
Aquí hay un malentendido de base (cree que Always Up es un club al que te apuntas o haces prueba). Respuesta honesta, cálida, que reencuadra y cualifica de una vez:
```
Hi! Thanks for reaching out. Quick note on what we do: Always Up isn't a club
you join — we help players get football scholarships at US universities (study
+ play) and we run training programs in Spain with professional clubs. Both are
paid programs. Scholarships work best for players aged 15-18 who already compete
regularly and have solid school grades.

To see if we can realistically help you, tell me honestly:
1. How old are you and what year of school are you in?
2. What level do you play at now (club, league)?
3. Do you have a recent video playing?
4. Would your family be able to support a paid program?

Being honest helps me tell you straight whether this is realistic for you.
```
(Es un lead de baja probabilidad: programa enfocado a EEUU, lo paga la familia, sin datos que sugieran encaje. Merece **una** respuesta de cualificación — no perseguirlo si no llega señal real.)

**Ejemplo C — nivel bajo (2ª Regional), pero honesto y con plazo real (2026-09):** 20 años, empieza un grado superior de deporte (termina junio 2028), quiere ir a EEUU con beca al terminar, juega en 2ª Regional de Madrid (el nivel más bajo), ya pagó por unas pruebas con otra empresa y le dieron un presupuesto que no podía permitirse. Aquí el nivel sí es un problema real, pero el lead se lo merece con matices — nunca decir "tu nivel no es suficiente" en esos términos (suena a juicio personal), sino enmarcarlo como un hecho sobre cómo reclutan los entrenadores. **Nunca llamar "agencia" a Always Up** (sí se puede usar la palabra para describir lo que hizo la otra empresa, si el lead ya la usó):

```
Te agradezco mucho la honestidad, de verdad — no es fácil escribir eso
y habla muy bien de ti.

Te lo digo con la misma sinceridad: nadie te debería garantizar una
beca jugando en 2ª Regional — no suele ser la primera opción de los
entrenadores, así que si alguien te lo promete sin más, desconfía.

Para poder ayudarte de verdad, cuéntame dos cosas: ¿qué presupuesto
tendrías en mente para este proceso, y cuáles son tus objetivos
exactos buscando ir a EEUU?

Con esto ya te puedo decir con honestidad qué es realista y cómo
podríamos ayudarte 🙌
```

**Por qué está escrito así:**
- Devuelve honestidad con honestidad — no es una plantilla fría, reconoce lo que el lead ya hizo bien.
- El nivel se presenta como un hecho externo (cómo buscan los entrenadores), no como un defecto del jugador — mismo mensaje, mucho menos hiriente.
- En vez de cerrar la conversación ("vuelve en 1-2 años"), se sigue cualificando con presupuesto y objetivos — un lead honesto con plazo real (aunque lejano) merece más esfuerzo que uno vago, incluso si el nivel es bajo hoy.
- Ojo con el presupuesto que responda: **no negociar precio ni prometer descuentos por escrito** — eso es una decisión de Joel, no algo que se resuelve en el DM.

### Qué responder cuando ya contestan a las 4 preguntas

Tres respuestas posibles según lo que digan — mirar primero cuál encaja antes de escribir nada, no hay una única plantilla:

**A) Encaja bien Y tiene vídeo → mandar el Calendly ya:**
```
¡Perfecto, [nombre]! Con esto ya tengo una idea clara — [1 línea que recoja lo
que dijeron, ej. "con 17 años, jugando de titular en [equipo/liga] y
graduándose en 2027, el timing es bueno"].

El siguiente paso es una videollamada donde evaluamos el vídeo con más
detalle y os cuento exactamente cómo sería el proceso para vuestro caso.
Aquí el enlace para elegir el día que mejor os venga: [Calendly]

Nos vemos ahí 🙌
```
CRM: Etapa → "Llamada agendada" (en cuanto reserve) o "Cualificado" mientras tanto. Próxima acción → "Esperar reserva de Calendly".

**B) Encaja en edad/nivel pero falta el vídeo → pedirlo, no agendar todavía:**
```
¡Genial, gracias por contarme! Con esa edad y ese nivel encaja bien. Lo único
que necesito antes de la llamada es un vídeo reciente jugando (últimos
meses) — puede ser de un partido o entreno, no hace falta que sea
profesional, solo que se le vea jugar con claridad.

En cuanto lo tengas me lo mandas y agendamos la llamada con eso ya evaluado 🙌
```
CRM: Etapa → "Cualificado". Próxima acción → "Esperar vídeo". Si no llega en 1-2 semanas, un único recordatorio suave — sin perseguir más.

**C) No encaja todavía (muy joven, nivel bajo, o respuesta vaga) → info async, sin llamada, con cariño real:**
```
¡Gracias por contarme! Ahora mismo, [con X años / al nivel que juega hoy],
todavía es pronto para el proceso de becas universitarias — normalmente
arranca en serio a partir de los 15-16 años, cuando ya se puede evaluar
bien el nivel competitivo.

Te dejo igualmente la guía con todo el proceso para que la tengáis a mano:
[guia-becas.md] — y en cuanto [esté más cerca de esa edad / juegue a un
nivel más competitivo / tengáis vídeo], escríbeme sin problema y lo
retomamos con calma.
```
CRM: Etapa → "Nuevo" con nota "solo info, revisar más adelante" — **no** marcar como perdido (puede volver en 1-2 años con el mismo hijo), pero tampoco como cualificado.

**Regla para elegir entre las 3:** si dudas entre B y C, pregúntate si con un vídeo *hoy* el caso sería defendible en una llamada — si sí, es B; si el problema es la edad o el nivel en sí (no la falta de vídeo), es C.

### Caso nuevo: ya está en EEUU con visado resuelto, deporte distinto al fútbol (2026-09)

Un padre escribe porque su hijo ya tiene beca de instituto en EEUU **por béisbol**, visado F1 de 5 años ya en marcha, y 2 años de instituto por delante. Menciona que el béisbol universitario es muy competitivo y que quiere usar estos años para "explorar otras vías" — **no confundir esto con que el hijo quiera cambiar a fútbol** (error real cometido aquí la primera vez: no asumir que "explorar otras vías" significa fútbol solo porque escribe a Always Up). El hijo juega béisbol, no fútbol, y la vía deportiva correcta sigue siendo esa — no tiene sentido ni es honesto intentar reconducirlo hacia un deporte que no juega, aunque sea el que domina Always Up.

**Qué hacer en un caso así:** no ofrecer nada de fútbol de entrada, ni presuponer que Always Up puede resolver la parte deportiva de un deporte que no es el suyo. Presentar los dos caminos reales de la familia — seguir con el béisbol para la vía deportiva, y la vía académica en paralelo — sin prometer que Always Up gestiona directamente el reclutamiento de béisbol:

```
¡Qué bien lo del béisbol, enhorabuena por la beca! Y tienes toda la
razón con lo del nivel — el béisbol universitario en EEUU es
brutalmente competitivo, así que es una decisión inteligente pensarlo
con tiempo.

Con 2 años de instituto por delante y el visado ya resuelto, tenéis
básicamente dos caminos reales que podéis trabajar en paralelo: seguir
desarrollando el béisbol de cara a una beca deportiva (nada
garantizado, pero con estos 2 años por delante es un buen momento para
construirlo) y una beca académica, que depende del expediente y es
independiente del deporte.

Para poder aconsejarte con criterio, cuéntame: ¿en qué nivel está
jugando ahora mismo (equipo del instituto, ligas, si hay algún vídeo
reciente)? Y en lo académico, ¿cómo va de notas?

Con esto te digo con honestidad qué es lo más realista para estos 2
años.
```

**Nota abierta:** queda pendiente confirmar si el servicio de beca académica de Always Up/partner es independiente del deporte (aplicable aunque el chico no juegue fútbol) — hasta confirmarlo, no prometer gestión activa de esa vía, solo dar consejo honesto.

### Caso real: ya cualificado, pero pregunta por prueba social antes de la llamada (2026-09)

A veces, tras las 4 preguntas, el lead no solo responde con datos buenos — además pregunta por pruebas ("¿con qué universidades trabajáis?", "¿tenéis contacto con coaches?", "¿ejemplos de jugadores colocados?") o pregunta algo personal sobre Joel ("¿estás en EEUU?"). Esto **no es una objeción, es una señal de compra fuerte** — no lo trates como un obstáculo, es alguien decidiendo si confiar. Responder con honestidad + la prueba real que sí tenemos, sin fabricar nombres de universidades o jugadores concretos que no estén confirmados:

```
¡Qué bien lo de [nombres], gracias por todo el detalle! 🙌

Sobre tu pregunta: yo personalmente ahora mismo estoy en EEUU (Nueva York,
estudiando), y el proceso de colocación en universidades lo llevamos con
nuestro equipo que trabaja directamente allí, con contacto con coaches y
universidades según el perfil de cada jugador — eso es justo lo que vemos
en la llamada, con vuestro caso concreto.

Para que te hagas una idea: hemos colocado cerca de 400 jugadores en
universidades de EEUU desde 2019, con contacto directo en varios países.

Con último año de prepa y el objetivo de agosto 2027, el timing es bueno
para empezar ya. Te propongo:
1. Me mandáis el vídeo que ya tenéis de cada uno (el del año pasado vale
   para arrancar, no hace falta esperar al actualizado)
2. Agendamos la llamada aquí: [Calendly]

Ahí vemos todo con detalle — universidades, proceso, y qué encaja mejor
para cada uno de los dos 🙌
```

**Por qué está escrito así:**
- Responde la pregunta personal con honestidad simple, sin dar más vueltas de las necesarias.
- Usa la única cifra agregada que sí está verificada (~400 colocados desde 2019, scouts en varios países — ver [playbook-ventas.md](playbook-ventas.md)/línea de becas) — **nunca inventar nombres concretos de universidades, coaches o jugadores** que no estén confirmados; el detalle específico se da en la llamada, no por escrito.
- No bloquea por el vídeo "actualizado" que están preparando — el que ya tienen alcanza para empezar, así no se pierde tiempo esperando.
- Cierra con Calendly porque ya hay señal real suficiente (edad, nivel, plazo, nivel de detalle en las preguntas) — no hace falta seguir cualificando por texto.

## Las 5 etapas (versión general, para el resto de servicios)

### 1. Mensaje entrante — alguien pregunta por info

No reaccionar todavía con información — primero cualificar. Responder siempre con calidez + 2-3 preguntas, nunca con un muro de texto de entrada.

### 2. Cualificación — identificar servicio + encaje, en un solo mensaje

Plantilla base (ajustar tono, no hace falta enviarlo literal palabra por palabra):

```
Hey! Thanks for reaching out 🙌 Happy to give you all the info.
Quick questions so I can point you to the right program:
- What's your age / what age is the player?
- Are you looking more for a team/club experience in Spain, a scholarship
  in the US, or something else (like individual player development)?
- What country are you / your team based in?
```

**Por qué importa la 2ª pregunta:** desde agosto va a llegar gente interesada en cosas distintas (no solo becas) — esta pregunta dirige automáticamente a la ficha correcta del punto 3.

### 3. Qué enviar según el servicio (ficha corta + activos de autoridad, no la presentación completa)

| Si pregunta por... | Qué mandar | Precio a mencionar si preguntan directamente |
|---|---|---|
| **Team/Coach Experience** (equipo/club quiere viajar a España) | Ficha corta: "training with pro Spanish clubs (Atlético, Real Sociedad, Sporting), full logistics included" + caso Greystones (título de liga) + **fotos/vídeos reales de experiencias pasadas si Joel los tiene (pendiente confirmar qué material existe)** | $1.500 (5 días estándar) — desde $2.500-$3.500 si es formato premium multi-club |
| **Becas EEUU** (jugador quiere estudiar+jugar en universidad) | Enviar [guia-becas.md](guia-becas.md) (lead magnet) + pedir vídeo/perfil del jugador para evaluar nivel | $2.500-$4.000 lo paga el jugador a University Soccer (Joel no cobra directo al lead, cobra comisión de University Soccer) |
| **Colegio privado EEUU** (más joven, boarding school) | Explicar proceso vía GEE | 2.500€-3.500€ (fee de GEE, aparte de matrícula del colegio) |
| **International Program** (Real Sociedad, residencial) | Explicar los 3 formatos (1/5/10 meses), pedir perfil/vídeo para evaluación | 5.000€ / 25.000€ / 45.000€ según duración |
| **Player Development** (guía individual, sin ser club ni beca) | **Servicio todavía en desarrollo — no comprometer precio ni programa cerrado.** Responder con interés genuino, explicar que es un programa personalizado que se está afinando, pedir contacto para avisar en cuanto esté listo, y registrar como lead caliente en el pipeline | Sin definir todavía |
| Alemania/España (oportunidades profesionales) | Mencionar que existe pero está en fase muy temprana — no es prioridad activa, no ofrecer como producto cerrado | Sin definir todavía |

**Regla general:** nunca mandar precio como primer mensaje sin contexto — siempre después de entender el caso (edad, nivel, objetivo). Evita que el precio se lea sin el valor detrás.

**Sobre "activos de autoridad" (idea de la revisión externa, 2026-07):** antes de la llamada, cuanta más prueba social real se mande (no solo texto), más confianza se genera. **Pendiente de Joel:** ¿existen fotos/vídeos reales de las experiencias con Greystones u otros clientes? Si sí, hay que reunirlos en una carpeta de acceso rápido — no inventar ni usar contenido genérico de stock.

### 4. Agendar llamada — combinar formulario + agenda en un solo paso

Objetivo: pasar de DM a videollamada lo antes posible — por texto no se cierra nada, como ya se ha visto con becas.

**Sobre la idea del formulario (pregunta de Joel, 2026-07):** es una buena idea, pero con un matiz que ahorra un paso — en vez de formulario aparte + luego enlace de Calendly, **usar las "preguntas personalizadas" que Calendly permite añadir al reservar la llamada**. Así el lead responde las preguntas de cualificación en el mismo momento en que reserva hora, en un solo paso en vez de dos. Cada paso adicional en un embudo pierde gente por el camino — menos pasos = más gente que llega al final.

Preguntas a incluir en el Calendly (ajustar según servicio): edad del jugador, posición/nivel, país, objetivo (universidad/colegio/experiencia/desarrollo individual), presupuesto aproximado si se atreve a compartirlo.

**Cuándo sí tiene sentido un formulario aparte, sin Calendly integrado:** solo cuando el volumen crezca tanto que Joel no pueda cualificar por DM uno a uno — un formulario filtra antes de invertir tiempo. Con el volumen de hoy, ir directo por DM + Calendly con preguntas cierra más rápido que añadir un paso extra.

**Hecho (2026-08): Joel creó un único evento de Calendly, "Always Up - Assessment Call"**, más simple que la idea original de un evento por servicio — resuelve el "qué servicio" con la primera pregunta en vez de con eventos separados. Preguntas reales configuradas:
1. What would you like to discuss? (Team Experience / Coach Experience / USA Sports Scholarships / International Program / Professional Football Opportunities / Player Development / Other)
2. Who are you / what is your role? (Player / Parent / Coach / Academy Director / Sporting-Technical Director / Club Director / University Staff / Other)
3. What country are you currently based in?
4. Who is the opportunity for? (Myself / My son-daughter / My team-club / My organization / Other)
5. Please briefly tell us about your situation and what you are looking to achieve.
6. What would you ideally like to achieve and when?
7. (Opcional) Is there anything you'd like us to review before the call? (vídeo del jugador, perfil del equipo, etc.)

La pregunta 2 (rol de quien reserva) es una mejora real sobre lo planteado inicialmente — permite saber antes de la llamada si quien reserva es un jugador suelto o un Academy/Technical Director, y ajustar el enfoque en consecuencia. Falta solo que Joel añada sus horarios de disponibilidad.

### 5. Guion de la llamada (estructura + preguntas reales por bloque)

**Nombre real usado (2026-08):** Joel unificó todo en un solo evento, **"Always Up - Assessment Call"** — cumple igual el objetivo de sonar a evaluación y no a venta, simplificando de paso la gestión (un evento, no cinco).

**Bloque 1 — Reconfirmar el caso (2-3 min):**
- "Cuéntame un poco más de [jugador] — ¿cuánto lleva jugando a este nivel?"
- "¿Qué es lo que más os importa ahora mismo — el fútbol, lo académico, la experiencia en sí, o un poco de todo?"
- Para becas/colegio específicamente: "¿Tenéis ya alguna referencia de presupuesto que os iría bien, o todavía está abierto?"

**Bloque 2 — Explicar el programa que mejor encaja (con el valor por delante del precio, ver [playbook-ventas.md](playbook-ventas.md)):**
- Team/Coach Experience: liderar con el caso Greystones (título de liga) antes de hablar de logística.
- Becas: liderar con el proceso y lo que hace especial a University Soccer (scouts en 4 países, ~400 colocados desde 2019), no con el precio.
- International Program: liderar con la metodología de la Real Sociedad y el formato residencial, no con los tres precios de golpe.

**Bloque 3 — Dar el precio con seguridad, sin disculparte por él.** Decirlo una vez, con naturalidad, y quedarte en silencio — no rellenar el silencio justificando el precio antes de que reaccionen.

**Bloque 4 — Sacar la objeción real, no asumirla** (lección del caso Renegades: "es caro" resultó ser "el coste total del viaje + vuelos", no que el precio no fuera competitivo):
- "¿Qué necesitarías ver para sentirte seguro dando el paso?"
- Si dicen que es precio: "¿Es el número en sí, o es más el conjunto con otros gastos (viajes, otros costes)?" — distingue entre objeción de precio real y de presupuesto total.

**Bloque 5 — Cerrar con siguiente paso concreto y con fecha** (nunca "lo pensamos y os digo" sin fecha):
- "¿Os parece si seguimos el [día concreto] con esta info ya decidida?"
- Si piden tiempo para decidir en familia/club: proponer tú la fecha del siguiente contacto, no dejar que quede abierto.

### 5.5. Propuesta escrita — enviar siempre después de la llamada, no solo "quedamos en hablarlo"

Idea adoptada de la revisión externa: cerrar una llamada sin dejar nada por escrito es la forma más fácil de perder un lead caliente. Usar la plantilla en [propuesta-template.md](propuesta-template.md) — un único documento reutilizable con campos variables (nombre, servicio, fechas, qué se ofrece, precio, siguiente paso), no una propuesta distinta por servicio.

### 6. Seguimiento si no cierra en la llamada

Cadencia de seguimiento (afinada 2026-07, más específica que "7-10 días"):
- **Día 2:** seguimiento corto tras enviar la propuesta, sin presionar — confirmar que la recibió bien.
- **Día 5-7:** si no hay respuesta, mensaje breve con una pieza nueva de valor (ej. un caso de éxito adicional), no repetir el pitch.
- **Día 10-14:** último seguimiento activo, directo — preguntar si sigue siendo el momento adecuado.
- **Día 20-40 (opcional, solo si el lead era de calidad real):** un check-in muy espaciado, sin presión — a veces se cierra meses después.
- Registrar en [pipeline.md](../01-clients/pipeline.md) siempre con fecha y motivo real de la objeción (no genérico).
- Si no hay respuesta tras el seguimiento del día 10-14, pasar a "en pausa" — no insistir más sin señal de interés real.

## Textos para WhatsApp Business (2026-07-16)

> Requiere número propio para Always Up, distinto del personal de Joel — pendiente de decidir (número nuevo o reutilizar uno existente sin uso personal).

**Mensaje de bienvenida (auto-respuesta al primer contacto):**
```
¡Hola! 👋 Gracias por escribir a Always Up.

Cuéntame rápido para poder ayudarte mejor:
- ¿Qué te interesa — una experiencia de tu equipo/club en España, una beca
  deportiva en EEUU, el programa internacional con la Real Sociedad, o algo
  distinto?
- ¿Qué edad tiene el jugador/a y en qué país estáis?

En cuanto lo sepa, te explico exactamente cómo podemos ayudarte 🙌
```

**Respuestas rápidas (`/atajo`), una por servicio:**

`/becas`
```
¡Genial! Así funciona el proceso de becas universitarias en EEUU:
nos encargamos de todo el proceso (perfil, contacto con universidades,
admisión). Para evaluar tu caso necesitamos:
1. Edad y año de graduación del jugador/a
2. Equipo/categoría en la que juega ahora (¿titular?)
3. Vídeo reciente jugando (últimos ~6 meses)
4. Situación académica (promedio/notas)
Cuéntame esos 4 y te digo si es realista y cuál es el siguiente paso.
```

`/colegio`
```
Para colegios privados en EEUU (boarding school) trabajamos con GEE,
especializados en encontrar el colegio y beca académica que mejor encaje.
¿Qué edad tiene y en qué curso está ahora mismo?
```

`/experience`
```
Team Experience: entrenamos con clubes profesionales españoles (Atlético
de Madrid, Real Sociedad, Sporting de Gijón) — entrenamientos, partidos,
instalaciones profesionales, todo incluido. Nuestro club de Irlanda llegó
a ganar su primera liga en la historia tras estas experiencias 🏆
¿Cuántos jugadores seríais y para qué fechas lo estáis pensando?
```

`/intlprogram`
```
El International Program es un programa residencial con la Real Sociedad
en San Sebastián — 1, 5 o 10 meses, entrenando con su metodología y
viviendo allí. Para evaluar el nivel necesitamos un vídeo del jugador/a.
¿Qué duración os interesa más?
```

`/pd`
```
Player Development es un programa de desarrollo individual que estamos
terminando de dar forma — te aviso en cuanto esté listo para arrancar.
Mientras tanto, cuéntame tu caso para tenerlo guardado y ser de los
primeros en saberlo.
```

`/llamada` (una vez cualificado, para pasar a videollamada)
```
Perfecto, con esto ya tengo lo que necesito. Te propongo que hablemos
por videollamada para contarte todo con detalle — [enlace de Calendly].
¿Te va bien esta semana?
```

## Qué se puede automatizar de verdad (pregunta de Joel, 2026-07)

**Sí, con una herramienta tipo ManyChat** (conectada a Instagram — Joel tiene que crear la cuenta, Claude no puede hacerlo en su nombre):
- Auto-responder el comentario del vídeo y mandar el primer DM automáticamente.
- Hacer las 2-3 preguntas de cualificación como mini-cuestionario dentro del chat.
- Mandar automáticamente el PDF/documento correcto según el servicio (tabla de la sección 3).
- Mandar el enlace de Calendly (con las preguntas de cualificación integradas) al final del flujo.

**No automatizar: la llamada de cierre en sí.** Con tickets de $2.500-$45.000 y de por medio menores de edad viajando a otro país, el cierre tiene que seguir siendo Joel en persona — es donde se genera la confianza real. Automatizar justo esa parte arriesgaría lo que más importa para ahorrar lo que menos cuesta.

**Orden recomendado para montarlo:** validar primero el flujo manual (DM + Calendly) durante 2-3 semanas reales, confirmar que cierra clientes, y solo entonces automatizar con ManyChat el tramo de cualificación + envío de documentos — automatizar un proceso que todavía no se sabe si funciona es automatizar el problema, no la solución.
