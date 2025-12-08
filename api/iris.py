import requests
import xml.etree.ElementTree as ET
import json

def get_content(url):
    payload = {"source": url, "items": [], "error": None}

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.RequestException as exc:
        payload["error"] = str(exc)
        return payload

    try:
        root = ET.fromstring(response.content)
    except ET.ParseError as exc:
        payload["error"] = f"XML parse error: {exc}"
        return payload

    items = rss_to_json(root)
    if not items:
        items = xml_to_json(root)

    payload["items"] = items
    return payload


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
        title_elem = item.find('default:title', ns)
        link_elem = item.find('default:link', ns)
        description_elem = item.find('default:description', ns)
        pub_date_elem = item.find('default:pubDate', ns)

        item_data = {
            'title': title_elem.text if title_elem is not None else None,
            'link': link_elem.text if link_elem is not None else None,
            'description': description_elem.text if description_elem is not None else None,
            'pubDate': pub_date_elem.text if pub_date_elem is not None else None
        }
        items.append(item_data)
    return items
