"""Busca rebotes en la bandeja de la cuenta Alwaysup de Apple Mail (últimas horas).

Lo usa la sesión de envíos después de mandar los correos del día. Es un solo comando para que la sesión
automática no se quede esperando un permiso (18/11/2026: los comandos con $( ), bucles o sleep piden aprobación).

Uso:
    python3 revisar_rebotes.py [--esperar 540] [--horas 2]
"""
import argparse
import subprocess
import time

CLAVES = ("undeliverable", "delivery status notification", "mail delivery", "returned mail", "delivery has failed",
          "no se puede entregar", "failure notice", "address not found")

SCRIPT = '''
on run argv
  set horas to (item 1 of argv) as integer
  set out to ""
  tell application "Mail"
    set mb to mailbox "INBOX" of account "Alwaysup"
    set msgs to (messages of mb whose date received > ((current date) - horas * hours))
    repeat with m in msgs
      set out to out & ((date received of m) as «class isot» as string) & tab & (sender of m) & tab & (subject of m) & linefeed
    end repeat
  end tell
  return out
end run
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--esperar", type=int, default=0, help="segundos de espera antes de mirar (máx. 560)")
    ap.add_argument("--horas", type=int, default=2)
    a = ap.parse_args()
    if a.esperar:
        time.sleep(min(a.esperar, 560))
    r = subprocess.run(["osascript", "-", str(a.horas)], input=SCRIPT, capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        print("ERROR al leer la bandeja:", r.stderr.strip())
        return 1
    filas = [l.split("\t") for l in r.stdout.splitlines() if l.strip()]
    rebotes = [f for f in filas if any(c in (" ".join(f[1:])).lower() for c in CLAVES)]
    print("Correos recibidos en las últimas %d horas: %d" % (a.horas, len(filas)))
    for f in filas:
        print("  " + " | ".join(f))
    print("REBOTES: %d" % len(rebotes))
    for f in rebotes:
        print("  REBOTE: " + " | ".join(f))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
