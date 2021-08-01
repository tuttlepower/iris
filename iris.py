# Imports
import requests
import xml.etree.ElementTree as ET
import json
from datetime import datetime, timedelta
from Paper import Paper

url_list = {
    'FiveThirtyEight': 'https://feeds.megaphone.fm/ESP8794877317',
    # TODO: Fix NASA date Parse/ Abstract out Date Parsing
    # 'NASA': 'https://www.nasa.gov/rss/dyn/breaking_news.rss',
    'FRED': 'https://news.research.stlouisfed.org/feed/',
    'MIT News': 'https://news.mit.edu/rss/feed',
    'MIT Data': 'https://news.mit.edu/rss/topic/data-management-and-statistics',
    'EconTalk': 'https://feeds.simplecast.com/wgl4xEgL',
    'NPR': 'https://feeds.npr.org/1001/rss.xml'
}

# TODO: Fix Looping to improve speed, cut dataset size, no need to go through all of Econtalk
def getArticles(url):
    r = requests.get(url)
    root = ET.fromstring(r.text)
    articles = []
    root = root[0]
    old = False
    while not old:
        for item in root:
            title = ''
            link = ''
            description = ''
            date = ''
            for article in item:
                if(article.tag == 'title'):
                    title = article.text
                if (article.tag == 'link'):
                    link = article.text
                if (article.tag == 'description'):
                    description = article.text
                if (article.tag == 'pubDate'):
                    date = article.text
                    try:
                        date = datetime.strptime(
                            date, '%a, %d %b %Y %H:%M:%S %z').date()
                    except:
                        pass

            if(title != '' and link != '' and description != '' and date > datetime.now().date() - timedelta(days=7)):
                p = Paper(title, description, link, date)
                articles.append(p)
        return articles


def getPapersFromAllUrls():
    articles = []
    for key, value in url_list.items():
        print(value)
        articles.extend(getArticles(value))
    return articles


def getPapersFromTestUrls():
    articles = []
    short_list = {
        # 'FiveThirtyEight': 'https://feeds.megaphone.fm/ESP8794877317',
        'NASA': 'https://www.nasa.gov/rss/dyn/breaking_news.rss',
        # 'FRED': 'https://news.research.stlouisfed.org/feed/',
        # 'MIT News': 'https://news.mit.edu/rss/feed',
        # 'MIT Econ': 'https://news.mit.edu/rss/topic/economics',
        # 'MIT Data': 'https://news.mit.edu/rss/topic/data-management-and-statistics',
        # 'MIT Robotics': 'https://news.mit.edu/rss/topic/robotics',
        'EconTalk': 'https://feeds.simplecast.com/wgl4xEgL',
        'NPR': 'https://feeds.npr.org/1001/rss.xml',
        # 'Stanford News': 'https://www.sup.org/rss/?feed=economics'
    }
    for key, value in short_list.items():
        print(value)
        articles.extend(getArticles(value))
    return articles


def populate():
    articles = getPapersFromAllUrls()
    # articles = getPapersFromTestUrls()
    articles = sorted(articles, key=lambda x: x.date, reverse=True)
    return [article.__dict__ for article in articles]
