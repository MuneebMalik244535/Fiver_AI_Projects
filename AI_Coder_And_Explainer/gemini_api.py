
import google.generativeai as genai
import os

# Direct API key likha hai abhi
genai.configure(api_key="AIzaSyBJnLpWyU94PCrjB4ohXGicDt8yfERDLTc")

def get_fixed_code(code, explain=False):
    # Find the full path of prompt_template.txt correctly
    current_dir = os.path.dirname(__file__)
    prompt_path = os.path.join(current_dir, "prompt_template.txt")

    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt = f.read()

    prompt = prompt.replace("<CODE_HERE>", code)

    if not explain:
        prompt = prompt.split("3.")[0] + f"\n\nHere is the code:\n{code}"

    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)
    return response.text
