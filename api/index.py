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
date = str(int(datetime_kst.strftime("%m"))) + "월 "+ str(int(datetime_kst.strftime("%d"))) + "일"
week = int(datetime_kst.strftime("%w"))

# NEIS 설정
url = "https://open.neis.go.kr/hub/mealServiceDietInfo"
service_key = os.environ.get('NEIS_Key')
edu_code = os.environ.get('NEIS_edu')
school_code = os.environ.get('NEIS_school')

# @app.route('/service', methods = ["POST"])
# 	body = request.get_json()
# 	userTimezone = body['userRequest']['timezone']

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/time')
def time():
	return str(datetime_kst) + "  " + str(day)

@app.route('/mealjson', methods = ["POST"])
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

	#급식 미제공 날짜 구별
	find = contents.find('해당하는 데이터가 없습니다.')
	return find



@app.route('/service', methods = ["POST"])
def service():
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

	#급식 미제공 날짜 구별
	find = contents.find('해당하는 데이터가 없습니다.')
	
	if find == -1:
		meal = "오늘은 급식이 없습니다!"
	else:
		findstart = contents.find('DDISH_NM') + 11
		findend = contents.find('ORPLC_INFO') - 3
		content = contents[findstart:findend]
		meal ="\n".join(content.split('<br/>'))
	
	responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
        			"textCard": {
          				"title": date + " 오늘의 급식",
          				"description": meal ,
          				"buttons": [
            				{
              					"action": "webLink",
              					"label": "온라인 건의함",
              					"webLinkUrl": "https://m.site.naver.com/1k4Sj"
            				}
            						]
        						}
				}
						]
		}
	}
	
	return responseBody
