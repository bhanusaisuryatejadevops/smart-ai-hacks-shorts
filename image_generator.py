import os
import logging
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import random

logger = logging.getLogger(__name__)
BG_DIR = Path("assets/background")
BG_DIR.mkdir(parents=True, exist_ok=True)

def _gradient_image(size=(1080, 1080), a=(255, 80, 120), b=(80, 160, 240)):
    w, h = size
    img = Image.new("RGB", size)
    for y in range(h):
        t = y / (h - 1)
        r = int(a[0] * (1 - t) + b[0] * t)
        g = int(a[1] * (1 - t) + b[1] * t)
        bch = int(a[2] * (1 - t) + b[2] * t)
        for x in range(w):
            img.putpixel((x, y), (r, g, bch))
    return img

def _add_noise(img, intensity=30):
    px = img.load()
    w, h = img.size
    for _ in range(int(w * h * intensity / 1000)):
        x = random.randrange(w)
        y = random.randrange(h)
        px[x, y] = tuple(max(0, min(255, c + random.randint(-30, 30))) for c in px[x, y])
    return img

def generate_backgrounds(script_text=None, count=3):
    count = int(count)
    paths = []
    for i in range(1, count + 1):
        path = BG_DIR / f"bg_{i}.png"
        # random gradient colors
        a = (random.randint(40, 255), random.randint(40, 255), random.randint(40, 255))
        b = (random.randint(40, 255), random.randint(40, 255), random.randint(40, 255))
        img = _gradient_image(a=a, b=b)
        img = img.filter(ImageFilter.GaussianBlur(radius=random.uniform(2, 6)))
        img = _add_noise(img, intensity=20)
        draw = ImageDraw.Draw(img)
        cx = random.randint(200, 880)
        cy = random.randint(200, 880)
        r = random.randint(200, 450)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=None, fill=None)
        img.save(path, optimize=True)
        paths.append(str(path))
    logger.info("Generated %d backgrounds: %s", count, paths)
    return paths
