import os

import requests # external library to send external HTTP requests with URL provided

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models import Result


@app.route('/', methods=['GET', 'POST'])
def hello():
    errors = []
    results = {}
    if request.method == "POST":
        # get the url from the input form
        try:
            url = request.form['url']
            r = requests.get(url)
            print(r.text)
        except:
            errors.append("Unable to get URL. Please make sure your url is valid and try again.")
    return render_template('index.html', errors=errors, results=results)

@app.route('/<name>')
def hi_there(name):
    return "Hi {}!".format(name)

if __name__ == '__main__':
    app.run()