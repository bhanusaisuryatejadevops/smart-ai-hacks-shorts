# voice_generator.py
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
OUT_DIR = Path("assets/audio")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def text_to_speech(text: str, voice: str = "alloy") -> str:
    """
    Generate TTS audio. Try OpenAI TTS first; fallback to gTTS if it fails.
    Returns path to MP3 file.
    """
    filename = OUT_DIR / f"voice_{abs(hash(text)) % (10**9)}.mp3"

    # Try OpenAI TTS
    try:
        import openai
        openai.api_key = os.getenv("OPENAI_API_KEY")
        logger.info("Trying OpenAI TTS...")
        resp = openai.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice=voice,
            input=text
        )
        # resp might have .read() or bytes
        audio_bytes = resp if isinstance(resp, (bytes, bytearray)) else resp.read()
        with open(filename, "wb") as f:
            f.write(audio_bytes)
        logger.info(f"OpenAI TTS successful: {filename}")
        return str(filename)

    except Exception as e:
        logger.warning(f"OpenAI TTS failed: {e}, falling back to gTTS...")

    # Fallback: gTTS
    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang="en")
        tts.save(str(filename))
        logger.info(f"gTTS fallback successful: {filename}")
        return str(filename)
    except Exception as e2:
        logger.error(f"gTTS fallback failed: {e2}")
        raise RuntimeError("Both OpenAI TTS and gTTS failed.") from e2
