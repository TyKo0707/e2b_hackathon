import os
from e2b_code_interpreter import Sandbox
from anthropic import Anthropic
import ast

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
E2B_API_KEY = os.getenv("E2B_API_KEY")
MODEL_NAME = "claude-3-7-sonnet-latest"

SYSTEM_PROMPT = """
You are an expert level Manim (Python library that 3B1B uses) expert. 
Return only code without any explanation. DO NOT USE LATEX.

Here are examples of scenes:
Square to circle animation:
```
from manim import *

class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        square.flip(RIGHT)
        square.rotate(-3 * TAU / 8)
        circle.set_fill(PINK, opacity=0.5)

        self.play(Create(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(square))
```
"""

def ask_claude(system_prompt, user_message, api_key, model_name):
    client = Anthropic(api_key=api_key)
    
    print(f"\n{'='*50}\nUser Message: {user_message}\n{'='*50}")

    message = client.messages.create(
        model=model_name,
        system=system_prompt,
        max_tokens=20096,
        messages=[{"role": "user", "content": user_message}],
        # tools=tools,
    )
    
    return message.content[0].text

def initialize_box(template=None):

    if not template:
        sbx = Sandbox(api_key=os.environ['E2B_API_KEY'], timeout=0)
        sbx.commands.run("sudo apt-get update && sudo apt-get install -y libsdl-pango-dev ffmpeg")
        sbx.commands.run("pip install manim")
    else:
        sbx = Sandbox(template="2ulazwy6l44ghm46535z", timeout=0)

    print('Sandbox initialized')

    return sbx

def generate_video(sbx, code: str, scene_name: str):
    with open(code, "r") as file:
        sbx.files.write(f"/home/user/{code.split('/')[-1]}", file)

    sbx.commands.run(f"manim /home/user/code.py {scene_name}", timeout=600)

    content = sbx.files.read(f'/home/user/media/videos/code/1080p60/{scene_name}.mp4', format='bytes')
    with open("SquareToCircle.mp4", "wb") as file:
        file.write(content)

def postprocess_program(program: str):
    program = program.replace("```", "")
    if program.startswith("python"): # stupid but "program.replace("```python", "")." doesn't work idk why
        program = program[len("python"):]
    return program

def get_class_names(program_code):
    """
    Extract all top-level class names from a Python program string.
    
    Args:
        program_code (str): String containing Python code.
        
    Returns:
        list of str: List of class names defined in the code.
    """
    tree = ast.parse(program_code)
    return [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

if __name__ == '__main__':
    print("Initializing E2B box...")
    sbx = initialize_box("2ulazwy6l44ghm46535z")
    print("Finished initializing E2B box.\n")

    user_prompt = f"Generate a Manim animation that visualizes how backpropagation works. Make it educational and intuitive. The length of the scene should not exceed 100 lines."

    print("Sending LLM call...")
    program = ask_claude(SYSTEM_PROMPT, user_prompt, ANTHROPIC_API_KEY, MODEL_NAME)
    program = postprocess_program(program)    
    print("Received response from LLM.\n")

    generated_program_filename = "code.py"
    
    with open(generated_program_filename, "w") as file:
        print(f"Generated program: {program}")
        file.write(program)

    print(f"Saved program with scenes to {generated_program_filename}.")

    for class_name in get_class_names(program):
        print(f"Processing {class_name} scene...")
        generate_video(sbx, generated_program_filename, class_name)