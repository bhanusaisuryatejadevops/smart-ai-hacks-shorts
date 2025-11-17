import os
import subprocess
import logging
from PIL import Image

logger = logging.getLogger(__name__)

OUTPUT_DIR = "assets/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def make_video_from_assets(images, audio_path):
    """
    Create a slideshow video (1080x1920) from given images + provided audio.
    """

    # 1️⃣ Create FFmpeg concat file
    list_file = os.path.join(OUTPUT_DIR, "img_list.txt")

    with open(list_file, "w") as f:
        for img in images:
            abs_path = os.path.abspath(img)
            f.write(f"file '{abs_path}'\n")
            f.write("duration 2\n")

    logger.info(f"✔ Created list: {list_file}")

    # 2️⃣ Final MP4 output file
    video_output = os.path.join(OUTPUT_DIR, "slideshow.mp4")

    # 3️⃣ FFmpeg slideshow creation
    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", list_file,
        "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
        "-r", "30",
        video_output,
    ]

    logger.info("▶ Running FFmpeg slideshow...")
    result = subprocess.run(ffmpeg_cmd, text=True)

    if result.returncode != 0:
        raise Exception("FFmpeg slideshow generation failed")

    # 4️⃣ Merge slideshow + audio
    final_video = os.path.join(OUTPUT_DIR, "final_output.mp4")

    merge_cmd = [
        "ffmpeg", "-y",
        "-i", video_output,
        "-i", audio_path,
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        final_video
    ]

    logger.info("▶ Merging audio + video...")
    result = subprocess.run(merge_cmd, text=True)

    if result.returncode != 0:
        raise Exception("FFmpeg merge failed")

    logger.info(f"🎉 Final video saved → {final_video}")
    return final_video
