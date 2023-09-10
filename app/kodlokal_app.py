from flask import Flask
app_name = 'kodlokal'
app = Flask(__name__)
app.config.from_pyfile('../config.py')
