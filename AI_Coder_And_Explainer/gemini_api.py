import google.generativeai as genai
import os

# API key configure
genai.configure(api_key="AIzaSyBJnLpWyU94PCrjB4ohXGicDt8yfERDLTc")

def get_fixed_code(code, explain=False):
    # Yeh code ab exact current file ke directory se prompt_template.txt dhoondta hai
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(current_dir, "prompt_template.txt")

    # Check karo ke prompt_template.txt exist karti hai
    if not os.path.exists(prompt_path):
        raise FileNotFoundError(f"prompt_template.txt not found at {prompt_path}")

    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt = f.read()

    prompt = prompt.replace("<CODE_HERE>", code)

    if not explain:
        prompt = prompt.split("3.")[0] + f"\n\nHere is the code:\n{code}"

    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)
    return response.text
