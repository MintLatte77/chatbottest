from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'

@app.route('/meal')
def meal():
    timezone = "Asia/Seoul"
    try json_data = request.get_json()
    try timezone = json_data['userRequest']['timezone']
    return {"version": "2.0","template":{"outputs": [{"simpleText": {"text": json_data}}]}}
