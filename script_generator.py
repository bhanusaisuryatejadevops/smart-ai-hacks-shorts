import os
import random
import logging
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
logger = logging.getLogger("script_generator")

DEFAULT_TOPICS = [
    "Insane new AI tool everyone is using",
    "Open-source AI update breaking the internet",
    "New AI website going viral today",
    "AI tool that replaces 10 apps at once",
    "This AI just changed everything",
    "Shocking AI upgrade released right now"
]

def pick_topic():
    return random.choice(DEFAULT_TOPICS)

def generate_script(topic=None):
    if topic is None:
        topic = pick_topic()
    logger.info(f"🎯 Selected topic: {topic}")
    prompt = f"""
You are a YouTube Shorts script writer.
Write a HIGH-ENERGY MrBeast-style script about this topic: "{topic}"
Rules:
- 20 to 28 seconds
- Fast, punchy, energetic lines
- Include on-screen captions
- Add scene directions like [Zoom in], [Flash text], etc.
- Must end with: "Follow for more AI updates!"
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=250
    )
    script = response.choices[0].message.content.strip()
    return script
