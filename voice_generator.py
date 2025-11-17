# voice_generator.py
import requests
import os

def generate_voice(text, output_path="assets/audio/output.mp3"):
    """
    Generate speech using OpenAI TTS and save to output_path.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")

    url = "https://api.openai.com/v1/audio/speech"
    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    data = {
        "model": "gpt-4o-mini-tts",
        "voice": "alloy",
        "input": text
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code != 200:
        raise RuntimeError(f"TTS Error: {response.text}")

    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path
