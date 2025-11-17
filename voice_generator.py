# voice_generator.py
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
OUT_DIR = Path("assets/audio")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Try OpenAI client presence
try:
    import openai
    openai.api_key = os.getenv("OPENAI_API_KEY")
    OPENAI_AVAILABLE = True
except Exception:
    OPENAI_AVAILABLE = False

def text_to_speech(text: str, voice: str = "alloy") -> str:
    """
    Try OpenAI TTS first (if available), fall back to gTTS.
    Returns path to mp3 file.
    """
    filename = OUT_DIR / f"voice_{abs(hash(text)) % (10**9)}.mp3"

    # Try OpenAI TTS (best-effort; may hit quota)
    if OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
        try:
            logger.info("Trying OpenAI TTS...")
            resp = openai.audio.speech.create(
                model="gpt-4o-mini-tts",
                voice=voice,
                input=text
            )
            # resp may be bytes-like or streaming; handle both
            audio_bytes = resp if isinstance(resp, (bytes, bytearray)) else getattr(resp, "read", lambda: None)()
            if audio_bytes is None:
                # some libs return a response object with content attribute
                audio_bytes = getattr(resp, "content", b"")
            with open(filename, "wb") as f:
                f.write(audio_bytes)
            logger.info("OpenAI TTS saved: %s", filename)
            return str(filename)
        except Exception as e:
            logger.warning("OpenAI TTS failed: %s — falling back to gTTS", e)

    # Fallback to gTTS
    try:
        logger.info("Using gTTS fallback...")
        from gtts import gTTS
        tts = gTTS(text=text, lang="en")
        tts.save(str(filename))
        logger.info("gTTS saved: %s", filename)
        return str(filename)
    except Exception as e:
        logger.exception("gTTS fallback failed: %s", e)
        raise
