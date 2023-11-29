from dataclasses import dataclass
from datetime import datetime

from flask import Flask
from flask_cors import CORS, cross_origin
from flask_json import FlaskJSON, as_json, json_response



app = Flask(__name__)


@app.route('/healthcheck')
def healthcheck():
    return "Healthcheck Endpoint"


@app.route('/')
def data():
    return json_response(data="Data")


@app.route('/get_time')
def get_time():
    return json_response(time=datetime.utcnow())
