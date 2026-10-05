"""Catálogo del Archivo visual (Mundos pequeños), con el estilo del catálogo de obra.

Lee las fotografías de categoría «archivo-visual» de _data/obras.yml y arma un PDF carta
horizontal: portada, presentación, tres fotografías por página y «Cómo adquirir».

Produce en _privado/ (no se publica):
  catalogo-archivo-visual.pdf

Uso, desde la raíz del sitio:  python _catalogo/archivo.py
Requiere lo mismo que _catalogo/generar.py.
"""

import html
import shutil
import subprocess
import sys

import yaml
from PIL import Image
from pypdf import PdfWriter

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import generar  # noqa: E402  (reutiliza rutas, fecha y compresión)

RAIZ, CAT, BUILD = generar.RAIZ, generar.CAT, generar.BUILD / "archivo"
SALIDA = RAIZ / "_privado/catalogo-archivo-visual.pdf"
PORTADA = "Iris"

PRESENTACION = [
    "Las fotografías del archivo son de 2006 a 2017, hechas con cámaras compactas, empezando por mi "
    "primera cámara digital, una Canon PowerShot. Tomé estas fotos en mis tiempos de estudiante, "
    "principalmente cuando me paseaba por el Campus Morelos de la UNAM y por Ciudad Universitaria. "
    "Algunas de ellas provienen de paseos familiares o escapadas que hice al interior de la república "
    "en esos años.",
    "Fueron mis primeros acercamientos a los mundos pequeños: insectos, flores y seres pocas veces "
    "notados. Su resolución ya no alcanza para una impresión grande, así que las ofrezco en formato "
    "postal, firmadas.",
]

CSS_EXTRA = """
.h .presenta { grid-template-columns: 1fr 1fr; gap: 48px; align-items: center; }
.presenta p { font-size: 14px; line-height: 1.6; color: var(--tinta-relato); max-width: 58ch; }
.presenta p + p { margin-top: 12px; }
.presenta-foto img { display: block; width: 100%; height: 380px; object-fit: cover; }
.h .tres { grid-template-columns: repeat(3, 1fr); gap: 30px; align-items: start; align-content: center; }
.ficha .caja { height: 250px; display: flex; align-items: center; justify-content: center; }
.ficha .caja img { max-width: 100%; max-height: 250px; display: block; }
.ficha h3 { margin-top: 16px; font-weight: 400; font-size: 19px; color: var(--verde); }
.ficha .lugar { margin-top: 2px; font-style: italic; font-size: 13px; color: var(--tinta-media); }
.ficha .datos { margin-top: 8px; font-size: 12.5px; line-height: 1.45; color: var(--tinta-relato); }
.ficha .precio { margin-top: 6px; font-size: 14px; }
.ficha .precio span { color: var(--tinta-media); font-style: italic; font-size: 12.5px; }
.h .adquirir { grid-template-columns: 300px 1fr; gap: 48px; align-content: center; }
.adquirir li { font-size: 14px; line-height: 1.55; margin-bottom: 8px; list-style: none; }
.adquirir .contacto { margin-top: 18px; font-size: 13px; line-height: 1.6; color: var(--tinta-media); }
"""


def e(t):
    return html.escape(str(t), quote=True)


def main():
    config = yaml.safe_load((RAIZ / "_config.yml").read_text())
    obras = [o for o in yaml.safe_load((RAIZ / "_data/obras.yml").read_text()) if o.get("category") == "archivo-visual"]
    src = lambda o: "../../" + o["image"].lstrip("/")
    portada = next(o for o in obras if o["title"] == PORTADA)
    p = []
    p.append(f"""<section class="pagina marfil portada">
      <div class="portada-obra"><img class="obra" src="{e(src(portada))}" alt="" style="width:400px;height:auto"></div>
      <div class="portada-texto"><h1>Archivo visual</h1><span class="filete"></span>
        <p class="portada-sub">Mundos pequeños · fotografías 2006–2017</p>
        <p class="portada-linea">Libertad Pantoja</p></div></section>""")
    otra = next(o for o in obras if o["title"] == "Nono")
    p.append(f"""<section class="pagina marfil presenta">
      <div><h2>Mundos pequeños</h2><span class="filete"></span>{''.join(f'<p>{e(t)}</p>' for t in PRESENTACION)}</div>
      <div class="presenta-foto"><img src="{e(src(otra))}" alt=""></div></section>""")
    for i in range(0, len(obras), 3):
        fichas = []
        for o in obras[i:i + 3]:
            lugar = f'<p class="lugar">{e(o["subtitle"])}</p>' if o.get("subtitle") else ""
            nota = f'<br><span>{e(o["price_note"])}</span>' if o.get("price_note") else ""
            fichas.append(f"""<div class="ficha"><div class="caja"><img src="{e(src(o))}" alt=""></div>
              <h3>{e(o['title'])}</h3>{lugar}
              <p class="datos">Fotografía de archivo · impresión firmada<br>{e(o['dimensions'])}</p>
              <p class="precio">{e(o['price'].split(' · ')[0])}{nota}</p></div>""")
        p.append(f'<section class="pagina marfil tres">{"".join(fichas)}</section>')
    p.append(f"""<section class="pagina marfil adquirir">
      <div><h2>Cómo adquirir</h2><span class="filete"></span></div>
      <div><ul>
        <li>Impresión postal (10 × 15 cm), firmada: <strong>$250 MXN</strong> cada una, o tres por <strong>$600 MXN</strong>.</li>
        <li><em>Iris</em>, <em>Nono</em> y <em>Cuerno</em> también en 13 × 18 cm: <strong>$450 MXN</strong>.</li>
        <li>Envío aparte, o entrega en persona en la Ciudad de México.</li>
        <li>Escríbeme con el título de las fotografías que te interesan.</li></ul>
        <p class="contacto">Correo: {e(config['email'])}<br>Instagram: @libertadpantoja<br>{e(generar.SITIO_CORTO)}/obra/#archivo-visual</p>
      </div></section>""")
    for n, s in enumerate(p[1:], start=2):
        p[n - 1] = s.replace("</section>", f'<p class="folio">{n}</p></section>', 1) if n > 1 else s

    css = (CAT / "catalogo.css").read_text() + CSS_EXTRA
    doc = f"""<!doctype html><html lang="es-MX"><head><meta charset="utf-8"><title>Archivo visual · Libertad Pantoja</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400;1,500&family=Libre+Caslon+Display&family=Libre+Caslon+Text:ital@1&display=block">
<style>{css}</style></head><body class="h">{''.join(p)}</body></html>"""
    if BUILD.exists():
        shutil.rmtree(BUILD)
    BUILD.mkdir(parents=True)
    html_path = generar.BUILD / "catalogo-archivo.html"
    html_path.write_text(doc)
    salida = BUILD / "pdf"
    salida.mkdir()
    exe = generar.BUILD / "exportar"
    if not exe.exists():
        subprocess.run(["swiftc", "-O", str(CAT / "exportar.swift"), "-o", str(exe)], check=True)
    subprocess.run([str(exe), str(html_path), "792", "612", str(salida)], check=True)
    escritor = PdfWriter()
    for pdf in sorted(salida.glob("p*.pdf")):
        escritor.append(str(pdf))
    escritor.add_metadata({"/Title": "Archivo visual · Libertad Pantoja", "/Author": "Libertad Pantoja"})
    crudo = salida / "unido.pdf"
    with open(crudo, "wb") as f:
        escritor.write(f)
    generar.comprimir(crudo, SALIDA, html_path)
    print("Listo:", SALIDA)


if __name__ == "__main__":
    main()
