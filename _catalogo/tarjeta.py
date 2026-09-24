"""Tarjeta de presentación con dos códigos QR (Obra e Instagram).

Tamaño 9 × 5 cm con 3 mm de sangrado por lado (9.6 × 5.6 cm en total).
Frente (marfil): nombre, oficio, correo y QR a la página de Obra.
Reverso (noche): Instagram, la línea de la artista y QR a Instagram.

Produce en _privado/tarjeta/ (no se publica):
  tarjeta-presentacion-imprenta.pdf   dos páginas con sangrado, para imprenta
  tarjeta-frente.png, tarjeta-reverso.png  vistas previas

Uso, desde la raíz del sitio:  python _catalogo/tarjeta.py
Requiere Python con segno y pypdf, y Swift (usa _catalogo/exportar.swift).
"""

import math
import shutil
import subprocess
from pathlib import Path

import segno
import yaml
from pypdf import PdfWriter

RAIZ = Path(__file__).resolve().parent.parent
CAT = RAIZ / "_catalogo"
BUILD = CAT / "build"
SALIDA = RAIZ / "_privado/tarjeta"

MM = 72 / 25.4  # puntos por milímetro
ANCHO, ALTO, SANGRADO = 90, 50, 3
# WebKit usa puntos enteros: se redondea hacia arriba (el sangrado queda en ~3.1 mm).
W = math.ceil((ANCHO + 2 * SANGRADO) * MM)
H = math.ceil((ALTO + 2 * SANGRADO) * MM)

config = yaml.safe_load((RAIZ / "_config.yml").read_text())
URL_OBRA = "https://liberph.github.io/libertad-pantoja_site/obra/"
URL_INSTAGRAM = config["instagram"]
CORREO = config["email"]


def qr_svg(url):
    qr = segno.make(url, error="m")
    return qr.svg_inline(scale=1, border=2, dark="#16091E", light="#FBF8F2", omitsize=True)


CSS = f"""
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ background: #FBF8F2; }}
.pagina {{
  position: relative; width: {W}px; height: {H}px; overflow: hidden;
  display: grid; grid-template-columns: 1fr {26 * MM:.2f}px; align-items: center;
  column-gap: {5 * MM:.2f}px;
  padding: {(SANGRADO + 5) * MM:.2f}px {(SANGRADO + 5) * MM:.2f}px;
}}
.frente {{ background: #FBF8F2; color: #2A2622; }}
.reverso {{ background: #16091E; color: #F4E3C8; }}
h1 {{ font-family: 'Cormorant', serif; font-weight: 500; font-size: 22px; line-height: 1; letter-spacing: -0.01em; color: #2C5D4F; }}
.filete {{ display: block; width: 18px; height: 0.6px; background: #2C5D4F; margin: 7px 0 7px; }}
.oficio {{ font-family: 'Hanken Grotesk', sans-serif; font-weight: 600; font-size: 6.4px; letter-spacing: 0.12em; text-transform: uppercase; color: #2A2622; }}
.dato {{ margin-top: 3px; font-family: 'Hanken Grotesk', sans-serif; font-size: 6.6px; color: #635A51; }}
.reverso h2 {{ font-family: 'Cormorant', serif; font-weight: 500; font-size: 17px; line-height: 1.05; color: #F4E3C8; }}
.reverso .filete {{ background: #F6A13A; }}
.linea {{ font-family: 'Cormorant', serif; font-style: italic; font-size: 9px; line-height: 1.3; color: #D8C3A8; }}
.qr {{ display: flex; flex-direction: column; align-items: center; gap: 3px; }}
.qr svg {{ width: {24 * MM:.2f}px; height: {24 * MM:.2f}px; display: block; }}
.qr span {{ font-family: 'Hanken Grotesk', sans-serif; font-weight: 600; font-size: 5.6px; letter-spacing: 0.14em; text-transform: uppercase; }}
.frente .qr span {{ color: #2C5D4F; }}
.marco {{ background: #FBF8F2; padding: {1.4 * MM:.2f}px; line-height: 0; }}
.marco svg {{ width: {21.2 * MM:.2f}px; height: {21.2 * MM:.2f}px; }}
.reverso .qr span {{ color: #F6A13A; }}
"""


def main():
    usuario = "@" + URL_INSTAGRAM.rstrip("/").rsplit("/", 1)[-1]
    frente = f"""
<section class="pagina frente">
  <div>
    <h1>Libertad Pantoja</h1>
    <span class="filete"></span>
    <p class="oficio">Escritura · pintura · imagen</p>
    <p class="dato">{CORREO}</p>
  </div>
  <div class="qr">{qr_svg(URL_OBRA)}<span>Ver obra</span></div>
</section>"""
    reverso = f"""
<section class="pagina reverso">
  <div>
    <h2>{usuario}</h2>
    <span class="filete"></span>
    <p class="linea">Escribo y pinto el territorio interior:<br>sueño, mito e inframundo.</p>
  </div>
  <div class="qr"><div class="marco">{qr_svg(URL_INSTAGRAM)}</div><span>Instagram</span></div>
</section>"""
    doc = f"""<!doctype html><html lang="es-MX"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant:ital,wght@0,500;1,500&family=Hanken+Grotesk:wght@400;600&display=block">
<style>{CSS}</style></head><body>{frente}{reverso}</body></html>"""
    BUILD.mkdir(exist_ok=True)
    (BUILD / "tarjeta.html").write_text(doc)

    salida = BUILD / "tarjeta"
    if salida.exists():
        shutil.rmtree(salida)
    salida.mkdir()
    exe = BUILD / "exportar"
    if not exe.exists():
        subprocess.run(["swiftc", "-O", str(CAT / "exportar.swift"), "-o", str(exe)], check=True)
    subprocess.run([str(exe), str(BUILD / "tarjeta.html"), str(W), str(H), str(salida), "png"], check=True)

    SALIDA.mkdir(parents=True, exist_ok=True)
    escritor = PdfWriter()
    for pdf in sorted(salida.glob("p*.pdf")):
        escritor.append(str(pdf))
    escritor.add_metadata({"/Title": "Tarjeta de presentación · Libertad Pantoja", "/Author": "Libertad Pantoja"})
    with open(SALIDA / "tarjeta-presentacion-imprenta.pdf", "wb") as f:
        escritor.write(f)
    shutil.copy(salida / "p01.png", SALIDA / "tarjeta-frente.png")
    shutil.copy(salida / "p02.png", SALIDA / "tarjeta-reverso.png")
    print("Listo:", SALIDA, f"({W} × {H} pt con sangrado)")


if __name__ == "__main__":
    main()
