from io import BytesIO

from flask import Flask, send_file
from flask import request

app = Flask(__name__)

@app.route("/ask/", methods=['POST'])
def ask():
    if 'file' not in request.files:
        return {'error': 'No file part'}, 400

    file = request.files['file']
    if file.filename == '':
        return {'error': 'No selected file'}, 400

    return send_file(
        file,
        mimetype="audio/wav",
        as_attachment=True,
        download_name="processed_audio.wav"
    )

if __name__ == '__main__':
    app.run(debug=True)