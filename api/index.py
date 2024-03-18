from flask import Flask, request
import sys

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'

@app.route('/meal', methods = ["POST"])
def meal():
    body = request.get_json()
    print(body)
    print(body['userRequest']['timezone'])

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "테스트"
                    }
                }
            ]
        }
	}
    
    return responseBody
