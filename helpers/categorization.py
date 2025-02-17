import re

def extract_tags(content):
    """
    Simple function to extract keywords as tags.
    """
    words = re.findall(r'\b\w+\b', content.lower())
    common_words = {"the", "is", "and", "to", "of", "a", "in", "for", "on", "with", "as"}
    tags = list(set(words) - common_words)
    
    return tags[:5]  # Return top 5 unique words as tags
