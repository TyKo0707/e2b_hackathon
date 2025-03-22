import os
from anthropic import Anthropic

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
E2B_API_KEY = os.getenv("E2B_API_KEY")
MODEL_NAME = 'claude-3-5-haiku-latest'

SYSTEM_PROMPT = """
You are an expert level Manim (Python library that 3B1B uses) expert.
"""

tools = [
    {
        "name": "execute_python",
        "description": "Execute python code in a Jupyter notebook cell and returns any result, stdout, stderr, display_data, and error.",
        "input_schema": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "The python code to execute in a single cell."
                }
            },
            "required": ["code"]
        }
    }
]

def code_interpret(e2b_code_interpreter, code):
  print("Running code interpreter...")
  exec = e2b_code_interpreter.run_code(code,
  on_stderr=lambda stderr: print("[Code Interpreter]", stderr),
  on_stdout=lambda stdout: print("[Code Interpreter]", stdout))

  if exec.error:
    print("[Code Interpreter ERROR]", exec.error)
  else:
    return exec.results
  


client = Anthropic(
    api_key=ANTHROPIC_API_KEY,
)

def process_tool_call(sbx, tool_name, tool_input):
    if tool_name == "execute_python":
        return code_interpret(sbx, tool_input["code"])
    return []

def chat_with_claude(e2b_code_interpreter, user_message):
    print(f"\n{'='*50}\nUser Message: {user_message}\n{'='*50}")

    message = client.messages.create(
        model=MODEL_NAME,
        system=SYSTEM_PROMPT,
        max_tokens=4096,
        messages=[{"role": "user", "content": user_message}],
        tools=tools,
    )

    print(f"\nInitial Response:")
    print(f"Stop Reason: {message.stop_reason}")
    print(f"Content: {message.content}")

    if message.stop_reason == "tool_use":
        tool_use = next(block for block in message.content if block.type == "tool_use")
        tool_name = tool_use.name
        tool_input = tool_use.input

        print(f"\nTool Used: {tool_name}")
        print(f"Tool Input: {tool_input}")

        code_interpreter_results = process_tool_call(e2b_code_interpreter, tool_name, tool_input)

        print(f"Tool Result: {code_interpreter_results}")
        return code_interpreter_results

from e2b_code_interpreter import Sandbox

with Sandbox(api_key=E2B_API_KEY) as sbx:
    sbx.commands.run("sudo apt-get update && sudo apt-get install -y pangocairo") # This will install the cowsay package
    sbx.commands.run("sudo apt-get update && sudo apt-get install -y libsdl-pango-dev") # This will install the cowsay package
    sbx.commands.run("pip install manimgl") # This will install the cowsay package
    execution = sbx.run_code("""
    from manimlib import *

    class InteractiveDevelopment(Scene):
        def construct(self):
            circle = Circle()
            circle.set_fill(BLUE, opacity=0.5)
            circle.set_stroke(BLUE_E, width=4)
            square = Square()

            self.play(ShowCreation(square))
            self.wait()

            # This opens an iPython terminal where you can keep writing
            # lines as if they were part of this construct method.
            # In particular, 'square', 'circle' and 'self' will all be
            # part of the local namespace in that terminal.
            self.embed()

            # Try copying and pasting some of the lines below into
            # the interactive shell
            self.play(ReplacementTransform(square, circle))
            self.wait()
            self.play(circle.animate.stretch(4, 0))
            self.play(Rotate(circle, 90 * DEGREES))
            self.play(circle.animate.shift(2 * RIGHT).scale(0.25))

            text = Text("In general, using the interactive shell is very helpful when developing new scenes")
            self.play(Write(text))

            # In the interactive shell, you can just type
            # play, add, remove, clear, wait, save_state and restore,
            # instead of self.play, self.add, self.remove, etc.

            # To interact with the window, type touch().  You can then
            # scroll in the window, or zoom by holding down 'z' while scrolling,
            # and change camera perspective by holding down 'd' while moving
            # the mouse.  Press 'r' to reset to the standard camera position.
            # Press 'q' to stop interacting with the window and go back to
            # typing new commands into the shell.

            # In principle you can customize a scene to be responsive to
            # mouse and keyboard interactions
            always(circle.move_to, self.mouse_point)

    if __name__ == '__main__':
        os.system("manimgl /home/tymofii/hackaton/e2b_hackathon/start.py InteractiveDevelopment -os")
    """)
    sbx.files.write("./hello.txt", "helloworld")
    execution1 = sbx.files.list('')

    print(execution1)

    execution1 = sbx.files. ('')

    print(execution1)

    execution2 = sbx.files.list('')
    