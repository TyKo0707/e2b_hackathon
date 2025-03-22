import os
from e2b_code_interpreter import Sandbox
from anthropic import Anthropic
import ast

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
E2B_API_KEY = os.getenv("E2B_API_KEY")
MODEL_NAME = "claude-3-7-sonnet-latest"

SYSTEM_PROMPT = """
You are an expert level Manim (Python library that 3B1B uses) expert. 
Return only code without any explanation.

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

Boolean operators animation:
```
from manim import *

class BooleanOperations(Scene):
    def construct(self):
        ellipse1 = Ellipse(
            width=4.0, height=5.0, fill_opacity=0.5, color=BLUE, stroke_width=10
        ).move_to(LEFT)
        ellipse2 = ellipse1.copy().set_color(color=RED).move_to(RIGHT)
        bool_ops_text = MarkupText("<u>Boolean Operation</u>").next_to(ellipse1, UP * 3)
        ellipse_group = Group(bool_ops_text, ellipse1, ellipse2).move_to(LEFT * 3)
        self.play(FadeIn(ellipse_group))

        i = Intersection(ellipse1, ellipse2, color=GREEN, fill_opacity=0.5)
        self.play(i.animate.scale(0.25).move_to(RIGHT * 5 + UP * 2.5))
        intersection_text = Text("Intersection", font_size=23).next_to(i, UP)
        self.play(FadeIn(intersection_text))

        u = Union(ellipse1, ellipse2, color=ORANGE, fill_opacity=0.5)
        union_text = Text("Union", font_size=23)
        self.play(u.animate.scale(0.3).next_to(i, DOWN, buff=union_text.height * 3))
        union_text.next_to(u, UP)
        self.play(FadeIn(union_text))

        e = Exclusion(ellipse1, ellipse2, color=YELLOW, fill_opacity=0.5)
        exclusion_text = Text("Exclusion", font_size=23)
        self.play(e.animate.scale(0.3).next_to(u, DOWN, buff=exclusion_text.height * 3.5))
        exclusion_text.next_to(e, UP)
        self.play(FadeIn(exclusion_text))

        d = Difference(ellipse1, ellipse2, color=PINK, fill_opacity=0.5)
        difference_text = Text("Difference", font_size=23)
        self.play(d.animate.scale(0.3).next_to(u, LEFT, buff=difference_text.height * 3.5))
        difference_text.next_to(d, UP)
        self.play(FadeIn(difference_text))
```
"""

def ask_claude(system_prompt, user_message, api_key, model_name):
    client = Anthropic(api_key=api_key)
    
    print(f"\n{'='*50}\nUser Message: {user_message}\n{'='*50}")

    message = client.messages.create(
        model=model_name,
        system=system_prompt,
        max_tokens=4096,
        messages=[{"role": "user", "content": user_message}],
        # tools=tools,
    )
    
    return message.content[0].text

def initialize_box():
    sbx = Sandbox(api_key=E2B_API_KEY)

    sbx.commands.run("sudo apt-get update && sudo apt-get install -y libsdl-pango-dev")
    sbx.commands.run("pip install manim")
    
    return sbx

def generate_video(sbx, code: str, scene_name: str):
    with open(code, "r") as file:
        sbx.files.write(f"/home/user/{code.split('/')[-1]}", file)

    sbx.commands.run(f"manim /home/user/code.py {scene_name}")

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
    sbx = initialize_box()
    print("Finished initializing E2B box.\n")

    user_prompt = f"Generate a Manim animation that visualizes how backpropagation works in neural networks. Make it educational and intuitive. The scene MUST have a name BackpropagationScene"
    
    print("Sending LLM call...")
    program = ask_claude(SYSTEM_PROMPT, user_prompt, ANTHROPIC_API_KEY, MODEL_NAME)
    program = postprocess_program(program)    
    print("Received response from LLM.\n")

    generated_program_filename = "code.py"
    
    with open(generated_program_filename, "w") as file:
        file.write(program)

    print(f"Saved program with scenes to {generated_program_filename}.")

    for class_name in get_class_names(program):
        print(f"Processing {class_name} scene...")
        generate_video(sbx, generated_program_filename, class_name)