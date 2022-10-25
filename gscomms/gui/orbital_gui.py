import atexit
import os
import signal
from flask import Flask, send_from_directory, abort as response_abort

from common.dispatcher import AckPing, Dispatcher
from gs.gs import GroundStation
from ws.ws_pollable import WsPollable

app = Flask(__name__)
gs = None
radio = None

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
    ack = AckPing(send_pings=False)
    Dispatcher().subscribe_station(ack.rx, ack.command_set)
    radio = WsPollable("ws://127.0.0.1:8081")
    Dispatcher().subscribe_radio(radio)
    gs = GroundStation()
    app.run(port=8080, debug=True)
    radio.stop()
