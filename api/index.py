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
	day = datetime_kst.strftime("%Y%m%d")
	
	return str(datetime_kst) + "  " + str(day)

@app.route('/meal', methods = ["POST"])
def meal():
	body = request.get_json()
	
	userTimezone = body['userRequest']['timezone']
	
	timezone_kst = timezone(timedelta(hours=9))
	datetime_kst = datetime_utc.astimezone(timezone_kst)
	day = datetime_kst.strftime("%Y%m%d")
	
	responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": str(day)
                    }
                }
            ]
        }
	}
	return responseBody
