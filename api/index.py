from flask import Flask, request
import sys
def KakaoSimpleText(text): # SimpleText 출력시 사용
	responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": text
                    }
                }
            ]
        }
	}
	return responseBody
TimezoneList = {'Asia/Seoul' : 9}
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
	userTimezone = body['userRequest']['timezone']
	timezone = TimezoneList[userTimezone]
	
    return KakaoSimpleText(timezone)
