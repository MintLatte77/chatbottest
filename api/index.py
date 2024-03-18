from flask import Flask, request
import sys
from datetime import datetime, timedelta, timezone

# Timezone 세팅
TimezoneList = {'Asia/Seoul' : 9}
datetime_utc = datetime.utcnow()

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/time')
def time():
    return datetime_utc

@app.route('/meal', methods = ["POST"])
def meal():
	body = request.get_json()
	
	userTimezone = body['userRequest']['timezone']
	timezone_user = timezone(timedelta(hours=TimezoneList[userTimezone]))
	datetime_user = datetime_utc.astimezone(timezone_user)
	
	responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": datetime_user
                    }
                }
            ]
        }
	}
	return responseBody
