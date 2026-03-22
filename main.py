from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/ask/", methods=['POST'])
def ask():
    if request.method == 'POST':
        request.files['messageFile']
    
    return {
        'anser':'null'
    }