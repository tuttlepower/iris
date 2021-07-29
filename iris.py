# Imports
import csv
import requests
import xml.etree.ElementTree as ET
import json
from datetime import datetime, timedelta
import Paper
# Paper Object


class Paper:
    def __init__(self, title, description, link, date):
        self.title = title
        self.description = description
        self.link = link
        self.date = date

    def __dict__(self):
        return {
            'Title': self.title,
            'Description': self.description,
            'Link': self.link,
            'Date': self.date}


url_list = {
    'FiveThirtyEight': 'https://feeds.megaphone.fm/ESP8794877317',
    'NASA': 'https://www.nasa.gov/rss/dyn/breaking_news.rss',
    'FRED': 'https://news.research.stlouisfed.org/feed/',
    # 'MIT News': 'https://news.mit.edu/rss/feed',
    # 'MIT Econ': 'https://news.mit.edu/rss/topic/economics',
    # 'MIT Data': 'https://news.mit.edu/rss/topic/data-management-and-statistics',
    # 'MIT Robotics': 'https://news.mit.edu/rss/topic/robotics',
    # 'EconTalk': 'https://feeds.simplecast.com/wgl4xEgL',
    # 'NPR': 'https://feeds.npr.org/1001/rss.xml',
    # 'Stanford News': 'https://www.sup.org/rss/?feed=economics'
}


def getPaper(item):
    title = ""
    link = ""
    description = ""
    date = ""
    for article in item:
        if(article.tag == 'title'):
            title = article.text

        if (article.tag == 'link'):
            link = article.text

        if (article.tag == 'pubDate'):
            date = article.text
            try:
                date = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %z').date()
            except:
                date = datetime.now().date()

        if (article.tag == 'description'):
            description = article.text

    if(title != "" and link != "" and description != "" and date != "" and date > datetime.now().date()-timedelta(days=7)):
        return Paper(title, description, link, date)
    else:
       return None


def getPapersFromUrl(url):
    r = requests.get(url)
    root = ET.fromstring(r.text)
    articles = []
    root = root[0]
    for item in root:
        articles.append(getPaper(item))
    return articles


def getPapersFromAllUrls():
    articles = []
    for key, value in url_list.items():
        print(value)
        articles.append(getPapersFromUrl(value))
    return articles


def populate():
    articles = getPapersFromAllUrls()
    articles = [article for article in articles if article is not None]
    articles.sort(key=lambda x: x.date, reverse=True)
    articles = [article.__dict__() for article in articles]
    articles = list(dict.fromkeys(articles.title))
    return articles
print('Fin')
