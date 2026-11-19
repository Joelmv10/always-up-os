"""Hook PermissionRequest: las sesiones automáticas nunca se quedan esperando un permiso.

Si la sesión la ha lanzado una tarea programada (su primer mensaje empieza por
<scheduled-task) y algo pide permiso, se deniega al momento con una explicación,
la sesión sigue con lo demás y el comando queda apuntado en denegados.log para
añadirlo a la lista de permitidos si hace falta. En las sesiones normales con Joel
no hace nada: el aviso de permiso sale como siempre.

Por qué denegar y no aprobar: las sesiones automáticas leen correos y webs de
terceros; aprobarlo todo sin mirar sería abrir la puerta a que un texto de fuera
ejecute comandos. Con la lista de permitidos bien hecha, no hace falta nada más.
"""
import datetime
import json
import os
import sys

LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "denegados.log")


def es_automatica(transcript_path):
    try:
        with open(transcript_path, encoding="utf-8") as f:
            for i, line in enumerate(f):
                if i > 200:
                    break
                try:
                    d = json.loads(line)
                except ValueError:
                    continue
                if d.get("type") != "user":
                    continue
                c = (d.get("message") or {}).get("content")
                if isinstance(c, list):
                    c = " ".join(b.get("text", "") for b in c if isinstance(b, dict))
                if isinstance(c, str) and c.strip():
                    return c.lstrip().startswith("<scheduled-task")
    except OSError:
        pass
    return False


def main():
    try:
        data = json.load(sys.stdin)
    except ValueError:
        return
    if not es_automatica(data.get("transcript_path", "")):
        return
    tool = data.get("tool_name", "")
    entrada = json.dumps(data.get("tool_input", {}), ensure_ascii=False)[:400]
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write("%s\t%s\t%s\t%s\n" % (datetime.datetime.now().isoformat(timespec="seconds"),
                                          data.get("session_id", ""), tool, entrada))
    except OSError:
        pass
    msg = ("Sesion automatica: nadie puede aprobar permisos, asi que esto se ha denegado solo. "
           "No lo reintentes igual. Usa la alternativa permitida (un comando simple por llamada, "
           "Read en vez de cat, WebFetch en vez del navegador fuera de LinkedIn, sin cd && ni git -C) "
           "o, si no la hay, apuntalo en el informe y sigue con el resto.")
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PermissionRequest",
                                             "decision": {"behavior": "deny", "message": msg}}}))


if __name__ == "__main__":
    main()
