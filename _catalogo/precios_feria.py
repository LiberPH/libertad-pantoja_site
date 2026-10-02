"""Tarjeta de precios para el stand de Malabar en la FIL del Zócalo.

Media carta vertical (14 × 21.6 cm), sin sangrado: se imprime en cualquier hoja carta o
tabloide y se recorta a mano. Lleva dos QR: a la página del taller y a Obra.

Produce en _privado/feria/ (no se publica):
  tarjeta-precios.pdf, tarjeta-precios.png

Uso, desde la raíz del sitio:  python _catalogo/precios_feria.py
Requiere Python con segno y pypdf, y Swift (usa _catalogo/exportar.swift).
"""

import shutil
import subprocess
from pathlib import Path

import segno

RAIZ = Path(__file__).resolve().parent.parent
CAT = RAIZ / "_catalogo"
BUILD = CAT / "build" / "precios"
SALIDA = RAIZ / "_privado/feria"

W, H = 396, 612  # media carta en puntos
SITIO = "https://liberph.github.io/libertad-pantoja_site/"
VERDE, TINTA, TINTA_MEDIA, MARFIL, GUINDA = "#2C5D4F", "#2A2622", "#635A51", "#FBF8F2", "#5A1F3A"

PRODUCTOS = [
    ("Postal", "$40"),
    ("3 postales", "$100"),
    ("Colección de 4 postales", "$130"),
    ("Fanzine <em>El ángel Hertebiuse</em>", "$120"),
]


def qr(url):
    return segno.make(url, error="m").svg_inline(scale=1, border=2, dark=TINTA, light=MARFIL, omitsize=True)


CSS = f"""
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ background: {MARFIL}; }}
.pagina {{ position: relative; width: {W}px; height: {H}px; overflow: hidden; background: {MARFIL};
  color: {TINTA}; font-family: 'Hanken Grotesk', sans-serif; padding: 40px 38px 0; }}
.cabeza {{ display: flex; align-items: center; gap: 10px; }}
.cabeza img {{ width: 34px; height: 34px; }}
.nombre {{ font-family: 'Cormorant', serif; font-weight: 500; font-size: 30px; line-height: 1; color: {VERDE}; }}
.oficio {{ margin-top: 6px; font-size: 7.5px; font-weight: 500; letter-spacing: .14em; text-transform: uppercase; color: {TINTA_MEDIA}; }}
.fil {{ display: block; width: 26px; height: .8px; background: {VERDE}; margin: 22px 0 16px; }}
table {{ width: 100%; border-collapse: collapse; }}
td {{ padding: 9px 0; border-bottom: .6px solid rgba(42,38,34,.18); font-size: 14px; }}
td:last-child {{ text-align: right; font-family: 'Fraunces', serif; font-weight: 500; font-size: 17px; white-space: nowrap; }}
td em {{ font-family: 'Fraunces', serif; font-style: italic; font-weight: 400; }}
.nota {{ margin-top: 10px; font-size: 9.5px; line-height: 1.5; color: {TINTA_MEDIA}; }}
.qrs {{ display: grid; grid-template-columns: 1fr 1fr; gap: 18px; margin-top: 26px; }}
.qrs svg {{ display: block; width: 92px; height: 92px; }}
.qrs p {{ margin-top: 7px; font-size: 9.5px; line-height: 1.4; }}
.qrs strong {{ display: block; font-family: 'Cormorant', serif; font-weight: 500; font-size: 16px; color: {VERDE}; margin-bottom: 2px; }}
.pie {{ position: absolute; left: 38px; right: 38px; bottom: 34px; font-size: 9.5px; color: {TINTA_MEDIA}; }}
.banda {{ position: absolute; left: 0; right: 0; bottom: 0; height: 14px; background: {GUINDA}; }}
"""


def main():
    if BUILD.exists():
        shutil.rmtree(BUILD)
    BUILD.mkdir(parents=True)
    SALIDA.mkdir(parents=True, exist_ok=True)
    shutil.copy(RAIZ / "assets/img/marca/fugu.png", BUILD / "fugu.png")
    filas = "".join(f"<tr><td>{n}</td><td>{p}</td></tr>" for n, p in PRODUCTOS)
    html = f"""<!doctype html><html lang="es-MX"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant:wght@500&family=Fraunces:ital,opsz,wght@0,9..144,500;1,9..144,400&family=Hanken+Grotesk:wght@400;500&display=block">
<style>{CSS}</style></head><body><section class="pagina">
  <div class="cabeza"><img src="fugu.png" alt=""><div><p class="nombre">Libertad Pantoja</p>
  <p class="oficio">Escritura · pintura · imagen</p></div></div>
  <span class="fil"></span>
  <table>{filas}</table>
  <p class="nota">Llévate gratis el separador del taller.</p>
  <div class="qrs">
    <div>{qr(SITIO + "talleres/la-imagen-y-el-narrador/")}<p><strong>Taller en línea</strong><em>La imagen y el narrador</em><br>Martes 8 p.&nbsp;m. por Zoom, desde el 20 de octubre</p></div>
    <div>{qr(SITIO + "obra/")}<p><strong>Obra</strong>Originales e impresiones firmadas desde $250</p></div>
  </div>
  <p class="pie">@libertadpantoja</p>
  <div class="banda"></div>
</section></body></html>"""
    (BUILD / "precios.html").write_text(html)
    salida = BUILD / "pdf"
    salida.mkdir()
    exe = CAT / "build" / "exportar"
    if not exe.exists():
        subprocess.run(["swiftc", "-O", str(CAT / "exportar.swift"), "-o", str(exe)], check=True)
    subprocess.run([str(exe), str(BUILD / "precios.html"), str(W), str(H), str(salida), "png"], check=True)
    shutil.copy(salida / "p01.pdf", SALIDA / "tarjeta-precios.pdf")
    shutil.copy(salida / "p01.png", SALIDA / "tarjeta-precios.png")
    print("Listo:", SALIDA)


if __name__ == "__main__":
    main()
