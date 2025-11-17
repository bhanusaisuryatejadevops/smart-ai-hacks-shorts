import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_script():
    prompt = """
Write a 30-second YouTube Shorts script about a trending AI tool or AI update released this week.
Make it short, energetic and end with: “Follow for more AI updates!”
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()
