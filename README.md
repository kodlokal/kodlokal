# Kodlokal server

## Install

```bash
git clone git@github.com:kodlokal/kodlokal-gateway.git
cd kodlokal-gateway
python -m venv v
pip install -r requirements.txt
```

## Run

```
gunicorn --timeout 60 -w 1 -b localhost:3737 app:app
```
