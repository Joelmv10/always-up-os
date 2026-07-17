# Roadmap maestro — AlwaysUp

> Reconcilia el plan original de 24 meses (creado en una sesión previa de Claude, pegado por Joel el 2026-07-10) con todo lo aprendido después en este repo. Este documento es la versión viva — actualizar el estado de cada tarea a medida que se avanza. Ver también [lineas-de-negocio.md](../00-company/lineas-de-negocio.md), [pipeline.md](../01-clients/pipeline.md), [procesos-actuales.md](procesos-actuales.md).

**Principio rector (del plan original, sigue vigente):** con 2 personas y objetivo de facturar x10 en 3 años, Claude Code tiene que multiplicar la capacidad de 2 personas, no añadirles trabajo. Cada tarea de este backlog se juzga por eso.

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
| WhatsApp Business + email corporativo unificado | 🔴 Abierto — sin empezar |

## Backlog priorizado (revisado 2026-07-16 — fusiona el backlog anterior con las 10 ideas propias de Joel)

**Criterio de reordenación:** arreglar fugas de conversión ya detectadas pesa más que generar más leads nuevos; SOP/modelo financiero son baratos y desbloquean decisiones; todo lo que no sea Team Experience o Becas espera a que esto esté estable.

| # | Tarea | Estado | Por qué este orden |
|---|---|---|---|
| 1 | **Embudo de ventas multi-servicio (no solo becas)** | ✅ Hecho, v2 (2026-07) — cualificación, ficha "qué mandar" + activos de autoridad, llamadas renombradas a diagnóstico, propuesta escrita (`propuesta-template.md`), cadencia de seguimiento afinada (día 2/5/10-14/20-40), Calendly con preguntas de cualificación configurable (Joel ya tiene cuenta) | Ya hay leads reales entrando y **0 cerrados** — es una fuga activa, más barata de arreglar que conseguir leads nuevos |
| — | **Decisión "Always Up Sales System" (revisión externa, 2026-07):** no se crea repo/estructura paralela — se adopta lo barato (nombres de llamada, propuesta escrita, referidos, revisión semanal, vídeos personalizados) directamente en este repo. Se aplaza email marketing, lead scoring y automatización (ManyChat/HubSpot/n8n) hasta validar el proceso manual. No se construye rama de embudo para Player Development (sin programa/precio definido) | Evitar sobre-ingeniería antes de validar con clientes reales |
| 2 | Modelo financiero vivo (proyección hacia +$200k 2027) | ✅ Hecho (`05-finance/modelo-financiero.md`) — **hallazgo clave: Renegades FC decide por sí solo si se llega a $200k**; sin él, el objetivo no se alcanza con lo que hay en marcha hoy | Sin esto no sabíamos cuántos cierres reales necesita cada línea |
| 3 | SOP Team Experience / Coach Experience | ✅ Hecho (`03-operations/sop-team-coach-experience.md`), incluye petición explícita de referidos | Necesario antes de delegar/contratar |
| 4 | Ejecutar outreach con la lista de clubes ya lista (Homefarm FC primero, con vídeo personalizado) | 🟢 Acción de Joel — plantilla, lista y ahora también la idea del vídeo de 20-30s ya listas | Necesario aunque cierre Renegades — el modelo muestra que sin 1-2 clientes nuevos más, tampoco se llega a $200k |
| 5 | Seguir ampliando/filtrando la lista de clubes objetivo, **con EEUU como prioridad geográfica** | 🟡 En progreso | Decisión 2026-07-16: no se eleva la línea 7 (consultoría EEUU) como track aparte, pero sí se prioriza geografía EEUU dentro de esta tarea |
| 6 | **International Program — cerrar % de comisión exacto con la Real Sociedad** | 🔴 Elevado de prioridad (2026-07-16) — el modelo financiero muestra que una sola colocación de temporada completa (45.000€) podría valer, en comisión, más que toda la meta de becas 2027 junta | Tarea más barata (una conversación) con más impacto potencial de todo el backlog |
| 7 | Resolver Renegades FC | 🔴 Máxima prioridad — decide el objetivo de 2027 | Seguimiento enviado, esperando respuesta |
| 8 | Perfil de LinkedIn (revisar/mejorar) | ⏸️ **Bloqueado hasta que Joel instale Claude in Chrome** — Joel ya tiene el perfil creado, pendiente de revisión conjunta. Campaña de conexión masiva sigue después del embudo validado | Joel decidió esperar a tener la extensión para trabajar sobre su sesión real |
| 9 | Checklist legal menores/GDPR/seguros | 🟡 Borrador hecho (incluye ahora el riesgo del visado F1 de Joel), falta abogado | Exposición activa, no depende de nada más |
| 10 | WhatsApp Business | ⏸️ **Pausado hasta el 05/08/2026** — Joel usará el número +1 814 329 1929 (necesita estar en EEUU para recibir el SMS de verificación). Textos de bienvenida y respuestas rápidas ya listos en `02-sales/embudo-ventas.md`. Email corporativo (@alwaysup.es) ya funciona, no requiere trabajo | Bloqueado por logística de Joel, no por trabajo pendiente |
| 11 | Campaña activa de LinkedIn (200-300 conexiones, 50 conversaciones) | ⏸️ Después de #1 y #6 | No generar más leads hasta que el embudo actual convierta |
| 12 | Perfeccionar presentaciones/web/documentos | ⏸️ **Conflicto con decisión previa de aparcar esto — mantener aparcado salvo que Joel lo eleve explícitamente.** Solo arreglos puntuales ya detectados (quitar "ESC Madrid", aclarar uso interno de Quality Servix) | Ya se decidió no priorizar — reabrir solo si Joel insiste |
| 13 | Auditoría de servicios/pricing | ✅ Ya cubierto en gran parte (`lineas-de-negocio.md`, `playbook-ventas.md`) | Confirmar con Joel si falta algún ángulo específico |
| 14 | CRM con leads y proceso de ventas | ✅ Ya hecho (`01-clients/pipeline.md`) | No reconstruir — usarlo |
| 15 | Documentación de contratación (primer perfil: ventas) | 🟢 Más adelante | No urge hasta tener SOPs/embudo estables |
| 16 | Estructura de sesiones/roles con Claude Code | ⏸️ La continuidad de memoria entre sesiones **ya funciona hoy** (repo + memoria persisten sin importar cuántas sesiones se abran) — lo que falta es diseñar roles específicos, y sigue siendo pronto para eso | Esperar a tener 2-3 semanas más de ritmo real antes de diseñar roles a ciegas |
| 17 | Always Up Player Development (línea 6) | ⏸️ Ritmo propio, ligado a Marca Personal | Sesión dedicada aparte — pendiente que Joel pase la conversación real |
| 18 | Marca personal / RRSS — plan y objetivos día a día | ⏸️ Sesión dedicada aparte (ya acordado antes) | No mezclar con estrategia general |

## Automatizaciones detectadas para más adelante (no urgentes hoy)

Del plan original, siguen siendo válidas cuando haya volumen suficiente para justificarlas: alertas de estacionalidad (verano/Semana Santa), dashboard de encuestas de satisfacción/testimonios, recordatorio automático de renovación a clubes que ya trabajaron con vosotros, plantilla estándar de contrato con clubes. No se construyen todavía — requieren datos/volumen que hoy no existen.

## Próximo paso inmediato (revisado 2026-07-16)

**#1 (embudo multi-servicio) ya está hecho.** Siguiente: **#2 (modelo financiero)** en paralelo con **#3 (SOP, ya en curso)**. Joel: ejecutar **#4** (outreach a Homefarm FC) en cuanto tengas un rato. El resto espera.
