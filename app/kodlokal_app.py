"""
The Flask app
"""

import os
from flask import Flask

APP_NAME = 'kodlokal'
app = Flask(APP_NAME)
environment = os.environ.get('ENV', 'production')

if environment == 'test':
    app.config.from_pyfile('tests/config.py')
else:
    app.config.from_pyfile('config.py')
