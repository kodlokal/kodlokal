from app.kodlokal_app import app, app_name


@app.route("/")
def main():
    return jsonify({ "server": f"{app_name} Server" })
