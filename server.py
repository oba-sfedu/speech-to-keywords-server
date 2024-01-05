from flask import Flask, render_template, request
from flask_socketio import SocketIO
from audio_handler import handle_audio_message
import speech_recognition as sr

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

r = sr.Recognizer()

@app.route("/")
def hello_world():
    return render_template('index.html')


@socketio.on('connect')
def on_connect():
    print('connected:', request.sid)


@socketio.on('disconnect')
def on_connect():
    print('disconnected:', request.sid)


socketio.on_event('audio', handle_audio_message)


if __name__ == '__main__':
    socketio.run(app)
