# run_pipeline.py
import logging
from script_generator import generate_script
from voice_generator import text_to_speech
from video_generator import make_video_from_assets
from youtube_upload import upload_video, get_youtube_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_once():
    topic = "I did not think it would be this good. Holy shit. I am blown away"
    logger.info("Starting single pipeline run")
    logger.info("Selected topic: %s", topic)

    # 1️⃣ Generate script
    script = generate_script(topic)
    logger.info("Generated script (len %d): %s", len(script), script[:100] + "...")

    # 2️⃣ Generate audio
    try:
        audio_path = text_to_speech(script, voice="en-US-Wavenet-F")
        logger.info("Audio generated: %s", audio_path)
    except Exception as e:
        logger.error("Failed to generate audio: %s", e)
        return

    # 3️⃣ Generate background images (replace with your actual generator or static assets)
    bg_paths = [
        "assets/background/bg_1.png",
        "assets/background/bg_2.png",
        "assets/background/bg_3.png"
    ]
    logger.info("Background images selected: %s", bg_paths)

    # 4️⃣ Generate video
    try:
        output_path = make_video_from_assets(audio_path, script)
        logger.info("Final video: %s", output_path)
    except Exception as e:
        logger.error("Failed to generate video: %s", e)
        return

    # 5️⃣ Upload to YouTube (graceful fallback if API fails)
    try:
        # check if YouTube client is initialized
        yt_client = get_youtube_client()
        if yt_client:
            upload_result = upload_video(
                output_path,
                title=f"{topic} — AI Update",
                description=script,
                privacy="private"
            )
            logger.info("Upload result: %s", upload_result)
        else:
            logger.warning("YouTube client not initialized, skipping upload.")
    except Exception as e:
        logger.warning("Skipping YouTube upload due to error: %s", e)


if __name__ == "__main__":
    run_once()
