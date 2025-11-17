import logging
from script_generator import generate_script
from voice_generator import generate_voice
from image_generator import generate_backgrounds
from video_generator import make_video_from_assets
from youtube_upload import upload_video, is_youtube_ready

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

def run_once():
    logger.info("🚀 Starting single pipeline run")

    # 1) Generate script (topic = None → auto trending)
    topic = None
    script = generate_script(topic)
    logger.info(f"📝 Script generated: {script[:200]}...")

    # 2) Generate TTS audio  
    audio_path = generate_voice(script)
    logger.info(f"🎤 Audio created: {audio_path}")

    # 3) Generate backgrounds (AI images)
    image_paths = generate_backgrounds(script)
    logger.info(f"🖼️ Generated backgrounds: {image_paths}")

    # 4) Make video (AI images + audio)
    final_video_path = make_video_from_assets(image_paths, audio_path)
    logger.info(f"🎬 Final video created: {final_video_path}")

    # 5) Upload to YouTube
    if is_youtube_ready():
        upload_video(final_video_path, script)
        logger.info("📤 Uploaded video to YouTube")
    else:
        logger.warning("⚠️ Skipped upload — YouTube not configured correctly.")

    logger.info("✅ Pipeline finished successfully!")

if __name__ == "__main__":
    run_once()
