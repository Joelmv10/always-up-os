#!/usr/bin/env python3
"""Envía los correos de campaña del día (campanas_envios.json) con correo_smtp.py. Textos aprobados por Joel.

Uso:  python3 envio_campana.py [--fecha 2026-11-23] [--dry-run]
- Solo envía las entradas con la fecha de hoy (o --fecha) que no estén ya en campanas_enviados.json.
- 45 segundos entre correos (Hostinger corta si van seguidos). Si falla la conexión, para y no reintenta el envío.
- Cada envío queda apuntado en campanas_enviados.json con su Message-ID.
"""
import argparse
import datetime as dt
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import correo_smtp  # noqa: E402

DATOS = os.path.join(HERE, "campanas_envios.json")
HECHOS = os.path.join(HERE, "campanas_enviados.json")
FIRMA = "Best,\nJoel Martinez\nFounder, Always Up\njoel.martinez@alwaysup.es | +1 (814) 329 1929 | alwaysup.es\n"

TEXTOS = {
    "programa-12-dias": {
        "asunto": "For your players who want to keep playing",
        "cuerpo": ("Hi Coach {apellido},\n\n"
                   "Hope the season went well. Quick one: some {jugadores} want to keep playing after their last season and don't know where to start.\n\n"
                   "We run a 12 day training programme with Real Unión in the Basque Country (Spain's third tier) for players over 18: daily training "
                   "with the club, housing, meals, video and a written report from their staff.\n\n"
                   "If any of your players might be interested, I'm happy to send you a one page outline to share.\n\n" + FIRMA),
    },
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fecha", default=dt.date.today().isoformat())
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    datos = json.load(open(DATOS, encoding="utf-8"))["envios"]
    hechos = json.load(open(HECHOS, encoding="utf-8")) if os.path.exists(HECHOS) else []
    ya = {(h["para"].lower(), h["campana"]) for h in hechos}
    hoy = [d for d in datos if d["fecha"] == a.fecha and (d["para"].lower(), d["campana"]) not in ya]
    print("Envíos de campaña para %s: %d" % (a.fecha, len(hoy)))
    for i, d in enumerate(hoy):
        t = TEXTOS[d["campana"]]
        cuerpo = t["cuerpo"].format(apellido=d["nombre"].split()[-1], jugadores=d.get("jugadores", "players"))
        if a.dry_run:
            print("---- %s <%s>\n%s\n%s" % (d["nombre"], d["para"], t["asunto"], cuerpo))
            continue
        if i:
            time.sleep(45)
        try:
            mid = correo_smtp.nuevo(d["para"], t["asunto"], cuerpo)
        except Exception as e:  # noqa: BLE001
            print("ERROR con %s: %s. Paro aquí, no se reintenta." % (d["para"], e))
            break
        hechos.append({"fecha": a.fecha, "hora": dt.datetime.now().strftime("%H:%M"), "campana": d["campana"],
                       "para": d["para"], "nombre": d["nombre"], "org": d["org"], "message_id": mid})
        json.dump(hechos, open(HECHOS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("Enviado a %s (%s) %s" % (d["nombre"], d["para"], mid))
    return 0


if __name__ == "__main__":
    sys.exit(main())
