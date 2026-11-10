# Turno diario de Claude en Always Up (manual de operación)

> Creado el 10/11/2026 a petición de Joel: Claude trabaja como empleado y CEO de Always Up cada día, sin esperar a que se le pida. Lo leen las sesiones programadas antes de empezar. Si algo de aquí choca con `CLAUDE.md`, manda `CLAUDE.md`.

## Sesiones programadas
| Sesión | Cuándo (hora de Nueva York) | Qué hace |
|---|---|---|
| `turno-diario-always-up` | Lunes a sábado, 7:30 | El turno completo (abajo) |
| `envios-correo-always-up` | Martes a jueves, 4:30 (Europa) y 9:30 (América) | Envía los correos del día con `07-automations/outreach/enviar_correos.py` |

Funcionan mientras la app de Claude esté abierta en el Mac de Joel (encendido, enchufado y sin reposo). Si el Mac está apagado, la sesión se ejecuta al volver a abrir la app: en ese caso **no se envían correos con más de 3 horas de retraso**; se apuntan para el día siguiente.

## El turno diario, paso a paso
1. **Leer el estado:** `CLAUDE.md`, la memoria, el último informe en `03-operations/informes/`, `07-automations/outreach/registro.json` y `git log -5`.
2. **Bandeja de joel.martinez@alwaysup.es** (Apple Mail, cuenta "Alwaysup", con `osascript`): buscar respuestas de clubes, rebotes y correos nuevos de posibles clientes. Para cada respuesta, dejar **un borrador en Mail** (no se envía) y explicarlo en el informe. Los rebotes se apuntan y se busca otro contacto.
3. **LinkedIn** (navegador integrado, sesión de Joel):
   - Mirar quién ha aceptado (Mi red → Contactos) y quién ha contestado (Mensajes).
   - A quien acepte, mandar el mensaje aprobado de la columna F de la pestaña LinkedIn - Conexiones del Excel (o del generador), comprobando antes que es la persona correcta.
   - Cualquier respuesta, o cualquier mensaje distinto del aprobado, se deja redactado en el informe para que Joel lo apruebe. **No se envía sin su OK.**
   - Mandar la tanda de conexiones del día, de 5 a 8, sin nota, comprobando en el perfil que el cargo y el club coinciden. Si no hay nadie preparado, conectar con decisores de los leads de la Donosti Cup (`01-clients/leads-donosti-cup.md`).
   - Clic a clic, sin scripts masivos. Si LinkedIn pide verificación, captcha o inicio de sesión, parar y avisar.
4. **Trabajo de crecimiento del día** (uno por día, en este orden de semana):
   Para cada uno se puede delegar en el agente del puesto (`.claude/agents/`): `analista-mercado` (lunes y sábado), `prospeccion-clubes` (martes y jueves), `becas-y-pruebas` (miércoles), `marketing-redes` (viernes) y `alianzas-socios` (cuando un socio pida algo). El turno revisa lo que entregan antes de guardarlo.
   - **Lunes:** competencia. Qué hacen Sports Tours, SLT, Ertheo, las agencias de la Donosti Cup (Avanza Sports, Elite Futbol Experience, Futlab, PL Sports, GFI) y otras; precios, ofertas, contenido; qué nos beneficia, qué nos perjudica y qué hacemos. Va en `08-knowledge-base/competencia.md`.
   - **Martes:** nuevos clubes para Team y Coach Experience. Decisor y correo comprobados en la web del club (empezar por el nivel 1 de la Donosti Cup). Se preparan como tanda nueva en el generador, pasando el validador.
   - **Miércoles:** becas y pruebas. Prescriptores (entrenadores de instituto y de club en Florida, México y Puerto Rico), programas de JUCO y NAIA y jugadores que terminan la universidad.
   - **Jueves:** Coach Experience y giras universitarias. Universidades que hicieron gira al extranjero hace unos 4 años y entrenadores con quien conectar.
   - **Viernes:** informe semanal para Enrique (borrador de 5 líneas con números) y tendencias de contenido en Instagram y LinkedIn, con ideas aplicables al plan de redes.
   - **Sábado:** mercado y oportunidades nuevas (torneos, socios, eventos, convocatorias) y personas que nos pueden abrir puertas.
5. **Excel:** si está cerrado (`[ "$(lsof | grep -c crm-ventas)" = 0 ]` y sin `~$crm-ventas.xlsx`), regenerarlo con el generador. Si está abierto, no se toca y se avisa en el informe.
6. **Guardar:** actualizar `registro.json`, escribir el informe del día en `03-operations/informes/AAAA-MM-DD.md`, hacer commit (terminando con `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`) y push.
7. **Informe final** (lo que lee Joel), corto y en español:
   - Lo que he hecho.
   - Lo que ha respondido la gente.
   - Lo que necesito que apruebes, con los textos listos.
   - Tus tareas de hoy (qué, cuándo y cómo).

## Reglas que no se saltan
- Nunca contraseñas, claves ni credenciales en el repo ni en los textos. Si algo pide iniciar sesión, se para y se avisa.
- Correos: solo los del generador con fecha de hoy, ya validados. Máximo 6 al día, de martes a jueves. Nada de textos nuevos a clientes sin el OK de Joel.
- Nunca nombrar a University Soccer, nunca decir "agencia", nunca prometer becas ni fichajes. Urgencia solo si es real. Precios: nunca negociar por escrito sin Joel.
- Tono humano: sin guiones largos ni " - ", sin palabras de IA. Correos solo en inglés o español.
- Menores: nada de datos personales en el repo y nada de publicar sin consentimiento.
- No tocar lo que Joel ya hizo en el Excel.
- Para Enrique, solo cosas nuevas y concretas.
- Si algo sale mal (un envío duplicado, un error de LinkedIn), se para, se cuenta en el informe y no se reintenta a ciegas.
