from flask import Flask
import os
from flask_json import FlaskJSON

app = Flask(__name__)
FlaskJSON(app)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/healthcheck')
def healthcheck():
    return "Healthcheck Endpoint"

@app.route('/get_data')
def get_data():
    return json_response(data={"key": "value"})


# @app.route('/')
# def data():
#     return json_response(data="Data")


# @app.route('/get_time')
# def get_time():
#     return json_response(time=datetime.utcnow())
