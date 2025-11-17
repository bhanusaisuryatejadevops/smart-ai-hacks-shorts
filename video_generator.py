import os
import subprocess
import logging

VIDEO_DIR = "assets/output"
os.makedirs(VIDEO_DIR, exist_ok=True)
logger = logging.getLogger("video_generator")

def make_video_from_assets(image_paths, audio_path, captions=None):
    if captions is None or len(captions) != len(image_paths):
        captions = ["" for _ in image_paths]

    # Compute audio duration
    import wave
    import contextlib
    try:
        import mutagen
        audio = mutagen.File(audio_path)
        audio_len = audio.info.length
    except Exception:
        try:
            with contextlib.closing(wave.open(audio_path, 'rb')) as f:
                frames = f.getnframes()
                rate = f.getframerate()
                audio_len = frames / float(rate)
        except Exception:
            audio_len = 20.0
    duration = audio_len / len(image_paths)

    segment_paths = []
    for idx, (img, text) in enumerate(zip(image_paths, captions)):
        segment_path = os.path.join(VIDEO_DIR, f"segment_{idx}.mp4")
        safe_text = text.replace(":", " -").replace("'", "")
        drawtext = f"drawtext=fontsize=52:fontcolor=white:borderw=2:x=(w-text_w)/2:y=h-180:text='{safe_text}'"
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", img,
            "-t", str(duration),
            "-vf", f"scale=1080:1920,{drawtext}",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-an",
            segment_path
        ]
        subprocess.run(cmd, check=True)
        segment_paths.append(segment_path)
    with open("segments.txt", "w") as f:
        for p in segment_paths:
            f.write(f"file '{os.path.abspath(p)}'\n")
    concat_path = os.path.join(VIDEO_DIR, "concatenated.mp4")
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", "segments.txt",
        "-c", "copy",
        concat_path
    ]
    subprocess.run(cmd, check=True)
    output_path = os.path.join(VIDEO_DIR, "final_video.mp4")
    cmd = [
        "ffmpeg", "-y", "-i", concat_path, "-i", audio_path,
        "-c:v", "copy", "-c:a", "aac", "-shortest", output_path
    ]
    subprocess.run(cmd, check=True)
    logger.info(f"Video created: {output_path}")
    return output_path
