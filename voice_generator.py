import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_voice(text, output_audio_path):
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text,
        format="mp3"
    )
    with open(output_audio_path, "wb") as f:
        f.write(response.read())
