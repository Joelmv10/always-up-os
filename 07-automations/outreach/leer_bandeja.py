"""Lee la bandeja de entrada de joel.martinez@alwaysup.es y enseña solo los correos de personas.

Uso: python3 leer_bandeja.py --horas 4
Quita notificaciones (LinkedIn, Calendly, avisos automáticos) y nunca enseña códigos de verificación.
Corta el texto citado del hilo para que se lea solo la respuesta nueva.
Lo usan el turno diario y la revisión de bandeja de varias veces al día.
"""
import argparse
import re
import subprocess

RUIDO = ("linkedin.com", "calendly", "noreply", "no-reply", "donotreply", "do-not-reply", "notifications@",
         "google.com", "apple.com", "hostinger", "mailer@", "newsletter", "info@em.", "accounts.")
CORTES = (r"\nOn .{5,80}wrote:", r"\nEl .{5,80}escribió:", r"\nFrom: ", r"\nDe: ", r"\n-----Original Message",
          r"\nSent from my")

SEP_M = "<<<MSG>>>"
SEP_C = "<<<CAMPO>>>"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--horas", type=float, default=4)
    a = ap.parse_args()
    scr = '''
set out to ""
set lim to (current date) - (%d * minutes)
tell application "Mail"
  set mb to mailbox "INBOX" of account "Alwaysup"
  set ms to (messages of mb whose date received > lim)
  repeat with m in ms
    set out to out & "%s" & (sender of m) & "%s" & ((date received of m) as string) & "%s" & (subject of m) & "%s" & (content of m)
  end repeat
end tell
return out
''' % (int(a.horas * 60), SEP_M, SEP_C, SEP_C, SEP_C)
    r = subprocess.run(["osascript", "-e", scr], capture_output=True, text=True)
    if r.returncode != 0:
        print("ERROR leyendo Mail:", r.stderr.strip()[:300])
        return
    n = 0
    for bloque in r.stdout.split(SEP_M)[1:]:
        partes = bloque.split(SEP_C)
        if len(partes) < 4:
            continue
        de, fecha, asunto, cuerpo = partes[0], partes[1], partes[2], SEP_C.join(partes[3:])
        if any(x in de.lower() for x in RUIDO):
            continue
        if re.search(r"verification code|código de verificación|one-time code|security code", asunto + cuerpo[:300], re.I):
            continue
        texto = cuerpo
        for c in CORTES:
            mm = re.search(c, texto)
            if mm:
                texto = texto[:mm.start()]
        texto = re.sub(r"[￼͏]", "", texto)
        texto = re.sub(r"\n\s*\n+", "\n\n", texto).strip()
        n += 1
        print("=====")
        print("DE:", de)
        print("FECHA:", fecha)
        print("ASUNTO:", asunto)
        print(texto[:2000])
    if n == 0:
        print("NADA NUEVO: ningún correo de personas en las últimas %s horas." % a.horas)


if __name__ == "__main__":
    main()
