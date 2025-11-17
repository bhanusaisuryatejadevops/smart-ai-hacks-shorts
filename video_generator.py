import os
import subprocess
from PIL import Image

OUTPUT_DIR = "assets/output"
BACKGROUND_DIR = "assets/background"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def make_video_from_assets(bg_paths, audio_path, output_name="final_video.mp4"):
    """
    Generate a final video using background images (or videos) + audio.
    """

    print("✔ Using background assets:", bg_paths)
    print("✔ Using audio:", audio_path)

    # ----------------------------------------------------
    # Ensure absolute paths for ffmpeg (THIS FIXES YOUR ERROR)
    # ----------------------------------------------------
    abs_bg_paths = [os.path.abspath(p) for p in bg_paths]
    abs_audio = os.path.abspath(audio_path)
    abs_output = os.path.abspath(os.path.join(OUTPUT_DIR, output_name))

    # ----------------------------------------------------
    # 1. Create img_list.txt for ffmpeg slideshow
    # ----------------------------------------------------
    img_list_file = os.path.abspath(os.path.join(OUTPUT_DIR, "img_list.txt"))
    with open(img_list_file, "w") as f:
        for img in abs_bg_paths:
            f.write(f"file '{img}'\n")
            f.write("duration 2\n")   # 2 seconds per slide

        # Repeat last frame so slideshow holds
        f.write(f"file '{abs_bg_paths[-1]}'\n")

    print("✔ Created list:", img_list_file)

    # ----------------------------------------------------
    # 2. Create slideshow video (no audio yet)
    # ----------------------------------------------------
    slideshow_path = os.path.abspath(os.path.join(OUTPUT_DIR, "slideshow.mp4"))

    slideshow_cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", img_list_file,
        "-vf", "scale=1080:1920",
        "-r", "30",
        slideshow_path
    ]

    print("▶ Running FFmpeg slideshow...")
    subprocess.run(slideshow_cmd, check=True)
    print("✔ Slideshow created:", slideshow_path)

    # ----------------------------------------------------
    # 3. Merge slideshow + audio
    # ----------------------------------------------------
    final_cmd = [
        "ffmpeg", "-y",
        "-i", slideshow_path,
        "-i", abs_audio,
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        abs_output
    ]

    print("▶ Running FFmpeg final combine...")
    subprocess.run(final_cmd, check=True)

    print("🎉 FINAL VIDEO READY:", abs_output)
    return abs_output
