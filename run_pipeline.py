import logging
from script_generator import generate_script
from voice_generator import generate_voice
from image_generator import generate_backgrounds
from video_generator import make_video_from_assets
from youtube_upload import upload_video, is_youtube_ready

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

def split_script(script):
    # Split script into non-empty lines/sentences
    return [line.strip() for line in script.split("\n") if line.strip() and not line.strip().startswith("[")]

def run_once():
    logger.info("🚀 Starting single pipeline run")
    script = generate_script()  # FULL MrBeast-style script about a trending/random AI topic
    logger.info(f"📝 Script generated: {script[:200]}...")
    segments = split_script(script)
    logger.info(f"Script segments: {segments}")
    backgrounds = generate_backgrounds(script, count=len(segments))  # different bg per script segment
    voice_audio = generate_voice(script)  # entire script gets spoken as narration
    logger.info(f"🎤 Audio created: {voice_audio}")
    final_video = make_video_from_assets(backgrounds, voice_audio, captions=segments)
    logger.info(f"🎬 Final video created: {final_video}")
    if is_youtube_ready():
        upload_video(final_video, segments[0] + " | AI Shorts")  # use first line as title
        logger.info("📤 Uploaded video to YouTube")
    else:
        logger.warning("⚠️ Skipped upload — YouTube not configured correctly.")
    logger.info("✅ Pipeline finished successfully!")

if __name__ == "__main__":
    run_once()
