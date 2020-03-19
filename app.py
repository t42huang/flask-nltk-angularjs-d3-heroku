import os
import operator
from collections import Counter


import requests # external library to send external HTTP requests with URL provided
import re
import nltk
from bs4 import BeautifulSoup
from rq import Queue
from rq.job import Job

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from stop_words import stops
from worker import conn


app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
q = Queue(connection=conn) # set up Redis connection & initialize a queue based on the conn

from models import *


def count_and_save_words(url):

    errors = []

    try:
        resp = requests.get(url)
    except:
        errors.append(
            "Unable to get URL. Please make sure it's valid and try again."
        )
        return {"error": errors}

    # text processing
    raw = BeautifulSoup(resp.text, features="html.parser").get_text()
    nltk.data.path.append('./nltk_data/')  # set the path
    tokens = nltk.word_tokenize(raw)
    text = nltk.Text(tokens)

    # remove punctuation, count raw words
    nonPunct = re.compile('.*[A-Za-z].*')
    raw_words = [w for w in text if nonPunct.match(w)]
    raw_word_count = Counter(raw_words)

    # stop words
    no_stop_words = [w for w in raw_words if w.lower() not in stops]
    no_stop_words_count = Counter(no_stop_words)

    # save the results
    try:
        from models import Result
        result = Result(
            url=url,
            result_all=raw_word_count,
            result_no_stop_words=no_stop_words_count
        )
        db.session.add(result)
        db.session.commit()
        return result.id
    except:
        errors.append("Unable to add item to database.")
        return {"error": errors}


@app.route('/', methods=['GET', 'POST'])
def hello():
    results = {}

    if request.method == "POST":
        # this import solves a rq bug which currently exists
        from app import count_and_save_words

        # get the url from the input form
        url = request.form['url']
        if not url[:8].startswith(('https://', 'http://')):
            url = 'http://' + url
        
        job = q.enqueue_call(
            func=count_and_save_words, args=(url,), result_ttl=5000)
        print(job.get_id())

    return render_template('index.html', results=results)


@app.route('/<name>')
def hi_there(name):
    return "Hi {}!".format(name)


@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):
    
    job = Job.fetch(job_key, connection=conn)
    
    if job.is_finished:
        result = Result.query.filter_by(id=job.result).first()
        results = sorted(
            result.result_no_stop_words.items(),
            key=operator.itemgetter(1),
            reverse=True
        )[:10]
        return jsonify(results)
    else:
        return "Job in Progress: {}!".format(job_key), 202


if __name__ == '__main__':
    app.run()