from app.kodlokal_app import app

@app.route("/")
def main():
    return jsonify({ "server": "Kodlokal Server" })
