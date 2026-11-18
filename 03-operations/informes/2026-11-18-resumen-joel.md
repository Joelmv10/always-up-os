# Resumen del 18/11/2026: todo lo decidido y hecho con Joel

> Para no tener que volver al chat. Cada punto dice qué pasó, qué se ha hecho y qué queda.

## 1. Sesiones automáticas

### Qué falló hoy
| Sesión | Qué pasó |
|---|---|
| Envíos 4:30 (Europa) | Parada esperando un permiso (un comando con `$( )`). No envió los follow-ups de Ballymun, Porte d'Aquitaine, Hastings y Holbeach. |
| Turno 7:30 | Revisó la bandeja: solo había una aceptación de LinkedIn (Marcos Landivar). Vio que Richard Clarke confirmaba la llamada. Se paró por un comando con un bucle `for`. Sin conexiones de LinkedIn, sin informe y sin Excel. |
| Envíos 9:30 (América) | Funcionó. Follow-ups a Cedar Stars y Colorado Rapids, sin rebotes. Se quedó un rato en el commit (mensaje de varias líneas), pero acabó guardándolo. |

**Causa:** un comando que pide permiso deja la sesión parada horas porque nadie está delante para aprobarlo.

### Qué se ha arreglado
- Las órdenes de las dos tareas ahora dan los comandos exactos. Quedan prohibidos `$( )`, los bucles, las tuberías, `sleep` y los commits de varias líneas.
- Nuevo `07-automations/outreach/revisar_rebotes.py`, para revisar los rebotes con un solo comando.
- `generar_outreach.py --si-cerrado` comprueba él solo si el Excel está abierto.
- Se han permitido comandos de solo lectura (`git log`, `git status`, `git diff`, `date`).
- **Los correos salen de lunes a viernes (antes, de martes a jueves), con un máximo de 6 al día.** La tarea de envíos pasa a las 4:30 y 9:30, de lunes a viernes.
- Los 4 follow-ups que no salieron van el jueves 19/11 a las 4:30. El resto del calendario se ha reajustado sin pasar de 6 al día.
- **El turno prepara prospectos nuevos cada día laborable.** Cuando quedan menos de 10 días de primeros correos, añade 3 prospectos nuevos (prioridad: universidades de EEUU y entrenadores). Con 6 correos al día, los clubes en cola se gastan para el 10/12.
- **Prueba real:** el turno se ha relanzado hoy a mano (sobre las 12:45) para que haga las conexiones de LinkedIn de hoy. El resultado está en la sección 7.
- **Comprobación automática el jueves 19/11 a las 10:15** (tarea `verificar-turnos-19-11`).

### Lo que tiene que pasar cada día
- **Correos:** de lunes a viernes, hasta 6 (4:30 Europa, 9:30 América). Solo los que prepara el generador.
- **LinkedIn:** de lunes a sábado. De 5 a 8 conexiones sin nota, el mensaje aprobado a quien acepta y las respuestas redactadas para Joel.
- **Bandeja:** borradores de respuesta en Mail para Joel.
- **Excel e informe** del día en `03-operations/informes/`.

## 2. Richard Clarke
- **La llamada se perdió:** confirmó a las 6:03 la llamada de las 12:30 y no le mandamos el enlace.
- **12:40, enviado por LinkedIn (con el OK de Joel):** "Hi Rich, I'm really sorry, I missed sending you the invite for today and I know your time is valuable. Could we do next Tuesday (24th) or Wednesday (25th) at 12:30 ET instead? I'll send the link as soon as you confirm. Apologies again. Joel"
- **Cuando conteste:** invitación de Zoom, Teams o Google Meet a rich@mrrichardclarke.com, con copia a Joel. En este Mac no hay Zoom ni Teams y el navegador integrado no tiene Google iniciado. O la crea Joel (Google Meet desde su Gmail, 10 segundos), o Joel inicia sesión en Google en el navegador integrado y la crea Claude.
- **Guion y para qué hablamos:** `04-marketing/llamada-rich-clarke.md`. Es una llamada de consejo sobre contenido y marca, no de venta.

## 3. Adjuntos en blanco (correo a David Spruce)
- **Qué se quería mandar:** el deck de empresa (14 páginas) y la ficha de Team Experience (2 páginas).
- **Qué se ha hecho:**
  - Los PDF se han recomprimido. Antes Apple Mail los mandaba codificados como texto y Gmail podía enseñarlos en blanco.
  - Los generadores están corregidos.
  - Hay una regla nueva en el manual del turno: comprobar cada PDF antes de enviarlo y revisarlo en Enviados después.
- **Prueba 3 (17/11):** lleva solo 2 PDF. Mail mete entre ellos dos trozos de HTML vacíos, que Gmail enseña como dos adjuntos más sin nombre y en blanco. Por eso Joel vio 4 adjuntos y 2 vacíos.
- **Pendiente de Joel:**
  1. Decir si se abren los dos que se llaman "Always-Up-Company-Deck.pdf" y "Always-Up-Team-Experience.pdf".
  2. Dar el OK para una prueba 4 en formato de texto sin estilo, que quitaría los trozos vacíos.
  3. Dar el OK para reenviar a David los PDF en su hilo, con este texto: "Hi David, I noticed the two PDFs in my last email may show up blank on some email apps, so here they are again: our company presentation and the Team Experience overview. Let me know if they open fine on your side. Best, Joel"

## 4. Cursos UEFA: cómo lo hace WARUBI
- **No se salta el viaje.** La licencia la da la federación de Turingia (TFV), una federación regional de la DFB, en inglés.
- **El curso online no es la licencia.** Cuesta 495 $, es una preparación y, según su propia web, no equivale a la UEFA C ni garantiza plaza.
- **La licencia se saca en Alemania:** unas dos semanas presenciales en Bad Blankenburg. Desde 2027, una semana de UEFA C y otra de UEFA B, con hotel y comidas incluidos y el vuelo aparte.
- **Oportunidad:** que una federación territorial española haga lo mismo en inglés. Pregunta para los contactos de Enrique. La dificultad es que en España es enseñanza oficial y se imparte en español.
- **Mientras tanto, Gibraltar,** que permite hacer el curso y la semana en el club en un solo viaje. Gales es el plan B. Plazos: Gibraltar, 30/11; Gales, 5/12. Falta el OK de Joel para escribirles.
- **Fuentes:** [WARUBI, curso UEFA B y C](https://coach.warubi-sports.com/about-the-course) y [WARUBI, curso online de la TFV](https://coach.warubi-sports.com/courses/german-coaching-prep-course).

## 5. Documentos para Enrique (versión del 18/11)
- **Documento 1:** `00-company/entregables/Always Up 2027 · Catalogo de productos` (PDF de 25 páginas y Word). La fuente es `00-company/catalogo-productos-2027.md`.
- **Documento 2:** `00-company/entregables/Always Up 2027 · Manual de producto y venta` (PDF y Word). Marcado como documento de trabajo de Joel; solo se han tocado los precios de los extras.

### Precios que cambian con la tarifa del Atlético
La tarifa está en `08-knowledge-base/tarifas-atletico-2027.md`.

| Producto | Antes | Ahora |
|---|---|---|
| Team Experience, Madrid Week | Desde 1.950 € (7 días) | **Desde 2.600 € (7 días) y desde 1.950 € (5 días).** El Atlético cobra 1.600 € la semana con residencia. Falta pedirle el precio de 5 días. |
| Methodology Week (entrenadores) | 2.600 € | **3.600 €.** El Atlético cobra 250 € (5 o más) o 300 € por día, **solo el programa**. Confirmar con Enrique: Joel lo tenía como "todo incluido". |
| Short Week (3 días, nueva) | No existía | Desde 2.400 € |
| UEFA C Pathway + Spain | Unos 3.800 € en total | Unos 3.550 € (3 días) o 4.750 € (semana), con Gibraltar |
| Madrid + San Sebastián | 3.400 € | 3.900 € |
| College Preseason | 3.500 $ | Desde 3.900 $ (unos 4.300 $ con el Atlético) |
| Campus fuera de España | Unos 15.500 € | **Unos 20.800 €, unos 300 € por niño.** El kit Nike es obligatorio, a 49 € por niño. A SADE le propusimos unos 110 €. |
| Vacaciones en familia | Desde 450 € | Con el Atlético no salen (1.250 € por entrenamiento y grupo). Hay que hacerlas con otros clubes. |

### Feedback de Joel aplicado
- **Prioridad número 1 de 2027:** cerrar una Team Experience y una Coach Experience. Está en el punto 1 y en CLAUDE.md.
- **Paquetes listos para contratar, más extras con precio.** Así se responde a la duda de Enrique ("cerrados y modificables no casan").
- **Tarifas:** de todos los clubes y para todos los servicios, incluidas las categorías a las que podemos mandar jugadores (anexo C).
- **Anexo A:** ahora se indica que empieza en la página 16.
- **Orientación de carrera** (6.c), antes y después de la universidad: evaluación por 150 €, que se descuenta del programa. El límite legal es que orientamos, pero no ofrecemos jugadores a clubes; eso es trabajo de agente.
- **Cobro legal de las "pruebas":** cinco reglas en el apartado 6, para que las valide el abogado.
- **Mapa de clubes con acceso,** no solo un segundo club cerca del Real Unión.
- **International Program:** paquete cerrado, cuándo se vende, si es individual o en grupo, comisión y material.
- **Nueva tabla en el apartado 12:** qué falta para vender cada producto el 1 de enero.

### Mensaje para Enrique (Joel lo manda con los dos documentos)
> Te paso los dos documentos. El 1 es para la reunión: todos los productos con lo que tenemos y lo que falta para venderlos desde enero, y ya lleva las tarifas del Atlético que me pasaste (he ajustado la Team Experience a 5 días). El 2 es un manual mío de cómo vender, por si quieres verlo. Lo de los paquetes: me refiero a una propuesta estándar de cada producto que el cliente pueda contratar tal cual, con programa, precio y condiciones. Si quiere algo distinto, se le suman extras que ya tienen precio. Está en el punto 1 y las fichas en el anexo A. Lo más importante de la reunión es que cada club nos dé su tarifa 2027 para todo, como ha hecho el Atlético (anexo C). Ojo: en Coach Experience, el Atlético cobra solo el programa, sin hotel ni comidas. ¿Es así?

## 6. Pendientes
| Quién | Qué | Cuándo |
|---|---|---|
| Joel | Mandar los documentos y el mensaje a Enrique | Hoy |
| Joel | Decir si se abren los PDF de la prueba 3 y dar el OK para la prueba 4 y el reenvío a David | Hoy |
| Joel | Crear el enlace de la llamada con Richard cuando confirme | Cuando conteste |
| Joel | OK para escribir a Gibraltar y a Gales | Esta semana (Gibraltar cierra el 30/11) |
| Enrique | Precio de 5 días del Atlético; confirmar que Coach Experience es solo el programa; hojas de tarifas de los demás clubes | Antes de la reunión (26/11 a 3/12) |
| Claude | Comprobar las sesiones del 19/11 y avisar | 19/11, 10:15 |
