from flask import Flask, request
import sys
from datetime import datetime, timedelta, timezone
import os
import requests
import json

# 시간 설정

datetime_utc = datetime.utcnow()
timezone_kst = timezone(timedelta(hours=9))
datetime_kst = datetime_utc.astimezone(timezone_kst)
day = datetime_kst.strftime("%Y%m%d")

# NEIS 설정
url = "https://open.neis.go.kr/hub/mealServiceDietInfo"
service_key = os.environ.get('NEIS_Key')
edu_code = os.environ.get('NEIS_edu')
school_code = os.environ.get('NEIS_school')

# body = request.get_json()
# userTimezone = body['userRequest']['timezone']

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/time')
def time():
	return str(datetime_kst) + "  " + str(day)

@app.route('/mealjson')
def mealjson():
	params = {
		'KEY' : service_key,
		'Type' : 'json',
		'pIndex' : '1',
		'pSize' : '100',
		'ATPT_OFCDC_SC_CODE' : edu_code,
		'SD_SCHUL_CODE' : school_code,
		'MLSV_YMD' : day
	}

	response = requests.get(url, params=params)
	contents = response.text
	return contents

@app.route('/meal', methods = ["POST"])
def meal():
	params = {
		'KEY' : service_key,
		'Type' : 'json',
		'pIndex' : '1',
		'pSize' : '100',
		'ATPT_OFCDC_SC_CODE' : edu_code,
		'SD_SCHUL_CODE' : school_code,
		'MLSV_YMD' : day
	}

	response = requests.get(url, params=params)
	contents = response['mealServiceDietInfo']['row']['DDISH_NM']
	
	responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": contents
                    }
                }
            ]
        }
	}
	return responseBody
