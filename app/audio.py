import io
import ffmpeg


def save_to_file(data, file_path):
    file_obj = io.BytesIO()
    file_obj.write(data)
    file_obj.seek(0)

    with open(file_path, "wb") as f:
        f.write(file_obj.getbuffer())


def convert_to_wav(input_file_path, wav_file_path):
    stream = ffmpeg.input(input_file_path)
    stream = ffmpeg.output(stream, wav_file_path, loglevel="quiet")
    ffmpeg.run(stream)
