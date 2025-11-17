# script_generator.py
import os
import logging
import random

logger = logging.getLogger(__name__)

# Use OpenAI if key present, otherwise fallback to simple templates
try:
    import openai
    OPENAI_AVAILABLE = True
    openai.api_key = os.getenv("OPENAI_API_KEY")
except Exception:
    OPENAI_AVAILABLE = False

PROMPT_TEMPLATE = """Write a short energetic 30-45 second YouTube Shorts script about the following trending AI topic.
Make it hooky in the first 1-2 seconds, add 2 quick benefits, and end with a strong CTA: "Follow for more AI updates!"
Keep lines short and punchy.

Topic:
{topic}

Script:
"""

DEFAULT_TOPICS = [
    "An AI tool that instantly turns text prompts into videos",
    "A tiny new model that runs locally and still rocks",
    "An update that makes image-to-text unbelievably accurate",
    "A productivity AI that automates boring dev tasks",
    "A surprising new open-source AI release"
]

def generate_script(topic: str = None) -> str:
    if topic is None:
        topic = random.choice(DEFAULT_TOPICS)

    prompt = PROMPT_TEMPLATE.format(topic=topic)

    if OPENAI_AVAILABLE and openai.api_key:
        try:
            # new OpenAI python lib usage
            resp = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=220,
                temperature=0.7
            )
            text = resp.choices[0].message.content.strip()
            return text
        except Exception as e:
            logger.warning("OpenAI script generation failed: %s — falling back to template", e)

    # fallback template
    lines = [
        f"{topic} — you need to see this!",
        "It can save time and boost your results.",
        "Super simple to use — you'll love it.",
        "Follow for more AI updates!"
    ]
    return "\n".join(lines)
