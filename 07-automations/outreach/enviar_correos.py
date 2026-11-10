"""Envía desde Apple Mail (cuenta joel.martinez@alwaysup.es) los correos del día que salen del generador.

Lo usa el turno de envíos programado de Claude (martes a jueves). Joel lo autorizó el 10/11/2026.

Uso:
    python3 enviar_correos.py --region europa|america [--fecha 2026-11-12] [--dry-run]

Reglas (no se saltan nunca):
- Solo correos del generador con fecha de hoy y tipo Email 1, Follow-up 1, Follow-up 2 o Cierre. Nada de textos nuevos.
- Los textos pasan antes el validador del generador.
- No se envía si ya está en registro.json, en Enviados o en la cola de Enviar más tarde.
- Un follow-up no se envía si el club ha contestado (cualquier correo suyo en la bandeja de entrada): se avisa a Joel.
- Máximo CAP_DIA correos al día en total.
- Los follow-ups van como respuesta dentro del hilo del correo original. Si no se encuentra el original, no se envía.
- Copia oculta al Gmail de Joel. Cada envío queda apuntado en registro.json.
"""
import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import generar_outreach as g  # noqa: E402

CUENTA = "Alwaysup"
REMITENTE = "Joel Martinez <joel.martinez@alwaysup.es>"
CCO = "joel.martinez.vicente.10@gmail.com"
TIPOS = ("Email 1", "Follow-up 1", "Follow-up 2", "Cierre")
REGISTRO = os.path.join(HERE, "registro.json")


def osa(script, *args):
    r = subprocess.run(["osascript", "-", *args], input=script, capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip())
    return r.stdout.strip()


LISTAR = '''
on run argv
  set out to ""
  tell application "Mail"
    set acc to account "%s"
    repeat with mb in mailboxes of acc
      set nm to name of mb
      if nm is "INBOX" then
        set ss to sender of messages of mb
        repeat with x in ss
          set out to out & "INBOX" & tab & x & tab & "-" & tab & "-" & linefeed
        end repeat
      else if nm starts with "Sent" then
        set subs to subject of messages of mb
        set fechas to date sent of messages of mb
        set msgs to messages of mb
        repeat with i from 1 to count of msgs
          try
            set out to out & nm & tab & (address of first to recipient of (item i of msgs)) & tab & (item i of subs) & tab & ((item i of fechas) as «class isot» as string) & linefeed
          end try
        end repeat
      end if
    end repeat
    repeat with m in messages of mailbox "SendLater"
      try
        set out to out & "SendLater" & tab & (address of first to recipient of m) & tab & subject of m & tab & "-" & linefeed
      end try
    end repeat
  end tell
  return out
end run
''' % CUENTA

NUEVO = '''
on run argv
  set para to item 1 of argv
  set asunto to item 2 of argv
  set cuerpo to read (POSIX file (item 3 of argv)) as «class utf8»
  tell application "Mail"
    set m to make new outgoing message with properties {sender:"%s", subject:asunto, content:cuerpo, visible:false}
    tell m
      make new to recipient at end of to recipients with properties {address:para}
      make new bcc recipient at end of bcc recipients with properties {address:"%s"}
    end tell
    send m
  end tell
  return "ok"
end run
''' % (REMITENTE, CCO)

RESPONDER = '''
on run argv
  set para to item 1 of argv
  set asuntoOriginal to item 2 of argv
  set cuerpo to read (POSIX file (item 3 of argv)) as «class utf8»
  tell application "Mail"
    set acc to account "%s"
    set original to missing value
    repeat with mb in mailboxes of acc
      if name of mb starts with "Sent" then
        repeat with m in (messages of mb)
          try
            if (address of first to recipient of m) is para and (subject of m) is asuntoOriginal then
              set original to m
              exit repeat
            end if
          end try
        end repeat
      end if
      if original is not missing value then exit repeat
    end repeat
    if original is missing value then return "sin original"
    set r to reply original with opening window
    delay 1
    set content of r to cuerpo
    tell r to make new bcc recipient at end of bcc recipients with properties {address:"%s"}
    send r
  end tell
  return "ok"
end run
''' % (CUENTA, CCO)


def dominio(addr):
    return addr.split("@")[-1].lower().strip(">")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--region", choices=("europa", "america"), required=True)
    ap.add_argument("--fecha")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    hoy = dt.date.fromisoformat(a.fecha) if a.fecha else dt.date.today()

    sends = g.build_sends()
    problemas = g.validate(sends)
    if problemas:
        print("NO SE ENVÍA NADA: el validador encuentra problemas:", *problemas, sep="\n- ")
        return 1

    reg = json.load(open(REGISTRO, encoding="utf-8"))
    hechos = {(e["key"], e["kind"]) for e in reg.get("envios", [])}
    enviados_hoy = sum(1 for e in reg.get("envios", []) if e.get("date") == hoy.isoformat())

    filas = [l.split("\t") for l in osa(LISTAR).splitlines() if l.count("\t") >= 3]
    en_mail = {(f[1].lower(), f[2].replace("Re: ", "")) for f in filas if f[0] != "INBOX"}
    hoy_mail = sum(1 for f in filas if f[0].startswith("Sent") and f[3][:10] == hoy.isoformat())
    import re
    def addr(x):
        m = re.search(r"[\w.+-]+@[\w.-]+", x)
        return m.group(0).lower() if m else x.lower()
    entrantes = {dominio(addr(f[1])) for f in filas if f[0] == "INBOX"} | {addr(f[1]) for f in filas if f[0] == "INBOX"}

    def europeo(s):
        return str(s.get("tz", "")).startswith(("Europe/", "Atlantic/"))

    del_dia = [s for s in sends if s["kind"] in TIPOS and (s["date"].date() if isinstance(s["date"], dt.datetime) else s["date"]) == hoy and "@" in str(s["to"])
               and (europeo(s) if a.region == "europa" else not europeo(s))]
    primeros = {}
    for s in sends:
        if s["kind"] == "Email 1":
            primeros[s["key"]] = s

    hechos_hoy = max(enviados_hoy, hoy_mail)
    informe = []
    for s in del_dia:
        para, asunto = s["to"].strip(), s["subj"]
        base = primeros.get(s["key"], s)["subj"]
        if (s["key"], s["kind"]) in hechos or (para.lower(), base) in en_mail and s["kind"] == "Email 1":
            informe.append("YA ESTABA: %s (%s) a %s" % (s["club"], s["kind"], para))
            continue
        if s["kind"] != "Email 1" and (para.lower() in entrantes or dominio(para) in entrantes and dominio(para) not in ("gmail.com", "hotmail.com", "outlook.com", "yahoo.com")):
            informe.append("NO ENVIADO, PUEDE HABER CONTESTADO: %s (%s). Revisar la bandeja." % (s["club"], s["kind"]))
            continue
        if hechos_hoy >= g.CAP_DIA:
            informe.append("NO ENVIADO, TOPE DIARIO: %s (%s)" % (s["club"], s["kind"]))
            continue
        if a.dry_run:
            informe.append("ENVIARÍA: %s (%s) a %s | %s" % (s["club"], s["kind"], para, asunto))
            hechos_hoy += 1
            continue
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
            f.write(s["body"])
            ruta = f.name
        try:
            if s["kind"] == "Email 1":
                res = osa(NUEVO, para, asunto, ruta)
            else:
                res = osa(RESPONDER, para, base, ruta)
        finally:
            os.unlink(ruta)
        if res != "ok":
            informe.append("NO ENVIADO (%s): %s (%s) a %s" % (res, s["club"], s["kind"], para))
            continue
        reg.setdefault("envios", []).append({"key": s["key"], "kind": s["kind"], "date": hoy.isoformat(),
                                             "nota": "Enviado por Claude a las %s" % dt.datetime.now().strftime("%H:%M")})
        json.dump(reg, open(REGISTRO, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        hechos_hoy += 1
        informe.append("ENVIADO: %s (%s) a %s" % (s["club"], s["kind"], para))
    print("\n".join(informe) if informe else "Nada que enviar hoy en %s." % a.region)
    return 0


if __name__ == "__main__":
    sys.exit(main())
