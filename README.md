# Libertad Pantoja · sitio Jekyll reestructurado

Este paquete es una versión de prueba para reorganizar la página personal alrededor de:

- Obra visual
- Ediciones limitadas
- Fotografía impresa
- Fotografía intervenida
- Libros y publicaciones
- Club de lectura
- Talleres
- Bio y contacto

## Cómo probar localmente

```bash
bundle install
bundle exec jekyll serve
```

Luego abre `http://localhost:4000`.

## Qué editar primero

1. Reemplaza las imágenes placeholder en `assets/img/obra/` y `assets/img/perfil/`.
2. Edita `_data/obras.yml` para agregar títulos, técnicas, precios, estados e imágenes reales.
3. Edita `_data/publicaciones.yml` para depurar el archivo de publicaciones.
4. Revisa `_config.yml`:
   - Para Netlify o dominio propio: `baseurl: ""`.
   - Para GitHub Pages de proyecto: `baseurl: "/nombre-del-repo"`.

## Estructura

```text
_data/
  navigation.yml
  obras.yml
  publicaciones.yml
_includes/
  header.html
  footer.html
_layouts/
  default.html
  page.html
assets/css/main.css
index.html
obra.html
publicaciones.html
club.html
talleres.html
bio.html
contacto.html
archivo-visual.html
```

## Nota

La divulgación se conserva como archivo secundario, no como eje principal de navegación.
