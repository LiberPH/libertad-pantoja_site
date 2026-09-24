"""Tarjeta de presentación: frente con la marca de agua del gato, reverso con QR a Obra.

Tamaño 9 × 5 cm con 3 mm de sangrado por lado (9.6 × 5.6 cm en total).
Frente (marfil): franja azul a la izquierda, «El rescate del gato blanco» como marca
de agua, nombre, oficio, teléfono y correo.
Reverso (marfil): usuario de Instagram, la línea de la artista, QR a la página de Obra
y franja guinda abajo.

Produce en _privado/tarjeta/ (no se publica):
  tarjeta-presentacion-imprenta.pdf   dos páginas con sangrado, para imprenta
  tarjeta-frente.png, tarjeta-reverso.png  vistas previas

Uso, desde la raíz del sitio:  python _catalogo/tarjeta.py
Requiere Python con segno, pypdf, numpy y pillow, y Swift (usa _catalogo/exportar.swift).
"""

import math
import shutil
import subprocess
from pathlib import Path

import numpy as np
import segno
import yaml
from PIL import Image
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
B = SANGRADO * MM

config = yaml.safe_load((RAIZ / "_config.yml").read_text())
URL_OBRA = "https://liberph.github.io/libertad-pantoja_site/obra/"
URL_INSTAGRAM = config["instagram"]
CORREO = config["email"]
TELEFONO = "55 3452 1622"

MARFIL, VERDE, GUINDA, AZUL, TINTA_MEDIA = "#FBF8F2", "#2C5D4F", "#5A1F3A", "#1B4A68", "#635A51"
AZUL_MARCA = (0x22, 0x5C, 0x80)  # el azul de la franja, un poco más claro para la pintura

PINTURA = RAIZ / "assets/img/obra/el-rescate-del-gato-blanco.jpg"
RECORTE = (140, 410, 640, 730)  # el gato y los brazos del niño
MARCA_ANCHO, MARCA_ALTO = 64 * MM, 41 * MM


def marca_de_agua(destino):
    """Tiñe el recorte de la pintura en azul sobre marfil.

    Los desvanecidos (viñeta, borde inferior y borde izquierdo) se hornean en la imagen
    porque mask-image sale negro al exportar a PDF con WebKit.
    """
    rgb = np.asarray(Image.open(PINTURA).convert("RGB").crop(RECORTE), float) / 255
    luz = rgb.mean(axis=2)
    bajo, alto = np.percentile(luz, 55), np.percentile(luz, 99.5)
    a = np.clip((luz - bajo) / (alto - bajo), 0, 1) ** 0.9
    h, w = a.shape
    y, x = np.mgrid[0:h, 0:w]
    a *= np.clip(1 - ((x / w - 0.45) ** 2 / 0.25 + (y / h - 0.5) ** 2 / 0.34), 0, 1) ** 0.6
    a *= np.clip((0.90 - y / h) / 0.30, 0, 1)            # abajo: se apaga entre 60 % y 90 %
    a *= np.clip(x / (w * 6 * MM / MARCA_ANCHO), 0, 1)   # izquierda: 6 mm de desvanecido
    fondo = np.array([251, 248, 242], float)
    tinta = np.array(AZUL_MARCA, float)
    opacidad = a[..., None] * 0.76
    img = fondo * (1 - opacidad) + tinta * opacidad
    Image.fromarray(img.astype("uint8")).resize((1500, 960), Image.LANCZOS).save(destino, quality=92)


def qr_svg(url):
    qr = segno.make(url, error="m")
    return qr.svg_inline(scale=1, border=2, dark=AZUL, light=MARFIL, omitsize=True)


CSS = f"""
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ background: {MARFIL}; }}
.pagina {{ position: relative; width: {W}px; height: {H}px; overflow: hidden; background: {MARFIL};
  font-family: 'Hanken Grotesk', sans-serif; color: #2A2622; }}
.abs {{ position: absolute; }}
.franja-izq {{ left: 0; top: 0; bottom: 0; width: {B + 6 * MM:.1f}px; background: {AZUL}; }}
.franja-abajo {{ left: 0; right: 0; bottom: 0; height: {B + 6 * MM:.1f}px; background: {GUINDA}; }}
.marca {{ right: -20px; top: 4px; width: {MARCA_ANCHO:.1f}px; height: {MARCA_ALTO:.1f}px;
  background: url(marca-tarjeta.jpg) center / cover; }}
.nombre {{ font-family: 'Cormorant', serif; font-weight: 500; font-size: 21px; line-height: .98;
  letter-spacing: -.01em; color: {VERDE}; }}
.fil {{ display: block; width: 16px; height: .6px; margin: 8px 0; }}
.oficio {{ margin-bottom: 3px; font-weight: 500; font-size: 6.6px; letter-spacing: .12em;
  text-transform: uppercase; color: {VERDE}; }}
.dato {{ font-size: 7px; line-height: 1.6; color: {GUINDA}; }}
.usuario {{ font-family: 'Cormorant', serif; font-weight: 500; font-size: 14px; color: {VERDE}; }}
.linea {{ font-family: 'Fraunces', serif; font-style: italic; font-weight: 400; font-size: 8px;
  line-height: 1.45; color: {TINTA_MEDIA}; }}
.qr svg {{ display: block; width: {19 * MM:.2f}px; height: {19 * MM:.2f}px; }}
.qr span {{ display: block; margin-top: 3px; text-align: center; font-weight: 500; font-size: 5.8px;
  letter-spacing: .14em; text-transform: uppercase; color: {AZUL}; }}
"""


def main():
    BUILD.mkdir(exist_ok=True)
    marca_de_agua(BUILD / "marca-tarjeta.jpg")

    usuario = "@" + URL_INSTAGRAM.rstrip("/").rsplit("/", 1)[-1]
    texto_izq = B + 11 * MM  # 5 mm libres junto a la franja de 6 mm
    frente = f"""
<section class="pagina">
  <div class="abs franja-izq"></div>
  <div class="abs marca"></div>
  <div class="abs" style="left:{texto_izq:.1f}px; top:{B + 6 * MM:.1f}px">
    <p class="nombre">Libertad<br>Pantoja</p>
    <span class="fil" style="background:{GUINDA}"></span>
  </div>
  <div class="abs" style="left:{texto_izq:.1f}px; bottom:{B + 6 * MM:.1f}px">
    <p class="oficio">Escritura · pintura · imagen</p>
    <p class="dato">{TELEFONO} · {CORREO}</p>
  </div>
</section>"""
    reverso = f"""
<section class="pagina">
  <div class="abs franja-abajo"></div>
  <div class="abs" style="left:{B + 6 * MM:.1f}px; top:{B + 6 * MM:.1f}px; width:{44 * MM:.1f}px">
    <p class="usuario">{usuario}</p>
    <span class="fil" style="background:{VERDE}; margin:10px 0"></span>
  </div>
  <div class="abs" style="left:{B + 6 * MM:.1f}px; bottom:34px; width:{52 * MM:.1f}px">
    <p class="linea">Escribo y pinto el territorio interior:<br>sueño, mito e inframundo.</p>
  </div>
  <div class="abs qr" style="right:{B + 6 * MM:.1f}px; top:{B + 6 * MM:.1f}px">{qr_svg(URL_OBRA)}<span>Ver obra</span></div>
</section>"""
    doc = f"""<!doctype html><html lang="es-MX"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant:wght@500&family=Fraunces:ital,opsz,wght@1,9..144,400&family=Hanken+Grotesk:wght@400;500&display=block">
<style>{CSS}</style></head><body>{frente}{reverso}</body></html>"""
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
