from flask_socketio import emit
import io
import os
import ffmpeg
import speech_recognition as sr
import random
import string

r = sr.Recognizer()


def generate_random_key(length):
    return ''.join(random.choice(string.ascii_letters) for i in range(length))


def handle_audio_message(data):
    file_obj = io.BytesIO()
    file_obj.write(data)
    file_obj.seek(0)

    key = generate_random_key(32)
    input_name = "tmp/{key}.webm".format(key=key)
    output_name = "tmp/{key}.wav".format(key=key)

    with open(input_name, "wb") as f:
        f.write(file_obj.getbuffer())

    stream = ffmpeg.input(input_name)
    stream = ffmpeg.output(stream, output_name, loglevel="quiet")
    ffmpeg.run(stream)

    with sr.AudioFile(output_name) as source:
        audio = r.record(source)
        recognized = r.recognize_whisper(audio, model="base", language="ru")
        emit('recognized', recognized)

    os.remove(input_name)
    os.remove(output_name)