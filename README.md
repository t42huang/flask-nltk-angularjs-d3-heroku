# Note

## Steps

- make sure installed python version is python 3, install it if not

- create virtual environment, install flask, add project dependencies in requirements.txt

```bash
# create virtual environment - venv
python -m venv venv
# activate the venv virtual environment
source venv/bin/activate

# install flask
pip install flask
# dump project dependencies in requirements.txt
pip freeze > requirements.txt
```

- bootstrap flask with Hello World code in `app.py`
- run `python app.py`
- double check the app is running at http://localhost:5000/

### deploy to heroku

```bash
# create heroku account if you don't have one
# login heroku from terminal
heroku login -i

# create heroku projects, one for production, one for staging
heroku create tinas-text-analyzer
heroku create tinas-text-analyzer-stage

# configure the git remotes
# - check what git remotes do we have at the moment
git remote -v

# - heroku is the default remote name, let's remove it first
git remote remove heroku

# - add one remote for production, one for staging
git remote add prod https://git.heroku.com/tinas-text-analyzer.git
git remote add stage https://git.heroku.com/tinas-text-analyzer-stage.git

# - check git remotes again,
#   this time we should have two: prod & stage
git remote -v

# deploy the app to staging
git push stage master
# - double-check it works at: https://tinas-text-analyzer-stage.herokuapp.com/

# deploy the app to production
git push prod master
# - double-check it works at: https://tinas-text-analyzer.herokuapp.com/


# Set up environment variables
export APP_SETTINGS="config.DevelopmentConfig"
heroku config:set APP_SETTINGS=config.StagingConfig --remote stage
heroku config:set APP_SETTINGS=config.ProductionConfig --remote prod
```

### Database

- [install Postgres](https://postgresapp.com/documentation/install.html)
  - for Mac, you might need to add an alias `alias psql='/Applications/Postgres.app/Contents/Versions/latest/bin/psql'`
- create dev database

```bash
$ psql
# create database text_analyzer_dev;
CREATE DATABASE
# \q    # \q to exit

export DATABASE_URL="postgresql:///text_analyzer_dev"
python manage.py db init
python manage.py db migrate
python manage.py db upgrade

python manage.py runserver

# add the Heroku Postgres addon for Staging environment
heroku addons:create heroku-postgresql:hobby-dev --app tinas-text-analyzer-stage

# check environment variables in Staging environment, 
#   you should see an entry for `DATABASE_URL`
heroku config --app tinas-text-analyzer-stage

# push the changes to staging
git push stage master
# run the migrations on staging
heroku run python manage.py db upgrade --app tinas-text-analyzer-stage

## check if all is working as expected on https://tinas-text-analyzer-stage.herokuapp.com/


## do the same for production
# add the Heroku Postgres addon for Production environment
heroku addons:create heroku-postgresql:hobby-dev --app tinas-text-analyzer

# check environment variables in Production environment, 
#   you should see an entry for `DATABASE_URL`
heroku config --app tinas-text-analyzer

# push the changes to Production
git push prod master
# run the migrations on Production
heroku run python manage.py db upgrade --app tinas-text-analyzer

## check if all is working as expected on https://tinas-text-analyzer.herokuapp.com/

```

### Workflow: Development > Staging > Production

1. make some changes, e.g. bug fix, or add a new feature.
2. confirm it works on your local development environment.
3. commit the change (ask for peer reviews to get it approved).
4. push the change to staging environment, confirm it works.
5. push the change to live production environment for customers / end users.

### NLTK

```bash
mkdir nltk_data; cd nltk_data; pwd
# copy the path of this folder
python
>>> import nltk
>>> nltk.download()
# - on the window opened, change the Downloading Directory to the nltk_data copied above
# - select Models tab > punkt, then click `download`

```

Note: to reduce the size of the commit and stay focused, we removed support for other languages. We only support English language - Only English tokenier is kept, all others in `plunkt` are deleted, including the `plunkt.zip`

### Redis Task Queue

```bash
# install redis
brew install redis

# open a new shell window
# start the Redis server:
redis-server

# open a new shell window
# config environemnt variable for this shell session
export APP_SETTINGS="config.DevelopmentConfig"
export DATABASE_URL="postgresql:///text_analyzer_dev"

# run a worker process to listen for queued tasks
python worker.py

# go to http://localhost:5000, submit using an url, for example https://realpython.com


# deploy to Staging environment
# add Redis to the staging environment
heroku addons:create redistogo:nano --app tinas-text-analyzer-stage
# then you can double-check making sure Redis environment variable is set
heroku config --app tinas-text-analyzer-stage | grep REDISTOGO_URL
# to check running heroku dynos details, run this
heroku addons

# test it locally before pusing to the staging server [Not working yet?]
redis-server
heroku local

# push changes to Staging for deployment
git push stage master # or use: git push --force stage master


# deploy to Production environment
# add Redis to the Production environment
heroku addons:create redistogo:nano --app tinas-text-analyzer
# then you can double-check making sure Redis environment variable is set
heroku config --app tinas-text-analyzer | grep REDISTOGO_URL
# to check running heroku dynos details, run this
heroku addons
# push changes to Production for deployment
git push prod master # or use: git push --force prod master

```

## Reference

1. [Project Setup](https://realpython.com/flask-by-example-part-1-project-setup/)

    - Set up a local development environment.
    - Deploy both a staging and a production environment on Heroku.
    - [code reference](https://github.com/realpython/flask-by-example)

2. [Setup PostgreSQL, SQLAlchemy & Alembic](https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/)
  
    - Postgres database to store the results of our word counts
    - SQLAlchemy, an Object Relational Mapper
    - Alembic to handle database migrations.
3. [Text Processing with Requests, BeautifulSoup, and NLTK (Natural Language Toolkit) libraries](https://realpython.com/flask-by-example-part-3-text-processing-with-requests-beautifulsoup-nltk/)
    - Add in the back-end logic to scrape and then process the word counts from a webpage using the requests, BeautifulSoup, and Natural Language Toolkit (NLTK) libraries
4. [Implement a Redis Task Queue](https://realpython.com/flask-by-example-implementing-a-redis-task-queue/)
    - implement a Redis task queue to handle text processing
5. [Integrate Flask and AngularJS](https://realpython.com/flask-by-example-integrating-flask-and-angularjs/)
    - Set up Angular on the front-end to continuously poll the back-end to see if the request is done processing.
    - wrap some angular related code in {% raw %} and {% endraw %} so that Jinja knows to evaluate this as raw HTML. If we didn’t do this, Flask will try to evaluate the {{ variable }} as a Jinja variable and Angular won’t get a chance to evaluate it.
6. [Update Staging Environment](https://realpython.com/updating-the-staging-environment/)
    - Push to the staging server on Heroku - setting up Redis and detailing how to run two processes (web and worker) on a single Dyno.
7. [Update FrontEnd UI](https://realpython.com/flask-by-example-updating-the-ui/)

### Learn more

- [Heroku](https://devcenter.heroku.com/)
  - [heroku local](https://devcenter.heroku.com/articles/heroku-local)
- [Heroku Postgres Follower(Slave) Databases](https://devcenter.heroku.com/articles/heroku-postgres-follower-databases)
- [Natural Language Toolkit (NLTK)](https://www.nltk.org/index.html)
  - Book: [Natural Language Processing with Python
– Analyzing Text with the Natural Language Toolkit](http://www.nltk.org/book/)
  - [Install NLTK Data](https://www.nltk.org/data.html#command-line-installation)
  - [nltk.tokenize](https://www.nltk.org/api/nltk.tokenize.html)
  - [nltk.text](https://www.nltk.org/_modules/nltk/text.html)
- [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Redis](https://redis.io/)
  - [Heroku Redis ToGo](https://devcenter.heroku.com/articles/redistogo)
- [AngularJS](https://angularjs.org/)
  - [Bitcoin Caculator with Data Visualization using AngularJS & D3](https://github.com/mjhea0/thinkful-angular)
  - [AngularJS $timeout](https://code.angularjs.org/1.4.9/docs/api/ng/service/$timeout)
  - [D3.js - Data Driven Documents](https://d3js.org/)
