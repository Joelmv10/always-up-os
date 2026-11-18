"""Deja un PDF listo para mandarlo por correo y comprueba que se ve.

Por qué existe (17/11/2026): los PDF de 02-sales/assets salían de ReportLab con ASCII85.
Apple Mail los codifica entonces como texto (quoted-printable) y el visor de Gmail los
enseña en blanco. Este script pasa las imágenes a JPEG/PNG binario y comprime el resto,
sin cambiar cómo se ve el documento.

Uso:
    python3 optimizar_pdf.py archivo.pdf [...]            # optimiza en su sitio
    python3 optimizar_pdf.py --comprobar archivo.pdf [...] # solo comprueba (antes de adjuntar)
"""
import os
import sys

import fitz


def comprobar(ruta):
    """Devuelve una lista de problemas; vacía si el PDF está bien para adjuntar."""
    problemas = []
    try:
        d = fitz.open(ruta)
    except Exception as e:  # noqa: BLE001
        return ["no se abre: %s" % e]
    if d.page_count == 0:
        problemas.append("no tiene páginas")
    for i, p in enumerate(d):
        pix = p.get_pixmap(dpi=20)
        s = pix.samples
        if s and min(s) > 245:
            problemas.append("la página %d sale en blanco" % (i + 1))
    for x in range(1, d.xref_length()):
        if d.xref_is_stream(x) and "ASCII85" in (d.xref_get_key(x, "Filter")[1] or ""):
            problemas.append("tiene ASCII85 (Gmail puede enseñarlo en blanco): pasar optimizar_pdf.py")
            break
    return problemas


def optimizar(ruta):
    d = fitz.open(ruta)
    hechos = set()
    for p in d:
        for img in p.get_images(full=True):
            x = img[0]
            if x in hechos:
                continue
            hechos.add(x)
            pix = fitz.Pixmap(d, x)
            if pix.alpha or img[1]:
                datos = pix.tobytes("png")
            else:
                if pix.n > 3:
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                datos = pix.tobytes("jpg", jpg_quality=88)
            p.replace_image(x, stream=datos)
    for x in range(1, d.xref_length()):
        if d.xref_is_stream(x) and "ASCII85" in (d.xref_get_key(x, "Filter")[1] or ""):
            d.update_stream(x, d.xref_stream(x), compress=True)
    tmp = ruta + ".tmp"
    d.save(tmp, garbage=4, deflate=True)
    d.close()
    os.replace(tmp, ruta)


if __name__ == "__main__":
    solo = "--comprobar" in sys.argv
    rutas = [a for a in sys.argv[1:] if a != "--comprobar"]
    mal = 0
    for r in rutas:
        if not solo:
            antes = os.path.getsize(r)
            optimizar(r)
            print("optimizado: %s (%d KB -> %d KB)" % (r, antes // 1024, os.path.getsize(r) // 1024))
        pr = comprobar(r)
        print(("OK: " + r) if not pr else ("MAL: %s: %s" % (r, "; ".join(pr))))
        mal += bool(pr)
    sys.exit(1 if mal else 0)
