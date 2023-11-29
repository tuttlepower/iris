from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'
@app.route('/healthcheck')
def healthcheck():
    return "Healthcheck Endpoint"


# @app.route('/')
# def data():
#     return json_response(data="Data")


# @app.route('/get_time')
# def get_time():
#     return json_response(time=datetime.utcnow())
