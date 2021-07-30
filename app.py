from datetime import datetime
from flask import Flask, request
from flask_json import FlaskJSON, JsonError, json_response, as_json
import iris

app = Flask(__name__)
FlaskJSON(app)

@app.route('/')
def data():
    return "Hello"
#     data = iris.populate()
#     return json_response(data=data)

@app.route('/get_time')
def get_time():
    now = datetime.utcnow()
    return json_response(time=now)


@app.route('/get_value')
@as_json
def get_value():
    return dict(value=12)


if __name__ == '__main__':
    app.run(debug=True)