# video_generator.py
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw
import logging

logger = logging.getLogger(__name__)

# -----------------------------
# 1️⃣ Generate simple backgrounds
# -----------------------------
def generate_backgrounds(num_bg=3):
    bg_dir = Path("assets/background")
    bg_dir.mkdir(parents=True, exist_ok=True)
    bg_paths = []

    for i in range(1, num_bg + 1):
        img_path = bg_dir / f"bg_{i}.png"
        # Create a simple colored gradient background
        img = Image.new("RGB", (1080, 1080), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, 1080, 1080], fill=(i*50 % 256, i*80 % 256, i*120 % 256))
        img.save(img_path)
        bg_paths.append(str(img_path))

    return bg_paths

# -----------------------------
# 2️⃣ Generate img_list.txt for ffmpeg
# -----------------------------
def generate_img_list(bg_paths, duration=5):
    output_file = Path("assets/output/img_list.txt")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for path in bg_paths:
        lines.append(f"file '{path}'")
        lines.append(f"duration {duration}")
    # repeat last image for ffmpeg compatibility
    lines.append(f"file '{bg_paths[-1]}'")
    output_file.write_text("\n".join(lines))
    return str(output_file)

# -----------------------------
# 3️⃣ Make video from audio + backgrounds
# -----------------------------
def make_video_from_assets(audio_path, script=""):
    try:
        # Auto-generate backgrounds
        bg_paths = generate_backgrounds()

        # Auto-generate img_list.txt
        img_list_file = generate_img_list(bg_paths)

        # Output video path
        output_path = Path("assets/output") / f"short_{abs(hash(script)) % (10**9)}.mp4"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # ffmpeg command
        ffmpeg_cmd = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(img_list_file),
            "-i", str(audio_path),
            "-vf", "scale=1080:1920,format=yuv420p",
            "-c:v", "libx264", "-c:a", "aac", "-shortest", str(output_path)
        ]

        logger.info(f"Running ffmpeg command: {' '.join(ffmpeg_cmd)}")
        subprocess.run(ffmpeg_cmd, check=True)
        logger.info(f"Video generated: {output_path}")
        return str(output_path)

    except Exception as e:
        logger.exception("Failed to generate video")
        raise
