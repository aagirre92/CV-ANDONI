import os
import sys
import google.generativeai as genai

# MAIN EXECUTION LOGIC Setup
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY environment variable not set.")
    sys.exit(1)

# Configure the Gemini client
genai.configure(api_key=api_key)

# 1. Define the exact rules for Gemini
SYSTEM_PROMPT = """You are an expert technical translator. Translate the provided Markdown CV from Spanish to English.

CRITICAL RULES:
1. Preserve exact Markdown structure, spacing, and formatting.
2. Preserve the exact YAML frontmatter. ONLY translate textual values (like the subtitle). DO NOT translate YAML keys.
3. DO NOT translate any LaTeX commands, packages, or variables (e.g., \\usepackage, \\faMapMarker*).
4. Do not translate proper names.
5. Output ONLY the translated markdown. Do NOT wrap the response in ```markdown formatting blocks or include any conversational filler."""

# 2. Initialize the model
# gemini-1.5-flash is ideal for fast, high-quality text translation (and is free-tier friendly)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)

def translate_cv_to_en(prompt):
    # Set temperature to 0.0 for deterministic, literal translation output
    generation_config = genai.GenerationConfig(
        temperature=0.0
    )
    
    response = model.generate_content(
        prompt,
        generation_config=generation_config
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
                # Strip out the word "markdown" if the model accidentally included it
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