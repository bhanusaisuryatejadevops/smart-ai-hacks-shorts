# script_generator.py
import os
import openai
import logging
openai.api_key = os.getenv("OPENAI_API_KEY")
logger = logging.getLogger(__name__)

PROMPT_TEMPLATE = """Write a short energetic 30-45 second YouTube Shorts script about the following trending AI topic. Make it hooky in the first 1-2 seconds, add 2 quick benefit lines, and end with a strong CTA: "Follow Smart AI Hacks!" Keep lines short and punchy.

Topic:
{topic}

Script:
"""

def generate_script(topic: str) -> str:
    prompt = PROMPT_TEMPLATE.format(topic=topic)
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content": prompt}],
            max_tokens=220,
            temperature=0.7
        )
        text = resp["choices"][0]["message"]["content"].strip()
        return text
    except Exception as e:
        logger.exception("OpenAI script generation failed, falling back to simple template")
        # fallback simple template
        lines = [
            f"{topic} — you need to see this!",
            "It can save time and boost your results.",
            "It's easy to use and completely changing how people work with AI.",
            "Follow Smart AI Hacks!"
        ]
        return "\n".join(lines)
