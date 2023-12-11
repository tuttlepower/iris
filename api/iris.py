import requests
import xml.etree.ElementTree as ET
import json

import requests
import xml.etree.ElementTree as ET
import json

def get_content(url):
      # Fetch feed
      response = requests.get(url, timeout=5)
      root = ET.fromstring(response.content)
      # do rss first
      data = rss_to_json(root)
      # then try xml
      if not data: 
        data = xml_to_json(root)
     
      return data

def rss_to_json(root):    
    feed_data = []
    for item in root.findall('.//item'):
        feed_item = {}
        for child in item:
            feed_item[child.tag] = child.text
        feed_data.append(feed_item)
    return feed_data

def xml_to_json(root):
    ns = {'default': 'http://purl.org/rss/1.0/'}
    items = []
    for item in root.findall('default:item', ns):
        item_data = {
            'title': item.find('default:title', ns).text,
            'link': item.find('default:link', ns).text,
            'description': item.find('default:description', ns).text,
            'pubDate': item.find('default:pubDate', ns).text if item.find('default:pubDate', ns) is not None else None
        }
        items.append(item_data)
    return items

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