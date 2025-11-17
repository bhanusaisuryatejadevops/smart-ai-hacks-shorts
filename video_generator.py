# video_generator.py
import os
import subprocess
from pathlib import Path
import logging

logger = logging.getLogger(__name__)
OUT_DIR = Path("assets/output")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def _write_img_list(bg_paths, duration_per=3):
    list_file = OUT_DIR / "img_list.txt"
    with open(list_file, "w") as f:
        for p in bg_paths:
            abs_p = os.path.abspath(p)
            # ffmpeg concat requires both file and duration lines
            f.write(f"file '{abs_p}'\n")
            f.write(f"duration {duration_per}\n")
        # repeat last file to ensure proper concat behavior
        f.write(f"file '{os.path.abspath(bg_paths[-1])}'\n")
    return str(list_file)

def make_video_from_assets(audio_path: str, bg_paths: list, script_text: str = "", duration_per_img: int = 3) -> str:
    """
    Create a 9:16 video by concatenating bg_paths and overlaying audio_path.
    Uses ffmpeg (no MoviePy).
    Returns path to generated mp4.
    """
    # ensure ffmpeg available
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except Exception:
        raise RuntimeError("ffmpeg not found. Install ffmpeg in your environment or runner.")

    list_file = _write_img_list(bg_paths, duration_per=duration_per_img)
    slideshow_path = OUT_DIR / "slideshow.mp4"
    out_file = OUT_DIR / f"short_{abs(hash(audio_path)) % (10**9)}.mp4"

    # 1) make slideshow (scale & pad to 1080x1920)
    cmd_slideshow = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_file,
        "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
        "-r", "30",
        str(slideshow_path)
    ]
    logger.info("Running ffmpeg slideshow: %s", " ".join(cmd_slideshow))
    subprocess.run(cmd_slideshow, check=True)

    # 2) merge audio and slideshow (shortest)
    cmd_merge = [
        "ffmpeg", "-y",
        "-i", str(slideshow_path),
        "-i", str(audio_path),
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        str(out_file)
    ]
    logger.info("Merging audio + video: %s", " ".join(cmd_merge))
    subprocess.run(cmd_merge, check=True)

    logger.info("Video generated: %s", out_file)
    return str(out_file)
