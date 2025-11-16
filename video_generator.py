# video_generator.py
import os
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip, TextClip
from pathlib import Path
import logging
import math

logger = logging.getLogger(__name__)
OUT_DIR = Path("assets/output")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def make_video_from_assets(audio_path: str, bg_image_paths: list, script_text: str, duration_target: float = None) -> str:
    """
    Create a 9:16 (1080x1920) video by animating the provided background images.
    audio_path: path to mp3
    bg_image_paths: list of image paths (square 1080x1080 recommended)
    script_text: used to generate captions overlay
    duration_target: if provided, enforce total length; otherwise use audio duration.
    """
    audio = AudioFileClip(audio_path)
    audio_duration = audio.duration
    if duration_target is None:
        duration_target = audio_duration

    per_img = duration_target / max(1, len(bg_image_paths))
    clips = []
    for img_path in bg_image_paths:
        img_clip = ImageClip(img_path).set_duration(per_img).resize(height=1920).fx(lambda c: c)
        # Center crop to 1080x1920
        img_clip = img_clip.crop(width=1080, height=1920, x_center=img_clip.w/2, y_center=img_clip.h/2)
        # optional zoom-in effect
        img_clip = img_clip.resize(lambda t: 1+0.02*t)
        clips.append(img_clip)

    video = concatenate_videoclips(clips, method="compose")
    # Add captions as a TextClip overlay (simple)
    # Split script into lines of ~40 chars
    lines = []
    for paragraph in script_text.split("\n"):
        paragraph = paragraph.strip()
        while len(paragraph) > 0:
            piece = paragraph[:40]
            # try break at space
            if len(paragraph) > 40:
                idx = piece.rfind(" ")
                if idx > 10:
                    piece = paragraph[:idx]
            lines.append(piece.strip())
            paragraph = paragraph[len(piece):].strip()
    # Show first 2 lines near top for entire video (simple approach)
    caption_text = "\n".join(lines[:6])
    txt_clip = TextClip(caption_text, fontsize=48, color='white', font='Amiri-Bold', method='label', align='center')
    txt_clip = txt_clip.set_position(('center', 150)).set_duration(duration_target).resize(width=900)

    final = CompositeVideoClip([video, txt_clip])
    final = final.set_audio(audio)
    out_file = OUT_DIR / f"short_{abs(hash(audio_path)) % (10**9)}.mp4"
    # write file with reasonable settings
    final.write_videofile(str(out_file), fps=30, codec="libx264", audio_codec="aac", threads=2, preset="medium", bitrate="3000k")
    return str(out_file)
