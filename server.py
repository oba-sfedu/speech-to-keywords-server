import os
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from nanoid import generate
from app.audio import save_to_file, convert_to_wav
from app.recognition import recognize_audio_file
from app.text_cache import get_text_cache, set_text_cache
from app.keywords import extract_keywords

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ["TOKENIZERS_PARALLELISM"] = "false"

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def hello_world():
    return render_template('index.html')


@socketio.on('connect')
def on_connect():
    print('connected:', request.sid)


@socketio.on('disconnect')
def on_connect():
    print('disconnected:', request.sid)


@socketio.on('audio')
def on_audio(message):
    key = generate()
    input_file_path = "{root}/tmp/{key}.webm".format(root=ROOT_DIR, key=key)
    wav_file_path = "{root}/tmp/{key}.wav".format(root=ROOT_DIR, key=key)

    save_to_file(message['data'], input_file_path)
    convert_to_wav(input_file_path, wav_file_path)

    recognized = recognize_audio_file(wav_file_path)

    text_cache = get_text_cache(message['sessionId'])
    new_text = text_cache + recognized if text_cache else recognized
    set_text_cache(message['sessionId'], new_text)

    emit('recognized', {"recognized": recognized, "keywords": extract_keywords(new_text)})

    os.remove(input_file_path)
    os.remove(wav_file_path)


if __name__ == '__main__':
    socketio.run(app)
