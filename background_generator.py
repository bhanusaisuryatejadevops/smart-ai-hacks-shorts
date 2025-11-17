import os
import openai
import logging
from pathlib import Path
from PIL import Image
from io import BytesIO
import random

openai.api_key = os.getenv("OPENAI_API_KEY")
logger = logging.getLogger(__name__)
OUT_DIR = Path("assets/background")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def generate_image(prompt: str, idx: int) -> str:
    filename = OUT_DIR / f"bg_{idx}.png"
    try:
        resp = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        b64 = resp["data"][0]["b64_json"]
        img_bytes = BytesIO(base64.b64decode(b64))
        img = Image.open(img_bytes).convert("RGB")
        img = img.resize((1080,1080))
        img.save(filename, format="PNG")
        return str(filename)
    except Exception as e:
        logger.debug("Image API failed, using gradient fallback: %s", e)
        from PIL import ImageDraw
        im = Image.new("RGB", (1080,1080), "#0b0f1a")
        draw = ImageDraw.Draw(im)
        for i in range(6):
            x = random.randint(0,1080)
            y = random.randint(0,1080)
            r = random.randint(80,300)
            draw.ellipse((x-r, y-r, x+r, y+r), outline=(random.randint(80,200), random.randint(60,220), random.randint(100,255)))
        im.save(filename)
        return str(filename)

def generate_background_sequence(topic: str, count: int = 3):
    base_prompt = f"futuristic AI neon city, abstract digital pattern, cinematic 9:16 vibe, high detail, trending on artstation - inspired by: {topic}"
    paths = []
    for i in range(count):
        p = generate_image(base_prompt + f" variation {i+1}", i+1)
        paths.append(p)
    return paths
