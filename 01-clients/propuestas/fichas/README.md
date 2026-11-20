# Propuestas de Team Experience: cómo sacar una en 5 minutos

Cuando un club contesta con interés, o después de la llamada, se manda una propuesta en PDF con su nombre **ese mismo día**. Tiene el mismo diseño que la de Greystones: portada con foto, por qué con nosotros, testimonio, tres opciones con precio "desde", fotos, programa real de 5 días, qué incluye, fechas y pasos para reservar.

**Regla de Joel (19/11/2026): la propuesta se prepara cuando el club contesta, y nunca sale sin el OK de Joel.** Joel cambiará varias cosas del modelo antes del primer envío. Los precios por defecto (1.950 € por 5 días) no valen: el orientativo actual es **unos 1.500 $ por jugador, 5 días con el Atlético**, por confirmar.

## Pasos
1. Copia `home-farm-2027.json` con el nombre del club y cambia solo esto:
   - `title`: NOMBRE DEL CLUB 2027 (en mayúsculas)
   - `slug`: Nombre-Club-2027 (sale en el nombre del archivo)
   - `tagline`: una línea con lo que pidieron (equipos, chicas o chicos, Semana Santa o verano)
   - `intro`: tres puntos. **El primero o el segundo tiene que repetir algo que dijeron en la llamada o en el correo.** Es lo que hace que no parezca una plantilla.
2. Opcional: `prices` (si Enrique cierra otro precio), `cards` (otras opciones), `dates` (otros plazos), `quote` (`null` para quitar el testimonio).
3. Genera el PDF:
   `python3 07-automations/materiales/materiales.py propuesta 01-clients/propuestas/fichas/<club>.json`
   Sale en `01-clients/propuestas/Always-Up-<slug>-Proposal.pdf`.
4. Ábrelo y revísalo entero antes de mandarlo.
5. **No se manda por correo como adjunto pesado** (1,6 MB está bien; más de 4 MB no). Si pesa más, se sube a Drive y se manda el enlace.

## Reglas
- Precios siempre "from" hasta que Enrique confirme el precio de 5 días del Atlético para 2027 (catálogo 2027, anexo A1).
- No negociar precio por escrito: si piden descuento, se ofrece una llamada.
- Nada que no podamos cumplir (personal femenino, partidos del primer equipo seguros, contactos con otros clubes sin su permiso).

## Fichas hechas
| Club | Archivo | Estado |
|---|---|---|
| Greystones (Irlanda) | se genera con `materiales.py greystones` | No sale de momento: Enrique les escribe primero |
| Home Farm FC (chicas U13 a U15, Dublín) | `home-farm-2027.json` | Borrador de modelo. Si contestan, se ajusta con Joel y sale solo con su OK |
