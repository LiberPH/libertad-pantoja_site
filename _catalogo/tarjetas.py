"""Genera las tarjetas para compartir (Open Graph) de las páginas principales.

Produce assets/img/compartir/<pagina>.jpg a 1200 × 630 px: una obra o el retrato
a la izquierda y el nombre en verde a la derecha, con la estética del catálogo.

Uso, desde la raíz del sitio:  python _catalogo/tarjetas.py
Requiere Python con pillow y Swift (usa _catalogo/exportar.swift).
"""

import html
import shutil
import subprocess
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
CAT = RAIZ / "_catalogo"
BUILD = CAT / "build"
SALIDA = RAIZ / "assets/img/compartir"

# pagina: (imagen, recorte, línea 1, línea 2)
# recorte: "cubrir" para fotos (se puede recortar), "completa" para obra (nunca se recorta).
TARJETAS = {
    "inicio": ("assets/img/home/hero-obra.jpg", "cubrir", "Escritura · pintura · imagen", "Escribo y pinto el territorio interior"),
    "obra": ("assets/img/obra/lo-que-deje-secar.jpg", "completa", "Obra", "Pintura, dibujo y fotografía"),
    "publicaciones": ("assets/img/publicaciones/tu-enfermo-no-estas.jpg", "completa", "Libros y publicaciones", "Cuentos, antologías y revistas"),
    "bio": ("assets/img/perfil/hero-obra.jpg", "cubrir", "Bio", "Narradora y artista visual"),
    "club": ("assets/img/obra/el-rescate-del-gato-blanco.jpg", "completa", "Club de lectura", "Los sueños y el inframundo"),
    "talleres": ("assets/img/obra/el-rescate-del-gato-blanco.jpg", "completa", "Talleres", "Escritura, imagen y narración"),
}

CSS = """
* { margin: 0; box-sizing: border-box; }
html, body { background: #FBF8F2; }
.pagina { width: 1200px; height: 630px; display: grid; grid-template-columns: 520px 1fr; overflow: hidden; background: #FBF8F2; }
.obra { background: #16091E; display: flex; align-items: center; justify-content: center; overflow: hidden; }
.obra.completa { padding: 36px; }
.obra.completa img { width: 100%; height: 100%; object-fit: contain; display: block; }
.obra.cubrir img { width: 100%; height: 100%; object-fit: cover; object-position: 55% 30%; display: block; }
.texto { padding: 70px 64px; display: flex; flex-direction: column; justify-content: center; }
h1 { font-family: 'Cormorant', serif; font-weight: 500; font-size: 96px; line-height: .95; color: #2C5D4F; letter-spacing: -.02em; }
.filete { display: block; width: 70px; height: 2px; background: #2C5D4F; margin-top: 30px; }
.l1 { margin-top: 28px; font-family: 'Hanken Grotesk', sans-serif; font-weight: 600; font-size: 28px; color: #2A2622; }
.l2 { margin-top: 8px; font-family: 'Hanken Grotesk', sans-serif; font-weight: 500; font-size: 25px; color: #635A51; }
"""


def main():
    BUILD.mkdir(exist_ok=True)
    paginas = []
    for nombre, (img, modo, l1, l2) in TARJETAS.items():
        paginas.append(f"""
<section class="pagina">
  <div class="obra {modo}"><img src="../../{img}" alt=""></div>
  <div class="texto">
    <h1>Libertad<br>Pantoja</h1>
    <span class="filete"></span>
    <p class="l1">{html.escape(l1)}</p>
    <p class="l2">{html.escape(l2)}</p>
  </div>
</section>""")
    doc = f"""<!doctype html><html lang="es-MX"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant:wght@500&family=Hanken+Grotesk:wght@500;600&display=block">
<style>{CSS}</style></head><body>{''.join(paginas)}</body></html>"""
    (BUILD / "tarjetas.html").write_text(doc)

    salida = BUILD / "tarjetas"
    if salida.exists():
        shutil.rmtree(salida)
    salida.mkdir()
    exe = BUILD / "exportar"
    if not exe.exists():
        subprocess.run(["swiftc", "-O", str(CAT / "exportar.swift"), "-o", str(exe)], check=True)
    subprocess.run([str(exe), str(BUILD / "tarjetas.html"), "1200", "630", str(salida), "png"], check=True)

    SALIDA.mkdir(parents=True, exist_ok=True)
    for i, nombre in enumerate(TARJETAS, start=1):
        with Image.open(salida / f"p{i:02d}.png") as im:
            im.convert("RGB").resize((1200, 630), Image.LANCZOS).save(
                SALIDA / f"{nombre}.jpg", quality=85, optimize=True, progressive=True)
    print("Listo:", SALIDA)


if __name__ == "__main__":
    main()
