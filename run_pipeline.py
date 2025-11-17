import logging
from trending import get_trending_ai_script  # Make sure trending.py is imported
from voice_generator import generate_voice
from image_generator import generate_backgrounds
from video_generator import make_video_from_assets
from youtube_upload import upload_video, is_youtube_ready

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

def run_once():
    logger.info("🚀 Starting single pipeline run")
    topic = get_trending_ai_script()  # fetch a trending AI topic
    logger.info(f"🎯 Chosen topic: {topic}")
    # Use the topic as both script for speech and on-video text
    script = topic
    image_paths = generate_backgrounds(topic, count=5)  # 5 images for variety (adjust count as needed)
    captions = [topic] * len(image_paths)  # repeat topic on each image
    logger.info(f"🖼️ Generated backgrounds: {image_paths}")
    audio_path = generate_voice(script)
    logger.info(f"🎤 Audio created: {audio_path}")
    final_video_path = make_video_from_assets(image_paths, audio_path, captions)
    logger.info(f"🎬 Final video created: {final_video_path}")
    if is_youtube_ready():
        upload_video(final_video_path, topic)
        logger.info("📤 Uploaded video to YouTube")
    else:
        logger.warning("⚠️ Skipped upload — YouTube not configured correctly.")
    logger.info("✅ Pipeline finished successfully!")

if __name__ == "__main__":
    run_once()
