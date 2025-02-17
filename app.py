import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from helpers.excel_utils import save_to_excel
from helpers.wordpress_utils import publish_to_wordpress

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend requests

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
WORDPRESS_URL = os.getenv("WORDPRESS_URL")
WORDPRESS_USERNAME = os.getenv("WORDPRESS_USERNAME")
WORDPRESS_APP_PASSWORD = os.getenv("WORDPRESS_APP_PASSWORD")

def fetch_trending_topics(industry):
    """
    Fetch trending topics using Google Gemini AI.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}

    prompt = f"Provide three trending topics in the {industry} industry. Return them as a comma-separated list."

    data = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code != 200:
            return None
        
        json_data = response.json()
        topics_text = json_data.get("candidates", [])[0].get("content", {}).get("parts", [])[0].get("text", "")

        if topics_text:
            topics_list = [t.strip() for t in topics_text.split(",") if t.strip()]
            
            if topics_list:
                save_to_excel(topics_list)  # Save topics to Excel
                return topics_list
        return None

    except Exception as e:
        print("❌ Error fetching topics from AI:", str(e))
        return None

def generate_blog(topic):
    """
    Generates a blog post using Google Gemini AI.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}

    prompt = f"""
    Write a blog post about '{topic}' with this structure:
    
    ## Table of Contents
    1. Introduction
    2. Main Content
    3. Conclusion
    4. Relevant Tags & Categories

    Ensure it is well-structured and informative.
    """

    data = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code != 200:
            return None
        
        json_data = response.json()
        blog_content = json_data.get("candidates", [])[0].get("content", {}).get("parts", [])[0].get("text", "")

        if blog_content:
            return blog_content
        return None

    except Exception as e:
        print("❌ Error generating blog:", str(e))
        return None

@app.route('/generate-blog', methods=['POST'])
def generate_blog_endpoint():
    """
    API endpoint to generate a blog based on industry trends.
    """
    data = request.json
    industry = data.get("industry")

    if not industry:
        return jsonify({"error": "Industry is required"}), 400

    print(f"\n🚀 Fetching trending topics for: {industry}")
    topics = fetch_trending_topics(industry)

    if not topics:
        return jsonify({"error": "No trending topics found"}), 400

    topic = topics[0]
    print(f"\n📝 Generating blog for topic: {topic}")
    blog_content = generate_blog(topic)

    if not blog_content:
        return jsonify({"error": "Failed to generate blog content"}), 500

    post_url = publish_to_wordpress(topic, blog_content)

    return jsonify({
        "message": "Blog generated and published successfully!",
        "topic": topic,
        "blog_content": blog_content,
        "wordpress_url": post_url
    })

if __name__ == '__main__':
    app.run(debug=True)
