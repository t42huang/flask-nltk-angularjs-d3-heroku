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

### Workflow: Development > Staging > Production

1. make some changes, e.g. bug fix, or add a new feature.
2. confirm it works on your local development environment.
3. commit the change (ask for peer reviews to get it approved).
4. push the change to staging environment, confirm it works.
5. push the change to live production environment for customers / end users.
