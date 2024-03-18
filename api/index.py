from flask import Flask, request
import sys
from datetime import datetime, timedelta, timezone

datetime_utc = datetime.utcnow()

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/time')
def time():
	datetime_utc = datetime.utcnow()
	
	timezone_kst = timezone(timedelta(hours=9))
	datetime_kst = datetime_utc.astimezone(timezone_kst)
	
	return str(datetime_kst)

@app.route('/meal', methods = ["POST"])
def meal():
	body = request.get_json()
	
	userTimezone = body['userRequest']['timezone']
	
	timezone_kst = timezone(timedelta(hours=9))
	datetime_kst = datetime_utc.astimezone(timezone_kst)
	
	responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": str(datetime_kst)
                    }
                }
            ]
        }
	}
	return responseBody
