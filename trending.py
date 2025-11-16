# trending.py
import requests
import random
import logging

logger = logging.getLogger(__name__)

# A lightweight composite approach:
# 1) Try CurrentsAPI (demo key in examples) or Newsdata (demo)
# 2) If fails, check Reddit r/artificial or r/MachineLearning RSS
# 3) If still fails, pick from fallback list of AI topics

def currents_latest_demo():
    try:
        url = "https://api.currentsapi.services/v1/latest-news?category=technology&apiKey=demo"
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            data = r.json()
            if "news" in data and len(data["news"])>0:
                choice = random.choice(data["news"])
                return choice.get("title") or choice.get("description") or choice.get("summary")
    except Exception as e:
        logger.debug("Currents failed: %s", e)
    return None

def reddit_fallback():
    try:
        r = requests.get("https://www.reddit.com/r/artificial/top/.rss?t=day", headers={"User-Agent":"YouTubeAutoBot/1.0"}, timeout=15)
        if r.status_code == 200:
            txt = r.text
            # quick-and-dirty extract first <title> after <entry>
            import re
            m = re.search(r"<entry>.*?<title>(.*?)</title>", txt, re.S)
            if m:
                title = m.group(1)
                return title
    except Exception as e:
        logger.debug("Reddit failed: %s", e)
    return None

FALLBACK_TOPICS = [
    "OpenAI releases a major update that speeds up code generation",
    "A new text-to-image AI produces photorealistic faces",
    "New free AI tool that makes YouTube thumbnails in seconds",
    "AI assistant that writes emails in 10× faster",
    "Groundbreaking open-source LLM that runs on your laptop",
]

def pick_trending_topic():
    topic = currents_latest_demo()
    if topic:
        return topic
    topic = reddit_fallback()
    if topic:
        return topic
    # random fallback
    return random.choice(FALLBACK_TOPICS)
