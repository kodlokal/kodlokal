"""
The index route
"""

from flask import jsonify
from app.kodlokal_app import app, APP_NAME


@app.route("/")
def main():
    return jsonify({"server": f"{APP_NAME} Server"})
