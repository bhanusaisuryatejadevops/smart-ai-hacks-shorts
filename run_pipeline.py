# run_pipeline.py
import logging
from script_generator import generate_script
from voice_generator import generate_voice
from image_generator import generate_backgrounds
from video_generator import make_video_from_assets
from youtube_upload import upload_video, is_youtube_ready

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

def run_once():
    logger.info("Starting single pipeline run")

    # 1) pick or generate topic + script
    topic = None  # None -> generator will use trending/defaults
    script = generate_script(topic)
    logger.info("Generated script (len %d): %s", len(script), script[:200].replace("\n"," ") + "...")

    # 2) get TTS audio (OpenAI TTS attempted; falls back to gTTS)
    try:
        audio_path = text_to_speech(script)
        logger.info("Audio generated: %s", audio_path)
    except Exception as e:
        logger.exception("TTS failed completely: %s", e)
        return

    # 3) generate backgrounds automatically (returns list of image paths)
    bg_paths = generate_backgrounds(count=3)
    logger.info("Background images generated: %s", bg_paths)

    # 4) make video via ffmpeg
    try:
        output_path = make_video_from_assets(audio_path, bg_paths, script_text=script)
        logger.info("Final video: %s", output_path)
    except Exception as e:
        logger.exception("Video generation failed: %s", e)
        return

    # 5) upload to YouTube if configured; otherwise log and continue
    try:
        if is_youtube_ready():
            result = upload_video(output_path, title=f"{topic or 'AI Update'} — Smart AI Hacks", description=script)
            logger.info("Upload result: %s", result)
        else:
            logger.warning("YouTube not configured or API not enabled; skipping upload.")
    except Exception as e:
        logger.exception("Upload failed (skipping): %s", e)

if __name__ == "__main__":
    run_once()
