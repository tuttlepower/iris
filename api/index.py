from flask import Flask
import os
from flask import jsonify

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
    d = [0,0,9,8,7]
    return jsonify(d)


# @app.route('/')
# def data():
#     return json_response(data="Data")


# @app.route('/get_time')
# def get_time():
#     return json_response(time=datetime.utcnow())
