#!/usr/bin/env python3
"""Genera las páginas HTML del sitio a partir de los Markdown de /fuentes.

Uso:
    pip install markdown
    python build.py

Las páginas generadas (index.html, anexo-a.html, anexo-b.html) se versionan en el repo,
así GitHub Pages las sirve tal cual, sin proceso de compilación.
"""
import html
import math
import re
from pathlib import Path

import markdown

# --- Configuración -----------------------------------------------------------
SITE_URL = "https://mardopazo.github.io/ErrorValor-IA"   # confirmar usuario de GitHub
REPO_URL = "https://github.com/mardopazo/ErrorValor-IA"
SITE_NAME = "ErrorValor-IA"
AUTOR = "Martín Dopazo"

ROOT = Path(__file__).parent
SRC = ROOT / "fuentes"

PAGINAS = {
    "paper": {"archivo": "index.html", "fuente": "paper.md", "nav": "Paper",
              "pdf": "descargas/ErrorValor-IA_Paper.pdf"},
    "paper_en": {"archivo": "en/index.html", "fuente": "paper.en.md", "nav": "Paper", "idioma": "en",
                 "pdf": "descargas/ErrorValor-IA_Paper_EN.pdf"},
    "a": {"archivo": "anexo-a.html", "fuente": "anexo-a-postmortem.md", "nav": "Anexo A",
          "pdf": "descargas/ErrorValor-IA_Anexo-A_Post-mortem-sin-culpa.pdf"},
    "b": {"archivo": "anexo-b.html", "fuente": "anexo-b-dailys.md", "nav": "Anexo B",
          "pdf": "descargas/ErrorValor-IA_Anexo-B_Dailys-sin-vigilancia.pdf"},
}

# Textos de interfaz por idioma. El español está en la raíz; el inglés en /en/ (solo el paper).
IDIOMAS = {
    "es": {
        "html_lang": "es-AR", "og_locale": "es_AR", "prefijo": "", "carpeta": "",
        "nav": {"paper": "Paper", "a": "Anexo A", "b": "Anexo B", "repo": "Repositorio"},
        "nav_aria": "Principal", "nav_movil_aria": "Secciones del sitio",
        "salto": "Saltar al contenido", "inicio": "inicio", "tema": "Cambiar entre tema claro y oscuro",
        "menu": "Contenido", "lateral_aria": "Contenido de la página", "en_esta_pagina": "En esta página",
        "pie1": "{autor}. Este texto es un borrador en revisión: se puede discutir, corregir y mejorar.",
        "pie2": ('Contenido bajo licencia <a href="https://creativecommons.org/licenses/by/4.0/deed.es" rel="license noopener">'
                 'Creative Commons Atribución 4.0 (CC BY 4.0)</a>: podés copiarlo, adaptarlo y compartirlo, incluso con fines '
                 'comerciales, citando a {autor} y este sitio.'),
        "pie3": "Código y fuentes en GitHub", "pdf": "Descargar PDF", "autor": "Autor", "version": "Versión",
        "tabla": "Tabla", "og_alt": "Planta de un panóptico con una celda resaltada y el título del paper.",
        "leyenda1": "Celda observada", "leyenda2": "El error, a la vista del equipo",
        "pano_titulo": "Planta de un panóptico: una torre central rodeada de celdas iluminadas, con una celda resaltada.",
        "idioma_aria": "Idioma",
        "desc_paper": ("Con la IA escribimos código más rápido de lo que podemos entenderlo. "
                       "Un modelo de gestión para equipos de desarrollo donde el error se ve, se discute y se aprende."),
        "regla": "Quien aprueba se hace responsable", "notas": ("Una aclaración", "Alcance"),
        "anexo_palabra": "Anexo", "cabecera_autor": "Autor", "cabecera_version": "Versión", "refs": "referencias",
    },
    "en": {
        "html_lang": "en", "og_locale": "en_US", "prefijo": "../", "carpeta": "en/",
        "nav": {"paper": "Paper", "a": "Annex A (ES)", "b": "Annex B (ES)", "repo": "Repository"},
        "nav_aria": "Main", "nav_movil_aria": "Site sections",
        "salto": "Skip to content", "inicio": "home", "tema": "Switch between light and dark theme",
        "menu": "Contents", "lateral_aria": "Page contents", "en_esta_pagina": "On this page",
        "pie1": "{autor}. This text is a draft under review: it can be discussed, corrected and improved.",
        "pie2": ('Content under the <a href="https://creativecommons.org/licenses/by/4.0/deed.en" rel="license noopener">'
                 'Creative Commons Attribution 4.0 (CC BY 4.0)</a> license: you may copy, adapt and share it, even for '
                 'commercial purposes, crediting {autor} and this site.'),
        "pie3": "Code and sources on GitHub", "pdf": "Download PDF", "autor": "Author", "version": "Version",
        "tabla": "Table", "og_alt": "Plan of a panopticon with one highlighted cell and the title of the paper.",
        "leyenda1": "Observed cell", "leyenda2": "Error, in plain view of the team",
        "pano_titulo": "Plan of a panopticon: a central tower surrounded by lit cells, with one cell highlighted.",
        "idioma_aria": "Language",
        "desc_paper": ("With AI we write code faster than we can understand it. "
                       "A management model for development teams where error is seen, discussed and learned from."),
        "regla": "Whoever approves takes responsibility", "notas": ("A note on the metaphor", "Scope"),
        "anexo_palabra": "Annex", "cabecera_autor": "Author", "cabecera_version": "Version", "refs": "references",
    },
}

DESC_PAPER = ("Con la IA escribimos código más rápido de lo que podemos entenderlo. "
              "Un modelo de gestión para equipos de desarrollo donde el error se ve, se discute y se aprende.")
DESC_A = ("Plantilla para analizar un incidente sin buscar culpables. Copiala, completala con el equipo "
          "y guardala junto al ticket.")
DESC_B = ("Reglas de juego para que la daily coordine el trabajo del equipo en lugar de controlar a las personas.")


# --- Utilidades --------------------------------------------------------------
def esc(s):
    return html.escape(s, quote=True)


def polar(cx, cy, r, grados):
    a = math.radians(grados)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def sector(cx, cy, r0, r1, a0, a1):
    """Sector anular entre los ángulos a0 y a1 (grados, sentido horario desde +x)."""
    x0, y0 = polar(cx, cy, r1, a0)
    x1, y1 = polar(cx, cy, r1, a1)
    x2, y2 = polar(cx, cy, r0, a1)
    x3, y3 = polar(cx, cy, r0, a0)
    return (f"M{x0:.2f} {y0:.2f} A{r1} {r1} 0 0 1 {x1:.2f} {y1:.2f} "
            f"L{x2:.2f} {y2:.2f} A{r0} {r0} 0 0 0 {x3:.2f} {y3:.2f} Z")


def slug(texto):
    t = re.sub(r"<[^>]+>", "", texto).lower()
    for a, b in (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"), ("ü", "u"), ("ñ", "n")):
        t = t.replace(a, b)
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t or "seccion"


# --- Figuras -----------------------------------------------------------------
def svg_panoptico(n=28, error=9, titulo=None):
    """Planta de un panóptico: anillo de celdas, torre central, una celda destacada."""
    cx = cy = 300
    r0, r1 = 205, 262
    paso = 360 / n
    hueco = 1.7
    partes = []
    partes.append(f'<circle class="pano-aro" cx="{cx}" cy="{cy}" r="{r1 + 18}"/>')
    for i in range(n):
        a = -90 + (i + 0.5) * paso
        x0, y0 = polar(cx, cy, 64, a)
        x1, y1 = polar(cx, cy, r0, a)
        partes.append(f'<line class="pano-linea" x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}"/>')
    # haz de luz de la torre (un solo barrido)
    xa, ya = polar(cx, cy, r1, -98)
    xb, yb = polar(cx, cy, r1, -82)
    partes.append(f'<path class="pano-haz" d="M{cx} {cy} L{xa:.1f} {ya:.1f} A{r1} {r1} 0 0 1 {xb:.1f} {yb:.1f} Z"/>')
    for i in range(n):
        a0 = -90 + i * paso + hueco / 2
        a1 = -90 + (i + 1) * paso - hueco / 2
        cls = "pano-celda error" if i == error else "pano-celda"
        partes.append(f'<path class="{cls}" style="--i:{i}" d="{sector(cx, cy, r0, r1, a0, a1)}"/>')
    partes.append(f'<circle class="pano-torre" cx="{cx}" cy="{cy}" r="58"/>')
    partes.append(f'<circle class="pano-luz" cx="{cx}" cy="{cy}" r="9"/>')
    return ('<svg viewBox="0 0 600 600" role="img" aria-labelledby="pano-t" focusable="false">'
            f'<title id="pano-t">{esc(titulo or IDIOMAS["es"]["pano_titulo"])}</title>' + "".join(partes) + "</svg>")


def svg_anillo(entradas):
    """Anillo de progreso para la barra lateral: una celda por sección."""
    n = len(entradas)
    cx = cy = 60
    r0, r1 = 34, 56
    paso = 360 / n
    hueco = 3.0 if n > 8 else 4.0
    cel = []
    for i, (hid, titulo) in enumerate(entradas):
        a0 = -90 + i * paso + hueco / 2
        a1 = -90 + (i + 1) * paso - hueco / 2
        cel.append(f'<a href="#{hid}" aria-hidden="true" tabindex="-1">'
                   f'<path data-sec="{i}" d="{sector(cx, cy, r0, r1, a0, a1)}"><title>{esc(titulo)}</title></path></a>')
    return (f'<svg class="anillo" viewBox="0 0 120 120" aria-hidden="true" focusable="false">'
            + "".join(cel) + f'<circle cx="{cx}" cy="{cy}" r="14"/></svg>')


def svg_favicon():
    cx = cy = 32
    n = 12
    paso = 360 / n
    p = []
    for i in range(n):
        a0 = -90 + i * paso + 3
        a1 = -90 + (i + 1) * paso - 3
        fill = "#e8a317" if i == 3 else "none"
        op = "1" if i == 3 else "1"
        p.append(f'<path d="{sector(cx, cy, 18, 29, a0, a1)}" fill="{fill}" stroke="#1b262b" stroke-width="2" opacity="{op}"/>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
            '<rect width="64" height="64" fill="#edf0ec"/>' + "".join(p) +
            '<circle cx="32" cy="32" r="8" fill="#1b262b"/></svg>')


# --- Markdown -> HTML --------------------------------------------------------
def md_a_html(texto):
    md = markdown.Markdown(
        extensions=["tables", "sane_lists", "smarty"],
        extension_configs={"smarty": {
            "smart_quotes": True, "smart_dashes": False, "smart_ellipses": False,
            "substitutions": {"left-double-quote": "“", "right-double-quote": "”",
                              "left-single-quote": "‘", "right-single-quote": "’"},
        }},
    )
    return md.convert(texto)


def separar_cabecera(texto):
    """Devuelve (h1, autor, version, resto) tomando las primeras líneas del Markdown."""
    lineas = texto.strip("\n").split("\n")
    h1 = re.sub(r"^#\s+", "", lineas[0]).strip()
    resto = "\n".join(lineas[1:]).strip("\n")
    autor = version = None
    m = re.search(r"^\*\*(?:Autor|Author):\*\*\s*(.+)$", resto, re.M)
    if m:
        autor = m.group(1).strip()
        resto = resto.replace(m.group(0), "", 1)
    m = re.search(r"^\*\*(?:Versión|Version):\*\*\s*(.+)$", resto, re.M)
    if m:
        version = m.group(1).strip()
        resto = resto.replace(m.group(0), "", 1)
    resto = re.sub(r"^\s*---\s*\n", "", resto.lstrip("\n"), count=1) if autor or version else resto
    return h1, autor, version, resto.strip("\n")


def procesar_cuerpo(cuerpo_html, autolink_anexos, editorial=False, idioma="es"):
    L = IDIOMAS[idioma]
    # tablas: contenedor desplazable y, si tienen 3 columnas o más, etiquetas para apilarlas en el móvil
    def preparar_tabla(m):
        t = m.group(0)
        cabeceras = [re.sub(r"<[^>]+>", "", h).strip() for h in re.findall(r"<th[^>]*>(.*?)</th>", t, flags=re.S)]
        apilable = len(cabeceras) >= 3
        if apilable:
            def etiquetar_fila(mf):
                celdas = iter(cabeceras)
                return re.sub(r"<td([^>]*)>",
                              lambda mc: f'<td{mc.group(1)} data-label="{esc(next(celdas, ""))}">', mf.group(0))
            cuerpo = re.search(r"<tbody>.*?</tbody>", t, flags=re.S)
            if cuerpo:
                t = t.replace(cuerpo.group(0), re.sub(r"<tr>.*?</tr>", etiquetar_fila, cuerpo.group(0), flags=re.S))
        clase = "tabla apilable" if apilable else "tabla"
        return f'<div class="{clase}" tabindex="0" role="region" aria-label="{L["tabla"]}">{t}</div>'
    cuerpo_html = re.sub(r"<table>.*?</table>", preparar_tabla, cuerpo_html, flags=re.S)

    # citas: tres usos
    def clasificar(m):
        inner = m.group(1)
        txt = re.sub(r"<[^>]+>", "", inner).strip()
        if not editorial:
            cls = ""
        elif txt.startswith(L["regla"]):
            cls = "regla"
        elif any(inner.lstrip().startswith("<p><strong>" + n) for n in L["notas"]):
            cls = "nota"
        elif not re.search(r"<strong>", inner) and len(txt) < 400:
            cls = "tesis"
        else:
            cls = ""
        return f'<blockquote class="{cls}">{inner}</blockquote>' if cls else f"<blockquote>{inner}</blockquote>"
    cuerpo_html = re.sub(r"<blockquote>(.*?)</blockquote>", clasificar, cuerpo_html, flags=re.S)

    # h2: número, id; h3: id
    def h2(m):
        t = m.group(1)
        mm = re.match(r"^(\d+)\.\s+(.*)$", t)
        if mm:
            return (f'<h2 id="seccion-{mm.group(1)}"><span class="num">{mm.group(1)}</span>{mm.group(2)}</h2>', mm.group(1), mm.group(2))
        return (f'<h2 id="{slug(t)}">{t}</h2>', None, t)
    # sección por h2
    partes = re.split(r"(?=<h2>)", cuerpo_html)
    intro = partes[0] if not partes[0].startswith("<h2>") else ""
    secciones = partes[1:] if intro or not partes[0].startswith("<h2>") else partes
    if not intro and partes and partes[0].startswith("<h2>"):
        secciones = partes
    entradas = []
    salida = []
    for s in secciones:
        m = re.match(r"<h2>(.*?)</h2>", s, flags=re.S)
        if not m:
            salida.append(s)
            continue
        nuevo_h2, num, titulo = h2(m)
        hid = re.search(r'id="([^"]+)"', nuevo_h2).group(1)
        resto = s[m.end():]
        resto = re.sub(r"<h3>(.*?)</h3>",
                       lambda mm: f'<h3 id="seccion-{mm.group(1).split()[0].replace(".", "-")}">{mm.group(1)}</h3>'
                       if re.match(r"^\d+\.\d+\s", mm.group(1)) else f'<h3 id="{slug(mm.group(1))}">{mm.group(1)}</h3>', resto)
        clase = ' class="refs"' if hid == L["refs"] else ""
        etiqueta = (f"{num}. {titulo}" if num else re.sub(r"<[^>]+>", "", titulo))
        entradas.append((hid, etiqueta))
        salida.append(f'<section id="{hid}"{clase}>{nuevo_h2}{resto}</section>')
    cuerpo = "".join(salida)
    if intro.strip():
        cuerpo = f'<div class="intro">{intro}</div>' + cuerpo

    cuerpo = autolink(cuerpo, anexos=autolink_anexos, idioma=idioma)
    return cuerpo, entradas


def autolink(h, anexos=True, idioma="es"):
    """Enlaza 'Anexo A' / 'Anexo B' y las URL sueltas en el texto corrido (fuera de enlaces, títulos y código)."""
    out, pila = [], []
    for tok in re.split(r"(<[^>]+>)", h):
        if tok.startswith("<"):
            m = re.match(r"<(/?)(a|h1|h2|h3|code)\b", tok)
            if m:
                if m.group(1):
                    if pila:
                        pila.pop()
                else:
                    pila.append(m.group(2))
            out.append(tok)
        else:
            if not pila:
                if anexos:
                    pal = IDIOMAS[idioma]["anexo_palabra"]
                    pre = IDIOMAS[idioma]["prefijo"]
                    tok = re.sub(rf"\b{pal} ([AB])\b",
                                 lambda mm: f'<a href="{pre}anexo-{mm.group(1).lower()}.html">{pal} {mm.group(1)}</a>', tok)
                tok = re.sub(r"(https?://[^\s<>()]+[^\s<>().,;:])",
                             lambda mm: f'<a href="{mm.group(1)}" rel="noopener">{mm.group(1)}</a>', tok)
            out.append(tok)
    return "".join(out)


# --- Plantilla ----------------------------------------------------------------
ICONO_SOL = ('<svg class="icono-sol" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
             'stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/>'
             '<path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>')
ICONO_LUNA = ('<svg class="icono-luna" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
              'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/></svg>')


def nav_html(actual, idioma="es", clase="nav", etiqueta=None):
    L = IDIOMAS[idioma]
    etiqueta = etiqueta or L["nav_aria"]
    pre = L["prefijo"]
    claves = ("paper_en", "a", "b") if idioma == "en" else ("paper", "a", "b")
    items = []
    for clave in claves:
        p = PAGINAS[clave]
        if clave == "paper_en":
            href = "index.html"
        else:
            href = pre + p["archivo"]
        cur = ' aria-current="page"' if clave == actual else ""
        etiqueta_item = L["nav"]["paper"] if clave.startswith("paper") else L["nav"][clave]
        items.append(f'<a href="{href}"{cur}>{etiqueta_item}</a>')
    items.append(f'<a href="{REPO_URL}" rel="noopener">{L["nav"]["repo"]}</a>')
    return f'<nav class="{clase}" aria-label="{etiqueta}">' + "".join(items) + "</nav>"


def selector_idioma(idioma):
    """ES | EN. El inglés existe solo para el paper: desde los anexos, EN lleva al paper en inglés."""
    L = IDIOMAS[idioma]
    if idioma == "es":
        es_href, en_href = "index.html", "en/index.html"
    else:
        es_href, en_href = "../index.html", "index.html"
    ces = ' aria-current="true"' if idioma == "es" else ""
    cen = ' aria-current="true"' if idioma == "en" else ""
    return (f'<nav class="idiomas" aria-label="{L["idioma_aria"]}">'
            f'<a href="{es_href}" lang="es" hreflang="es"{ces}>ES</a>'
            f'<a href="{en_href}" lang="en" hreflang="en"{cen}>EN</a></nav>')


def pagina(clave, titulo_doc, descripcion, hero, cuerpo, entradas, extra_scripts="", idioma="es"):
    p = PAGINAS[clave]
    L = IDIOMAS[idioma]
    pre = L["prefijo"]
    url = f"{SITE_URL}/{'' if p['archivo'] == 'index.html' else p['archivo'].replace('en/index.html', 'en/')}"
    indice = "".join(f'<li><a href="#{hid}">{esc(t)}</a></li>' for hid, t in entradas)
    if clave in ("paper", "paper_en"):
        alternos = (f'<link rel="alternate" hreflang="es" href="{SITE_URL}/">\n'
                    f'<link rel="alternate" hreflang="en" href="{SITE_URL}/en/">\n'
                    f'<link rel="alternate" hreflang="x-default" href="{SITE_URL}/">')
    else:
        alternos = ""
    otro_locale = ""
    if clave == "paper":
        otro_locale = '<meta property="og:locale:alternate" content="en_US">'
    elif clave == "paper_en":
        otro_locale = '<meta property="og:locale:alternate" content="es_AR">'
    og_img = f"{SITE_URL}/assets/og-en.png" if idioma == "en" else f"{SITE_URL}/assets/og.png"
    inicio = "index.html"
    return f"""<!doctype html>
<html lang="{L['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(titulo_doc)} — {SITE_NAME}</title>
<meta name="description" content="{esc(descripcion)}">
<meta name="author" content="{esc(AUTOR)}">
<link rel="canonical" href="{url}">
{alternos}
<meta name="theme-color" content="#edf0ec" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#11181b" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="article">
<meta property="og:locale" content="{L['og_locale']}">
{otro_locale}
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{esc(titulo_doc)}">
<meta property="og:description" content="{esc(descripcion)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(L['og_alt'])}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{pre}assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="{pre}assets/fonts/literata-latin-opsz-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{pre}assets/fonts/archivo-latin-wdth-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{pre}assets/style.css">
<script>try{{var t=localStorage.getItem("tema");if(t)document.documentElement.setAttribute("data-tema",t)}}catch(e){{}}</script>
</head>
<body class="{"anexo" if clave in ("a", "b") else "paper"}">
<a class="salto" href="#contenido">{L['salto']}</a>
<header class="barra">
  <a class="marca" href="{inicio}" aria-label="{SITE_NAME}, {L['inicio']}">Error<b>Valor</b>-IA</a>
  {nav_html(clave, idioma)}
  <div class="herramientas">
    {selector_idioma(idioma)}
    <button class="boton-icono" id="boton-tema" type="button" aria-label="{L['tema']}">{ICONO_SOL}{ICONO_LUNA}</button>
    <button class="boton-icono" id="boton-menu" type="button" aria-expanded="false" aria-controls="lateral">{L['menu']}</button>
  </div>
</header>
{hero}
<div class="pagina">
  <aside class="lateral" id="lateral" aria-label="{L['lateral_aria']}">
    {nav_html(clave, idioma, "nav-movil", L['nav_movil_aria'])}
    {svg_anillo(entradas)}
    <p class="contenido-titulo">{L['en_esta_pagina']}</p>
    <ol class="indice">{indice}</ol>
  </aside>
  <main class="prosa" id="contenido">
{cuerpo}
  </main>
</div>
<footer class="pie">
  <div>
    <p>{L['pie1'].format(autor=esc(AUTOR))}</p>
    <p>{L['pie2'].format(autor=esc(AUTOR))}</p>
    <p><a href="{REPO_URL}" rel="noopener">{L['pie3']}</a></p>
  </div>
</footer>
<script src="{pre}assets/site.js" defer></script>
{extra_scripts}
</body>
</html>
"""


# --- Armado de cada página -----------------------------------------------------
def construir_paper(clave, idioma):
    L = IDIOMAS[idioma]
    pg = PAGINAS[clave]
    texto = (SRC / pg["fuente"]).read_text(encoding="utf-8")
    h1, autor, version, resto = separar_cabecera(texto)
    principal, _, sub = h1.partition(":")
    sub = sub.strip()
    cuerpo_html, entradas = procesar_cuerpo(md_a_html(resto), autolink_anexos=True, editorial=True, idioma=idioma)
    ficha = ""
    if autor or version:
        ficha = '<dl class="ficha">'
        if autor:
            ficha += f"<dt>{L['autor']}</dt><dd>{esc(autor)}</dd>"
        if version:
            ficha += f"<dt>{L['version']}</dt><dd>{esc(version)}</dd>"
        ficha += "</dl>"
    pdf = L["prefijo"] + pg["pdf"]
    hero = f"""<section class="portada" aria-labelledby="titulo">
  <div>
    <h1 id="titulo">{esc(principal.strip())}</h1>
    {f'<p class="subtitulo">{esc(sub)}</p>' if sub else ''}
    {ficha}
    <div class="acciones">
      <a class="boton principal" href="{pdf}" download>{L['pdf']}</a>
    </div>
  </div>
  <figure class="figura-panoptico">
    {svg_panoptico(titulo=L['pano_titulo'])}
    <figcaption><span class="leyenda"><i class="tenue"></i>{L['leyenda1']}</span><span class="leyenda"><i class="fuerte"></i>{L['leyenda2']}</span></figcaption>
  </figure>
</section>"""
    destino = ROOT / pg["archivo"]
    destino.parent.mkdir(exist_ok=True)
    destino.write_text(
        pagina(clave, h1, L["desc_paper"], hero, cuerpo_html, entradas, idioma=idioma), encoding="utf-8")


def construir():
    construir_paper("paper", "es")
    construir_paper("paper_en", "en")

    # Anexos (solo en español)
    for clave, desc in (("a", DESC_A), ("b", DESC_B)):
        p = PAGINAS[clave]
        texto = (SRC / p["fuente"]).read_text(encoding="utf-8")
        assert "</" not in texto, "El Markdown contiene '</'; escaparlo antes de incrustarlo"
        h1, _, _, resto = separar_cabecera(texto)
        cuerpo_html, entradas = procesar_cuerpo(md_a_html(resto), autolink_anexos=False)
        cuerpo = f'<div class="hoja">{cuerpo_html}</div>'
        hero = f"""<section class="encabezado-anexo" aria-labelledby="titulo">
  <h1 id="titulo">{esc(h1)}</h1>
  <p>{esc(desc)}</p>
  <div class="acciones">
    <a class="boton principal" href="{p['pdf']}" download>Descargar PDF</a>
    <button class="boton" id="boton-copiar" type="button">Copiar plantilla</button>
    <span class="estado" id="estado-copia" role="status" aria-live="polite"></span>
  </div>
</section>"""
        extra = f'<script type="text/plain" id="fuente-md">\n{texto}</script>'
        (ROOT / p["archivo"]).write_text(
            pagina(clave, h1, desc, hero, cuerpo, entradas, extra), encoding="utf-8")

    (ROOT / "assets" / "favicon.svg").write_text(svg_favicon(), encoding="utf-8")
    print("Sitio generado:", ", ".join(p["archivo"] for p in PAGINAS.values()))


if __name__ == "__main__":
    construir()
