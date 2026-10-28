#!/usr/bin/env python3
"""Genera los PDF de descarga a partir de las páginas HTML del sitio.

Requiere:
    pip install playwright
    playwright install chromium

Uso (desde la raíz del repo, después de correr build.py):
    python tools/generar_pdf.py
"""
import asyncio
import functools
import http.server
import socketserver
import threading
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent

PDFS = [
    ("index.html", "descargas/ErrorValor-IA_Paper.pdf", "Gestionar el error en la era de la IA"),
    ("anexo-a.html", "descargas/ErrorValor-IA_Anexo-A_Post-mortem-sin-culpa.pdf", "Anexo A. Plantilla de post-mortem sin culpa"),
    ("anexo-b.html", "descargas/ErrorValor-IA_Anexo-B_Dailys-sin-vigilancia.pdf", "Anexo B. Pautas para dailys sin vigilancia"),
]

PIE = """
<div style="width:100%;font-family:Arial,sans-serif;font-size:8px;color:#4a5a60;padding:0 17mm;
            display:flex;justify-content:space-between;">
  <span>Martín Dopazo · ErrorValor-IA · {titulo}</span>
  <span><span class="pageNumber"></span> / <span class="totalPages"></span></span>
</div>
"""


def servir():
    class Silencioso(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args, **kwargs):
            pass

    handler = functools.partial(Silencioso, directory=str(ROOT))
    httpd = socketserver.TCPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


async def main():
    httpd = servir()
    base = f"http://127.0.0.1:{httpd.server_address[1]}/"
    (ROOT / "descargas").mkdir(exist_ok=True)
    async with async_playwright() as p:
        navegador = await p.chromium.launch()
        ctx = await navegador.new_context(color_scheme="light", reduced_motion="reduce")
        pagina = await ctx.new_page()
        for archivo, salida, titulo in PDFS:
            await pagina.goto(base + archivo)
            await pagina.evaluate("document.fonts.ready")
            await pagina.emulate_media(media="print", color_scheme="light")
            await pagina.pdf(
                path=str(ROOT / salida),
                format="A4",
                print_background=True,
                display_header_footer=True,
                header_template="<span></span>",
                footer_template=PIE.format(titulo=titulo),
                margin={"top": "18mm", "bottom": "20mm", "left": "17mm", "right": "17mm"},
                prefer_css_page_size=False,
            )
            print("PDF:", salida)
        await navegador.close()
    httpd.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
