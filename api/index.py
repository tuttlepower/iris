from flask import Flask, redirect,render_template,session, url_for, request,jsonify,send_from_directory
from flask import jsonify
import datetime
import requests
from supabase import create_client, Client
import os
from . import iris
from flask_cors import CORS

app = Flask(__name__)
CORS(app) #, resources={r"/*": {"origins": "https://tuttlepower.github.io"}})
# Supabase setup
url = "https://bnmeoegpseguowtfulja.supabase.co"
key = os.environ.get('SUPABASE_KEY')
supabase: Client = create_client(url, key)

@app.route('/api/getData', methods=['GET'])
def get_data():
    data = supabase.table("feeds").select("*").execute()
    return jsonify(data.data)

@app.route('/')
def home():
    return jsonify('Hello, World!')

@app.route('/time')
def data():
    x = datetime.datetime.now()
    return jsonify(x)

@app.route('/rss')
def get_rss():
    try:
        x = requests.get('https://back.nber.org/rss/new.xml', timeout=5)  # Timeout in seconds
    # Process response here
    except requests.exceptions.Timeout:
        x = ('Request timeout')
    #print the response text (the content of the requested file):
    return x.text

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/full')
def full_rss():
    sources = [
'https://back.nber.org/rss/new.xml'
,'https://www.journals.uchicago.edu/action/showFeed?type=etoc&feed=rss&jc=jole'
,'https://www.journals.uchicago.edu/action/showFeed?type=etoc&feed=rss&jc=jpe'
,'http://export.arxiv.org/rss/cs'
,'http://export.arxiv.org/rss/q-fin'
,'https://back.nber.org/rss/releases.xml'
,'https://netflixtechblog.com/feed'
,'https://eng.lyft.com/feed'
,'https://engineering.atspotify.com/rss'
,'https://engineering.fb.com/rss'
,'https://medium.com/feed/airbnb-engineering'
,'https://github.blog/feed'
,'https://stackoverflow.blog/feed'
,'https://slack.engineering/feed'
,'https://medium.com/feed/draftkings-engineering'
,'https://medium.com/feed/fanduel-life/tagged/engineering'
,'https://hnrss.org/frontpage'
,'https://feeds.npr.org/1019/rss.xml'
,'https://ir.thomsonreuters.com/rss/news-releases.xml?items=15'
,'https://feeds.bloomberg.com/markets/news.rss'
,'https://feeds.bloomberg.com/politics/news.rss'
,'https://feeds.bloomberg.com/technology/news.rss'
,'https://feeds.bloomberg.com/wealth/news.rss'
,'https://fredblog.stlouisfed.org/feed'
,'https://www.jmlr.org/jmlr.xml'
,'https://www.jpl.nasa.gov/feeds/news/'
,'https://www.nasa.gov/feeds/iotd-feed/'
,'https://www.nasa.gov/technology/feed/'
,'http://www.federalreserve.gov/feeds/Data/CP_RATES.xml'
,'https://www.natesilver.net/feed'
]
    full = []
    for x in sources:
        full.append(iris.get_content(x))
    return jsonify(full)
