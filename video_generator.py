# video_generator.py
import os
import subprocess
from pathlib import Path
import logging
import math

logger = logging.getLogger(__name__)
OUT_DIR = Path("assets/output")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def make_video_from_assets(audio_path: str, bg_image_paths: list, script_text: str, duration_target: float = None) -> str:
    """
    Create a 9:16 video by combining background images with audio using ffmpeg.
    No MoviePy dependency.
    """
    if len(bg_image_paths) == 0:
        raise ValueError("No background images provided")

    out_file = OUT_DIR / f"short_{abs(hash(audio_path)) % (10**9)}.mp4"

    # Prepare image list file for ffmpeg
    list_file = OUT_DIR / "img_list.txt"
    per_img_duration = 3  # default 3 seconds per image
    with open(list_file, "w") as f:
        for img in bg_image_paths:
            f.write(f"file '{img}'\n")
            f.write(f"duration {per_img_duration}\n")
        # repeat last image for audio padding
        f.write(f"file '{bg_image_paths[-1]}'\n")

    # ffmpeg command to create video from images
    ffmpeg_cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_file),
        "-i", audio_path, "-vf", "scale=1080:1920,format=yuv420p",
        "-c:v", "libx264", "-c:a", "aac", "-shortest", str(out_file)
    ]

    logger.info(f"Running ffmpeg command: {' '.join(ffmpeg_cmd)}")
    subprocess.run(ffmpeg_cmd, check=True)
    return str(out_file)
