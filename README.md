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
