# Comprobación de los turnos automáticos: viernes 20/11/2026

> Hecha por la tarea `verificar-turnos-19-11`. Horas en Nueva York (UTC-5). Solo lectura: no se ha enviado ni cambiado nada.

## Sesiones de hoy

| Sesión | Hora prevista | Hora real (inicio → última actividad) | Estado | Qué hizo |
|---|---|---|---|---|
| envios-correo-always-up (Europa) | 4:30 | 5:41 → 8:39 | succeeded | Envió 2 de 5 (Maidstone FU2 y Ross FU1, 5:42). El servidor SMTP cortó la conexión tras el segundo correo. Empezó con 1 h 11 min de retraso y siguió activa casi 3 h |
| turno-diario-always-up | 7:30 | 7:37 → 9:09 | succeeded | Bandeja, mensajes de LinkedIn a Shawn Burke y Pedro Sousa, respuesta de Khalil Lazrek, tanda 3 de universidades (Ithaca, Clemson, Trine), informe semanal. **Conexiones: 0** (el diálogo de LinkedIn no se abría con el panel oculto) |
| instagram-daily-sales-sweep | 9:00 | — | **sin ejecución hoy** | La tarea figura como **eliminada**; su última ejecución fue el 19/11 (9:01 → 11:12). Si no se borró a propósito, hay que volver a crearla |
| envios-correo-always-up (América) | 9:30 | 9:34 → 9:44 | succeeded | Envió Ballistic United (Jerry Losson, correo 1) a las 9:34. **Rebotó** a las 9:35 |
| Sesión manual con Joel (no automática) | — | mañana | — | Arregló el envío (pausa de 45 s y reintento de la conexión). Envió Søreide, Virtu y Whitehaven a las 9:10–9:12 y la respuesta a Khalil a las 9:21. Hizo 3 conexiones (Wakeman, Grimes, Radwanski) |

Ninguna sesión se quedó en "running" ni terminó en error.

## Correos enviados hoy (registro.json, 2026-11-20)

| Club | Tipo | Hora | Por |
|---|---|---|---|
| Maidstone | Follow-up 2 | 5:42 | sesión automática (Europa) |
| Ross | Follow-up 1 | 5:42 | sesión automática (Europa) |
| Søreide | Follow-up 2 | 9:10 | sesión con Joel |
| Virtu | Follow-up 1 | 9:11 | sesión con Joel |
| Whitehaven | Follow-up 2 | 9:12 | sesión con Joel |
| Ballistic United | Email 1 | 9:34 | sesión automática (América), **rebotado** |

- **Coinciden con lo previsto:** sí, los 6 (Ballistic United, Maidstone, Ross, Søreide, Virtu y Whitehaven), ni más ni menos. Pero solo 3 salieron solos: los otros 3 de Europa necesitaron la sesión manual.
- **Por SMTP, no por Mail:** todos los registros dicen "Enviado por Claude" con el flujo nuevo y el informe del día confirma que en Enviados se ven con el texto limpio y en su hilo. Con Read no se puede abrir Mail para confirmar que no hay un mensaje creado por script; no hay ningún indicio de que lo haya.
- **Rebotes (últimas 8 h, `revisar_rebotes.py`):** 1, MAILER-DAEMON@mailchannels.net, "Undelivered Mail Returned to Sender", 9:35. Es el de Ballistic United (un minuto después del envío). Hay que buscar otro correo de Jerry Losson; ya está conectado con él en LinkedIn (17/11).

## Lo denegado por el hook

`07-automations/hooks/denegados.log` no existe: **hoy no se denegó nada**. Ninguna sesión pidió un permiso fuera de lo permitido.

## Qué hay que hacer

1. **Ballistic United:** buscar otro correo de Jerry Losson (o escribirle por LinkedIn) y volver a colocar el correo 1.
2. **instagram-daily-sales-sweep:** confirmar si se borró a propósito; si no, volver a crearla.
3. **Envío de Europa:** hoy arrancó a las 5:41 en lugar de las 4:30, y los 3 correos que faltaban se arreglaron a mano. El lunes 23/11 (6 correos) es la primera prueba real del arreglo de la pausa de 45 s.
4. **Turno diario:** dejar visible el panel del navegador para que LinkedIn abra la invitación al conectar.
