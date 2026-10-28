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
| `assets/` | Estilos, script, tipografías, imagen para compartir |
| `borradores/` | Versiones anteriores y notas de revisión |
| `build.py` | Genera las páginas HTML a partir de `fuentes/` |

## Cómo se actualiza

1. Editar los archivos de `fuentes/`.
2. Regenerar las páginas:

   ```
   pip install markdown
   python build.py
   ```

3. Hacer commit y push. GitHub Pages publica los HTML tal como están.

## Cómo se publica en GitHub Pages

En el repositorio: **Settings → Pages → Build and deployment → Source: Deploy from a branch**, rama `main`, carpeta `/ (root)`.

## Tipografías

Archivo y Literata, incluidas en `assets/fonts/` bajo licencia SIL Open Font License 1.1 (ver los archivos de licencia en esa carpeta).

## Licencia del contenido

Pendiente de definir.
