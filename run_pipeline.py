import os
import random
import logging
from script_generator import generate_script
from voice_generator import generate_voice
from video_generator import make_video_from_assets

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCRIPT_TOPICS = [
    "I did not think it would be this good. Holy shit. I am blown away",
    "AI just changed everything again",
    "This new AI tool is crazy",
    "OpenAI just dropped a bomb update",
    "This AI website will save you hours",
]

BACKGROUND_DIR = "assets/background"
AUDIO_DIR = "assets/audio"
OUTPUT_DIR = "assets/output"

os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


def select_backgrounds():
    """Pick random 3 background images"""
    files = [f for f in os.listdir(BACKGROUND_DIR) if f.endswith((".png", ".jpg", ".jpeg"))]
    if not files:
        raise Exception("No images found in assets/background")

    selected = random.sample(files, min(3, len(files)))
    full_paths = [os.path.join(BACKGROUND_DIR, f) for f in selected]

    logger.info(f"Background images selected: {full_paths}")
    return full_paths


def run_pipeline():
    logger.info("Starting single pipeline run")

    topic = random.choice(SCRIPT_TOPICS)
    logger.info(f"Selected topic: {topic}")

    script = generate_script(topic)

    audio_path = generate_voice(script)

    bg_images = select_backgrounds()
