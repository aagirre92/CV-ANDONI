import os
import sys
from anthropic import Anthropic

# MAIN EXECUTION LOGIC Setup
api_key = os.environ.get("CLAUDE_API_KEY")
if not api_key:
    print("Error: CLAUDE_API_KEY environment variable not set.")
    sys.exit(1)

client = Anthropic(api_key=api_key)

# 1. Define the model
MODEL = "claude-haiku-4-5"

# 2. Define the exact rules for Claude
SYSTEM_PROMPT = """You are an expert technical translator. Translate the provided Markdown CV from Spanish to English.

CRITICAL RULES:
1. Preserve exact Markdown structure, spacing, and formatting.
2. Preserve the exact YAML frontmatter. ONLY translate textual values (like the subtitle). DO NOT translate YAML keys.
3. DO NOT translate any LaTeX commands, packages, or variables (e.g., \\usepackage, \\faMapMarker*).
4. Do not translate proper names.
5. Output ONLY the translated markdown."""

# Helper functions
def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)

def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)

def chat(messages, system=None, temperature=0.0, stop_sequences=[]):
    params = {
        "model": MODEL,
        "max_tokens": 2000,
        "messages": messages,
        "temperature": temperature,
        "stop_sequences": stop_sequences,
    }

    if system:
        params["system"] = [
            {
                "type": "text",
                "text": system
                # CANNOT CACHE IF SYSTEM PROMPT IS LESS THAN 1024 TOKENS =(
            }
        ]

    message = client.messages.create(**params)
    return message.content[0].text

def translate_cv_to_en(prompt):
    messages = []
    add_user_message(messages, prompt)
    
    # Assistant prefill: forces Claude to skip conversational text
    add_assistant_message(messages, "```markdown")
    
    # Pass the SYSTEM_PROMPT here!
    text = chat(messages, system=SYSTEM_PROMPT, stop_sequences=["```"])
    
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

            # Ensure there are no lingering backticks at the very end
            translated_content = translated_content.strip().strip("`")

            new_filename = file_path.replace("_ES.MD", "_EN.MD").replace("_ES.md", "_EN.md")
            
            with open(new_filename, 'w', encoding='utf-8') as f:
                f.write(translated_content)
                
            print(f"Successfully generated {new_filename}")
            
        except Exception as e:
            print(f"Error translating {file_path}: {e}")

if __name__ == "__main__":
    # Grab the exact files passed from the GitHub Action
    files = sys.argv[1:]
    if not files:
        print("No files were modified in this commit. Skipping translation.")
        sys.exit(0)
    
    translate_markdown(files)