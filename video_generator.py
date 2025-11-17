# video_generator.py
import os
import subprocess
from pathlib import Path
import logging

logger = logging.getLogger(__name__)
OUT_DIR = Path("assets/output")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def make_video_from_assets(audio_path: str, bg_image_paths: list, script_text: str) -> str:
    """
    Create a 9:16 video by concatenating images and adding audio using ffmpeg.
    bg_image_paths: list of images (ideally 1080x1920)
    audio_path: mp3 path
    """
    img_list_file = OUT_DIR / "img_list.txt"
    with open(img_list_file, "w") as f:
        for img in bg_image_paths:
            f.write(f"file '{os.path.abspath(img)}'\n")
            # Each image is displayed 3 seconds
            f.write("duration 3\n")
        # Repeat last image duration line
        f.write(f"file '{os.path.abspath(bg_image_paths[-1])}'\n")

    out_file = OUT_DIR / f"short_{abs(hash(audio_path)) % (10**9)}.mp4"

    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(img_list_file),
        "-i", audio_path,
        "-vf", "scale=1080:1920,format=yuv420p",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        str(out_file)
    ]

    logger.info(f"Running ffmpeg command: {' '.join(ffmpeg_cmd)}")
    subprocess.run(ffmpeg_cmd, check=True)
    return str(out_file)
