import os
import requests

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def fetch_trending_topics(industry):
    """
    Mock function to return trending topics based on industry.
    Ideally, integrate an API that fetches real trends.
    """
    return [
        f"Latest advancements in {industry} AI",
        f"The impact of {industry} technology on daily life",
        f"Future of {industry} innovation"
    ]

def generate_blog_content(topic):
    """
    Use Google Gemini API to generate blog content for a given topic.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GOOGLE_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": f"Write a detailed blog on: {topic}"}]}]}

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("contents", [{}])[0].get("parts", [{}])[0].get("text", "")
    return None
