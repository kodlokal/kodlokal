from flask import Flask
import os

app_name = 'kodlokal'
app = Flask(app_name)
environment = os.environ.get('ENV', 'production')

if environment == 'test':
  app.config.from_pyfile('tests/config.py')
else:
  app.config.from_pyfile('config.py')
