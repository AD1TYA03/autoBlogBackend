import os
import requests
from requests.auth import HTTPBasicAuth

WORDPRESS_URL = os.getenv("WORDPRESS_URL")  # Example: "https://yourblog.com/wp-json/wp/v2"
WORDPRESS_USERNAME = os.getenv("WORDPRESS_USERNAME")
WORDPRESS_APP_PASSWORD = os.getenv("WORDPRESS_APP_PASSWORD")

def publish_to_wordpress(title, content):
    """
    Publishes a blog post to WordPress using REST API.
    """
    url = f"{WORDPRESS_URL}/posts"  # Ensure /posts endpoint is correct
    auth = HTTPBasicAuth(WORDPRESS_USERNAME, WORDPRESS_APP_PASSWORD)
    
    headers = {"Content-Type": "application/json"}
    
    data = {
        "title": title,
        "content": content,
        "status": "publish"  # Change to "draft" if testing
    }

    try:
        print("\n📤 Sending request to WordPress...")  # Debugging log
        response = requests.post(url, json=data, headers=headers, auth=auth)

        print("\n🔍 WordPress API Response Status:", response.status_code)
        print("📥 Response JSON:", response.json())

        if response.status_code == 201:  # 201 = Created
            post_id = response.json().get("id")
            post_url = f"{WORDPRESS_URL}/?p={post_id}"
            print(f"✅ Published Successfully: {post_url}")
            return post_url

        else:
            print(f"❌ Failed to publish. Response: {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Error publishing to WordPress: {e}")
        return None
