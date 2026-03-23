from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/ask/", methods=['POST'])
def ask():
    if 'file' not in request.files:
        return {'error': 'No file part'}, 400

    file = request.files['file']
    if file.filename == '':
        return {'error': 'No selected file'}, 400

    # Читаем аудиофайл (например, mp3)
    audio = AudioSegment.from_file(file.stream)

    # Здесь можно обработать аудио по вашему желанию
    # Например, для примера просто уменьшим громкость
    processed_audio = audio - 10  # уменьшает громкость на 10 дБ

    # Сохраняем обработанный файл во временный буфер
    buf = BytesIO()
    processed_audio.export(buf, format="wav")
    buf.seek(0)

    # Возвращаем файл клиенту
    return send_file(
        buf,
        mimetype="audio/wav",
        as_attachment=True,
        download_name="processed_audio.wav"
    )

if __name__ == '__main__':
    app.run(debug=True)