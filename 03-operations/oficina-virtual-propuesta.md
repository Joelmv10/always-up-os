# La oficina virtual de Always Up en Claude Code: propuesta para la sesión con Joel

> Preparada por Claude el 17/11/2026 (tarea programada `preparar-sesion-oficina-virtual`). La sesión estaba prevista para el martes 17/11 de 10:00 a 12:00 (Nueva York), pero esta preparación se ejecutó tarde, a las 16:00 del mismo día, así que sirve para cuando la sesión se haga. **Nada de esto está creado todavía:** ni agentes nuevos ni skills. Se decide en la sesión.

## 0. Resumen en 5 frases
1. Esta semana el problema no fue que faltaran departamentos, sino que **la base falló**: los turnos automáticos no pudieron trabajar del 11 al 17/11 por permisos, no hay ni un informe diario y hubo un correo duplicado (Carrigaline) y otro que salió antes de hora (Colorado).
2. Lo que trajo resultados vino de la red cálida y los socios (Real Unión con 1.500 € por 12 días y permiso para nombrarle, el catálogo para Iñigo y Dani), no del correo frío (unos 21 primeros correos y 6 seguimientos con cero respuestas de interés).
3. Propuesta: **7 departamentos, pero solo 6 agentes** (los 5 de hoy más uno de finanzas y legal); operaciones de eventos se activa con la primera venta, y la dirección es el propio turno diario, no un agente.
4. Lo que más valor añade no son más agentes, son **8 skills propias** que convierten en procedimiento lo que ya hacemos a mano cada semana; de los plugins de Anthropic sirven unas 8 skills y el resto necesita un CRM que no tenemos.
5. Regla de oro: Claude prepara, comprueba y registra; **Joel aprueba en una ventana fija al día** y solo él (o Enrique) decide precios, envía textos nuevos y firma.

---

## 1. Qué ha funcionado y qué no esta semana (11 a 17/11)

**Lo que ha funcionado**
| Qué | Resultado | Lección para la oficina |
|---|---|---|
| Red de Enrique con el Real Unión | Producto de pruebas definido: 1.500 € por 12 días con alojamiento y comida, 500 € a quien lleva al jugador, se les puede nombrar. Ficha y plan de venta en `02-sales/ficha-prueba-real-union.md` | El departamento de becas y pruebas tiene por fin algo concreto que vender. Prioridad de enero |
| Catálogo 2027 para la reunión con Iñigo y Dani | 12 productos con lo sabido y lo que falta decidir (`00-company/catalogo-productos-2027.md`) | Buen ejemplo de entregable para Enrique: concreto, sin advertencias |
| LinkedIn | Aceptaron Christian Henry, Tyler Botte (NY Empire) y David Spruce (Bollington). Jordan Salamido contestó (no viajan hasta 2029) | LinkedIn da conversación; el correo frío no. Merece más peso |
| Respuesta de Seacoast United | "Viajamos solo con WorldStrides Sports". Se respondió proponiendo a WorldStrides como posible socio | Un "no" de un club puede abrir un socio. Esto lo debe recoger alianzas, no prospección |
| Sesiones con Joel delante | Guion de Richard Clarke, registro de mensajes, ficha del Real Unión, todo el mismo día | Cuando Joel está, la oficina rinde. El reto es que rinda cuando no está |

**Lo que no ha funcionado**
| Qué | Qué pasó | Arreglo propuesto |
|---|---|---|
| Turnos automáticos | Del 11 al 17/11 no pudieron trabajar por permisos. Cero informes en `03-operations/informes/` | Bloque 1 de la sesión: revisar permisos con una ejecución de prueba y que el turno avise si falla |
| Envíos programados en Apple Mail | Carrigaline salió dos veces (4:33 y 5:45) y además es un buzón no vigilado. Colorado salió a las 23:34 del día anterior. NJ14 no salió el 11/11 | Que envíe solo el script (`enviar_correos.py`) con sus comprobaciones, no la programación de Mail. Revisar el buzón antes de dar un club por bueno |
| Correo frío a clubes | Unos 27 envíos en total desde octubre, ninguna respuesta de interés | Mantenerlo como fondo, sin crecer, hasta revisar el 30/11 qué canal trae respuestas |
| Mensaje de LinkedIn a Bollington | El envío del 17/11 no cargó a la primera | Registrar siempre "enviado" solo cuando se ve el mensaje en la conversación |

**Conclusión:** antes de montar más departamentos hay que conseguir que el turno diario funcione 5 días seguidos sin Joel. Una oficina con 10 agentes sobre una base que falla solo multiplica los fallos.

---

## 2. Organigrama propuesto

```
                        JOEL (dirección real: aprueba, decide, envía lo nuevo)
                        ENRIQUE (relaciones con clubes y socios, firma, gastos grandes, legal)
                                         │
                  DIRECCIÓN DEL TURNO (Claude, sesión principal del turno diario)
                  reparte el trabajo, revisa lo que entregan los agentes, escribe el informe
                                         │
  ┌──────────────┬──────────────┬────────┴─────┬──────────────┬──────────────┬──────────────┐
Ventas y        Alianzas       Becas y        Marketing y    Análisis de    Finanzas y     Operaciones
prospección     y socios       pruebas        redes          mercado        legal (nuevo)  de eventos
prospeccion-    alianzas-      becas-y-       marketing-     analista-      finanzas-      (se activa con
clubes          socios         pruebas        redes          mercado        legal          la 1ª venta)
```

| Departamento | Qué hace | Frecuencia | Qué entrega |
|---|---|---|---|
| **Dirección del turno** | Lee el estado, mira bandeja y LinkedIn, decide qué agente trabaja hoy, revisa lo que entrega, guarda y escribe el informe | Lunes a sábado, 7:30 | Informe diario en `03-operations/informes/` con "lo que necesito que apruebes" listo para copiar |
| **Ventas y prospección** | Clubes, academias y universidades que pueden comprar Team, Coach o giras. Decisor y correo comprobados | Martes y jueves | Tanda nueva en el generador, validada. Tabla de leads en `01-clients/` |
| **Alianzas y socios** | SADE, Gonzalo Lamas, agentes, organizadores de torneos, Greystones y sus recomendaciones, y empresas como WorldStrides que ya tienen los clientes | Cuando un socio pide algo, y una revisión el lunes | Propuesta en 48 h desde que llega un dato. Mensaje corto para Enrique |
| **Becas y pruebas** | Cada lead de familia o jugador, prescriptores, y desde ahora la venta de las pruebas del Real Unión | Cada vez que Joel pega un mensaje, y los miércoles | Respuesta lista, próxima acción y fecha, apuntado en Segmento C |
| **Marketing y redes** | Plan de contenido, guiones de reels con los clips, textos, el caso de Puerto Rico desde el 7/1 | Viernes, y cuando haya material nuevo | Guiones segundo a segundo y textos listos para publicar |
| **Análisis de mercado** | Competencia, precios de referencia, torneos, ferias y convocatorias | Lunes y sábado | `08-knowledge-base/competencia.md` con 3 recomendaciones como máximo |
| **Finanzas y legal** (nuevo) | Precio de cada propuesta (coste / 0,65), cifras del viernes, modelo financiero, checklist de menores y seguros, borradores de condiciones | Viernes y cada vez que haya una propuesta | 5 líneas de números para Enrique; precio comprobado en cada propuesta; lista de lo que necesita abogado |
| **Operaciones de eventos** | Logística de cada experiencia vendida (SOP en `03-operations/sop-team-coach-experience.md`): fechas, proveedores, seguros, listas, consentimientos | **Solo cuando haya una venta** | Plan del evento y lista de comprobación |

**Por qué no crear más agentes ahora:** cada agente vuelve a leer el contexto desde cero, así que cuesta más y tarda más. Un agente solo merece la pena si tiene trabajo cada semana y reglas propias. Operaciones de eventos hoy no tiene trabajo. Un "agente de QA" o un "agente de dirección" tampoco: la revisión es el trabajo del turno y del validador.

---

## 3. Ficha de cada agente

### 3.1 Ventas y prospección (`prospeccion-clubes`, ya existe)
- **Puesto:** investigador de clubes y decisores.
- **Lo que sabe:** `estrategia-captacion-nov-2026.md`, `leads-donosti-cup.md`, el generador y su validador, la regla de 6 correos al día de martes a jueves.
- **Reglas:** no inventar ningún dato; correo comprobado en la web del club y dominio con MX; un saludo a una sola persona; comprobar que la persona sigue en el cargo; si el buzón es genérico o no vigilado, se marca. No envía.
- **Herramientas:** búsqueda web, navegador integrado, el generador, lectura del Excel.
- **Cómo mide si lo hace bien:** rebotes por debajo del 5 %; ningún saludo ni cargo equivocado; respuestas por cada 20 envíos (hoy 0, objetivo 1). Y como el cuello de botella es la capacidad de envío, no la lista, **no investiga clubes nuevos mientras haya más de 3 semanas de cola**.
- **Cambio propuesto:** que dé prioridad a la red cálida y a LinkedIn sobre el frío, y que pase a alianzas los "no" que mencionan a un intermediario (caso WorldStrides).

### 3.2 Alianzas y socios (`alianzas-socios`, ya existe)
- **Puesto:** prepara propuestas para quien ya tiene los clientes.
- **Lo que sabe:** precios de socios (`precio-showcase-sade.md`), catálogo 2027, reuniones con Enrique, las condiciones estándar (50/50, cancelación, exclusividad, aprobación de marca).
- **Reglas:** Enrique tiene la relación y firma; precios por escrito solo con la decisión de Joel o Enrique; nunca University Soccer; para Enrique solo lo nuevo y concreto.
- **Herramientas:** repo, búsqueda web, plantilla de propuesta.
- **Cómo mide:** propuesta entregada en menos de 48 h desde el dato; socios con conversación abierta (SADE, Gonzalo, WorldStrides); € propuestos y € cerrados por trimestre.

### 3.3 Becas y pruebas (`becas-y-pruebas`, ya existe)
- **Puesto:** responde a familias y jugadores y vende las pruebas.
- **Lo que sabe:** Segmento C del Excel, guiones (Pavel, Omar), guía de becas, precio estándar de becas (2.500 €), ficha del Real Unión.
- **Reglas:** nunca University Soccer, nunca "agencia", nunca prometer beca ni fichaje; precios los decide Joel; menores sin datos personales en el repo.
- **Herramientas:** repo, Excel en lectura; Instagram solo si Joel pega los mensajes o abre la bandeja en Chrome.
- **Cómo mide:** respuesta en menos de 12 h desde que Joel pega el mensaje; leads con próxima acción y fecha (100 %); llamadas conseguidas; jugadores de pruebas cerrados (objetivo: 3 para enero y febrero).
- **Cambio propuesto:** añadir la ficha del Real Unión a lo que lee antes de empezar.

### 3.4 Marketing y redes (`marketing-redes`, ya existe)
- **Puesto:** contenido de @Joel_alwaysup, Always Up y LinkedIn.
- **Lo que sabe:** plan del caso de Puerto Rico, la biblioteca de clips (iCloud, carpeta Joel Content), las reglas de imagen.
- **Reglas:** nada con menores sin consentimiento escrito; los padres revisan las piezas del jugador; sin escudos como respaldo; los profesionales y el partido nunca son protagonistas; tono humano. No publica.
- **Herramientas:** repo, lectura de la biblioteca de clips, búsqueda web para tendencias.
- **Cómo mide:** piezas listas por semana frente a las publicadas (si Joel no publica, el plan está mal dimensionado); seguidores (2.150 hacia 10.000); y lo que importa: mensajes de familias y clubes que llegan por redes.

### 3.5 Análisis de mercado (`analista-mercado`, ya existe)
- **Puesto:** competencia, precios y oportunidades.
- **Reglas:** solo datos con fuente y fecha; hechos separados de opinión; 3 recomendaciones como máximo.
- **Cómo mide:** cuántas de sus recomendaciones se convierten en una tarea con fecha. Si en 4 semanas ninguna, se baja a una vez cada dos semanas.
- **Propuesta:** reducirlo a **un día por semana** (sábado). El lunes lo usa alianzas.

### 3.6 Finanzas y legal (`finanzas-legal`, **nuevo, a decidir**)
- **Puesto:** controller ligero y guardián de lo legal.
- **Lo que sabe:** `05-finance/modelo-financiero.md`, la regla de precio (coste / 0,65, margen del 35 %), los mínimos (por ejemplo, pruebas no por debajo de 1.950 € sin hablarlo), `03-operations/checklist-legal-menores.md`, el límite del F-1 de Joel.
- **Reglas:** no da asesoría legal ni fiscal: dice qué tiene que ver un abogado o un gestor; nunca maneja datos bancarios; nada de gastos sin Joel.
- **Herramientas:** repo y Excel en lectura.
- **Cómo mide:** ninguna propuesta sale sin precio comprobado; el informe de los viernes sale cada viernes; la lista de "pendiente de abogado" baja.

### 3.7 Operaciones de eventos (**dormido hasta la primera venta**)
- Se crea el día que se cierre una experiencia o una prueba, a partir del SOP que ya existe. Hasta entonces no tiene trabajo.

---

## 4. Skills propias de Always Up

Una skill es un procedimiento que se repite, escrito una vez y usado igual siempre. Los agentes son "quién"; las skills son "cómo". Propongo 8, en orden de valor:

| # | Skill | Cuándo se usa | Qué hace | Quién la usa |
|---|---|---|---|---|
| 1 | **respuesta-club** | Un club o universidad contesta a un correo o a LinkedIn | Clasifica (interesado, no ahora, ya viajan con otro, derivación a otra persona, rebote o buzón muerto), deja el borrador en Mail, actualiza `registro.json` y, si hay intermediario, lo pasa a alianzas | Turno, prospección |
| 2 | **propuesta-club** | Un club pide información o precio | Propuesta con la ficha del servicio, fechas, precio (coste / 0,65) marcado "a confirmar por Joel" y siguiente paso. Objetivo: en 24 h | Prospección, alianzas, finanzas |
| 3 | **respuesta-lead-becas** | Joel pega un mensaje de Instagram o WhatsApp | Cualifica (edad, graduación, nivel, notas, inglés, presupuesto, quién decide), responde en su idioma, fija próxima acción y fecha y lo apunta en Segmento C | Becas y pruebas |
| 4 | **investigar-club** | Hace falta una tanda nueva | Web oficial, decisor, correo comprobado en la web con MX, cargo vigente, un dato real para el primer párrafo, LinkedIn; lo deja en el generador y pasa el validador | Prospección |
| 5 | **informe-semanal-enrique** | Viernes | 5 líneas con números sacados de `registro.json` y del Excel (enviados, respuestas, llamadas, propuestas, € cerrados) y solo lo nuevo | Finanzas, turno |
| 6 | **guion-reel** | Hay clips nuevos o toca pieza del plan | Elige clips de la biblioteca, guion segundo a segundo, texto en pantalla, descripción y llamada a la acción, y comprueba las reglas de imagen | Marketing |
| 7 | **preparar-llamada** | Hay una llamada con familia, club, socio o mentor | Guion como el de Pavel o Richard Clarke: objetivo, lo que sabemos, preguntas, objeciones, cierre y qué apuntar después | Todos |
| 8 | **cierre-de-turno** | Final del turno diario | Comprueba que todo lo enviado está registrado, que no hay duplicados, escribe el informe, hace commit y push | Turno |

Las 4 primeras se construirían primero porque cubren el camino del dinero: alguien responde, se le contesta bien y rápido, y se le hace una propuesta.

### Qué skills de los plugins de Anthropic sirven de verdad
Casi todas las skills de Sales dan por hecho un CRM conectado (HubSpot, Salesforce) y llamadas grabadas (Gong). Nosotros trabajamos con el Excel, `registro.json` y Apple Mail, y esos conectores no están autorizados. Por eso:

**Sirven (con nuestro repo como fuente):**
- `sales:account-research`: base para investigar un club o socio; hay que añadirle nuestra regla del correo comprobado.
- `sales:call-prep` y `sales:call-summary`: preparar una llamada y convertir las notas en correo de seguimiento y registro.
- `sales:handle-objection`: respuestas a "es caro", "ya viajamos con otra empresa" (caso Seacoast).
- `sales:create-an-asset`: one-pagers y presentaciones sin cifras inventadas; útil para la ficha del Real Unión.
- `sales:close-plan`: para un trato grande con socio (SADE, Gonzalo).
- `marketing:content-creation` / `marketing:draft-content` y `marketing:campaign-plan`: posts y la campaña del caso de Puerto Rico.
- `marketing:brand-review`: revisar un texto contra nuestras reglas (tono, promesas, menores) antes de que Joel lo envíe.
- `marketing:competitive-brief`: complemento del analista.

**No sirven hoy:** `pipeline-review`, `forecast`, `crm-hygiene-check`, `deal-signals`, `deal-review`, `deal-slip-scenario`, `renewal-radar`, `team-pipeline`, `rep-context`, `route-lead`, `update-opportunity`, `log-activity`, `expansion-whitespace` y `account-tiering` (todas necesitan CRM o un equipo de comerciales); `inbox-sweep` y `daily-briefing` (leen Gmail y nuestra bandeja es Apple Mail de alwaysup.es); `marketing:seo-audit` y `performance-report` (necesitan Ahrefs o datos de Instagram que no están conectados; tendrán sentido cuando se trabaje la web).

**Recomendación:** no instalar ni conectar nada nuevo en la sesión. Las 8 skills propias reutilizan lo bueno de las de los plugins y respetan nuestras reglas.

---

## 5. Cómo se coordina la oficina

**El turno diario es el director.** Cada mañana: lee el estado, mira la bandeja y LinkedIn, aplica `respuesta-club` a lo que haya llegado, encarga el trabajo del día al agente que toca, revisa lo que entrega y cierra con `cierre-de-turno`. Los agentes no se hablan entre ellos: se pasan el trabajo por archivos (`registro.json`, tablas de `01-clients/`, informes).

**Calendario semanal propuesto**
| Día | Departamento que trabaja | Entregable |
|---|---|---|
| Lunes | Alianzas | Estado de cada socio y propuestas pendientes |
| Martes | Prospección | Tanda nueva (solo si la cola baja de 3 semanas) o LinkedIn |
| Miércoles | Becas y pruebas | Seguimientos y venta de pruebas del Real Unión |
| Jueves | Prospección (universidades y Coach Experience) | Giras universitarias y entrenadores |
| Viernes | Finanzas y marketing | Informe para Enrique y guiones de la semana |
| Sábado | Análisis de mercado | Oportunidades y competencia |

**Qué se automatiza y qué pasa siempre por Joel**
| Lo hace Claude solo | Lo prepara Claude y lo aprueba Joel | Solo Joel o Enrique |
|---|---|---|
| Leer la bandeja y LinkedIn, investigar, registrar, regenerar el Excel cerrado, informes, commit y push | Cualquier texto nuevo a un cliente o socio, respuestas a quien acepta en LinkedIn, propuestas, publicaciones | Precios y descuentos, llamadas, reuniones en persona, firmas, gastos, temas legales |
| Enviar los correos del generador del día ya validados (máx. 6, martes a jueves) | Cambios en el plan de la semana | Relación con clubes anfitriones y socios (Enrique) |
| Conectar en LinkedIn de 5 a 8 personas sin nota | | |

**Propuesta para que Joel no sea el cuello de botella:** una sola ventana de aprobación al día de 15 minutos, a hora fija (por ejemplo a las 8:00, después del turno), desde el móvil, con todo lo que hay que aprobar en el informe y listo para copiar. Y respuestas tipo ya aprobadas para casos que se repiten ("no viajamos este año", "contactad con otra persona"), que Claude pueda enviar sin pedir OK cada vez.

---

## 6. Lo que hay que decidir en la sesión (6 preguntas)
1. **¿Arreglamos primero la base?** Es decir, permisos, Mac despierto y un turno de prueba que funcione delante de nosotros, antes de crear nada nuevo. (Recomendación: sí.)
2. **¿Creamos el agente de finanzas y legal ahora** y dejamos operaciones de eventos dormido hasta la primera venta? (Recomendación: sí a las dos.)
3. **¿Qué skills se construyen primero?** (Recomendación: `respuesta-club`, `propuesta-club`, `respuesta-lead-becas` e `investigar-club`.)
4. **¿Qué respuestas tipo puede enviar Claude sin tu OK?** Propuesta: la de "no este año" y la de "gracias, ¿con quién hablo?", siempre registradas en el informe.
5. **¿A qué hora es tu ventana diaria de aprobación** y desde dónde (móvil u ordenador)?
6. **¿Bajamos el correo frío a mantenimiento** y pasamos esas horas a LinkedIn, red cálida y la venta de las pruebas del Real Unión, hasta la revisión del 30/11?

## 7. Plan de la sesión (2 horas en bloques de 20 minutos)
| Bloque | Tema | Resultado |
|---|---|---|
| 1 (0:00 a 0:20) | Qué ha pasado esta semana (sección 1) y por qué falló el turno | Pregunta 1 decidida. Lanzamos el turno a mano y vemos dónde pide permiso |
| 2 (0:20 a 0:40) | Arreglar la base en directo: permisos de las sesiones, aviso si el turno falla, envío solo por script | El turno de mañana funciona sin Joel |
| 3 (0:40 a 1:00) | Organigrama y agentes (secciones 2 y 3) | Pregunta 2 decidida; cambios en los 5 agentes acordados |
| 4 (1:00 a 1:20) | Skills (sección 4) | Pregunta 3 decidida. Creamos la primera (`respuesta-club`) y la probamos con la respuesta real de Seacoast |
| 5 (1:20 a 1:40) | Coordinación y autonomía (sección 5) | Preguntas 4, 5 y 6 decididas; calendario semanal fijado |
| 6 (1:40 a 2:00) | Cerrar: actualizar `turno-diario-claude.md`, CLAUDE.md y la memoria; tareas con fecha | Todo documentado; lista de lo que queda para la semana |

## 8. Riesgos y límites reales
- **Coste y límites de uso.** Cada agente y cada sesión programada vuelve a leer el contexto, y eso consume el límite del plan. Más agentes no es más trabajo: puede ser menos si se agota el uso a mitad de semana. Por eso, pocos agentes y skills cortas.
- **Depende del Mac de Joel.** Las sesiones programadas solo funcionan con la app abierta, el Mac enchufado y sin reposo. Si el Mac se apaga, no hay oficina. (Una alternativa a valorar más adelante son las tareas programadas en la nube, pero no tienen acceso a Apple Mail ni a la sesión de LinkedIn.)
- **Calidad.** El riesgo grave es un dato inventado o un envío duplicado a un club. Se controla con el validador del generador, las comprobaciones de `enviar_correos.py` y la regla de parar y avisar si algo sale mal. Esta semana falló dos veces por la programación de Mail, no por el script.
- **LinkedIn.** Una cuenta que actúa de forma automática puede ser limitada. Por eso clic a clic, 5 a 8 al día y parar ante cualquier verificación.
- **Lo que Claude no puede hacer solo:** llamar, ir a ver un club, ganarse la confianza de un director en persona, firmar, decidir precios, entrar en Instagram o WhatsApp sin que Joel lo abra, ni sustituir a un abogado en lo de menores, seguros o el F-1.
- **Enrique.** Lo que le llegue de la oficina tiene que ser nuevo y concreto. Un informe genérico de los agentes daña la relación más de lo que ayuda.
- **La trampa de la oficina perfecta.** Montar departamentos se siente como avanzar, pero el objetivo es la primera venta propia. Si en la sesión algo no acerca una venta en las próximas 4 semanas, se aparca.
