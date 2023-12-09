import requests
import xml.etree.ElementTree as ET
import json

def rss_to_json(url):
    # Fetch the RSS feed
    response = requests.get(url, timeout=5)
    # Parse the RSS feed
    root = ET.fromstring(response.content)
    feed_data = []
    for item in root.findall('.//item'):
        feed_item = {}
        for child in item:
            feed_item[child.tag] = child.text
        feed_data.append(feed_item)
    # Convert to JSON
    return json.dumps(feed_data, indent=4)