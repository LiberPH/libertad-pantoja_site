"""Postales para la FIL del Zócalo: frentes y reversos impuestos en tabloide.

Cuatro postales de 10 × 15 cm (106 × 156 mm con 3 mm de sangrado), dos por fila y dos
filas por hoja, separadas 10 mm, en tabloide (11 × 17 in). Página 1: frentes. Página 2: reversos, con las
columnas invertidas para imprimir a doble cara volteando por el lado largo.

Imágenes: si existe `_privado/postales/<clave>.jpg` (archivo original en alta resolución) se
usa ese; si no, la imagen del sitio (1200 px como máximo), que solo sirve como prueba.

Produce en _privado/postales/ (no se publica):
  postales-tabloide.pdf        las dos hojas, con marcas de corte
  postales-frentes.png, postales-reversos.png   vistas previas

Uso, desde la raíz del sitio:  python _catalogo/postales.py
Requiere Python con segno, pillow, pyyaml y pypdf, y Swift (usa _catalogo/exportar.swift).
"""

import math
import shutil
import subprocess
import urllib.parse
from pathlib import Path

import segno
import yaml
from PIL import Image
from pypdf import PdfWriter

RAIZ = Path(__file__).resolve().parent.parent
CAT = RAIZ / "_catalogo"
BUILD = CAT / "build" / "postales"
SALIDA = RAIZ / "_privado/postales"

MM = 72 / 25.4
HOJA_W, HOJA_H = 792, 1224            # tabloide, 11 × 17 in, en puntos
CORTE_W, CORTE_H, SANGRADO = 100, 150, 3
CARTA_W, CARTA_H = (CORTE_W + 2 * SANGRADO) * MM, (CORTE_H + 2 * SANGRADO) * MM
SITIO = "https://liberph.github.io/libertad-pantoja_site/obra/"

VERDE, TINTA, TINTA_MEDIA, MARFIL = "#2C5D4F", "#2A2622", "#635A51", "#FBF8F2"

# clave: (título, recorte (centro x, centro y, alto relativo), cita de su historia)
POSTALES = {
    "peces-globo": ("El sueño de los peces globo", (0.40, 0.43, 0.86),
                    "El pez no tiene sangre ni entrañas, es como si fuera una fruta y Samantha dice que saben a guayaba."),
    "gato-blanco": ("El rescate del gato blanco", (0.50, 0.50, 1.00),
                    "El gato hablaba, agradecía en la lengua de los humanos."),
    "luz-insectos": ("La luz de los insectos", (0.62, 0.55, 0.95),
                     "El daimon de este dibujo está inspirado en un personaje de una novela que estoy escribiendo."),
    "fruto-hojarasca": ("El fruto de la hojarasca", (0.52, 0.45, 0.90),
                        "Al caminar por un parque, las cerezas de Jerusalén deslumbran como un fruto de la hojarasca."),
}


def slug(texto):
    """El mismo id que Jekyll da a cada ficha de obra (conserva los acentos)."""
    import re
    return re.sub(r"[^\w]+", "-", texto.lower()).strip("-")


def recortar(obra, clave, recorte):
    alta = SALIDA / f"{clave}.jpg"
    origen = alta if alta.exists() else RAIZ / obra["image"].lstrip("/")
    with Image.open(origen) as im:
        im = im.convert("RGB")
        W, H = im.size
        cx, cy, alto = recorte
        ch = H * alto
        cw = ch * CARTA_W / CARTA_H
        if cw > W:
            cw, ch = W, W * CARTA_H / CARTA_W
        x = min(max(W * cx - cw / 2, 0), W - cw)
        y = min(max(H * cy - ch / 2, 0), H - ch)
        pieza = im.crop((round(x), round(y), round(x + cw), round(y + ch)))
    ppp = pieza.width / ((CORTE_W + 2 * SANGRADO) / 25.4)
    destino = BUILD / f"{clave}.jpg"
    pieza.save(destino, quality=92)
    return destino.name, ppp, origen == alta


def qr_svg(url):
    return segno.make(url, error="m").svg_inline(scale=1, border=2, dark=TINTA, light=MARFIL, omitsize=True)


CSS = f"""
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ background: #fff; }}
.pagina {{ position: relative; width: {HOJA_W}px; height: {HOJA_H}px; overflow: hidden; background: #fff; }}
.carta {{ position: absolute; width: {CARTA_W:.2f}px; height: {CARTA_H:.2f}px; overflow: hidden; }}
.frente img {{ display: block; width: 100%; height: 100%; object-fit: cover; }}
.reverso {{ background: {MARFIL}; color: {TINTA}; font-family: 'Hanken Grotesk', sans-serif; }}
.caja {{ position: absolute; left: {(SANGRADO + 7) * MM:.1f}px; right: {(SANGRADO + 7) * MM:.1f}px;
  top: {(SANGRADO + 9) * MM:.1f}px; bottom: {(SANGRADO + 8) * MM:.1f}px; display: flex; flex-direction: column; }}
.titulo {{ font-family: 'Cormorant', serif; font-weight: 500; font-size: 20px; line-height: 1.05; color: {VERDE}; }}
.datos {{ margin-top: 5px; font-size: 7px; letter-spacing: .03em; color: {TINTA_MEDIA}; }}
.fil {{ display: block; width: 18px; height: .6px; background: {VERDE}; margin: 10px 0; }}
.cita {{ font-family: 'Fraunces', serif; font-style: italic; font-weight: 400; font-size: 9.5px; line-height: 1.5; color: {TINTA_MEDIA}; }}
.pie {{ margin-top: auto; display: flex; gap: 10px; align-items: flex-end; }}
.pie svg {{ width: {22 * MM:.1f}px; height: {22 * MM:.1f}px; flex: none; display: block; }}
.firma {{ font-size: 6.6px; line-height: 1.5; color: {TINTA_MEDIA}; }}
.firma strong {{ display: flex; align-items: center; gap: 4px; margin-bottom: 3px; font-family: 'Cormorant', serif;
  font-weight: 500; font-size: 12px; color: {VERDE}; }}
.firma img {{ width: 14px; height: 14px; }}
.marca {{ position: absolute; background: #000; }}
"""


def marcas(x, y):
    """Marcas de corte en las cuatro esquinas de la zona de corte de una postal."""
    s = SANGRADO * MM
    x0, y0, x1, y1 = x + s, y + s, x + CARTA_W - s, y + CARTA_H - s
    largo, sep, grosor = 9, 2, 0.4
    trazos = []
    for cx in (x0, x1):
        for cy in (y0, y1):
            dx = -1 if cx == x0 else 1
            dy = -1 if cy == y0 else 1
            hx = cx + dx * (s + sep) if dx > 0 else cx - s - sep - largo
            trazos.append(f'<i class="marca" style="left:{hx:.1f}px;top:{cy - grosor / 2:.1f}px;width:{largo}px;height:{grosor}px"></i>')
            vy = cy + dy * (s + sep) if dy > 0 else cy - s - sep - largo
            trazos.append(f'<i class="marca" style="left:{cx - grosor / 2:.1f}px;top:{vy:.1f}px;width:{grosor}px;height:{largo}px"></i>')
    return "".join(trazos)


def main():
    if BUILD.exists():
        shutil.rmtree(BUILD)
    BUILD.mkdir(parents=True)
    SALIDA.mkdir(parents=True, exist_ok=True)
    shutil.copy(RAIZ / "assets/img/marca/fugu.png", BUILD / "fugu.png")
    obras = {o["title"]: o for o in yaml.safe_load((RAIZ / "_data/obras.yml").read_text())}

    sep = 10 * MM  # separación entre postales: cada una conserva su sangrado y sus marcas
    ox = (HOJA_W - 2 * CARTA_W - sep) / 2
    oy = (HOJA_H - 2 * CARTA_H - sep) / 2
    pos = [(ox + c * (CARTA_W + sep), oy + f * (CARTA_H + sep)) for f in range(2) for c in range(2)]
    # Reversos: columnas invertidas para doble cara volteando por el lado largo.
    pos_rev = [(ox + (1 - c) * (CARTA_W + sep), oy + f * (CARTA_H + sep)) for f in range(2) for c in range(2)]

    frentes, reversos, avisos = [], [], []
    for i, (clave, (titulo, recorte, cita)) in enumerate(POSTALES.items()):
        obra = obras[titulo]
        archivo, ppp, alta = recortar(obra, clave, recorte)
        if ppp < 280:
            avisos.append(f"{titulo}: {ppp:.0f} ppp{' (original)' if alta else ' (imagen del sitio: solo prueba)'}")
        x, y = pos[i]
        frentes.append(f'<div class="carta frente" style="left:{x:.1f}px;top:{y:.1f}px"><img src="{archivo}" alt=""></div>' + marcas(x, y))
        url = SITIO + "#" + urllib.parse.quote(slug(titulo))
        datos = " · ".join(str(obra[k]) for k in ("technique", "year") if obra.get(k))
        x, y = pos_rev[i]
        reversos.append(f'''<div class="carta reverso" style="left:{x:.1f}px;top:{y:.1f}px"><div class="caja">
  <p class="titulo">{titulo}</p><p class="datos">{datos}</p><span class="fil"></span>
  <p class="cita">«{cita}»</p>
  <div class="pie">{qr_svg(url)}<p class="firma"><strong><img src="fugu.png" alt="">Libertad Pantoja</strong>
  Impresiones firmadas desde $250<br>y obra original en el sitio.<br>@libertadpantoja</p></div>
</div></div>''' + marcas(x, y))

    doc = f"""<!doctype html><html lang="es-MX"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant:wght@500&family=Fraunces:ital,opsz,wght@1,9..144,400&family=Hanken+Grotesk:wght@400;500&display=block">
<style>{CSS}</style></head><body>
<section class="pagina">{''.join(frentes)}</section>
<section class="pagina">{''.join(reversos)}</section>
</body></html>"""
    (BUILD / "postales.html").write_text(doc)

    salida = BUILD / "pdf"
    salida.mkdir()
    exe = CAT / "build" / "exportar"
    if not exe.exists():
        subprocess.run(["swiftc", "-O", str(CAT / "exportar.swift"), "-o", str(exe)], check=True)
    subprocess.run([str(exe), str(BUILD / "postales.html"), str(HOJA_W), str(HOJA_H), str(salida), "png"], check=True)

    escritor = PdfWriter()
    for pdf in sorted(salida.glob("p*.pdf")):
        escritor.append(str(pdf))
    escritor.add_metadata({"/Title": "Postales · Libertad Pantoja", "/Author": "Libertad Pantoja"})
    with open(SALIDA / "postales-tabloide.pdf", "wb") as f:
        escritor.write(f)
    shutil.copy(salida / "p01.png", SALIDA / "postales-frentes.png")
    shutil.copy(salida / "p02.png", SALIDA / "postales-reversos.png")
    print("Listo:", SALIDA)
    for a in avisos:
        print("  Resolución baja →", a)


if __name__ == "__main__":
    main()
