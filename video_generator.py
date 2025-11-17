import os
import subprocess
import logging

VIDEO_DIR = "assets/output"
os.makedirs(VIDEO_DIR, exist_ok=True)
logger = logging.getLogger("video_generator")

def make_video_from_assets(image_paths, audio_path, captions=None):
    """
    Creates a video slideshow with captions using FFmpeg.
    captions: list of strings (one for each image/segment)
    """
    if captions is None or len(captions) != len(image_paths):
        captions = ["" for _ in image_paths]

    # Set duration per image (change this depending on number of backgrounds and audio duration)
    duration = 1.3

    # Create individual video segments with text overlay
    segment_paths = []
    for idx, (img, text) in enumerate(zip(image_paths, captions)):
        segment_path = os.path.join(VIDEO_DIR, f"segment_{idx}.mp4")
        drawtext = f"drawtext=text='{text}':fontcolor=white:fontsize=72:borderw=2:x=(w-text_w)/2:y=h-200"
        cmd = [
            "ffmpeg",
            "-y",
            "-loop", "1",
            "-i", img,
            "-t", str(duration),
            "-vf", f"scale=1080:1920,{drawtext}",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-an",
            segment_path
        ]
        subprocess.run(cmd, check=True)
        segment_paths.append(segment_path)

    # Concatenate all segments
    with open("segments.txt", "w") as f:
        for p in segment_paths:
            f.write(f"file '{os.path.abspath(p)}'\n")

    concat_path = os.path.join(VIDEO_DIR, "concatenated.mp4")
    cmd = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", "segments.txt",
        "-c", "copy",
        concat_path
    ]
    subprocess.run(cmd, check=True)

    # Add audio, cut or pad to fit
    output_path = os.path.join(VIDEO_DIR, "final_video.mp4")
    cmd = [
        "ffmpeg",
        "-y",
        "-i", concat_path,
        "-i", audio_path,
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        output_path
    ]
    subprocess.run(cmd, check=True)
    logger.info(f"Video created: {output_path}")
    return output_path
