# Plantilla de propuesta escrita (post-llamada)

> **Desde 2026-10-02 la propuesta se genera como PDF con marca** con `07-automations/propuestas/generar_propuesta.py`: se rellena una ficha JSON por cliente (hay ejemplos en `07-automations/propuestas/ejemplos/`) y sale la propuesta lista para enviar. Presets: `team`, `coach`, `camp`, `becas`, `programa`. Revisar los presets (qué incluye / qué no incluye / condiciones) antes del primer uso real. La plantilla de texto de abajo sigue siendo la guía de contenido: el "Objetivo" siempre específico de la llamada, "siguiente paso" con fecha real.

> Enviar siempre tras la "Experience Planning Call" / "Scholarship Assessment" / etc. — nunca dejar una llamada en "lo hablamos y os digo". Una sola plantilla reutilizable para los 4 servicios activos (no crear una por servicio). Ver [embudo-ventas.md](embudo-ventas.md) sección 5.5.

```
ALWAYS UP — PROPUESTA

Para: [Nombre del club/familia/jugador]
Fecha: [fecha]

Objetivo
[1-2 líneas resumiendo lo que nos contaron en la llamada — demuestra que
escuchaste, no es una plantilla genérica]

Qué proponemos
[Servicio concreto: Team Experience / Coach Experience / Becas / Colegio
privado / International Program, con el formato exacto acordado —
duración, club(es), fechas]

Qué incluye
[Lista corta de lo que incluye el programa, ver playbook-ventas.md]

Fechas propuestas
[Fechas concretas, no "cuando queráis"]

Inversión
[Precio con seguridad, sin descuentos ya aplicados salvo que se haya
acordado en la llamada]

Siguiente paso
[Acción concreta y con fecha — ej. "Confirmar antes del [fecha] para
asegurar la disponibilidad con el club"]

Cualquier duda, aquí estoy.

Joel Martinez
Always Up
```

## Notas de uso

- Rellenar SIEMPRE el "Objetivo" con algo específico de la conversación — es lo que diferencia una propuesta personalizada de una plantilla copiada, y es la parte que más genera confianza.
- El "siguiente paso" con fecha concreta sustituye a la urgencia artificial — si hay una razón real de plazo (disponibilidad del club anfitrión, fecha límite de inscripción de becas), usarla aquí, no inventar prisa donde no la hay.
- Enviar en PDF o documento bien formateado, no como texto plano de WhatsApp — es precisamente lo que la separa de "otra conversación más".

## Cómo generar una propuesta

```bash
python3 07-automations/propuestas/generar_propuesta.py ficha_cliente.json -o 01-clients/propuestas/propuesta_cliente.pdf
```

Campos de la ficha: `servicio`, `cliente`, `fecha`, `moneda`, `objetivo`, `propuesta`, `datos` (tabla clave-valor), `programa_detalle`, `precio.lineas`, `precio.nota`, `precio.pago`, `siguiente_paso`. Se pueden sobrescribir `incluye`, `no_incluye`, `pasos` y añadir `terminos_extra`. Becas: sin garantizar nunca beca ni admisión (ya incluido en el preset).
