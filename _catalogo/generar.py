"""Genera el catálogo de obra desde _data/obras.yml.

Produce:
  assets/docs/catalogo-libertad-pantoja.pdf           horizontal (carta), para descarga y correo
  assets/docs/catalogo-libertad-pantoja-vertical.pdf  vertical 4:5, para WhatsApp
  _privado/instagram/catalogo-NN.png                  1080 × 1350, para carrusel de Instagram
  _data/catalogo.yml                                  fecha y peso, para el enlace de descarga en Obra

Requiere Python con pyyaml, pillow, pypdf y pymupdf, y Swift (Xcode Command Line Tools).
Uso, desde la raíz del sitio:  python _catalogo/generar.py
Con --sin-instagram (o en GitHub Actions) no genera las imágenes de Instagram.
Se corre solo en GitHub Actions al cambiar obras o precios (.github/workflows/catalogo.yml).
"""

import datetime
import html
import os
import re
import shutil
import subprocess
import sys
import urllib.parse
from pathlib import Path

import yaml
from PIL import Image
from pypdf import PdfWriter

RAIZ = Path(__file__).resolve().parent.parent
CAT = RAIZ / "_catalogo"
BUILD = CAT / "build"

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
_hoy = datetime.date.today()
FECHA = f"{MESES[_hoy.month - 1]} {_hoy.year}"
SITIO = "https://liberph.github.io/libertad-pantoja_site/"
SITIO_CORTO = "liberph.github.io/libertad-pantoja_site"

# ---------------------------------------------------------------------------
# Textos del catálogo (tomados del catálogo de septiembre 2026)
# ---------------------------------------------------------------------------

SOBRE = [
    "Trabajo en el diálogo entre la imagen y el relato. Mi práctica abarca la fotografía, el óleo, "
    "el pastel, el lápiz de color y la tinta, y se apoya en lo onírico, la mitología y la psicología "
    "profunda junguiana y hillmaniana.",
    "Formada en ciencias genómicas y biomédicas por la UNAM. En 2021 publiqué el libro de cuentos "
    "<em>Tú, enfermo no estás</em> (Malabar Editorial). Desde 2026 formo parte del taller de proyectos "
    "pictóricos de Darío Salzman, donde participé en la exposición colectiva <em>Manifestación</em>.",
    "Este catálogo reúne dos frentes de mi trabajo: una obra onírica de dibujo y pintura, y la serie "
    "fotográfica <em>Hadas urbanas</em>.",
]

ONIRICA = [
    "En ocasiones despertamos con la certeza de haber tenido un sueño y nos queda apenas un resabio "
    "de lo que fue: una atmósfera, un color o una inquietud. En otras ocasiones recordamos el sueño "
    "completo, vívido y a detalle. Tanto la serie de sensaciones e imágenes imprecisas como las vívidas "
    "imágenes del sueño constituyen una parte esencial de la materia prima de mis dibujos y pinturas.",
    "Estas piezas parten de un sueño o de una imagen recibida. El color restituye su atmósfera. "
    "Criaturas híbridas, escenas nocturnas, recuerdos transfigurados: lo que el sueño deja.",
]

HADAS = [
    "Insectos y flores encontrados en entornos urbanos. La macrofotografía convierte en protagonistas "
    "de su propia ficción a las criaturas que suelen pasar inadvertidas: un reino diminuto que "
    "sobrevive a la vista de todos, en parques, jardines y grietas de la ciudad.",
]

PASOS = [
    "Escríbeme por Instagram o correo la pieza que te interesa.",
    "Te confirmo disponibilidad y acordamos el pago.",
    "Entrega en persona en la Ciudad de México o envío asegurado a todo México, con costo según destino.",
]

CONDICIONES = [
    "Las ediciones limitadas van firmadas, numeradas y con certificado de autenticidad.",
    "Cada original indica si se entrega enmarcado. Las obras sin marco viajan de forma más económica y segura.",
    "Apartado con el 50 %; el resto contra entrega. Transferencia bancaria o efectivo.",
    "Los precios en dólares son de referencia y pueden ajustarse según el tipo de cambio.",
]

CIERRE = "Si esta obra encuentra a alguien de tu círculo, gracias por acercarla."
LINEA = "Escribo y pinto el territorio interior: sueño, mito e inframundo."

# ---------------------------------------------------------------------------
# Datos
# ---------------------------------------------------------------------------


def cargar():
    config = yaml.safe_load((RAIZ / "_config.yml").read_text())
    obras = yaml.safe_load((RAIZ / "_data/obras.yml").read_text())
    ui = yaml.safe_load((RAIZ / "_data/ui.yml").read_text())["obra"]
    onirica = [o for o in obras if o.get("category") in ("original", "edicion-limitada")]
    hadas = [o for o in obras if o.get("category") == "fotografia"]
    for o in onirica + hadas:
        ruta = RAIZ / o["image"].lstrip("/")
        o["ruta"] = ruta
        with Image.open(ruta) as im:
            o["aspecto"] = im.width / im.height
        o["serie"] = "Obra onírica" if o in onirica else "Hadas urbanas"
    return config, ui, onirica, hadas


def e(texto):
    return html.escape(str(texto), quote=True)


def partir_relato(texto):
    """Primera oración como verso destacado; el resto como relato."""
    texto = " ".join(str(texto or "").split())
    partes = re.split(r"(?<=[.!?])\s+", texto, maxsplit=1)
    return partes[0], (partes[1] if len(partes) > 1 else "")


def recortar(texto, palabras):
    """Corta en la última oración completa que cabe; si ninguna cabe, en una pausa."""
    if len(texto.split()) <= palabras:
        return texto
    oraciones = re.split(r"(?<=[.!?])\s+", texto)
    corto = ""
    for o in oraciones:
        prueba = (corto + " " + o).strip()
        if len(prueba.split()) > palabras:
            break
        corto = prueba
    if corto:
        return corto
    lista = texto.split()[:palabras]
    frase = " ".join(lista)
    corte = max(frase.rfind(","), frase.rfind(";"), frase.rfind(":"))
    if corte > len(frase) // 2:
        frase = frase[:corte]
    return frase.rstrip(",;: ") + "…"


def mailto(config, ui, o):
    asunto = f"{ui['mail_subject']} {o['title']}"
    linea = f"{ui['mail_interest']} «{o['title']}»"
    if o.get("edition"):
        linea += f" ({o['edition']})"
    cuerpo = f"{ui['mail_greeting']}\n\n{linea}."
    q = urllib.parse.urlencode({"subject": asunto, "body": cuerpo}, quote_via=urllib.parse.quote)
    return f"mailto:{config['email']}?{q}"


def estado(ui, o):
    st = ui["status"].get(o.get("status"), {})
    return st.get("label", o.get("status", "")), st.get("show_price", True)


# ---------------------------------------------------------------------------
# Piezas de la plantilla
# ---------------------------------------------------------------------------


def src(o):
    return "../../" + o["image"].lstrip("/")


def obra_img(ruta, aspecto, caja_w, caja_h, alt, clase="obra"):
    """La obra ajustada a una caja, sin recortes ni marco."""
    w, h = caja_w, caja_w / aspecto
    if h > caja_h:
        h, w = caja_h, caja_h * aspecto
    return f'<img class="{clase}" src="{e(ruta)}" alt="{e(alt)}" style="width:{w:.0f}px;height:{h:.0f}px">'


def datos(o):
    linea1 = e(o.get("technique", ""))
    resto = " · ".join(e(o[k]) for k in ("dimensions", "edition", "year") if o.get(k))
    return f'<p class="datos">{linea1}<br>{resto}</p>'


def precio(ui, o, config, compacto=False):
    etiqueta, mostrar = estado(ui, o)
    partes = []
    if mostrar and o.get("price"):
        if o.get("price_framed"):
            partes.append(
                f'<p class="precio">{e(o["price"])} <span>{e(ui["price_unframed"].lower())}</span></p>'
                f'<p class="precio">{e(o["price_framed"])} <span>{e(ui["price_framed"].lower())}</span></p>'
            )
        else:
            marco = f' <span>{e(o["framing"].lower())}</span>' if o.get("framing") else ""
            partes.append(f'<p class="precio">{e(o["price"])}{marco}</p>')
        if not compacto and (o.get("price_varies") or "Desde" in str(o.get("price"))):
            partes.append(f'<p class="nota">{e(ui["price_varies_note"])}</p>')
    else:
        partes.append(f'<p class="precio">{e(etiqueta)}</p>')
    if mostrar and not compacto:
        partes.append(f'<a class="escribir" href="{e(mailto(config, ui, o))}">Escribir por esta pieza</a>')
    return f'<div class="compra-pieza">{"".join(partes)}</div>'


def folio(n):
    return f'<span class="folio">{n}</span>'


# ---------------------------------------------------------------------------
# Páginas
# ---------------------------------------------------------------------------


def paginas(fmt, config, ui, onirica, hadas):
    H = fmt == "h"
    obras = onirica + hadas
    luz = next(o for o in obras if o["title"] == "La luz de los insectos")
    p = []

    # Portada
    img = obra_img(src(luz), luz["aspecto"], 400 if H else 472, 440 if H else 330, luz["title"])
    p.append(("marfil portada", f"""
      <div class="portada-obra">{img}</div>
      <div class="portada-texto">
        <h1>Libertad{'<br>' if H else ' '}Pantoja</h1>
        <span class="filete"></span>
        <p class="portada-sub">Catálogo de obra · {FECHA}</p>
        <p class="portada-linea">{e(LINEA)}</p>
      </div>"""))

    # Sobre mi obra
    parrafos = "".join(f"<p>{t}</p>" for t in SOBRE)
    p.append(("marfil sobre", f"""
      <figure class="sobre-foto"><img src="../img/taller.jpg" alt="Libertad Pantoja dibujando en su taller"></figure>
      <div class="sobre-texto"><h2>Sobre mi obra</h2>{parrafos}<p class="credito">Fotografía del taller: RV</p></div>"""))

    # Índice
    celdas = []
    for o in obras:
        etiqueta, mostrar = estado(ui, o)
        cifra = o["price"].split("·")[0].strip() if (mostrar and o.get("price")) else etiqueta
        if mostrar and o.get("category") != "original":
            cifra += " · impresión"
        celdas.append(f"""
          <li><img src="{e(src(o))}" alt="">
            <span class="indice-titulo">{e(o['title'])}</span>
            <span class="indice-precio">{e(cifra)}</span></li>""")
    p.append(("marfil indice", f"""
      <div class="indice-cabeza"><h2>Obras</h2>
        <p>Precios sin marco, en pesos mexicanos. Los detalles, en la página de cada obra.</p></div>
      <ol class="indice">{''.join(celdas)}</ol>"""))

    # Series
    for nombre, intro, lista, fondo in (("Obra onírica", ONIRICA, onirica, "gris"),
                                        ("Hadas urbanas", HADAS, hadas, "marfil")):
        texto = "".join(f"<p>{t}</p>" for t in intro)
        p.append((f"{fondo} portadilla", f"""
          <div class="portadilla-texto"><h2>{e(nombre)}</h2><span class="filete"></span>{texto}</div>"""))
        for o in lista:
            verso, resto = partir_relato(o.get("description"))
            if H:
                ancha = o["aspecto"] > 1.05
                img = obra_img(src(o), o["aspecto"], 430 if ancha else 360, 516, o["title"])
                chico = ""
                relato = f'<p class="relato">{e(resto)}</p>' if resto else ""
                texto = f"""
                  <h2>{e(o['title'])}</h2>
                  {f'<p class="subtitulo">{e(o["subtitle"])}</p>' if o.get('subtitle') and o['serie'] != 'Hadas urbanas' else ''}
                  <p class="verso">{e(verso)}</p>
                  {relato}
                  {datos(o)}
                  {precio(ui, o, config)}"""
            else:
                img = obra_img(src(o), o["aspecto"], 472, 360, o["title"])
                chico, ancha = "", False
                corto = recortar(resto, 30) if resto else ""
                relato = f'<p class="relato">{e(corto)}</p>' if corto else ""
                texto = f"""
                  <h2>{e(o['title'])}</h2>
                  {f'<p class="subtitulo">{e(o["subtitle"])}</p>' if o.get('subtitle') and o['serie'] != 'Hadas urbanas' else ''}
                  <p class="verso">{e(verso)}</p>
                  {relato}
                  <p class="datos">{e(' · '.join(str(o[k]) for k in ('technique', 'dimensions', 'year') if o.get(k)))}<br>{e(o.get('edition', ''))}</p>
                  {precio(ui, o, config, compacto=True)}"""
            p.append((f"{fondo} pieza{' apaisada' if H and ancha else ''}", f"""
              <div class="pieza-obra">{img}</div>
              <div class="pieza-texto{chico}">{texto}</div>"""))

    # Cómo adquirir y cierre
    pasos = "".join(f"<li>{e(t)}</li>" for t in PASOS)
    cond = "".join(f"<li>{e(t)}</li>" for t in CONDICIONES)
    p.append(("marfil compra", f"""
      <div class="compra-pasos">
        <h2>Cómo adquirir una pieza</h2>
        <ol class="pasos">{pasos}</ol>
        <ul class="condiciones">{cond}</ul>
      </div>
      <div class="contacto">
        <dl>
          <div><dt>Instagram</dt><dd><a href="{e(config['instagram'])}">@libertadpantoja</a></dd></div>
          <div><dt>Correo</dt><dd><a href="mailto:{e(config['email'])}">{e(config['email'])}</a></dd></div>
          <div><dt>Sitio</dt><dd><a href="{SITIO}">{SITIO_CORTO}</a></dd></div>
          <div><dt>El umbral</dt><dd><a href="{e(config['substack'])}">flyingfugu.substack.com</a></dd></div>
        </dl>
        <p class="cierre">{e(CIERRE)}</p>
      </div>"""))

    cuerpo = []
    for i, (clase, contenido) in enumerate(p, start=1):
        pie = "" if i == 1 else folio(i)
        cuerpo.append(f'<section class="pagina {clase}">{contenido}{pie}</section>')
    return "\n".join(cuerpo)


def documento(fmt, cuerpo):
    css = (CAT / "catalogo.css").read_text()
    return f"""<!doctype html>
<html lang="es-MX">
<head>
<meta charset="utf-8">
<title>Catálogo de obra · Libertad Pantoja</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400;1,500&family=Libre+Caslon+Display&family=Libre+Caslon+Text:ital@1&display=block">
<style>{css}</style>
</head>
<body class="{fmt}">
{cuerpo}
</body>
</html>"""


# ---------------------------------------------------------------------------
# Exportación
# ---------------------------------------------------------------------------


def comprimir(origen, destino):
    """WebKit guarda las imágenes sin pérdida; se recomprimen a JPEG."""
    import fitz

    doc = fitz.open(origen)
    doc.rewrite_images(quality=80, lossy=True, lossless=True, bitonal=False)
    doc.save(destino, garbage=4, deflate=True, clean=True)


def exportar(fmt, ancho, alto, destino_pdf, png_dir=None):
    html_path = BUILD / f"catalogo-{fmt}.html"
    salida = BUILD / fmt
    if salida.exists():
        shutil.rmtree(salida)
    salida.mkdir(parents=True)
    exe = BUILD / "exportar"
    if not exe.exists():
        subprocess.run(["swiftc", "-O", str(CAT / "exportar.swift"), "-o", str(exe)], check=True)
    args = [str(exe), str(html_path), str(ancho), str(alto), str(salida)]
    if png_dir:
        args.append("png")
    subprocess.run(args, check=True)

    escritor = PdfWriter()
    for pdf in sorted(salida.glob("p*.pdf")):
        escritor.append(str(pdf))
    escritor.add_metadata({
        "/Title": "Catálogo de obra · Libertad Pantoja",
        "/Author": "Libertad Pantoja",
        "/Subject": f"Catálogo de obra, {FECHA}",
    })
    destino_pdf.parent.mkdir(parents=True, exist_ok=True)
    crudo = salida / "unido.pdf"
    with open(crudo, "wb") as f:
        escritor.write(f)
    comprimir(crudo, destino_pdf)

    if png_dir:
        png_dir.mkdir(parents=True, exist_ok=True)
        for viejo in png_dir.glob("catalogo-*.png"):
            viejo.unlink()
        for png in sorted(salida.glob("p*.png")):
            shutil.copy(png, png_dir / f"catalogo-{png.stem[1:]}.png")


def main():
    config, ui, onirica, hadas = cargar()
    BUILD.mkdir(exist_ok=True)
    for fmt in ("h", "v"):
        (BUILD / f"catalogo-{fmt}.html").write_text(documento(fmt, paginas(fmt, config, ui, onirica, hadas)))
    if "--solo-html" in sys.argv:
        return
    docs = RAIZ / "assets/docs"
    exportar("h", 792, 612, docs / "catalogo-libertad-pantoja.pdf")
    sin_instagram = "--sin-instagram" in sys.argv or os.environ.get("CI")
    instagram = None if sin_instagram else RAIZ / "_privado/instagram"
    exportar("v", 540, 675, docs / "catalogo-libertad-pantoja-vertical.pdf", instagram)

    # Fecha y peso para el enlace de descarga en Obra.
    peso = (docs / "catalogo-libertad-pantoja.pdf").stat().st_size / 1e6
    (RAIZ / "_data/catalogo.yml").write_text(
        "# Lo escribe _catalogo/generar.py; no editar a mano.\n"
        f'fecha: "{FECHA}"\n'
        f'peso: "{peso:.1f} MB"\n'
    )
    print("Listo:", docs, f"({FECHA}, {peso:.1f} MB)")


if __name__ == "__main__":
    main()
