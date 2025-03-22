import datetime
from e2b_code_interpreter import Sandbox
import glob

E2B_API_KEY = "e2b_af8f93d273358e7b4001997b507d82ea32f3aab0"  # e2b_af8f93d273358e7b4001997b507d82ea32f3aab0


def initialize_box(sbx):
    sbx.commands.run("sudo apt-get update && sudo apt-get install -y libsdl-pango-dev")
    sbx.commands.run("pip install manim")


def generate_video(scripts_scene, videos_output_path):
    with Sandbox(api_key=E2B_API_KEY) as sbx:
        initialize_box(sbx)

        for script, scene_name in scripts_scene:
            with open(script, "r") as file:
                sbx.files.write(f"/home/user/{script.split('/')[-1]}", file)

            sbx.commands.run(f"manim /home/user/code.py {scene_name}")

            content = sbx.files.read(f'/home/user/media/videos/code/1080p60/{scene_name}.mp4', format='bytes')
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

            output_filename = f"{scene_name}-{timestamp}.mp4"
            with open(f'{videos_output_path}/{output_filename}', "wb") as file:
                file.write(content)


def merge_videos(videos, output_path="merged_video.mp4"):
    pass


if __name__ == '__main__':
    scripts_scene = [('code.py', 'SquareToCircle'), ('code.py', 'SquareToCircle')]
    generate_video(scripts_scene, 'videos')
    video_files = glob.glob("./videos/*.mp4")
    print(video_files)
    a = merge_videos(video_files)
