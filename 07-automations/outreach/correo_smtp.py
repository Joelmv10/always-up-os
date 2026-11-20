"""Envío de correos de joel.martinez@alwaysup.es sin pasar por el redactor de Apple Mail.

Por qué existe (19/11/2026): en macOS 26, todo texto que un script mete en un correo de Apple Mail
(make new outgoing message / set content / html content) se guarda como CITA. En texto normal sale
con ">" delante de cada línea y en HTML dentro de un <blockquote type="cite">. Pasó en todos los
correos automáticos del 10/11 al 19/11. Este módulo construye el correo él mismo (texto plano UTF-8,
sin citas), lo envía por el SMTP de Hostinger y guarda la copia en Enviados por IMAP, así que en
Mail se ve igual que siempre.

La contraseña NO está en el repo: se lee del Llavero de macOS (servicio "always-up-correo").
Joel la guarda una vez con:
    security add-generic-password -s always-up-correo -a joel.martinez@alwaysup.es -T /usr/bin/security -U -w

Uso desde la terminal:
    python3 correo_smtp.py comprobar                # prueba la conexión sin enviar nada
    python3 correo_smtp.py prueba                   # se manda un correo de prueba a sí mismo y revisa el texto
    python3 correo_smtp.py nuevo --para X --asunto Y --cuerpo archivo.txt
    python3 correo_smtp.py responder --para X --asunto-original Y --cuerpo archivo.txt
"""
import argparse
import email
import email.policy
import imaplib
import re
import smtplib
import ssl
import subprocess
import sys
import time
from email.header import decode_header, make_header
from email.message import EmailMessage
from email.utils import formatdate, make_msgid

USUARIO = "joel.martinez@alwaysup.es"
REMITENTE = "Joel Martinez <joel.martinez@alwaysup.es>"
CCO = "joel.martinez.vicente.10@gmail.com"
SMTP_HOST, SMTP_PORT = "smtp.hostinger.com", 465
IMAP_HOST, IMAP_PORT = "imap.hostinger.com", 993
SERVICIO_LLAVERO = "always-up-correo"


class ErrorCorreo(RuntimeError):
    pass


def _clave():
    r = subprocess.run(["/usr/bin/security", "find-generic-password", "-s", SERVICIO_LLAVERO, "-a", USUARIO, "-w"],
                       capture_output=True, text=True, timeout=20)
    if r.returncode != 0 or not r.stdout.strip():
        raise ErrorCorreo("Falta la contraseña en el Llavero (servicio %s). Joel tiene que guardarla una vez." % SERVICIO_LLAVERO)
    return r.stdout.rstrip("\n")


def _ctx():
    return ssl.create_default_context()


def _imap():
    m = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT, ssl_context=_ctx())
    m.login(USUARIO, _clave())
    return m


CARPETA_ENVIADOS = "INBOX.Sent"  # la que usa Mail para esta cuenta (comprobado el 19/11/2026)


def _carpetas_sent(m):
    nombres = []
    for raw in m.list()[1] or []:
        linea = raw.decode("utf-8", "replace")
        nombre = re.search(r'"([^"]*)"\s*$|(\S+)\s*$', linea)
        nombre = (nombre.group(1) or nombre.group(2)) if nombre else ""
        if "sent" in nombre.lower():
            nombres.append(nombre)
    return nombres


def _carpeta_enviados(m):
    if CARPETA_ENVIADOS in _carpetas_sent(m):
        return CARPETA_ENVIADOS
    typ, data = m.list()
    nombres = []
    for raw in data or []:
        linea = raw.decode("utf-8", "replace")
        nombre = re.search(r'"([^"]*)"\s*$|(\S+)\s*$', linea)
        nombre = (nombre.group(1) or nombre.group(2)) if nombre else ""
        if "\\Sent" in linea:
            return nombre
        nombres.append(nombre)
    for candidato in ("Sent", "INBOX.Sent", "Sent Messages", "Sent Items"):
        if candidato in nombres:
            return candidato
    raise ErrorCorreo("No encuentro la carpeta de Enviados en el servidor: %s" % nombres)


def _q(nombre):
    return '"%s"' % nombre.replace('"', '\\"')


def _texto_cabecera(v):
    return str(make_header(decode_header(v or ""))).strip()


def comprobar_texto(cuerpo):
    """El texto tiene que salir limpio: sin líneas citadas ni restos de HTML."""
    problemas = []
    for i, linea in enumerate(cuerpo.splitlines(), 1):
        if linea.lstrip().startswith(">"):
            problemas.append("línea %d empieza por '>'" % i)
    if re.search(r"<\s*(blockquote|div|br|html)\b", cuerpo, re.I):
        problemas.append("lleva etiquetas HTML")
    if not cuerpo.strip():
        problemas.append("está vacío")
    return problemas


def buscar_original(para, asunto):
    """Message-ID y References del primer correo enviado a `para` con ese asunto exacto."""
    m = _imap()
    try:
        for carpeta in _carpetas_sent(m):
            m.select(_q(carpeta), readonly=True)
            typ, data = m.search(None, "TO", _q(para))
            for i in (data[0] or b"").split():
                typ, d = m.fetch(i, "(BODY.PEEK[HEADER.FIELDS (SUBJECT MESSAGE-ID REFERENCES DATE)])")
                cab = email.message_from_bytes(d[0][1])
                if _texto_cabecera(cab.get("Subject")) == asunto.strip() and cab.get("Message-ID"):
                    return cab.get("Message-ID", "").strip(), cab.get("References", "").strip()
        return None, None
    finally:
        try:
            m.logout()
        except Exception:
            pass


def construir(para, asunto, cuerpo, responde_a=None, referencias=""):
    msg = EmailMessage(policy=email.policy.SMTP)
    msg["From"] = REMITENTE
    msg["To"] = para
    msg["Subject"] = asunto
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="alwaysup.es")
    if responde_a:
        msg["In-Reply-To"] = responde_a
        msg["References"] = (referencias + " " + responde_a).strip()
    texto = cuerpo.replace("\r\n", "\n").strip("\n") + "\n"
    msg.set_content(texto, subtype="plain", charset="utf-8", cte="quoted-printable")
    return msg


def enviar(msg, con_copia_oculta=True):
    problemas = comprobar_texto(msg.get_content())
    if problemas:
        raise ErrorCorreo("No se envía, el texto no está limpio: " + "; ".join(problemas))
    destinos = [msg["To"]] + ([CCO] if con_copia_oculta else [])
    clave = _clave()
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=_ctx(), timeout=60) as s:
        s.login(USUARIO, clave)
        rechazados = s.send_message(msg, to_addrs=destinos)
    if rechazados:
        raise ErrorCorreo("El servidor rechazó: %s" % rechazados)
    # Copia en Enviados para que Mail, registro y follow-ups la vean como siempre.
    copia = EmailMessage(policy=email.policy.SMTP)
    for k, v in msg.items():
        copia[k] = v
    if con_copia_oculta:
        copia["Bcc"] = CCO
    copia.set_content(msg.get_content(), subtype="plain", charset="utf-8", cte="quoted-printable")
    m = _imap()
    try:
        carpeta = _carpeta_enviados(m)
        m.append(_q(carpeta), r"(\Seen)", imaplib.Time2Internaldate(time.time()), copia.as_bytes())
    finally:
        try:
            m.logout()
        except Exception:
            pass
    return msg["Message-ID"]


def nuevo(para, asunto, cuerpo):
    return enviar(construir(para, asunto, cuerpo))


def responder(para, asunto_original, cuerpo):
    mid, refs = buscar_original(para, asunto_original)
    if not mid:
        raise ErrorCorreo("sin original")
    asunto = asunto_original if asunto_original.lower().startswith("re:") else "Re: " + asunto_original
    return enviar(construir(para, asunto, cuerpo, responde_a=mid, referencias=refs))


def _leer_enviado(message_id):
    m = _imap()
    try:
        m.select(_q(_carpeta_enviados(m)), readonly=True)
        typ, data = m.search(None, "HEADER", "Message-ID", _q(message_id))
        ids = (data[0] or b"").split()
        if not ids:
            return None
        typ, d = m.fetch(ids[-1], "(BODY.PEEK[])")
        return email.message_from_bytes(d[0][1], policy=email.policy.default)
    finally:
        m.logout()


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("comprobar")
    sub.add_parser("prueba")
    n = sub.add_parser("nuevo")
    n.add_argument("--para", required=True)
    n.add_argument("--asunto", required=True)
    n.add_argument("--cuerpo", required=True, help="archivo de texto con el cuerpo")
    r = sub.add_parser("responder")
    r.add_argument("--para", required=True)
    r.add_argument("--asunto-original", required=True)
    r.add_argument("--cuerpo", required=True)
    a = ap.parse_args()
    try:
        if a.cmd == "comprobar":
            m = _imap()
            print("IMAP correcto. Enviados:", _carpeta_enviados(m))
            m.logout()
            with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=_ctx(), timeout=60) as s:
                s.login(USUARIO, _clave())
            print("SMTP correcto. No se ha enviado nada.")
        elif a.cmd == "prueba":
            cuerpo = "Hi Joel,\n\nThis is an internal test of the new sender. No quotes, no HTML.\n\nBest,\nJoel Martinez\nFounder, Always Up\njoel.martinez@alwaysup.es | +1 (814) 329 1929 | alwaysup.es\n"
            mid = enviar(construir(USUARIO, "Prueba interna del envio (puedes borrarlo)", cuerpo), con_copia_oculta=False)
            copia = _leer_enviado(mid)
            texto = copia.get_body(("plain",)).get_content() if copia else ""
            ok = copia is not None and not comprobar_texto(texto) and copia.get_content_type() == "text/plain"
            print("PRUEBA %s. Message-ID %s\n----\n%s----" % ("CORRECTA" if ok else "FALLIDA", mid, texto))
            return 0 if ok else 1
        else:
            cuerpo = open(a.cuerpo, encoding="utf-8").read()
            if a.cmd == "nuevo":
                print("ok", nuevo(a.para, a.asunto, cuerpo))
            else:
                print("ok", responder(a.para, a.asunto_original, cuerpo))
    except ErrorCorreo as e:
        print("ERROR:", e)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
