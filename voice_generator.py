# voice_generator.py
import os
import openai
import base64
import logging
from pathlib import Path
openai.api_key = os.getenv("OPENAI_API_KEY")
logger = logging.getLogger(__name__)

OUT_DIR = Path("assets/audio")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def text_to_speech(text: str, voice: str = "nova-2") -> str:
    """
    Uses OpenAI TTS endpoint. Saves MP3 to assets/audio/
    Returns path to audio file.
    """
    filename = OUT_DIR / f"voice_{abs(hash(text)) % (10**9)}.mp3"
    # Use the OpenAI TTS-ish interface. If your OpenAI SDK version differs, adjust accordingly.
    try:
        # Modern OpenAI python library for TTS may vary; we'll attempt a generic request
        resp = openai.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice=voice,
            input=text
        )
        # resp is a bytes-like object in some libs, or has attribute .content
        audio_bytes = resp if isinstance(resp, (bytes, bytearray)) else resp.read()
        with open(filename, "wb") as f:
            if isinstance(audio_bytes, (bytes, bytearray)):
                f.write(audio_bytes)
            else:
                # if resp is a streaming object
                f.write(audio_bytes)
        return str(filename)
    except Exception as e:
        logger.exception("OpenAI TTS failed: %s", e)
        # fallback to gTTS if OpenAI TTS not available
        try:
            from gtts import gTTS
            tts = gTTS(text=text, lang="en")
            tts.save(str(filename))
            return str(filename)
        except Exception as e2:
            logger.exception("gTTS fallback failed: %s", e2)
            raise
