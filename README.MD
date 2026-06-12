# 📄 Curriculum Andoni - Pipeline

Este repositorio contiene mi Curriculum Vitae en formato Markdown (`.MD`) e implementa un flujo de CI/CD personalizado mediante GitHub Actions para automatizar su traducción y renderizado a PDF.

## ⚙️ ¿Cómo funciona?

El repositorio cuenta con un workflow que se dispara automáticamente cada vez que se hace un `push` a la rama `main` modificando un archivo de CV. 

El pipeline realiza las siguientes tareas de forma desatendida:

1. Traducción Automática al inglés (si procede)

2. **Generación de PDFs (Pandoc + xelatex)

3. **Auto-Commit


## 🛠️ Tecnologías utilizadas

* **GitHub Actions:** Orquestación del pipeline CI/CD.
* **Python + Gemini SDK:** Scripting y traducción inteligente basada en LLMs.
* **Pandoc & XeLaTeX:** Conversión de texto plano a PDF renderizando código LaTeX incrustado en Markdown.
* **tj-actions/changed-files:** Detección de cambios a nivel de commit para optimización de recursos.
