# ErrorValor-IA

**Gestionar el error en la era de la IA: del panóptico a la cultura del aprendizaje.**

Paper de Martín Dopazo sobre cómo gestionar equipos de desarrollo cuando la IA escribe código más rápido de lo que podemos revisarlo y entenderlo. Propone un entorno donde el error se ve, se discute y se aprende, y distingue culpa de responsabilidad.

Sitio: https://mardopazo.github.io/ErrorValor-IA/

## Qué hay en el repositorio

| Ruta | Contenido |
|---|---|
| `index.html` | El paper |
| `anexo-a.html` | Anexo A. Plantilla de post-mortem sin culpa |
| `anexo-b.html` | Anexo B. Pautas para dailys sin vigilancia |
| `fuentes/` | Los textos en Markdown. **Es lo que se edita.** |
| `descargas/` | PDF del paper y de los anexos (lo que se ofrece para descargar) |
| `assets/` | Estilos, script, tipografías, imagen para compartir |
| `borradores/` | Versiones anteriores y notas de revisión |
| `build.py` | Genera las páginas HTML a partir de `fuentes/` |
| `tools/generar_pdf.py` | Genera los PDF a partir de las páginas HTML |
| `_config.yml` | Excluye del sitio los Markdown, los borradores y las herramientas |

## Cómo se actualiza

1. Editar los archivos de `fuentes/`.
2. Regenerar las páginas:

   ```
   pip install markdown
   python build.py
   ```

3. Regenerar los PDF (requiere Python con Playwright):

   ```
   pip install playwright
   playwright install chromium
   python tools/generar_pdf.py
   ```

4. Hacer commit y push. GitHub Pages publica los HTML y los PDF.

Los Markdown de `fuentes/` y los `borradores/` están en el repositorio pero **no se sirven en el sitio** (ver `_config.yml`).

## Cómo se publica en GitHub Pages

En el repositorio: **Settings → Pages → Build and deployment → Source: Deploy from a branch**, rama `main`, carpeta `/ (root)`.

## Tipografías

Archivo y Literata, incluidas en `assets/fonts/` bajo licencia SIL Open Font License 1.1 (ver los archivos de licencia en esa carpeta).

## Licencia del contenido

Pendiente de definir.
