import atexit
import os
import signal
from flask import Flask, send_from_directory, abort as response_abort

from common.dispatcher import Dispatcher
from gs.gs import GroundStation

app = Flask(__name__)
gs = None

# Path for our main Svelte page
@app.route("/")
def base():
    return send_from_directory('client/public', 'index.html')

# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/public', path)

@app.route("/launch", methods = ['POST'])
def launch():
    global gs
    if gs := gs:
        gs.launch()
    return ('', 204)

@app.route("/abort", methods = ['POST'])
def abort():
    global gs
    if gs := gs:
        gs.abort()
    return ('', 204)

@app.route("/cut", methods = ['POST'])
def cut():
    global gs
    if gs := gs:
        gs.cut()
    return ('', 204)

@app.route("/telemetry", methods = ['GET'])
def telemetry():
    global gs
    if gs := gs:
        return {
            'pos': gs.location[0] if gs.location is not None else None,
            'acc': gs.location[1] if gs.location is not None else None,
            'temp': gs.temperature
        }

    response_abort(500)

@app.route("/update", methods = ['POST'])
def update():
    global gs
    if gs := gs:
        gs.request_location()
        gs.request_pressure()
        gs.request_temperature()

    return ('', 204)

@app.route("/map_token", methods = ['GET'])
def map_token():
    if 'MAPBOX_TOKEN' not in os.environ:
        response_abort(503)
    return {'token': os.environ['MAPBOX_TOKEN']}

if __name__ == '__main__':
    Dispatcher().start()
    gs = GroundStation()
    app.run(port=8080, debug=True)
    Dispatcher().stop()
