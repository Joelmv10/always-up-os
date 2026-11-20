# Borradores de respuesta

Aquí dejan las sesiones automáticas (bandeja y turno diario) las respuestas a clubes, familias y socios, una por archivo: `AAAA-MM-DD-<club>.txt`.

Formato:
```
PARA: correo@club.com
ASUNTO ORIGINAL: asunto del primer correo del hilo, sin "Re:"

Texto de la respuesta tal cual se envía.
```

Cuando Joel da el OK, Claude la envía dentro del hilo con:
`python3 07-automations/outreach/correo_smtp.py responder --para <correo> --asunto-original "<asunto>" --cuerpo <archivo con solo el texto>`

**Nunca se crean correos ni borradores en Apple Mail por script.** Desde el 19/11/2026 sabemos que Mail convierte en cita todo texto que mete un script (">" en cada línea en texto normal, `<blockquote>` en HTML). Si Joel prefiere enviarla él, copia y pega el texto en Mail a mano: así sale bien.
