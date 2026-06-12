import os
import sys
from google import genai
from google.genai import types

# MAIN EXECUTION LOGIC Setup
# The genai.Client() will automatically look for this variable.
if not os.environ.get("GEMINI_API_KEY"):
    print("Error: GEMINI_API_KEY environment variable not set.")
    sys.exit(1)

# Initialize the modern client
client = genai.Client()

# 1. Define the model
MODEL = "gemini-3.5-flash"

# 2. Define the exact rules
SYSTEM_PROMPT = """You are an expert technical translator. Translate the provided Markdown CV from Spanish to English.

CRITICAL RULES:
1. Preserve exact Markdown structure, spacing, and formatting.
2. Preserve the exact YAML frontmatter. ONLY translate textual values (like the subtitle). DO NOT translate YAML keys.
3. DO NOT translate any LaTeX commands, packages, or variables (e.g., \\usepackage, \\faMapMarker*).
4. Do not translate proper names.
5. Output ONLY the translated markdown. Do NOT wrap the response in ```markdown formatting blocks or include any conversational filler."""

def translate_cv_to_en(prompt):
    # Pass the system prompt and temperature via GenerateContentConfig
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        temperature=0.0
    )
    
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=config
    )
    
    text = response.text
    print(text)
    return text

def translate_markdown(files_to_process):
    for file_path in files_to_process:
        print(f"Translating specifically: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        try:
            # Get the translated content
            translated_content = translate_cv_to_en(content)

            # Ensure there are no lingering backticks or markdown declarations at the edges
            translated_content = translated_content.strip().strip("`")
            if translated_content.lower().startswith("markdown"):
                translated_content = translated_content[8:].strip()

            new_filename = file_path.replace("_ES.MD", "_EN.MD").replace("_ES.md", "_EN.md")
            
            with open(new_filename, 'w', encoding='utf-8') as f:
                f.write(translated_content)
                
            print(f"Successfully generated {new_filename}")

        except Exception as e:
            print(f"🔴🔴🔴Error translating {file_path}: {e}")
            # No voy a raisear aquí, sino no me pasa a PDF...si no puede traducir por lo que sea, mala suerte

if __name__ == "__main__":
    # Grab the exact files passed from the GitHub Action
    files = sys.argv[1:]
    if not files:
        print("No files were modified in this commit. Skipping translation.")
        sys.exit(0)
    
    translate_markdown(files)