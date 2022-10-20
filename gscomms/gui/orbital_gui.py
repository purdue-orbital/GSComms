import os
from flask import Flask, send_from_directory, abort as response_abort

app = Flask(__name__)

# Path for our main Svelte page
@app.route("/")
def base():
    return send_from_directory('client/public', 'index.html')

# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/public', path)

@app.route("/launch")
def launch():
    pass

@app.route("/abort")
def abort():
    pass

@app.route("/cut")
def cut():
    pass

@app.route("/telemetry")
def telemetry():
    pass

@app.route("/map_token")
def map_token():
    if 'MAPBOX_TOKEN' not in os.environ:
        response_abort(503)
    return {'token': os.environ['MAPBOX_TOKEN']}


if __name__ == '__main__':
    app.run(port=8080, debug=True)
