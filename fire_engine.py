from flask import Flask, render_template
from flask_socketio import SocketIO
import global_const as const
import stream

app = Flask(__name__)
sio = SocketIO(app)


@app.route("/")
def index():
    return render_template('index.html')


@sio.on("fire_start")
def on_start(json):
    if const.Debug:
        print('Client Request: Fire Service')
    stream.start_stream()


@sio.on('client_connected')
def handle_client_connect_event(json):
    print('received json: {0}'.format(str(json)))
    sio.emit('connection_accepted', json)


if __name__ == "__main__":
    app.debug = False
    sio.run(app, port=5000, debug=False, use_reloader=True)
    # sio.run(app, port=5000)
