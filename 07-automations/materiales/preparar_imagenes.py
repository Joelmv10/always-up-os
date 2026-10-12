#!/usr/bin/env python3
"""Prepara las imágenes que usan las fichas y el deck (extrae fotos de los PDFs fuente y recorta escudos).

Uso: python3 preparar_imagenes.py
Salida: .cache/ (no se versiona). Las rutas de origen están al principio del archivo: ajustarlas si los PDFs cambian de sitio.
Dependencias: pip install pymupdf pillow numpy
"""
import os
import fitz
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, ".cache"); IM = os.path.join(CACHE, "imgs"); NW = os.path.join(CACHE, "new")
DL = "/Users/joelmartinez/Downloads"
KEY = "/Users/joelmartinez/Library/Mobile Documents/com~apple~Keynote/Documents"

SRC_IMGS = {  # prefijo -> pdf (fotos >= 400x300)
    "tebro": f"{DL}/Team Experience Brochure.pdf",
    "qs": f"{DL}/Quality Servix_Inglés.pdf",
    "rsstage": f"{DL}/Real Sociedad - FOOTBALL STAGE .pdf",
    "rsirp": f"{DL}/RS_International_Residential_Program.pdf",
}
SRC_NEW = {  # prefijo -> pdf (fotos >= 350x250)
    "au": f"{KEY}/AlwaysUp.pdf",
    "exp": f"{KEY}/AlwaysUp - Experiences (PDF).pdf",
}
SPORTING_LOGO = f"{DL}/Fotos Sporting Gijon./01_Escudo_principal.jpg"
SPORTING_RES = f"{DL}/Residencia Sporting Gijon"


def extract(src, out, minw, minh):
    os.makedirs(out, exist_ok=True)
    for key, path in src.items():
        doc = fitz.open(path)
        for pi, page in enumerate(doc):
            for ii, img in enumerate(page.get_images(full=True)):
                try:
                    pix = fitz.Pixmap(doc, img[0])
                    if pix.n - pix.alpha >= 4:
                        pix = fitz.Pixmap(fitz.csRGB, pix)
                    if pix.width < minw or pix.height < minh:
                        continue
                    pix.save(f"{out}/{key}_p{pi+1:02d}_{ii}.png")
                except Exception:
                    pass


def trim(im, pad=6):
    a = np.array(im.convert("RGB")); m = a.sum(axis=2) < 255 * 3 - 20; ys, xs = np.where(m)
    return im.convert("RGB").crop((max(xs.min() - pad, 0), max(ys.min() - pad, 0), min(xs.max() + pad, im.width), min(ys.max() + pad, im.height)))


def main():
    extract(SRC_IMGS, IM, 400, 300)
    extract(SRC_NEW, NW, 350, 250)
    # escudos ATM y RS recortados de la portada del deck Quality Servix
    pg = fitz.open(SRC_IMGS["qs"])[0].get_pixmap(dpi=300)
    pg.save(f"{CACHE}/qs_p1_300.png"); im = Image.open(f"{CACHE}/qs_p1_300.png"); s = im.size[0] / 1470
    trim(im.crop((int(270*s), int(470*s), int(400*s), int(605*s)))).save(f"{CACHE}/crest_rs_t.png")
    trim(im.crop((int(445*s), int(478*s), int(560*s), int(608*s)))).save(f"{CACHE}/crest_atm_t.png")
    trim(Image.open(SPORTING_LOGO)).save(f"{CACHE}/crest_sporting.png")
    for n in ("_DSC4194", "_DSC4176", "_DSC4155", "_DSC4266"):
        r = Image.open(f"{SPORTING_RES}/{n}.jpg").convert("RGB"); r.thumbnail((1800, 1800)); r.save(f"{NW}/spor_{n}.png")
    print("imágenes listas en", CACHE)


if __name__ == "__main__":
    main()
