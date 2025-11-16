# run_pipeline.py
import os
import logging
from trending import pick_trending_topic
from script_generator import generate_script
from voice_generator import text_to_speech
from background_generator import generate_background_sequence
from video_generator import make_video_from_assets
from youtube_upload import upload_video

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

def run_once():
    logging.info("Starting single pipeline run")
    topic = pick_trending_topic()
    logging.info(f"Selected topic: {topic}")
    script = generate_script(topic)
    logging.info(f"Generated script (len {len(script)}): {script[:120]}...")
    audio_path = text_to_speech(script, voice="nova-2")
    logging.info(f"Audio generated: {audio_path}")
    bg_paths = generate_background_sequence(topic, count=3)
    logging.info(f"Background images generated: {bg_paths}")
    output_path = make_video_from_assets(audio_path, bg_paths, script)
    logging.info(f"Final video: {output_path}")
    # Upload
    upload_result = upload_video(output_path, title=f"{topic} — AI Update", description=script)
    logging.info(f"Upload result: {upload_result}")
    return upload_result

if __name__ == "__main__":
    run_once()
