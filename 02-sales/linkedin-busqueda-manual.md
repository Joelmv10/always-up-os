# LinkedIn: cómo encontrar más decisores sin poner en riesgo la cuenta

> Creado el 27/10/2026. LinkedIn es nuestro único canal con acceso directo a decisores, y la cuenta de Joel es el activo. Las condiciones de LinkedIn prohíben el rastreo y la automatización, y los límites (restricciones temporales o baja de la cuenta) se aplican sin aviso. Por eso la búsqueda la hace Joel a mano y la estructura Claude.

## Por qué no usar la extensión de Chrome para rastrear cientos de perfiles
- Un recorrido automático de perfiles es justo lo que detecta LinkedIn. Una restricción en la cuenta nos dejaría sin canal en pleno arranque.
- Además, a nosotros no nos hacen falta cientos: nos hace falta **acertar con los decisores**. 5 a 8 conexiones bien elegidas a la semana (con email ya enviado) rinden más que 200 al azar.
- Claude no puede entrar en LinkedIn desde este equipo (está bloqueado). Lo que sí hace bien es estructurar y puntuar lo que Joel pega.

## El método (10 minutos al día, a mano)
1. **Buscas tú** en LinkedIn con las recetas de abajo. Filtros: **Personas**, ubicación del país objetivo y, mejor, **conexiones de 2º grado** (aceptan más).
2. **Copias el texto visible** de los resultados (nombre, cargo, club, enlace) y lo pegas aquí en el chat. Vale pegar de 10 a 30 resultados de una vez.
3. **Claude** los limpia, descarta los que no encajan, los puntúa, prepara la nota de conexión de cada uno (máx. 300 caracteres, sin guiones largos), busca su email en la web del club y los añade a la hoja `LinkedIn - Conexiones` y al CRM.
4. **Tú conectas** 4 a 8 a la semana, dos días después del email, copiando la nota.

## Recetas de búsqueda (copiar en el buscador de LinkedIn)
**Clubes juveniles de EEUU (MLS NEXT, ECNL, Girls Academy):**
`("Director of Coaching" OR "Academy Director" OR "Technical Director") AND (soccer OR football) AND (youth OR academy OR "MLS NEXT" OR ECNL)`

**Clubes y academias de Reino Unido e Irlanda:**
`("Head of Academy" OR "Academy Director" OR "Head of Youth" OR "Club Secretary" OR "Chairman") AND (football OR soccer) AND (youth OR girls OR academy)`

**Entrenadores universitarios (D2, D3, NAIA, a partir de mediados de noviembre):**
`("Head Coach" OR "Head Women's Soccer Coach" OR "Head Men's Soccer Coach") AND soccer AND (university OR college)`

**Países nórdicos y Países Bajos:** `("Sportslig leder" OR "Sportdirektör" OR "Hoofd jeugdopleiding" OR "Head of Youth") AND (fotball OR fotboll OR voetbal)`

**Posibles partners (academias en el extranjero con volumen):** `("Academy Director" OR "Founder") AND ("football academy" OR "soccer academy") AND (international OR showcase OR "Puerto Rico" OR Brazil)`

## Qué hace buena a una persona de la lista
Alta: decide viajes o entrenamientos de equipos de 12 a 18 años, club que ya viaja (Donosti Cup, Costa Daurada Cup), cargo claro. Media: cargo técnico sin poder de decisión (pedir que nos derive). Baja: sin cargo claro, perfil sin actividad o club sin equipos de edad.

## Prompt para pegar el resultado en el chat con Claude
Copia este texto, cambia lo que va entre corchetes y pega debajo los resultados de LinkedIn:

```
Te pego resultados de una búsqueda de LinkedIn hecha por mí, a mano. Objetivo: encontrar decisores de clubes y academias de [país o región] a los que Always Up pueda ofrecer Team Experience (equipos de 12 a 18 años a entrenar en España con Atlético de Madrid y Real Sociedad).

Para cada persona:
1. Descarta si no encaja (sin cargo de decisión, club sin equipos juveniles, perfil de otro sector).
2. Puntúa el encaje: alto, medio o bajo, con una razón de una línea.
3. Escribe la nota de conexión (máximo 300 caracteres, tono humano, sin guiones largos, sin mencionar a University Soccer ni prometer nada).
4. Busca en la web del club el email del cargo y dime si sigue en el puesto (fuente reciente).
5. Devuélvemelo en tabla: nombre, cargo, club, país, enlace, encaje, motivo, nota de conexión, email verificado, fuente.
Después, añade los de encaje alto o medio a la hoja "LinkedIn - Conexiones" del CRM.

Resultados:
[pega aquí]
```

## Límites para cuidar la cuenta
- Máximo **4 a 8 solicitudes por semana** con nota, más actividad ligera (comentar y aceptar).
- Las cuentas gratuitas limitan las notas personalizadas por mes: si no te deja, conecta sin nota y manda el texto cuando acepten.
- Nada de mensajes masivos ni de herramientas externas.
