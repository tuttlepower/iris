from flask import Flask
from flask import jsonify
import datetime

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



# @app.route('/get_time')
# def get_time():
#     return json_response(time=datetime.utcnow())
