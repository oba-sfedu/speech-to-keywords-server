from flask_socketio import emit
import io
import os
import ffmpeg
import speech_recognition as sr
import redis
import yake
from nanoid import generate
from keywords import extract_keywords_yake, extract_keywords_keybert

r = sr.Recognizer()
kw_extractor = yake.KeywordExtractor()
language = "ru"

storage = redis.Redis(host='localhost', port=6379, decode_responses=True)


def handle_audio_message(message):
    file_obj = io.BytesIO()
    file_obj.write(message['data'])
    file_obj.seek(0)

    key = generate()
    input_name = "tmp/{key}.webm".format(key=key)
    output_name = "tmp/{key}.wav".format(key=key)

    with open(input_name, "wb") as f:
        f.write(file_obj.getbuffer())

    stream = ffmpeg.input(input_name)
    stream = ffmpeg.output(stream, output_name, loglevel="quiet")
    ffmpeg.run(stream)

    with sr.AudioFile(output_name) as source:
        audio = r.record(source)
        recognized = r.recognize_whisper(audio, model='small', language=language)
        stored_key = 'recognized-text-{sessionId}'.format(sessionId=message['sessionId'])

        content = storage.get(stored_key)
        new_content = content + recognized if content else recognized
        storage.set(stored_key, new_content, ex=3600)
        emit('recognized', {"recognized": recognized, "keywords": extract_keywords_keybert(new_content)})

    os.remove(input_name)
    os.remove(output_name)
