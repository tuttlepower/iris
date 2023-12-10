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
    return feed_data

def get_image_from_feed():
    feed_url = 'https://www.nasa.gov/feeds/iotd-feed/'
    response = requests.get(feed_url)
    content = response.content
    root = ET.fromstring(content)
    first_item = root.find('channel/item')
    if first_item is not None:
        link = first_item.find('link').text
        return link
    else:
        return 'https://apod.nasa.gov/apod/image/2206/NGC6744_chakrabarti1024R.jpg'