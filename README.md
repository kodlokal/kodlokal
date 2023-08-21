# Kodlokal server

## Install

```bash
git clone git@github.com:kodlokal/kodlokal-gateway.git
cd kodlokal-gateway
python -m venv v
pip install -r requirements.txt
python app.py # once do initially to run and download large files, because gunicorn times out with default settings
```

## Run

```
gunicorn --timeout 60 -w 1 -b localhost:3737 app:app
```
