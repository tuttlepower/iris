from flask import Flask
from flask import jsonify
import datetime
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify('Hello, World!')

@app.route('/healthcheck')
def healthcheck():
    return jsonify("Healthcheck Endpoint")

@app.route('/get_data')
def get_data():
    d = [0+8,0,9,8,7]
    return jsonify(d)


@app.route('/time')
def data():
    x = datetime.datetime.now()
    return jsonify(x)



@app.route('/reqs')
def get_time():
    #the required first parameter of the 'get' method is the 'url':
    x = requests.get('https://w3schools.com/python/demopage.htm')
    #print the response text (the content of the requested file):
    return jsonify(x)
