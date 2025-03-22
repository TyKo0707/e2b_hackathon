import datetime
from e2b_code_interpreter import Sandbox
import glob

E2B_API_KEY = "..."


def initialize_box(sbx):
    """
    Set up the sandbox environment for rendering Manim animations.

    Installs necessary system packages and the Manim Python package inside the sandbox.

    Args:
        sbx (Sandbox): An instance of the E2B sandbox where commands will be run.

    Returns:
        None
    """
    sbx.commands.run("sudo apt-get update && sudo apt-get install -y libsdl-pango-dev")
    sbx.commands.run("pip install manim")


def generate_video(scripts_scene, videos_output_path):
    """
    Render Manim animations for multiple scripts and save them with timestamped filenames.

    This function creates a new sandbox environment, sets it up for Manim rendering,
    executes Manim commands for each provided script and scene, and saves the resulting
    videos to the specified output directory.

    Args:
        scripts_scene (list of tuples): List of (script_path, scene_name) pairs to render.
        videos_output_path (str): Directory where output videos will be saved.

    Returns:
        None
    """
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
    """
    Merge multiple MP4 videos into a single video.

    Args:
        videos (list): List of paths to the videos to merge
        output_path (str): Path where the merged video will be saved

    Returns:
        str: Path to the merged video
    """
    import subprocess
    import tempfile
    import os

    if not videos:
        print("No videos to merge")
        return None

    # Create a temporary file listing all input videos
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        for video in videos:
            f.write(f"file '{os.path.abspath(video)}'\n")
        temp_list_path = f.name

    # Use FFmpeg to concatenate the videos
    cmd = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", temp_list_path,
        "-c", "copy",  # Copy codecs without re-encoding for speed
        output_path
    ]

    try:
        subprocess.run(cmd, check=True)
        os.remove(temp_list_path)  # Clean up the temporary file
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"Error merging videos: {e}")
        os.remove(temp_list_path)  # Clean up even on error
        return None


if __name__ == '__main__':
    scripts_scene = [('simple.py', 'SquareToCircle'), ('simple.py', 'SquareToCircle')]
    generate_video(scripts_scene, 'videos')
    video_files = glob.glob("./videos/*.mp4")
    a = merge_videos(video_files)
