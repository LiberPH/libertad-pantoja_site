"""Separadores del taller «La imagen y el narrador» para la FIL del Zócalo.

Separadores de 5 × 15 cm (56 × 156 mm con 3 mm de sangrado), ocho por hoja tabloide
(11 × 17 in): cuatro por fila, dos filas, separados 6 mm. Página 1: frente con los datos
del taller y un QR a su página. Página 2: reverso con la marca, en espejo por columnas para
imprimir a doble cara volteando por el lado largo.

Produce en _privado/separadores/ (no se publica):
  separadores-tabloide.pdf     las dos hojas, con marcas de corte
  separadores-frente.png, separadores-reverso.png   vistas previas

Uso, desde la raíz del sitio:  python _catalogo/separadores.py
Requiere Python con segno y pypdf, y Swift (usa _catalogo/exportar.swift).
"""

import shutil
import subprocess
from pathlib import Path

import segno
from pypdf import PdfWriter

RAIZ = Path(__file__).resolve().parent.parent
CAT = RAIZ / "_catalogo"
BUILD = CAT / "build" / "separadores"
SALIDA = RAIZ / "_privado/separadores"

MM = 72 / 25.4
HOJA_W, HOJA_H = 792, 1224
CORTE_W, CORTE_H, SANGRADO = 50, 150, 3
PIEZA_W, PIEZA_H = (CORTE_W + 2 * SANGRADO) * MM, (CORTE_H + 2 * SANGRADO) * MM
COLUMNAS, FILAS, SEP = 4, 2, 6 * MM
URL_TALLER = "https://liberph.github.io/libertad-pantoja_site/talleres/la-imagen-y-el-narrador/"

VERDE, TINTA, TINTA_MEDIA, MARFIL, GUINDA = "#2C5D4F", "#2A2622", "#635A51", "#FBF8F2", "#5A1F3A"

CSS = f"""
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ background: #fff; }}
.pagina {{ position: relative; width: {HOJA_W}px; height: {HOJA_H}px; overflow: hidden; background: #fff; }}
.pieza {{ position: absolute; width: {PIEZA_W:.2f}px; height: {PIEZA_H:.2f}px; overflow: hidden;
  background: {MARFIL}; color: {TINTA}; font-family: 'Hanken Grotesk', sans-serif; }}
.caja {{ position: absolute; left: {(SANGRADO + 5) * MM:.1f}px; right: {(SANGRADO + 5) * MM:.1f}px;
  top: {(SANGRADO + 8) * MM:.1f}px; bottom: {(SANGRADO + 7) * MM:.1f}px; display: flex; flex-direction: column; }}
.etiqueta {{ font-size: 6px; font-weight: 500; letter-spacing: .14em; text-transform: uppercase; color: {VERDE}; }}
.titulo {{ margin-top: 6px; font-family: 'Cormorant', serif; font-weight: 500; font-size: 21px; line-height: 1; color: {VERDE}; }}
.fil {{ display: block; width: 16px; height: .6px; background: {VERDE}; margin: 10px 0; }}
.con {{ font-family: 'Fraunces', serif; font-style: italic; font-size: 8.5px; line-height: 1.4; color: {TINTA_MEDIA}; }}
.lema {{ margin-top: 14px; font-family: 'Fraunces', serif; font-style: italic; font-size: 8px; line-height: 1.5; color: {TINTA_MEDIA}; }}
.datos {{ margin-top: 12px; font-size: 7.2px; line-height: 1.6; }}
.datos b {{ font-weight: 500; color: {VERDE}; }}
.pie {{ margin-top: auto; }}
.pie svg {{ display: block; width: {24 * MM:.1f}px; height: {24 * MM:.1f}px; }}
.inscr {{ margin-top: 6px; font-size: 6.4px; line-height: 1.5; color: {TINTA_MEDIA}; }}
.banda {{ position: absolute; left: 0; right: 0; bottom: 0; height: {(SANGRADO + 5) * MM:.1f}px; background: {GUINDA}; }}
.reverso .caja {{ align-items: center; justify-content: center; text-align: center; }}
.reverso img {{ width: 34px; height: 34px; }}
.reverso .nombre {{ margin-top: 10px; font-family: 'Cormorant', serif; font-weight: 500; font-size: 19px; line-height: 1; color: {VERDE}; }}
.reverso .oficio {{ margin-top: 8px; font-size: 5.8px; font-weight: 500; letter-spacing: .14em; text-transform: uppercase; color: {TINTA_MEDIA}; }}
.reverso .red {{ margin-top: 12px; font-size: 7px; color: {TINTA_MEDIA}; }}
.marca {{ position: absolute; background: #000; }}
"""


def qr_svg(url):
    return segno.make(url, error="m").svg_inline(scale=1, border=2, dark=TINTA, light=MARFIL, omitsize=True)


def marcas(x, y):
    s = SANGRADO * MM
    x0, y0, x1, y1 = x + s, y + s, x + PIEZA_W - s, y + PIEZA_H - s
    largo, sep, grosor = 7, 1.5, 0.4
    trazos = []
    for cx in (x0, x1):
        for cy in (y0, y1):
            if cy == y0:
                trazos.append(f'<i class="marca" style="left:{cx - grosor / 2:.1f}px;top:{cy - s - sep - largo:.1f}px;width:{grosor}px;height:{largo}px"></i>')
            else:
                trazos.append(f'<i class="marca" style="left:{cx - grosor / 2:.1f}px;top:{cy + s + sep:.1f}px;width:{grosor}px;height:{largo}px"></i>')
    for cy in (y0, y1):
        trazos.append(f'<i class="marca" style="left:{x0 - s - sep - largo:.1f}px;top:{cy - grosor / 2:.1f}px;width:{largo}px;height:{grosor}px"></i>')
        trazos.append(f'<i class="marca" style="left:{x1 + s + sep:.1f}px;top:{cy - grosor / 2:.1f}px;width:{largo}px;height:{grosor}px"></i>')
    return "".join(trazos)


def main():
    if BUILD.exists():
        shutil.rmtree(BUILD)
    BUILD.mkdir(parents=True)
    SALIDA.mkdir(parents=True, exist_ok=True)
    shutil.copy(RAIZ / "assets/img/marca/fugu.png", BUILD / "fugu.png")

    ox = (HOJA_W - COLUMNAS * PIEZA_W - (COLUMNAS - 1) * SEP) / 2
    oy = (HOJA_H - FILAS * PIEZA_H - (FILAS - 1) * SEP) / 2
    celdas = [(c, f) for f in range(FILAS) for c in range(COLUMNAS)]
    pos = lambda c, f: (ox + c * (PIEZA_W + SEP), oy + f * (PIEZA_H + SEP))

    frente = f"""<div class="caja">
  <p class="etiqueta">Taller en línea</p>
  <p class="titulo">La imagen<br>y el narrador</p>
  <span class="fil"></span>
  <p class="con">con Libertad Pantoja</p>
  <p class="lema">«La narrativa como un territorio de descubrimiento a través de la imagen y la voz.»</p>
  <p class="datos"><b>Martes 8:00 p.&nbsp;m.</b><br>desde el 20 de octubre<br>8 sesiones por Zoom<br>$2,500 MXN</p>
  <div class="pie">{qr_svg(URL_TALLER)}
    <p class="inscr">Inscripciones con Malabar Editorial<br>WhatsApp 55 1451 4556</p></div>
</div><div class="banda"></div>"""
    reverso = """<div class="caja"><img src="fugu.png" alt="">
  <p class="nombre">Libertad<br>Pantoja</p>
  <p class="oficio">Escritura · pintura · imagen</p>
  <p class="red">@libertadpantoja</p>
</div><div class="banda"></div>"""

    frentes = "".join(f'<div class="pieza" style="left:{pos(c, f)[0]:.1f}px;top:{pos(c, f)[1]:.1f}px">{frente}</div>' + marcas(*pos(c, f)) for c, f in celdas)
    reversos = "".join(f'<div class="pieza reverso" style="left:{pos(COLUMNAS - 1 - c, f)[0]:.1f}px;top:{pos(COLUMNAS - 1 - c, f)[1]:.1f}px">{reverso}</div>' + marcas(*pos(COLUMNAS - 1 - c, f)) for c, f in celdas)

    doc = f"""<!doctype html><html lang="es-MX"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant:wght@500&family=Fraunces:ital,opsz,wght@1,9..144,400&family=Hanken+Grotesk:wght@400;500&display=block">
<style>{CSS}</style></head><body>
<section class="pagina">{frentes}</section>
<section class="pagina">{reversos}</section>
</body></html>"""
    (BUILD / "separadores.html").write_text(doc)

    salida = BUILD / "pdf"
    salida.mkdir()
    exe = CAT / "build" / "exportar"
    if not exe.exists():
        subprocess.run(["swiftc", "-O", str(CAT / "exportar.swift"), "-o", str(exe)], check=True)
    subprocess.run([str(exe), str(BUILD / "separadores.html"), str(HOJA_W), str(HOJA_H), str(salida), "png"], check=True)

    escritor = PdfWriter()
    for pdf in sorted(salida.glob("p*.pdf")):
        escritor.append(str(pdf))
    escritor.add_metadata({"/Title": "Separadores · La imagen y el narrador", "/Author": "Libertad Pantoja"})
    with open(SALIDA / "separadores-tabloide.pdf", "wb") as f:
        escritor.write(f)
    shutil.copy(salida / "p01.png", SALIDA / "separadores-frente.png")
    shutil.copy(salida / "p02.png", SALIDA / "separadores-reverso.png")
    print("Listo:", SALIDA)


if __name__ == "__main__":
    main()
