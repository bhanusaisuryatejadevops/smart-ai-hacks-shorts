import os
from moviepy.editor import *
import textwrap

ASSETS_DIR = "assets"
BACKGROUND_DIR = os.path.join(ASSETS_DIR, "background")
OUTPUT_DIR = os.path.join(ASSETS_DIR, "output")


def generate_caption_clips(script_text, video_duration):
    """Create MrBeast-style captions."""
    words = script_text.split()
    clips = []
    start = 0

    chunk = []
    for w in words:
        chunk.append(w)
        if len(chunk) >= 4:
            txt = " ".join(chunk)
            txt_clip = TextClip(
                txt,
                fontsize=60,
                color="white",
                font="Impact",
                stroke_color="black",
                stroke_width=3,
                method="caption",
                size=(1080, None)
            ).set_position(("center", 850)).set_duration(0.6).set_start(start)

            clips.append(txt_clip)
            start += 0.6
            chunk = []

    return clips


def load_background():
    """Load background video or generate fallback dynamic motion."""
    files = [f for f in os.listdir(BACKGROUND_DIR) if f.endswith((".mp4", ".mov"))]

    if not files:
        # fallback animated background (no more 3× colors)
        clip = ColorClip((1080, 1920), color=(30, 30, 30))
        return clip.set_duration(30)

    return VideoFileClip(os.path.join(BACKGROUND_DIR, files[0])).resize((1080, 1920))


def make_video(script_text, audio_path):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    audio = AudioFileClip(audio_path)
    bg = load_background().set_duration(audio.duration)

    # Captions
    captions = generate_caption_clips(script_text, audio.duration)

    # Final video
    final = CompositeVideoClip([bg] + captions).set_audio(audio)

    output_path = os.path.join(OUTPUT_DIR, "short_generated.mp4")
    final.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac")

    return output_path
