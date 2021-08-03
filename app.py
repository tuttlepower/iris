from datetime import datetime
from flask import Flask, request, jsonify
from flask_json import FlaskJSON, JsonError, json_response, as_json
import iris
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import json
from dataclasses import dataclass
# from Paper import Paper

app = Flask(__name__)
FlaskJSON(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///article.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@dataclass
class Paper(db.Model):
    id: int
    title: str
    description: str
    link: str
    date: str
    title: str
    logo: str
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    link = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    logo = db.Column(db.String(100), nullable=False)

    def __init__(self, title, description, link, date, logo):
        self.title = title
        self.description = description
        self.link = link
        self.date = date
        self.logo = logo

@app.route('/')
@cross_origin()
def data():
    return json_response(data = Paper.query.all())

@app.route('/get_time')
def get_time():
    return json_response(time=datetime.utcnow())


@app.route('/get_value')
@as_json
def get_value():
    return dict(value=12)

@app.route('/initialize', methods=['GET'])
def initialize():
    db.create_all()
    articles = iris.populate()
    for article in articles:
        db.session.add(Paper(article['title'], article['description'], article['link'], article['date'], article['logo']))
        db.session.commit()
    db.session.flush()
    return json_response(status=200, message="Database initialized")


if __name__ == '__main__':
    app.run(debug=True)
