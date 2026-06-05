# 📄 CV Automation Pipeline

Este repositorio aloja mi Curriculum Vitae en formato Markdown (`.MD`) e implementa un flujo de CI/CD personalizado mediante GitHub Actions para automatizar su traducción y renderizado.

## ⚙️ ¿Cómo funciona?

El repositorio cuenta con un flujo de trabajo (Workflow) que se dispara automáticamente cada vez que se hace un `push` a la rama `main` modificando un archivo de CV. 

El pipeline realiza las siguientes tareas de forma desatendida:

1. **Traducción Automática (Claude AI):** 
   Si el commit incluye cambios en un currículum en español (archivos terminados en `_ES.MD`), un script en Python utiliza la API de Anthropic (claude-haiku-4-5) para traducirlo al inglés. El prompt del sistema está diseñado para traducir únicamente el texto humano, respetando estrictamente el *Frontmatter* YAML, la estructura Markdown y los comandos LaTeX (como los iconos de FontAwesome).
   > *Nota: El sistema está optimizado para identificar exactamente qué archivos han cambiado en el commit, evitando gastar tokens de la API en archivos no modificados.*

2. **Generación de PDFs (Pandoc + LaTeX):** 
   Una vez completada la traducción (o si se sube directamente un CV en inglés), el sistema compila todos los currículums `.MD` utilizando **Pandoc** y el motor **XeLaTeX**. Esto permite procesar fuentes modernas y caracteres Unicode (UTF-8) sin errores, generando documentos PDF con un formato profesional y limpio.

3. **Auto-Commit:** 
   Finalmente, los PDFs generados se guardan en la carpeta `/PDF/` añadiendo el sufijo `_AUTO.pdf` al nombre original, y el bot de GitHub Actions hace un commit automático integrando tanto el archivo `.MD` en inglés recién traducido como los PDFs actualizados de vuelta al repositorio.


## 🛠️ Tecnologías utilizadas

* **GitHub Actions:** Orquestación del pipeline CI/CD.
* **Python + Anthropic SDK:** Scripting y traducción inteligente basada en LLMs.
* **Pandoc & XeLaTeX:** Conversión de texto plano a PDF renderizando código LaTeX incrustado en Markdown.
* **tj-actions/changed-files:** Detección de cambios a nivel de commit para optimización de recursos.

---
*Desarrollado para mantener un CV siempre actualizado y en múltiples idiomas con el mínimo esfuerzo.*
