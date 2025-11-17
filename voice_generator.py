import os
import logging
from gtts import gTTS
from openai import OpenAI

client = OpenAI()

AUDIO_DIR = "assets/audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("voice_generator")


def generate_voice(script_text):
    """Generate voice using OpenAI → fallback to gTTS."""
    output_path = os.path.join(AUDIO_DIR, f"voice_{os.getpid()}.mp3")

    # --- Try OpenAI first ---
    try:
        logger.info("Trying OpenAI TTS...")
        response = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=script_text,
            format="mp3"
        )
        with open(output_path, "wb") as f:
            f.write(response.read())
        logger.info(f"OpenAI TTS success: {output_path}")
        return output_path

    except Exception as e:
        logger.warning(f"OpenAI TTS failed, using gTTS fallback → {e}")

    # --- Fallback to gTTS ---
    try:
        tts = gTTS(script_text, lang="en")
        tts.save(output_path)
        logger.info(f"gTTS fallback success: {output_path}")
        return output_path

    except Exception as e:
        logger.error(f"gTTS also failed → {e}")
        raise RuntimeError("Voice generation failed using both OpenAI and gTTS.")
