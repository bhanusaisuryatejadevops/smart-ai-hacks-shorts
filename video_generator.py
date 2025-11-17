import os
import subprocess
import logging

VIDEO_DIR = "assets/output"
os.makedirs(VIDEO_DIR, exist_ok=True)
logger = logging.getLogger("video_generator")

def make_video_from_assets(image_paths, audio_path):
    output_path = os.path.join(VIDEO_DIR, "final_video.mp4")
    list_file = "image_list.txt"
    with open(list_file, "w") as f:
        for image in image_paths:
            f.write(f"file '{image}'\n")
            f.write("duration 1.3\n")
        f.write(f"file '{image_paths[-1]}'\n")
    cmd = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", list_file,
        "-i", audio_path,
        "-vf", "scale=1080:1920",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        output_path
    ]
    logger.info("Running FFmpeg to create video...")
    subprocess.run(cmd, check=True)
    logger.info(f"Video created: {output_path}")
    return output_path
