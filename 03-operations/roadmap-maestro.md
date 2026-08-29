# Roadmap maestro — AlwaysUp

> Reconcilia el plan original de 24 meses (creado en una sesión previa de Claude, pegado por Joel el 2026-07-10) con todo lo aprendido después en este repo. Este documento es la versión viva — actualizar el estado de cada tarea a medida que se avanza. Ver también [lineas-de-negocio.md](../00-company/lineas-de-negocio.md), [pipeline.md](../01-clients/pipeline.md), [procesos-actuales.md](procesos-actuales.md).

**Principio rector (del plan original, sigue vigente):** con 2 personas y objetivo de facturar x10 en 3 años, Claude Code tiene que multiplicar la capacidad de 2 personas, no añadirles trabajo. Cada tarea de este backlog se juzga por eso.

## Objetivos vigentes (retomado tras vacaciones, agosto 2026)

- **$200.000 facturados en Always Up en 2027** — en riesgo real tras perder Renegades FC, ver [modelo-financiero.md](../05-finance/modelo-financiero.md). Necesita más volumen de prospectos, no un solo cliente grande.
- **Instagram: 10.000 seguidores antes de fin de 2026** (hito intermedio), **20.000 a finales de 2027** (meta final, sin cambios).
- **Primera venta real de Always Up en 1 mes** — objetivo con fecha, es el que más debe condicionar el trabajo de las próximas semanas. Ver plan más abajo.
- Contexto personal de Joel (nueva vida en NY, nueva universidad, búsqueda de trabajo) — de fondo, no se gestiona como tarea de Always Up salvo que Joel pida ayuda activa en algo concreto. Recordatorio: el estatus F1 sigue limitando qué tipo de trabajo puede aceptar en EEUU (ver `03-operations/checklist-legal-menores.md` sección 7).

## Plan de 30 días — primera venta real

Semana 1: contactar activamente a los candidatos ya identificados en [pipeline.md](../01-clients/pipeline.md) (Homefarm FC primero) + reanudar contenido de Instagram para generar inbound. Semana 2-3: llevar a llamada cualquier señal real (usar [manual-embudo-ventas.md](../02-sales/manual-embudo-ventas.md)), seguir ampliando la lista en paralelo. Semana 4: cerrar lo que esté más avanzado — no hace falta que sea un cliente grande, el objetivo es validar que el embudo cierra al menos una venta real. Revisar cada domingo con el ritual de métricas ya establecido en [pipeline.md](../01-clients/pipeline.md).

## Cambios de foco desde el plan original

- **Web/presentaciones nuevas (Fase 1 del plan original): aparcado.** Joel decidió explícitamente no priorizar esto ahora — seguir avanzando en captación antes de perfeccionar web/presentaciones.
- **CRM: versión ligera en el propio repo, no Airtable.** Claude Code no puede crear cuentas en herramientas externas en nombre de Joel — construido ahora en `01-clients/pipeline.md`. Migrar a Airtable u otra herramienta si el volumen lo justifica y Joel crea la cuenta.
- **Foco operativo real en 2 líneas** (Team & Coach Experience, Becas) — las otras 5 avanzan sin track de desarrollo propio, montadas sobre el trabajo ya planeado (detalle en [lineas-de-negocio.md](../00-company/lineas-de-negocio.md)).
- **El objetivo #1 de captación ya tiene 2 prospectos activos** (Renegades FC, Greystones — ver [pipeline.md](../01-clients/pipeline.md)), no se parte de cero como asumía el plan original.

## Estado de la Fase 0 (Fundación)

| Tarea | Estado |
|---|---|
| Repo `always-up-os` + `CLAUDE.md` | ✅ Hecho |
| Checklist legal menores/GDPR/seguros | 🔴 Abierto — pendiente, prioridad alta (exposición real con menores 8-20 años) |
| CRM mínimo viable | ✅ Versión ligera hecha (`01-clients/pipeline.md`) |
| Migrar conocimiento disperso a la KB | 🟡 En progreso — historia, líneas de negocio, auditoría de marca y procesos ya documentados; falta seguir volcando lo que surja |
| WhatsApp Business + email corporativo unificado | ✅ Instalado (2026-08) — email ya funcionaba. Textos de bienvenida/respuestas rápidas **aplazados a propósito** (decisión de Joel: sin contactos todavía no tiene sentido automatizarlo, se hace cuando haya volumen real) |

## Backlog priorizado (revisado 2026-07-16 — fusiona el backlog anterior con las 10 ideas propias de Joel)

**Criterio de reordenación:** arreglar fugas de conversión ya detectadas pesa más que generar más leads nuevos; SOP/modelo financiero son baratos y desbloquean decisiones; todo lo que no sea Team Experience o Becas espera a que esto esté estable.

| # | Tarea | Estado | Por qué este orden |
|---|---|---|---|
| 1 | **Embudo de ventas multi-servicio (no solo becas)** | ✅ **100% completo (2026-08)** — ver [`02-sales/manual-embudo-ventas.md`](../02-sales/manual-embudo-ventas.md). Calendly ("Always Up - Assessment Call") ya creado por Joel con preguntas de cualificación completas (servicio, rol de quien reserva, país, para quién es, situación/objetivo, material a revisar antes de la llamada) — mejor incluso que lo planteado originalmente. Solo falta que Joel añada sus horarios de disponibilidad cuando los tenga claros | Ya hay leads reales entrando — el embudo está listo de principio a fin |
| 1b | **Plan de ventas maestro** (auditoría de servicios, análisis de competencia, segmentación de mercado, estrategia por canal con datos reales de 2026) | ✅ Hecho (2026-08-29) — ver [`02-sales/plan-ventas-maestro.md`](../02-sales/plan-ventas-maestro.md). Incluye preguntas de cualificación Instagram (sección 5) y plantilla recortada (sección 6) | Joel pidió tratar septiembre "en serio, como un trabajo" — con plan, no acciones aisladas |
| 1c | **CRM operativo en Excel** (`01-clients/crm-ventas.xlsx`) — 6 pestañas: Hoy (panel diario con fórmulas), Segmento A Clubes, Segmento B América, Segmento C Becas, LinkedIn plan diario, Oportunidades | ✅ Hecho (2026-08-29) — sustituye las tablas de leads que antes vivían en `pipeline.md`. Homefarm FC y Søreide IL ya tienen email real redactado y listo para enviar | Joel pidió un sistema diario filtrable, con emails ya redactados por candidato — Markdown no lo permitía bien |
| — | **Decisión "Always Up Sales System" (revisión externa, 2026-07):** no se crea repo/estructura paralela — se adopta lo barato (nombres de llamada, propuesta escrita, referidos, revisión semanal, vídeos personalizados) directamente en este repo. Se aplaza email marketing, lead scoring y automatización (ManyChat/HubSpot/n8n) hasta validar el proceso manual. No se construye rama de embudo para Player Development (sin programa/precio definido) | Evitar sobre-ingeniería antes de validar con clientes reales |
| 2 | Modelo financiero vivo (proyección hacia +$200k 2027) | ✅ Hecho (`05-finance/modelo-financiero.md`) — **hallazgo clave: Renegades FC decide por sí solo si se llega a $200k**; sin él, el objetivo no se alcanza con lo que hay en marcha hoy | Sin esto no sabíamos cuántos cierres reales necesita cada línea |
| 3 | SOP Team Experience / Coach Experience | ✅ Hecho (`03-operations/sop-team-coach-experience.md`), incluye petición explícita de referidos | Necesario antes de delegar/contratar |
| 4 | **Ejecutar outreach real, empezando hoy** (Homefarm FC primero, con vídeo personalizado y el gancho de España campeona del mundo) | 🔴 **Máxima prioridad ahora** — acción de Joel | Con Renegades perdido, ya no hay margen para seguir posponiendo el primer contacto real |
| 5 | **Ampliar la lista de clubes objetivo a más volumen** (no solo 1-2 candidatos), con EEUU como prioridad geográfica | 🔴 Elevado (agosto 2026) — el hueco financiero dejado por Renegades requiere 3-4 clientes nuevos, no 1-2 | Sin más volumen en el embudo, el objetivo de $200k no es alcanzable con la tasa de conversión esperable |
| 6 | International Program — cerrar % de comisión con la Real Sociedad | 🟢 Bajado de prioridad — decisión de Joel: no mueve el cuello de botella actual (conversaciones/llamadas). Queda como palanca de reserva si el hueco financiero sigue abierto en unos meses | Ver [modelo-financiero.md](../05-finance/modelo-financiero.md) |
| 7 | ~~Resolver Renegades FC~~ | ✅ **Cerrado — perdido** (agosto 2026). Puerta abierta a futuro sin fecha fija. Ver [renegades-fc.md](../01-clients/leads/renegades-fc.md) | Joel gestionó bien el cierre, no cedió en precio |
| 8 | Perfil de LinkedIn (revisar/mejorar) | ⏸️ **Bloqueado hasta que Joel instale Claude in Chrome** — Joel ya tiene el perfil creado, pendiente de revisión conjunta. Campaña de conexión masiva sigue después del embudo validado | Joel decidió esperar a tener la extensión para trabajar sobre su sesión real |
| 9 | Checklist legal menores/GDPR/seguros | 🟡 Borrador hecho (incluye ahora el riesgo del visado F1 de Joel), falta abogado | Exposición activa, no depende de nada más |
| 10 | WhatsApp Business | ✅ **Instalado (2026-08)** con el +1 814 329 1929 — falta pegar los textos de bienvenida/respuestas rápidas de `02-sales/embudo-ventas.md` dentro de la app | Email corporativo (@alwaysup.es) ya funcionaba, no requería trabajo |
| 11 | Campaña activa de LinkedIn (200-300 conexiones, 50 conversaciones) | ⏸️ Después de #1 y #6 | No generar más leads hasta que el embudo actual convierta |
| 12 | Perfeccionar presentaciones/web/documentos | ⏸️ **Conflicto con decisión previa de aparcar esto — mantener aparcado salvo que Joel lo eleve explícitamente.** Solo arreglos puntuales ya detectados (quitar "ESC Madrid", aclarar uso interno de Quality Servix) | Ya se decidió no priorizar — reabrir solo si Joel insiste |
| 13 | Auditoría de servicios/pricing | ✅ Ya cubierto en gran parte (`lineas-de-negocio.md`, `playbook-ventas.md`) | Confirmar con Joel si falta algún ángulo específico |
| 14 | CRM con leads y proceso de ventas | ✅ Ya hecho (`01-clients/pipeline.md`) | No reconstruir — usarlo |
| 15 | Documentación de contratación (primer perfil: ventas) | 🟢 Más adelante | No urge hasta tener SOPs/embudo estables |
| 16 | Estructura de sesiones/roles con Claude Code | ⏸️ La continuidad de memoria entre sesiones **ya funciona hoy** (repo + memoria persisten sin importar cuántas sesiones se abran) — lo que falta es diseñar roles específicos, y sigue siendo pronto para eso | Esperar a tener 2-3 semanas más de ritmo real antes de diseñar roles a ciegas |
| 17 | Always Up Player Development (línea 6) | ⏸️ Ritmo propio, ligado a Marca Personal | Sesión dedicada aparte — pendiente que Joel pase la conversación real |
| 18 | Marca personal / RRSS — plan y objetivos día a día | ⏸️ Sesión dedicada aparte (ya acordado antes) | No mezclar con estrategia general |

## Giro de construir a vender — sigue vigente, ahora con más urgencia (retomado agosto 2026)

Después de varias sesiones construyendo (marca, web, presentaciones, CRM, embudo), la pregunta que filtra cada hora sigue siendo: **¿esto aumenta la probabilidad de cerrar un cliente?** El embudo y los materiales ya son suficientes para vender — no se sigue "completando" documentación de venta salvo que un cliente real revele un hueco concreto. Con Renegades perdido, esto ya no es una preferencia, es la única vía real hacia el objetivo de 2027.

**Las 3 cosas reales ahora, en orden:**
1. **Enviar el primer outreach real hoy** — Homefarm FC y los siguientes candidatos, con el gancho de España campeona del mundo. Acción de Joel.
2. **Ampliar la lista de clubes objetivo a más volumen** (3-4 candidatos serios, no 1-2) — el hueco financiero de Renegades lo exige.
3. **Reunir el material de autoridad que ya existe** (fotos/pocos vídeos) — tarea rápida, no bloquea el punto 1.

**Explícitamente no es prioridad esta semana:** LinkedIn (bloqueado hasta Claude in Chrome), comisión del International Program (no mueve el cuello de botella actual, según Joel), ampliar más la documentación del embudo salvo que un cliente real lo exija.

## Automatizaciones detectadas para más adelante (no urgentes hoy)

Del plan original, siguen siendo válidas cuando haya volumen suficiente para justificarlas: alertas de estacionalidad (verano/Semana Santa), dashboard de encuestas de satisfacción/testimonios, recordatorio automático de renovación a clubes que ya trabajaron con vosotros, plantilla estándar de contrato con clubes. No se construyen todavía — requieren datos/volumen que hoy no existen.

## Próximo paso inmediato (revisado 2026-07-16)

**#1 (embudo multi-servicio) ya está hecho.** Siguiente: **#2 (modelo financiero)** en paralelo con **#3 (SOP, ya en curso)**. Joel: ejecutar **#4** (outreach a Homefarm FC) en cuanto tengas un rato. El resto espera.
