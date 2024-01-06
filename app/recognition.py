import speech_recognition as sr
from tenacity import retry, stop_after_attempt
from app.settings import language, whisper_model, whisper_recognize_attempts

r = sr.Recognizer()


@retry(stop=stop_after_attempt(whisper_recognize_attempts))
def recognize_audio_file(file_path):
    with sr.AudioFile(file_path) as source:
        audio = r.record(source)
        return r.recognize_whisper(audio, model=whisper_model, language=language)
