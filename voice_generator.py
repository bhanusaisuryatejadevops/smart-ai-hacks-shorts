# voice_generator.py
import os
import logging
from pathlib import Path
import importlib.util
import subprocess

import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

logger = logging.getLogger(__name__)
OUT_DIR = Path("assets/audio")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Auto-install gTTS if missing
if importlib.util.find_spec("gtts") is None:
    subprocess.check_call([os.sys.executable, "-m", "pip", "install", "gtts"])
from gtts import gTTS

def text_to_speech(text: str, voice: str = "alloy") -> str:
    """
    Generate MP3 audio using OpenAI TTS (or fallback to gTTS if quota exceeded)
    Returns path to audio file.
    """
    filename = OUT_DIR / f"voice_{abs(hash(text)) % (10**9)}.mp3"

    # Try OpenAI TTS
    try:
        resp = openai.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice=voice,
            input=text
        )
        # write bytes to file
        with open(filename, "wb") as f:
            f.write(resp.read() if hasattr(resp, "read") else resp)
        return str(filename)
    except Exception as e:
        logger.warning("OpenAI TTS failed (%s), falling back to gTTS.", e)

    # gTTS fallback
    try:
        tts = gTTS(text=text, lang="en")
        tts.save(str(filename))
        return str(filename)
    except Exception as e2:
        logger.error("gTTS fallback failed: %s", e2)
        raise
