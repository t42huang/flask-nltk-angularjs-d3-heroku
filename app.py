import os
import operator
from collections import Counter

import requests # external library to send external HTTP requests with URL provided
import re
import nltk
from bs4 import BeautifulSoup

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

from stop_words import stops


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
            resp = requests.get(url)
            # print(resp.text)
        except:
            errors.append("Unable to get URL. Please make sure your url is valid and try again.")
            return render_template('index.html', errors=errors)
    
        if resp:
            # text processing
            # - get only text from the html, discard others like html tags, scripts, etc.
            raw = BeautifulSoup(resp.text, 'html.parser').get_text()
            
            # tokenize the raw text (into individual words)
            nltk.data.path.append('./nltk_data/') # set the path
            tokens = nltk.word_tokenize(raw)
            text = nltk.Text(tokens) # turn the tokens (words) into an nltk text object

            # remove punctuation, count raw words
            nonPunct = re.compile('.*[A-Za-z].*')
            raw_words = [w for w in text if nonPunct.match(w)]
            raw_word_count = Counter(raw_words)

            # stop words
            no_stop_words = [w for w in raw_words if w.lower() not in stops]
            no_stop_words_count = Counter(no_stop_words)

            # save the results
            results = sorted(
                no_stop_words_count.items(),
                key=operator.itemgetter(1),
                reverse=True
            )

            try:
                result = Result(
                    url=url,
                    result_all=raw_word_count,
                    result_no_stop_words=no_stop_words_count
                )
                db.session.add(result)
                db.session.commit()
            except:
                errors.append("Unable to add item to database.")

    return render_template('index.html', errors=errors, results=results)

@app.route('/<name>')
def hi_there(name):
    return "Hi {}!".format(name)

if __name__ == '__main__':
    app.run()