# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Dos públicos principales, con el mismo peso:

- **Compradores y coleccionistas de obra visual.** Llegan a conocer piezas originales, ediciones limitadas, fotografía impresa y fotografía intervenida; necesitan ver la obra con claridad, entender técnica, medidas, edición, estado y precio, y escribir para adquirirla.
- **El medio literario y cultural.** Editoriales, prensa, instituciones, programas de becas, organizadores de lecturas y presentaciones, y lectores. Buscan confirmar la trayectoria de Libertad Pantoja como autora: libros, antologías, cuentos publicados y credenciales.

Públicos secundarios: participantes del club de lectura *Los sueños y el inframundo*, interesados en los talleres y suscriptores de *El umbral* (Substack).

## Product Purpose

Sitio personal de Libertad Pantoja, narradora y artista visual nacida en Ciudad de México. Su trabajo cruza escritura, pintura, dibujo, fotografía e imagen intervenida alrededor del sueño, el mito, el cuerpo y el inframundo.

El sitio tiene dos tareas principales: **vender obra visual** y **dar presencia como autora**. Funciona bien cuando un comprador encuentra una pieza disponible y escribe para adquirirla, y cuando alguien del medio literario confirma en pocos minutos quién es y qué ha publicado. Club, talleres y El umbral son secundarios. Sirven para acercar a la gente y tienen salida propia, pero no compiten con las dos tareas principales.

## Positioning

Una sola autora cuya escritura y obra visual salen de las mismas obsesiones: sueños propios, mitología, psicología de las profundidades y una mirada casi biológica sobre insectos, plantas y animales híbridos. Muchas piezas nacen de un sueño concreto que también dio pie a un cuento. La ficha de cada obra cuenta ese origen en primera persona. Esa unión entre relato y obra, contada por la autora, es lo que distingue al sitio de una galería o de una página de escritora común.

## Operating Context

- **Adquisición de obra por correo.** Cada ficha tiene un enlace `mailto:` con el título de la pieza en el asunto. No hay carrito ni pagos en línea.
- **Precios en MXN y USD.** Algunas piezas tienen precio sin marco y enmarcada; las impresiones con precio "Desde" varían según el tamaño y se cotizan por correo.
- **El catálogo vive en datos.** La obra se edita en `_data/obras.yml` (categorías: `original`, `edicion-limitada`, `fotografia`, `fotografia-intervenida`, `archivo-visual`; estados: disponible, reservada, vendida, agotada, archivo, próximamente). Las publicaciones se editan en `_data/publicaciones.yml` (categorías: `libro`, `antologia`, `revista`, `divulgacion`).
- **El club de lectura avanza por ciclos bimestrales.** Tiene sesión presencial, repetición en línea una semana después, cupo de 5 lugares y cuesta $450 MXN por sesión. Las fechas se actualizan a mano en `club.html`.
- **Canales externos.** El umbral (Substack, flyingfugu.substack.com), Instagram, Bluesky y correo (rtonalli@gmail.com).

## Capabilities and Constraints

- Sitio estático en Jekyll. Hoy se publica en GitHub Pages como sitio de proyecto (`baseurl: "/libertad-pantoja_site"`), así que todas las rutas deben usar `relative_url`.
- Sin backend ni pagos. Las compras siguen por correo por ahora.
- **Por decidir:** usar una herramienta de venta (por ejemplo Shopify) más adelante. El sitio no debe cerrarle la puerta, pero tampoco debe simular un checkout que no existe.
- **Por decidir:** migrar a un dominio propio.
- **Idioma:** hoy solo español (`es-MX`). **Hay planes de una versión en inglés**, así que conviene que la estructura, los textos y los datos no la impidan (textos fuera de las plantillas cuando se pueda, campos traducibles en los YAML).
- Terminología propia: "Obra", "Ediciones limitadas", "Fotografía intervenida", "Archivo visual" / "Mundos pequeños", "El umbral", "Hadas urbanas" (serie fotográfica).

## Brand Commitments

- Nombre: **Libertad Pantoja**. Marca actual del encabezado: el glifo ☉.
- Voz en primera persona, íntima y literaria. Las fichas de obra cuentan el sueño o la circunstancia de donde salió cada pieza. Esa voz es de la autora y no se reescribe sin permiso.
- Líneas que definen el sitio: "Escribo y pinto el territorio interior: sueño, mito e inframundo". Cita de cierre: "Sólo lo difícil es estimulante." (Lezama Lima).
- Retrato de la bio: Foto © Horacio Flores. El crédito debe acompañar la imagen.

## Evidence on Hand

- Obra con fotografía real en `assets/img/obra/` (p. ej. *Planta carnívora*, *Lo que dejé secar sobre la alfombra*, *El rescate del gato blanco*, *El fruto de la hojarasca*, *El fuego*, *El reino del sol*, *Ciudad de los insectos*, *La luz de los insectos*, *Flor amarilla, Atlanta*). Las fichas completas están en `_data/obras.yml`. Todavía hay algunos placeholders SVG.
- Portadas reales de publicaciones en `assets/img/publicaciones/`: *Tú, enfermo no estás* (Malabar Editorial, 2021), *Fosca, antología siniestra* (2026), *Historias de las historias* (2011), *Lo fantástico no existe* (2018).
- Credenciales confirmadas en `bio.html`: Beca Jóvenes Creadores FONCA/SACPC 2018 (cuento) y 2021 (novela); tres participaciones en Under the Volcano.
- Archivo de divulgación científica, tratado como archivo secundario.
- **No existen** y no deben inventarse: testimonios de compradores, reseñas, prensa citada, exposiciones, galerías representantes, cifras de ventas, ni políticas de envío o devolución.
- El Archivo visual (Jardín Botánico, Cuernavaca, Xometla) sigue con series por seleccionar.

## Product Principles

1. **La obra primero, con sus datos completos.** Técnica, medidas, edición, estado y precio siempre a la vista. Un comprador no debería tener que escribir para saber si algo está disponible o cuánto cuesta.
2. **Escritura y obra son un mismo cuerpo.** El sitio muestra la conexión entre sueño, relato e imagen en vez de separar a la "escritora" de la "artista".
3. **La credibilidad se muestra con hechos.** Publicaciones, editoriales, becas y fechas reales, verificables y fáciles de encontrar para editores y prensa.
4. **Lo secundario acompaña sin competir.** Club, talleres y El umbral tienen su lugar y su salida propia, pero no le quitan protagonismo a vender obra ni a la presencia como autora.
5. **Crecer sin rehacer.** La estructura tiene que aguantar una versión en inglés y una futura herramienta de venta sin rediseñar desde cero.
