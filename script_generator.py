import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_dynamic_topic():
    prompt = """
    Give me one viral, trending YouTube Shorts topic related to:
    - new AI tools
    - AI updates this week
    - trending tech news
    - powerful AI websites
    Make it short, clickable, and hype.
    Return ONLY the topic text.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message["content"].strip()

def generate_script():
    topic = get_dynamic_topic()

    script_prompt = f"""
    Create a 30-second, high-energy YouTube Shorts script in MrBeast style
    based on this topic: "{topic}"

    Requirements:
    - very high energy
    - 3-color caption style (white, yellow, red)
    - fast-paced storytelling
    - hook in first 3 seconds
    - last line must be: "Follow for more AI updates!"
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": script_prompt}]
    )

    return response.choices[0].message["content"], topic
