from flask import Flask

app_name = 'kodlokal'
app = Flask(app_name)
app.config.from_pyfile('config.py')
