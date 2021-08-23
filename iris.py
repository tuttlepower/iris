# Imports
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

import requests

from Paper import Paper

url_list = {
    'FiveThirtyEight': 'https://feeds.megaphone.fm/ESP8794877317',
    # TODO: Fix NASA date Parse/ Abstract out Date Parsing
    # 'NASA': 'https://www.nasa.gov/rss/dyn/breaking_news.rss',
    'FRED': 'https://news.research.stlouisfed.org/feed/',
    'MIT News': 'https://news.mit.edu/rss/feed',
    'MIT Data': 'https://news.mit.edu/rss/topic/data-management-and-statistics',
    'EconTalk': 'https://feeds.simplecast.com/wgl4xEgL',
    'NPR': 'https://feeds.npr.org/1001/rss.xml',
    # 'NBER':'https://back.nber.org/rss/new.xml',
    'BEA': 'https://apps.bea.gov/rss/rss.xml',
    'Arxiv_econ': 'http://export.arxiv.org/rss/econ',
    'JMLR': "https://jmlr.org/jmlr.xml",
}
icon_list = {
    url_list['FiveThirtyEight']: 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/FiveThirtyEight_Logo.svg/1280px-FiveThirtyEight_Logo.svg.png',
    url_list['FRED']: 'https://research.stlouisfed.org/images/frb-logo-bw.png',
    url_list['MIT News']: 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/MIT_logo.svg/1280px-MIT_logo.svg.png',
    url_list['MIT Data']: 'https://dsl.mit.edu/sites/default/files/Final%20Zoomed.png',
    url_list['EconTalk']: 'http://files.libertyfund.org/econtalk/EconTalkCDcover1400y2007.jpg',
    url_list['NPR']: 'https://media.npr.org/chrome_svg/npr-logo.svg',
    # url_list['NBER']:'https://cdn.corporatefinanceinstitute.com/assets/national-bureau-of-economic-research-nber1.jpg',
    url_list['BEA']: 'https://www.commerce.gov/sites/default/files/styles/full_width_image_700x400max/public/media/images/branding/bea-logo-dark-background-citing.png?itok=C_RcEoKT',
    url_list['Arxiv_econ']: 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/ArXiv_web.svg/1200px-ArXiv_web.svg.png',
    url_list['JMLR']: 'https://jmlr.org/img/jmlr.jpg',
}
# TODO: Fix Looping to improve speed, cut dataset size, no need to go through all of Econtalk
# Limit the data BEFORE looping through, don't loop and cut, cut it off before looping


def getArticles(url):
    r = requests.get(url)
    root = ET.fromstring(r.text)
    articles = []
    root = root[0]
    old = False
    while not old and articles.__len__() < 10:
        for item in root:
            title = ''
            link = ''
            description = ''
            date = datetime.now().date()
            for article in item:
                if(article.tag == 'title'):
                    title = article.text
                if (article.tag == 'link'):
                    link = article.text
                if (article.tag == 'description'):
                    description = article.text
                if (article.tag == 'pubDate'):
                    temp_date = article.text
                    try:
                        date = datetime.strptime(
                            temp_date, '%a, %d %b %Y %H:%M:%S %z').date()
                    except:
                        date = datetime.now().date()

            if(title != '' and link != '' and description != '' and date > datetime.now().date() - timedelta(days=7)):
                p = Paper(title, description, link, date, logo=icon_list[url])
                articles.append(p)
        return articles[1:10]


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

# def prep(db):
#     list = db.query().all()
#     print(list)
