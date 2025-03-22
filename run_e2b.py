from e2b_code_interpreter import Sandbox

E2B_API_KEY = "..."


def initialize_box(sbx):
    sbx.commands.run("sudo apt-get update && sudo apt-get install -y libsdl-pango-dev")
    sbx.commands.run("pip install manim")


def generate_video(code: str, scene_name: str):
    with Sandbox(api_key=E2B_API_KEY) as sbx:
        initialize_box(sbx)

        with open(code, "r") as file:
            sbx.files.write(f"/home/user/{code.split('/')[-1]}", file)

        sbx.commands.run(f"manim /home/user/code.py {scene_name}")

        content = sbx.files.read(f'/home/user/media/videos/code/1080p60/{scene_name}.mp4', format='bytes')
        with open("SquareToCircle.mp4", "wb") as file:
            file.write(content)


if __name__ == '__main__':
    generate_video("code.py", "SquareToCircle")
