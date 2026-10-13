# Plan de outreach: 13 oct a 13 nov 2026

> Objetivo del mes: **primeras videollamadas de venta con clubes y primera venta real**. Los textos exactos están en la hoja `Outreach - Copiar y pegar` del CRM (`01-clients/crm-ventas.xlsx`), ordenada por fecha. Este documento explica el sistema; la hoja es lo que se usa cada día.
> Los textos se generan con `07-automations/outreach/generar_outreach.py` (ver `02-sales/outreach-textos-generados.md`). Para añadir un club: añadirlo en el script y volver a ejecutarlo.

## 1. Lo que hay que tener claro (honestidad primero)

- **Venta en octubre desde email en frío a clubes: improbable.** Un club necesita hablar con su comité, ver fechas y consultar a las familias. Lo realista es: respuestas y primeras llamadas en octubre-noviembre, cierre entre noviembre y enero (se reservan Semana Santa y verano 2027). Es una estimación mía basada en cómo compran los clubes amateur, no un dato medido; los primeros 30 envíos nos darán el dato real.
- **Si "primera venta en un mes" es innegociable, el camino más corto no son los clubes en frío:** son los leads que ya hablan con nosotros: Omar (becas), Daniel (MLS NEXT), el padre del béisbol, Leonardo Uren (Brasil, reactivación) y Deportivo. Clubes en frío = construir el pipeline de noviembre-enero; leads calientes = posible cierre este mes. Hay que hacer las dos cosas, pero conviene saber cuál es cuál.
- **El volumen manda.** Con 7 clubes no hay estadística. Para tener 1-2 clubes cerrados en el invierno hacen falta unos 40-60 clubes contactados con nombre y apellido. Ver sección 7.

## 2. Cadencia por club (se aplica igual a todos)

| Día | Acción | Canal |
|---|---|---|
| 0 | Email 1 (09:30 hora local, martes a jueves) | Email |
| 2 | Conectar con la persona con nota corta (solo si hay persona con nombre) | LinkedIn, a mano |
| 7 | Follow-up 1, en el mismo hilo, aporta un dato concreto (semana tipo) | Email |
| 14 | Follow-up 2, quita presión, ofrece salida elegante | Email |
| 15 | DM al club (opcional, solo si no hay respuesta) | Instagram/Facebook, a mano |
| 21 | Cierre: "asumo que no es el momento", puerta abierta | Email |
| 22+ | Pasar a "Retomar en 2027" en el CRM. No insistir más. | CRM |

**Por qué esta cadencia:** la mayoría de respuestas llegan a partir del 2.º o 3.er contacto, y a los comités de club (voluntarios, leen por la noche) les cuadra mejor una semana que tres días. Tres emails más el cierre es el máximo razonable; más se convierte en insistir.

**Dos cambios respecto a lo que había en el CRM:** (1) los follow-ups pasan de día 14 a **día 7 y 14** (antes solo había uno, el 27/10); (2) el email 1 incluye siempre una **pregunta de dos opciones** ("¿llamada corta o prefieres un resumen de una página?"), porque contestar "mándame el resumen" es mucho más fácil que aceptar una llamada con un desconocido, y esa respuesta ya cuenta como lead.

## 3. Calendario de las próximas dos semanas

| Fecha | Qué hacer |
|---|---|
| **Mar 13/10 (hoy)** | Programar para mañana el reenvío a Søreide y el email a Holbeach (hoja, filas del 14/10). Verificar el email de Whitehaven (ver sección 5). |
| **Mié 14/10** | Se envían Søreide (reenvío) y Holbeach. Tras 5 minutos, revisar bandeja por si hay rebote. |
| **Jue 15/10** | Se envían Whitehaven, Maidstone e IA Akranes. LinkedIn: conectar con Georgia Townsend (Hastings). |
| **Vie 16/10** | LinkedIn: conectar con Callum Lawe (Holbeach) y Marius Engen (Søreide). |
| **Lun 19/10** | LinkedIn: conectar con Luke Johnston (Whitehaven). |
| **Mar 20/10** | Follow-up 1 a Home Farm y Hastings. |
| **Mié 21/10** | Follow-up 1 a Søreide y Holbeach. |
| **Jue 22/10** | Follow-up 1 a Whitehaven, Maidstone y Akranes. |

Después sigue la hoja. Envía en horario laboral del destinatario: a ti te toca de madrugada en Nueva York, así que **escribe el correo la noche anterior y usa "Programar envío"** (en Outlook: flecha junto a Enviar, "Programar envío").

## 4. Control de calidad antes de pulsar enviar (obligatorio)

Cada fallo en un primer contacto es un lead perdido; el lunes lo vimos con Home Farm (saludo con tres nombres) y con Søreide (dirección que rebota).

1. **Para**: coincide con la hoja; el dominio es el del club.
2. **Saludo**: una persona o "Hi team"; nunca varios nombres separados por barras.
3. **Sin corchetes ni huecos** sin rellenar, nombre del club bien escrito.
4. **Firma** de texto plano al final. **Sin adjuntos.**
5. **Hora programada** = 09:30 locales del destinatario.
6. **5 minutos después de enviar**: abre la bandeja. Los rebotes llegan casi al instante (el de Søreide llegó en el mismo minuto). Si rebota: no lo des por perdido, busca otra dirección del club y repite.
7. **Marca la fila** como hecha, con la fecha real, y pasa el estado en el CRM.

El script comprueba por su cuenta placeholders, saludos múltiples y longitud (<150 palabras). Eso no sustituye los puntos 1, 5 y 6, que son humanos.

## 5. Lo que pasó con Søreide y los datos pendientes de verificar

- **Rebote de Søreide (13/10):** `ungdomsutvalget@soreideil.no` es un alias que reenvía a una cuenta (`@bergensskolen.com`) que ya no existe. El correo **no llegó**. Reenvío el 14/10 a `fotball@soreideil.no`, la dirección general de la sección de fútbol según la web del club, dirigido a Marius Engen (sportslig leder) y Gunn Eklund Breisnes (leder).
- **Whitehaven:** el email de Luke Johnston (presidente) lo he sacado de un buscador, no de la web del club. Antes de enviar, comprueba en whitehavenafc.com/contact que existe. Si no, usa la dirección que figure ahí. Es el presidente del club, no necesariamente quien lleva las chicas; el correo ya pide que te redirija.
- **Maidstone e IA Akranes:** solo tengo dirección general, así que el correo pide que te indiquen a la persona correcta. Este tipo de correo suele obtener más respuestas que uno dirigido a nadie, pero tienes que tratar la respuesta como "me han dado un nombre" y escribir un segundo correo al nombre.
- **Costa Daurada Cup:** los clubes ya fueron a Salou en 2026 (Semana Santa y 29/06-01/07). Aparecer en la lista confirma que estaban inscritos, no que fueran; por eso los textos nuevos dicen "listed for the Costa Daurada Cup".

## 6. Cuando contestan: qué hacer

| Respuesta | Qué haces | Plazo |
|---|---|---|
| "Sí, hablemos" | Proponer **dos horarios concretos** en su zona horaria (y el enlace de Calendly cuando esté listo). Confirmar y mandar invitación. | Menos de 4 horas en horario del club |
| "Mándame información" | Enviar `Always-Up-Team-Experience.pdf` + dos horarios para una llamada de 15 min. Un correo, no varios. | Menos de 4 horas |
| "¿Cuánto cuesta?" | "Depende de fechas y número de personas. Como referencia, desde unos $1.500 por jugador en el programa de 5 días. Con 15 minutos te doy una cifra exacta." Decide tú si quieres dar la referencia; yo recomiendo darla, porque esconderla genera desconfianza y mata el ritmo. | Mismo día |
| "No es el momento" | "Entendido. ¿Te escribo en enero para Semana Santa 2027 / verano?" Anotar fecha en el CRM. | Mismo día |
| "No soy la persona" | Pedir nombre y email, y escribir al nombre mencionando a quien te derivó. | Mismo día |
| Silencio | Seguir la cadencia. No cambiar nada. | Según hoja |

## 7. Guion de la videollamada de venta (20 min)

El objetivo no es "presentar Always Up" sino dejar la llamada con **una fecha de decisión**.

1. **Apertura (2 min):** agradecer, confirmar que tiene 20 minutos, decir el objetivo: "entender qué buscáis y ver si encaja".
2. **Descubrimiento (8 min):** cuántos jugadores y de qué edades, fechas posibles (Semana Santa, verano, otras), si han viajado antes y cómo les fue, quién decide, **cómo se financia** (familias, recaudación, club) y qué presupuesto por jugador manejan. Apunta las palabras exactas que usa.
3. **Propuesta (5 min):** describir la semana tipo con **sus** palabras: lo que dijo que buscaba, no el catálogo. Un caso: el club irlandés y el primer título de liga.
4. **Cierre (5 min):** "¿Qué necesitarías ver para decidir? Te mando la propuesta escrita en 48 horas; ¿hablamos el [fecha] para resolver dudas?" Salir con día y hora fijados. Si el cierre no es por precio, preguntar qué falta.

**Pendiente de tu decisión (dinero y legal, implica a Enrique):** política de **reserva de fechas**: qué se paga para confirmar (mi sugerencia: un anticipo, p. ej. 20-30 %, con condiciones de cancelación escritas), y qué dice el contrato sobre menores y seguros. Sin esto, la llamada termina en "lo pensamos" porque no hay nada concreto que firmar. No hace falta resolverlo hoy, sí antes de la primera llamada seria.

## 8. Cómo ganar volumen sin perder calidad

- **Cantera ya localizada:** Costa Daurada Cup (clubes del extranjero que ya viajan a España): Lower Ormond (Inglaterra), Morecambe Hawks, ES Manival, MBC FC, FC Porte d'Aquitaine (Francia), Team ALTI, JP Preparation, AEM, Virtu Academy. Excelsior Rotterdam es un club profesional con academia: prioridad baja. Fuente: costadauradacup.com (páginas de equipos confirmados).
- **Otras fuentes con el mismo perfil (club que ya viaja):** listas de participantes de otros torneos juveniles internacionales de España (Dream Cup, Barcelona y Madrid), y clubes juveniles de Irlanda/Reino Unido/Noruega/Países Bajos que publican sus giras en redes. Siempre clubes que **ya** viajan: venderles un cambio de destino es más fácil que convencer a un club que nunca ha viajado.
- **Ritmo:** 10 clubes nuevos por sesión, con **nombre del decisor y email verificado en la web del club**, antes de escribir. Dime "investiga 10 más" y los preparo con el mismo formato. Lo que no se puede verificar queda marcado.

## 9. Métricas semanales (ver hoja Hoy del CRM)

Enviados, respuestas, llamadas agendadas, llamadas hechas, propuestas, cierres. A partir de 30 emails enviados podemos comparar asuntos y CTA. Hasta entonces, no se cambia nada para "probar".
