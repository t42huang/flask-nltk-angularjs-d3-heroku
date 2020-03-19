import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models import Result


@app.route('/')
def hello():
    return "Hello World from {} mode.".format(
        os.environ['APP_SETTINGS'][7:-6])
        # e.g. APP_SETTINGS=config.ProductionConfig

@app.route('/<name>')
def hi_there(name):
    return "Hi {}!".format(name)

if __name__ == '__main__':
    app.run()