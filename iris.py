# Imports
import csv
import requests
import xml.etree.ElementTree as ET
import json
from datetime import datetime, timedelta
from Paper import Paper

url_list = {
    'FiveThirtyEight': 'https://feeds.megaphone.fm/ESP8794877317',
    'NASA': 'https://www.nasa.gov/rss/dyn/breaking_news.rss',
    'FRED': 'https://news.research.stlouisfed.org/feed/',
    'MIT News': 'https://news.mit.edu/rss/feed',
    'MIT Econ': 'https://news.mit.edu/rss/topic/economics',
    'MIT Data': 'https://news.mit.edu/rss/topic/data-management-and-statistics',
    # 'MIT Robotics': 'https://news.mit.edu/rss/topic/robotics',
    'EconTalk': 'https://feeds.simplecast.com/wgl4xEgL',
    'NPR': 'https://feeds.npr.org/1001/rss.xml',
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
            date = datetime.now().date()
            # try:
            #     date = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %z').date()
            # except:
            #     date = datetime.now().date()

        if (article.tag == 'description'):
            description = article.text

    if(title != "" and link != "" and description != "" and date != ""):
        return Paper.Paper(title, description, link, date)
    else:
        return None


def getArticles(url):
    r = requests.get(url)
    root = ET.fromstring(r.text)
    articles = []
    root = root[0]
    for item in root:
        title = ''
        link = ''
        description = ''
        date = ''
        for article in item:
            if(article.tag == 'title'):
                title = article.text
                print(title)
            if (article.tag == 'link'):
                link = article.text
                print(link)

            if (article.tag == 'description'):
                description = article.text
                print(description)
            if (article.tag == 'pubDate'):
                date = article.text
                # date = datetime.now().date()
                # datetime.now().date().strftime("%Y")
                print(date)
                
            
        if(title != '' and link != '' and description != ''):
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
    # articles = getPapersFromAllUrls()
    articles = getPapersFromTestUrls()
    # return json.dumps(articles, default=lambda o: o.__dict__, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
    return [article.__dict__ for article in articles]

# articles = populate()


# print(articles)
# for article in articles:
#     print(article.title)
#     print(article.description)
#     print(article.link)
#     print("")
