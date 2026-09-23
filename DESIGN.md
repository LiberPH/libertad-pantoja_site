---
name: Libertad Pantoja
description: Writer and visual artist; a night threshold that opens onto cream pages (site), and a quiet classical art book (catalog).
colors:
  noche: "#16091E"
  umbral: "#2B1133"
  vino: "#5A1F3A"
  brasa: "#9C3B32"
  sol: "#D65F27"
  horizonte: "#F6A13A"
  tinta-clara: "#F4E3C8"
  tinta-suave: "#D8C3A8"
  crema-fondo: "#F7E9D2"
  crema-panel: "#FFF6E8"
  crema-panel-suave: "#F2DEC1"
  tinta-oscura: "#2B1133"
  tinta-profunda: "#16091E"
  tinta-cafe: "#4A302F"
  tinta-media: "#765A4C"
  catalogo-marfil: "#FBF8F2"
  catalogo-gris: "#E7E3DD"
  catalogo-verde: "#2C5D4F"
  catalogo-tinta: "#2A2622"
  catalogo-tinta-relato: "#453F39"
  catalogo-tinta-media: "#635A51"
typography:
  display:
    fontFamily: "Cormorant, serif"
    fontSize: "clamp(3.4rem, 7vw, 6.6rem)"
    fontWeight: 500
    lineHeight: 0.96
    letterSpacing: "-0.035em"
  headline:
    fontFamily: "Fraunces, serif"
    fontSize: "clamp(1.55rem, 3vw, 2.35rem)"
    fontWeight: 500
    lineHeight: 1.12
  title:
    fontFamily: "Fraunces, serif"
    fontSize: "clamp(1.02rem, 1.6vw, 1.18rem)"
    fontWeight: 500
    lineHeight: 1.2
    letterSpacing: "-0.01em"
  story:
    fontFamily: "Fraunces, serif"
    fontSize: "1.04rem"
    fontWeight: 300
    lineHeight: 1.55
  price:
    fontFamily: "Fraunces, serif"
    fontSize: "1.1rem"
    fontWeight: 500
    lineHeight: 1.3
    fontFeature: "'lnum' 1, 'tnum' 1"
  body:
    fontFamily: "Hanken Grotesk, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.65
  label:
    fontFamily: "Hanken Grotesk, sans-serif"
    fontSize: "0.7rem"
    fontWeight: 600
    letterSpacing: "0.08em"
  catalogo-display:
    fontFamily: "Libre Caslon Display, serif"
    fontSize: "46px"
    fontWeight: 400
    lineHeight: 1.08
  catalogo-opener:
    fontFamily: "Libre Caslon Display, serif"
    fontSize: "44px"
    fontWeight: 400
    lineHeight: 1.2
  catalogo-subtitle:
    fontFamily: "Libre Caslon Text, serif"
    fontSize: "14px"
    fontWeight: 400
  catalogo-headline:
    fontFamily: "EB Garamond, serif"
    fontSize: "25px"
    fontWeight: 400
    lineHeight: 1.2
    letterSpacing: "0.02em"
  catalogo-verse:
    fontFamily: "EB Garamond, serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.4
  catalogo-body:
    fontFamily: "EB Garamond, serif"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.55
    fontFeature: "'onum' 1, 'pnum' 1"
  catalogo-relato:
    fontFamily: "EB Garamond, serif"
    fontSize: "11.5px"
    fontWeight: 400
    lineHeight: 1.5
  catalogo-label:
    fontFamily: "EB Garamond, serif"
    fontSize: "11px"
    fontWeight: 400
    letterSpacing: "0.12em"
    fontFeature: "'smcp' 1"
rounded:
  none: "0px"
  focus: "4px"
  nav: "24px"
  card: "28px"
  section: "32px"
  pill: "999px"
spacing:
  card-padding: "22px"
  grid-gap: "22px"
  section: "48px"
  catalogo-gutter: "44px"
  catalogo-margin: "48px"
components:
  button-primary:
    backgroundColor: "{colors.tinta-clara}"
    textColor: "{colors.noche}"
    rounded: "{rounded.pill}"
    padding: "12px 20px"
    height: "44px"
  button-primary-hover:
    backgroundColor: "{colors.horizonte}"
    textColor: "{colors.noche}"
  button-secondary:
    backgroundColor: "{colors.crema-panel}"
    textColor: "{colors.tinta-oscura}"
    rounded: "{rounded.pill}"
    padding: "12px 20px"
    height: "44px"
  button-secondary-hover:
    backgroundColor: "{colors.tinta-oscura}"
    textColor: "{colors.tinta-clara}"
  art-cta:
    backgroundColor: "{colors.tinta-profunda}"
    textColor: "{colors.tinta-clara}"
    rounded: "{rounded.pill}"
    padding: "12px 22px"
    height: "46px"
  art-cta-hover:
    backgroundColor: "{colors.horizonte}"
    textColor: "{colors.noche}"
  art-card:
    backgroundColor: "{colors.crema-panel}"
    textColor: "{colors.tinta-cafe}"
    rounded: "{rounded.card}"
    padding: "{spacing.card-padding}"
  status-pill-disponible:
    textColor: "{colors.brasa}"
    rounded: "{rounded.pill}"
    padding: "2px 10px"
  category-nav-link:
    backgroundColor: "{colors.crema-panel}"
    textColor: "{colors.tinta-profunda}"
    typography: "{typography.label}"
    rounded: "{rounded.pill}"
    padding: "7px 12px"
    height: "34px"
  category-nav-link-hover:
    backgroundColor: "{colors.tinta-profunda}"
    textColor: "{colors.tinta-clara}"
  visor:
    backgroundColor: "{colors.noche}"
    textColor: "{colors.tinta-clara}"
    padding: "24px 64px"
  catalogo-pagina:
    backgroundColor: "{colors.catalogo-marfil}"
    textColor: "{colors.catalogo-tinta}"
    rounded: "{rounded.none}"
    padding: "48px 56px"
    width: "792px"
    height: "612px"
  catalogo-pagina-vertical:
    backgroundColor: "{colors.catalogo-marfil}"
    textColor: "{colors.catalogo-tinta}"
    rounded: "{rounded.none}"
    padding: "34px 36px"
    width: "540px"
    height: "675px"
  catalogo-pagina-onirica:
    backgroundColor: "{colors.catalogo-gris}"
    textColor: "{colors.catalogo-tinta}"
  catalogo-titulo-obra:
    textColor: "{colors.catalogo-verde}"
    typography: "{typography.catalogo-headline}"
  catalogo-escribir:
    textColor: "{colors.catalogo-verde}"
    typography: "{typography.catalogo-verse}"
---

# Design System: Libertad Pantoja

## Overview

**Creative North Star: "El umbral y la página"**

The project has two visual worlds that share one body of work and one data source (`_data/obras.yml`, with interface strings in `_data/ui.yml`), but never share styling. Keep them apart: the site's night palette never enters the catalog, and the catalog's green and ivory never enter the site.

**The site (`assets/css/main.css`)** is a threshold. Each page opens with a band of night (noche to umbral to vino to brasa, with warm horizonte glows) holding a large Cormorant title, then drops onto a cream editorial body where the work and its first-person stories are read. Warm plum-tinted inks sit on cream. Components are soft (pill buttons, 28px cards) with faint ambient shadows. The artist's stories are set apart in light italic Fraunces, so the writing reads as a voice and not as captions.

**The catalog (`_catalogo/`, exported to `assets/docs/catalogo-libertad-pantoja.pdf` landscape 792×612pt and `-vertical.pdf` 540×675pt)** is a classical, serene art book. It uses ivory paper and large unframed work. Stories are set as book text in EB Garamond, titles are in a single green, and there is no ornament beyond a short hairline rule. The dream-work (obra onírica) pages turn a subtle warm gray, while the Hadas urbanas pages stay ivory. The artist chose this direction from previews on 23 Sep 2026 and approved the full PDFs. It replaces a rejected "Lotería de sueños" direction.

**Key Characteristics:**
- Site: night header band over a cream body. Soft pill and rounded-card forms. Ambient plum shadows. Cormorant, Fraunces and Hanken Grotesk.
- Catalog: flat ivory and warm-gray paper. Square edges. One green for lettering. Libre Caslon Display for the cover name and section openers only, and EB Garamond for everything else, always at regular weight.
- Shared: the work comes first, the story is told in the artist's words, and the data comes second and stays quiet. Buying happens by email (`mailto:`) and never through a simulated checkout.
- Shared: no published artwork image exceeds 1200px on its long side.

## Colors

The site uses a nocturnal plum-to-ember palette that resolves into warm cream. The catalog uses a restrained ivory-and-green book palette.

### Primary
- **Brasa, ember red** (brasa): the site's action color on cream. Used for the story "Seguir leyendo" toggle, acquire-panel and catalog-download links, the "Disponible" status pill, the 2px focus outline, and underline tints at 40% alpha.
- **Horizonte, dawn amber** (horizonte): the action and accent color on dark surfaces. Used for the header-nav active state, hero rules, the visor's button hover and focus, and the hover fill of the primary and art CTAs.
- **Catalog green** (catalogo-verde): the only colored ink in the catalog. Used for the cover name, section and work titles, the short filete rule, the "Escribir por esta pieza" link and its 40%-alpha underline, list markers, the contact hairline, and the closing line.

### Secondary
- **Vino, wine** (vino) and **Umbral, threshold plum** (umbral): mid-stops of the night gradient on the home hero, page heroes and the CTA band. Umbral also serves as the heading ink `tinta-oscura` on cream.
- **Sol, sun orange** (sol): appears only as a low-alpha glow in hero radial gradients. It is written as a literal and not through the variable.

### Neutral
- **Noche, night** (noche / tinta-profunda): the deepest ink. Used for the top of every hero gradient, the visor backdrop at 95% alpha, the art CTA fill, and headings on cream.
- **Tinta clara, candle paper** (tinta-clara): text on night surfaces and the fill of the primary button.
- **Tinta suave, dusk paper** (tinta-suave): secondary text on night surfaces (site nav, visor metadata).
- **Crema fondo, page cream** (crema-fondo): the site's body background below the 360px night band (300px on mobile).
- **Crema panel, card cream** (crema-panel): card and panel surfaces, used at 72–92% alpha.
- **Crema panel suave, tint cream** (crema-panel-suave): the tinted alternate sections and the mat behind artwork images, used at 36–48% alpha.
- **Tinta café, coffee ink** (tinta-cafe): body text and data values on cream.
- **Tinta media, mauve-brown ink** (tinta-media): secondary text, stories, metadata labels and notes on cream.
- **Catalog ivory** (catalogo-marfil): the base page for the cover, "Sobre mi obra", the index, the Hadas urbanas pages and "Cómo adquirir".
- **Catalog warm gray** (catalogo-gris): every page of the obra onírica section, including its section opener.
- **Catalog inks** (catalogo-tinta, catalogo-tinta-relato, catalogo-tinta-media): titles and prices, story and paragraph text, and data, notes and folios, in that order.

### Named Rules
**The Night-Over-Cream Rule.** On the site, night gradients belong only to the header band, page heroes, the home hero and the full CTA band. Reading content always sits on cream.

**The Two-Accent Rule.** Brasa is the action color on cream, and horizonte is the action color on night. Don't swap them.

**The Green Lettering Rule.** In the catalog, #2C5D4F is the only saturated color. It is used for lettering and hairlines only, never for fills or backgrounds.

**The Readable Dream Rule.** Obra onírica pages use the subtle warm gray #E7E3DD. The artist rejected the deeper #D5CFC6 because it reads worse. Don't darken the dream pages.

## Typography

**Site Display Font:** Cormorant 500 (serif fallback)
**Site Heading and Story Font:** Fraunces (opsz 9..144; 400/500/600, italic 300/400)
**Site Body/UI Font:** Hanken Grotesk 400/500/600 (sans-serif fallback)
**Catalog Display Font:** Libre Caslon Display 400, with Libre Caslon Text italic for the cover subtitle
**Catalog Text Font:** EB Garamond 400 and italic (500 is loaded but not used)

**Character:** The site pairs a tall, tightly tracked Cormorant title with Fraunces for sturdy headings and Hanken Grotesk for plain UI. The catalog is a single classical book voice: Caslon for the name and openers, and Garamond with oldstyle figures for everything else.

### Hierarchy
- **Display** (site): page-hero h1, set in the tint-clara color on night with a 74px horizonte hairline beneath. The home hero enlarges it to clamp(4.4rem, 10vw, 8.2rem).
- **Headline** (site): section and panel h2 on cream, in tinta-oscura or tinta-profunda.
- **Title** (site): artwork and publication card h3, with text-wrap balance.
- **Story** (site): the artist's first-person stories on artwork cards, in Fraunces italic 300, tinta-media.
- **Price** (site): Fraunces 500 with lining tabular figures, in tinta-profunda.
- **Body** (site): Hanken Grotesk 16px/1.65.
- **Label** (site): Hanken Grotesk 600, uppercase and tracked, for category nav, header nav (0.85rem) and metadata `dt` (0.68–0.75rem).
- **Catalog display**: "Libertad Pantoja" on the cover, green, 46px (40px vertical).
- **Catalog opener**: the "Obra onírica" and "Hadas urbanas" section titles, green, 44px (38px vertical).
- **Catalog headline**: work titles and page titles in green (23px vertical).
- **Catalog label**: contact terms on the "Cómo adquirir" page, small caps tracked 0.12em at 11px, catalog tinta media.
- **Catalog verse**: the first sentence of each story, in italic.
- **Catalog relato / body**: the rest of the story (12.5px vertical), with "Sobre mi obra" and opener paragraphs at 14–15px. Keep measure at or below 58–62ch.

### Named Rules
**The Story-In-Italic Rule.** The artist's own account of a piece is always set apart in italic: Fraunces 300 on the site, the EB Garamond verse line in the catalog. It is never rewritten.

**The Classic Light Type Rule.** Catalog type is regular weight (400) throughout, with no bold, slab or heavy display. Libre Caslon Display appears only on the cover name and the two section openers. The artist rejected the heavy Ultra slab titles.

**The First-Sentence Verse Rule.** In the catalog, a story's first sentence becomes the italic verse and the remainder becomes the relato. The vertical edition trims the relato to about 30 words at a sentence boundary.

## Layout

**Site.** The content column is `min(1120px, 100% − 32px)`, and editorial blocks narrow to 1040px. Heroes break out to full bleed with `calc(50% − 50vw)` and keep inner padding aligned to the column. The artwork grid is `repeat(auto-fit, minmax(min(100%, 320px), 1fr))` with a 22px gap, and cards stretch to equal height so their acquire block sits at the bottom. Collection sections use 48px vertical padding, and alternate sections are tinted cream panels. Breakpoints are at 900px (two-column panels stack) and 580px (smaller headings, a shorter night band, and single-column metadata). Each artwork card follows a fixed order: image, title, series, story, data, then acquisition.

**Catalog.** Pages are fixed CSS-grid pages: 792×612 with 48/56px margins in the landscape edition, and 540×675 with 34/36px margins in the vertical edition. The landscape edition places art and text side by side: art 360px (430px for landscape work), text in the remaining space, with a 36–44px gap and centered vertically. The vertical edition places art on top (360px row) and text below. The cover places the work at left (400px) and the name at right in the landscape edition, and stacks the work above a centered name in the vertical edition. Each work is fitted inside its box with its aspect ratio preserved and is never cropped. The index is a three-column grid with a 16/22px gap. Folios are 11px in the lower right, and the cover has none. Page order: cover, "Sobre mi obra", index, the obra onírica opener and works, the Hadas urbanas opener and works, then "Cómo adquirir".

## Elevation & Depth

**Site.** Depth is soft and ambient, created by plum-tinted diffuse shadows under cream cards and panels plus tonal layering of cream alphas. Nothing lifts on hover except the `.button` family (translateY −2px). The night band creates depth through gradient and glow, not shadow.

### Shadow Vocabulary
- **Card ambient** (`box-shadow: 0 16px 36px rgba(43, 17, 51, 0.08)`): artwork cards. This is the final layer; earlier layers used heavier values.
- **Panel ambient** (`box-shadow: 0 18px 42px rgba(43, 17, 51, 0.08)`): text blocks and contact and timeline panels.
- **Book cover** (`box-shadow: 0 16px 30px rgba(43, 17, 51, 0.14)`): publication covers on the home page.
- **Viewer image** (`box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5)`): the enlarged artwork in the visor.

**Catalog.** The catalog is completely flat. It has no shadows, frames or mats, and depth comes only from the two paper tones.

### Named Rules
**The Flat Paper Rule.** Catalog pages carry no shadow and no elevation of any kind.

## Shapes

**Site.** Forms are soft and rounded: pills (999px) for buttons, CTAs, status pills and category links; 28px cards; a 24px category-nav container; 32px tinted sections; and a 4px focus ring on inline links. Thin 1px hairlines in plum at 12–18% alpha separate metadata rows, the acquire block and panel columns. Hero titles carry a 74px 1px hairline in horizonte.

**Catalog.** Every edge is square (0 radius). The only drawn lines are the 40×1px green filete under titles and openers, the 1px green top rule on the contact block, and the 1px green underline on the email link. These rules are native to the world. The prohibition below applies to what surrounds artworks, not to typographic rules.

## Components

### Buttons
- **Shape:** full pill (999px), minimum height 44px.
- **Primary (on night):** candle-paper fill with night text, 12px 20px padding, uppercase 0.78rem tracked 0.08em, weight 600. On hover the fill changes to horizonte.
- **Secondary (on cream):** cream fill with a plum hairline and tinta-oscura text. On hover it inverts to a tinta-oscura fill with tinta-clara text.
- **Art CTA ("Escribir para adquirir"):** a noche fill with tinta-clara text, 46px high, sentence case 0.95rem weight 600, that opens a prefilled `mailto:`. On hover the fill changes to horizonte with noche text. The label comes from `ui.yml` per status, and an empty label means no button.
- **Focus:** 2px brasa outline offset 3px (horizonte on night surfaces). The outline follows the pill radius.

### Chips
- **Status pill:** 2px 10px pill. "Disponible" uses brasa text on an 8% brasa wash. "Reservada" and "Próximamente" use tinta-oscura text on a transparent fill, with Próximamente in italic. "Vendida", "Agotada" and "En archivo" use muted tinta-media text. Labels come from `ui.yml`.
- **Category nav links:** 34px pills in uppercase 0.7rem type, inside a 24px-radius cream container. On hover and focus they invert to a dark fill.

### Cards / Containers
- **Artwork card:** 28px radius, cream-panel fill at about 90% alpha, a 1px plum hairline, the card ambient shadow, and 22px body padding. The image is a link to the visor. It uses `object-fit: contain` with 18px padding on a tint-cream mat, at a height of clamp(220px, 32vw, 340px). Stories longer than 45 words show a 32-word teaser and a native `<details>` toggle labeled "Seguir leyendo" / "Cerrar" in brasa. Metadata is a two-column `dl` (80px terms). The acquire block is separated by a hairline and holds, in order, the status pill, the price or the framed/unframed price list, the note for variable prices, the CTA, "o escribe a" with a selectable email, and a process note.
- **Panels:** cream fill with a plum hairline and panel ambient shadow. Two-column panels drop the fill and shadow and keep only top and bottom hairlines.

### Navigation
- **Header:** the ☉ brand mark in a 32px circle, followed by the name in Fraunces. Nav links use uppercase 0.85rem Hanken, tracked 0.08em, in tinta-suave. The active and hover state is horizonte with a 1px underline.

### Visor (signature, site)
A native `<dialog>` lightbox built by `assets/js/visor.js`. It takes the full viewport on a 95% noche backdrop. The image is limited to `min(100%, 1200px)` wide and the viewport height minus 150px. The caption shows the title in Fraunces over technique, dimensions and year in tinta-suave. Previous, next and close are 48px round transparent buttons, and they move to the bottom center on mobile. Without JavaScript, the link opens the image directly. Button labels come from `ui.yml`.

### Catalog work page (signature, catalog)
The work is unframed, large and fitted. The text column follows a fixed order: the green title, an italic subtitle when present (obra onírica only), the italic verse, the relato, the data line (technique on one line; dimensions, edition and year on the next), the price or prices with italic qualifiers, a note for variable prices, and the green italic link "Escribir por esta pieza", which opens a `mailto:` built with the site's `ui.yml` strings. The vertical edition drops the series label, the price note and the link.

## Do's and Don'ts

### Do:
- **Do** keep every published artwork image at 1200px or less on its long side. This protects against print theft and applies to the site, the visor and both PDFs.
- **Do** read artwork content from `_data/obras.yml` and interface and status strings from `_data/ui.yml` in both worlds. Never hard-code a title, price or status label into a template.
- **Do** keep the site's card order: image, title, story, data, acquisition, with price visible whenever the status allows it.
- **Do** set the catalog's titles, filete and "Escribir" link in #2C5D4F, on ivory #FBF8F2, and use warm gray #E7E3DD for obra onírica pages.
- **Do** use Libre Caslon Display only for the catalog's cover name and section openers, and EB Garamond at weight 400 for all other catalog text.
- **Do** end every acquisition path in a `mailto:` with the piece's title in the subject.

### Don't:
- **Don't** put frames, borders, mats, drop shadows or numbers around artworks in the catalog. The artist rejected them as inelegant.
- **Don't** bring lotería cards, exvotos or other folk or national motifs into the catalog. The work speaks of the dream on its own.
- **Don't** use heavy, slab or bold display type in the catalog.
- **Don't** darken the catalog's dream pages to #D5CFC6 or deeper.
- **Don't** let the site's night palette, gradients or pill buttons into the catalog, and don't let the catalog's green into the site.
- **Don't** simulate a cart or checkout, and don't publish WhatsApp as a contact channel.
