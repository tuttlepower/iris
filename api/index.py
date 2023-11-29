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
    try:
        x = requests.get('https://w3schools.com/python/demopage.htm', timeout=5)  # Timeout in seconds
    # Process response here
    except requests.exceptions.Timeout:
        x = ('Request timeout')
    #print the response text (the content of the requested file):
    return x.text
