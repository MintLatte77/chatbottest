from flask import Flask, request
import sys
from datetime import datetime, timedelta, timezone
import os
import requests
import json
from pyairtable import Table, Base
from pyairtable.formulas import match
import time

# 시간 설정

datetime_utc = datetime.utcnow()
timezone_kst = timezone(timedelta(hours=9))
datetime_kst = datetime_utc.astimezone(timezone_kst)
twodayslater = timedelta(days=2)
datetime_kst_2 = datetime_kst + twodayslater
day = datetime_kst.strftime("%Y%m%d")
day_2 = datetime_kst_2.strftime("%Y%m%d")
date = str(int(datetime_kst.strftime("%m"))) + "월 "+ str(int(datetime_kst.strftime("%d"))) + "일"
week = int(datetime_kst.strftime("%w"))
time = int(datetime_kst.strftime("%H"))


# 환경변수/시간표 설정
# table1 - 시간표
NEISmealurl = "https://open.neis.go.kr/hub/mealServiceDietInfo"

NEIS_Key = os.environ.get('NEIS_Key')
edu_code = 'H10'
weeklist = {'0':'일','1':'월요','2':'화요','3':'수요','4':'목요','5':'금요','6':'토'}
timetabledict = {'월요1사회2': '박경환 | 2301(1-5)', '월요2체육': '강정현 | 6201(강당)', '월요3미술': '이창열 | 3202(미술실)', '월요4영어2': '이은정 | 2301(1-5)', '월요5수학': '김효정 | 2301(1-5)', '월요6한국사1': '윤선희 | 2301(1-5)', '월요7정보': '이상옥 | 4201(SW융합실)', '화요1한국사2': '김태경 | 2301(1-5)', '화요2과학2': '이정미 | 2402(생물과학실)', '화요3국어2': '남원정 | 2301(1-5)', '화요4사회1': '권민호 | 2301(1-5)', '화요5국어1': '김성은 | 2301(1-5)', '화요6영어2': '이은정 | 2301(1-5)', '화요7체육': '강정현 | 6201(강당)', '수요1미술': '이창열 | 3202(미술실)', '수요2수학': '김효정 | 2301(1-5)', '수요3과학3': '이정미 | 2402(생물과학실)', '수요4국어2': '남원정 | 2301(1-5)', '수요5직업': '장지연 | 2404(진로실)', '수요6진로': '남원정 | 2301(1-5)', '수요7오늘은 7교시가 없어요':' - ','목요1사회3': '박정호 | 2301(1-5)', '목요2정보': '이상옥 | 4201(SW융합실)', '목요3과학실험': '김명귀 | 2403(화학실험실)', '목요4영어1': '신지현 | 2301(1-5)', '목요5예술1': '이창열 | 3202(미술실)', '목요6수학': '김효정 | 2301(1-5)', '목요7국어1': '김성은 | 2301(1-5)', '금요1수학': '김효정 | 2301(1-5)', '금요2한국사2': '김태경 | 2301(1-5)', '금요3영어1': '신지현 | 2301(1-5)', '금요4과학1': '김명귀 | 2301(1-5)', '금요5자율': '', '금요6동아리': '', '금요7여유': ''}
timetablelist = []
teacherlist = []


airtable_token = os.environ.get('Airtable_Key')
scheduleID = 'app4Shep99fg80KYb'
Eonyang = 'tbluLhtM3VcwQdo8u'
Samnam = 'tblg8eounZNf1xCAs'
Eschedule = Table(airtable_token, scheduleID, Eonyang)
Sschedule = Table(airtable_token, scheduleID, Samnam)

# New code
# airtable_token = os.environ.get('Airtable_Key')
UserIdBase = 'appehbq0HhoF3Rk62'
UserIdTable = 'tblm8yAPlQ3wzjAKp'
UserIdData = Table(airtable_token, UserIdBase, UserIdTable)
areacode = {'서울':'B10', '부산':'C10', '대구':'D10', '인천':'E10', '광주':'F10', '대전':'G10', '울산':'H10', '세종':'I10', '경기':'J10', '강원':'K10', '충북':'M10', '충남':'N10', '전북':'P10', '전남':'Q10', '경북':'R10', '경남':'S10', '제주':'T10'}
newweeklist = {'0':'','1':'M','2':'T','3':'W','4':'H','5':'F','6':'','7':''}
UserTimeData = Table(airtable_token, UserIdBase, 'tblacWgSp8Z9x4Crw')

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

@app.route('/test1')
def test1():
	starttime = datetime.utcnow().timestamp()
	body = request.get_json()
	userID = body['userRequest']['user']['id'] # ID 조회
	print(userID)
	try:
		UserData = UserIdData.all(formula=match({"userID": userID, "Educode": '-', "schoolcode": '-', "schooltype":'-', "schoolname": '-', "gradecode": '-', "classcode": '-', "tablecode": '-'}, match_any=True))
		if UserData == 0 or UserData == "false" or UserData == "" or UserData == "NaN" or UserData == []:
			print("Can't Search Data")
			raise Exception("Can't Search Data")
		else:
			Educode = UserData[0]['fields']['Educode']
			schoolcode = UserData[0]['fields']['schoolcode']
			schooltype = UserData[0]['fields']['schooltype']
			schoolname = UserData[0]['fields']['schoolname']
			gradecode = UserData[0]['fields']['gradecode']
			classcode = UserData[0]['fields']['classcode']
			tablecode = UserData[0]['fields']['tablecode']
			

			timetablelink = 'https://open.neis.go.kr/hub/'+schooltype+'Timetable'
			
			Monday = timedelta(days=1-int(week))
			datetime_kst_M = datetime_kst + Monday
			day_M = datetime_kst_M.strftime("%Y%m%d")

			Tuesday = timedelta(days=2-int(week))
			datetime_kst_T = datetime_kst + Tuesday
			day_T = datetime_kst_T.strftime("%Y%m%d")

			Wednesday = timedelta(days=3-int(week))
			datetime_kst_W = datetime_kst + Wednesday
			day_W = datetime_kst_W.strftime("%Y%m%d")

			Thursday = timedelta(days=4-int(week))
			datetime_kst_H = datetime_kst + Thursday
			day_H = datetime_kst_H.strftime("%Y%m%d")

			Friday = timedelta(days=5-int(week))
			datetime_kst_F = datetime_kst + Friday
			day_F = datetime_kst_F.strftime("%Y%m%d")

			Weeklist = {day_M:'M', day_T:'T', day_W:'W', day_H:'H', day_F:'F'}
			
			output = []
			params = {
			'KEY' : NEIS_Key,
			'Type' : 'json',
			'pIndex' : '1',
			'pSize' : '100',
			'ATPT_OFCDC_SC_CODE' : Educode,
			'SD_SCHUL_CODE' : schoolcode,
			'AY' : '2024',
			'SEM' : '1',
			'GRADE' : gradecode,
			'CLASS_NM' : classcode,
			'TI_FROM_YMD' : day_M,
			'TI_TO_YMD' : day_F
			}
			
			response = requests.get(timetablelink, params=params)
			contentstext = response.text
			contents = response.json()
			
			find = contentstext.find('해당하는 데이터가 없습니다.')
			
			if find == -1:
				contentslist = contents[schooltype+'Timetable'][1]['row']
				for a in contentslist:
					Weekday = a['ALL_TI_YMD']
					Weekdayfind = Weeklist[a]
					class_time = Weeldayfind + a['PERIO']
					UserTimeData.all(formula=match({"Code": tablecode,class_time:'-'}, match_any=True))
					UserTimeData.update(tablecode, {class_time:a['ITRT_CNTNT']})
					print(class_time+" "+a['ITRT_CNTNT'])
				responsebody = {
  "version": "2.0",
  "template": {
	"outputs": [
	  {
		"textCard": {
		  "title": "업데이트 완료",
		  "description": "업데이트 완료, ",
		"buttons": [
			{
			  "action": "block",
			  "label": "재입력",
			  "blockId" : "66486e1826296c3bea93d1c0"
			},
			{
			  "action": "block",
			  "label": "오늘 급식 뭐임?",
			  "blockId" : "65f6ee3a58611458d29a92c2"
			},
			{
			  "action": "block",
			  "label": "오늘 시간표 뭐임?",
			  "blockId" : "65fa21294fc74f623ccfa55a"
			}
		]
		}
		  
	  }
	]
  }
}
			else:
				print("Can't Search time")
				raise Exception("Can't Search time")
	except:
		responseBody = {
		"version": "2.0",
		"template": {
			"outputs": [
				{
					"textCard": {
		  				"title": date + " 학사일정",
		  				"description": "먼저 사용자 등록을 통해 정보를 등록해 주세요! \n밑의 사용자 등록하기 메뉴를 통해 등록하거나 \'사용자 등록하기\'를 입력하세요." ,
		  				"buttons": [
			{
			  "action": "message",
			  "label": "사용자 등록하기",
			  "messageText": "사용자 등록하기"
			}
									]
								}
				}
						]
		}
	}
				
					
				
	return

@app.route('/test2')
def test2():
	timetablelink = 'https://open.neis.go.kr/hub/'+'his'+'Timetable'
	timetabledict = {'M1':'','M2':'','M3':'','M4':'','M5':'','M6':'','M7':'','T1':'','T2':'','T3':'','T4':'','T5':'','T6':'','T7':'','W1':'','W2':'','W3':'','W4':'','W5':'','W6':'','W7':'','H1':'','H2':'','H3':'','H4':'','H5':'','H6':'','H7':'','F1':'','F2':'','F3':'','F4':'','F5':'','F6':'','F7':''}
			
	Monday = timedelta(days=1-int(week))
	datetime_kst_M = datetime_kst + Monday
	day_M = datetime_kst_M.strftime("%Y%m%d")

	Tuesday = timedelta(days=2-int(week))
	datetime_kst_T = datetime_kst + Tuesday
	day_T = datetime_kst_T.strftime("%Y%m%d")

	Wednesday = timedelta(days=3-int(week))
	datetime_kst_W = datetime_kst + Wednesday
	day_W = datetime_kst_W.strftime("%Y%m%d")

	Thursday = timedelta(days=4-int(week))
	datetime_kst_H = datetime_kst + Thursday
	day_H = datetime_kst_H.strftime("%Y%m%d")

	Friday = timedelta(days=5-int(week))
	datetime_kst_F = datetime_kst + Friday
	day_F = datetime_kst_F.strftime("%Y%m%d")

	Weeklist = {day_M:'M', day_T:'T', day_W:'W', day_H:'H', day_F:'F'}
			
	output = []
	params = {
	'KEY' : NEIS_Key,
	'Type' : 'json',
	'pIndex' : '1',
	'pSize' : '100',
	'ATPT_OFCDC_SC_CODE' : 'H10',
	'SD_SCHUL_CODE' : '7480188',
	'AY' : '2024',
	'SEM' : '1',
	'GRADE' : '1',
	'CLASS_NM' : '5',
	'TI_FROM_YMD' : day_M,
	'TI_TO_YMD' : day_F
	}
			
	response = requests.get(timetablelink, params=params)
	contentstext = response.text
	contents = response.json()
	
	find = contentstext.find('해당하는 데이터가 없습니다.')
			
	if find == -1:
		contentslist = contents['his'+'Timetable'][1]['row']
		for a in contentslist:
			Weekday = a['ALL_TI_YMD']
			Weekdayfind = Weeklist[Weekday]
			class_time = Weekdayfind + a['PERIO']
			print(class_time+" "+a['ITRT_CNTNT'])
			updatedict = {class_time : a['ITRT_CNTNT']}
			timetabledict.update(updatedict)

	return timetabledict

@app.route('/test', methods = ['POST'])
def test():
	responsebody = {
  "version": "2.0",
  "template": {
    "outputs": [
	    {
            "simpleText": {
                "text": "1학년 5반 5월 20일 시간표"
            }
          },
      {
        "carousel": {
          "type": "itemCard",
          "items": [
            {
              "title": "5교시 과학탐구 과학탐구 과학탐구\n6교시 과학탐구 과학탐구 과학탐구\n7교시 과학탐구 과학탐구 과학탐구",
              "itemList": [
                {
                  "title": "　요일",
                  "description": " 월요일   화요일   수요일 "
                },
                {
                  "title": "1교시",
                  "description": "과학탐구 과학탐구 과학탐구"
                },
                {
                  "title": "2교시",
                  "description": "과학탐구 과학탐구 과학탐구"
                },
                {
                  "title": "3교시",
                  "description": "과학탐구 과학탐구 과학탐구"
                },
                {
                  "title": "4교시",
                  "description": "과학탐구 과학탐구 과학탐구"
                }
              ],
              "itemListAlignment": "left"
            },
            {
              "title": "5교시 과학탐구 과학탐구\n6교시 과학탐구 과학탐구\n7교시 과학탐구 과학탐구",
              "itemList": [
                {
                  "title": "　요일",
                  "description": " 목요일   금요일 "
                },
                {
                  "title": "1교시",
                  "description": "과학탐구 과학탐구"
                },
                {
                  "title": "2교시",
                  "description": "과학탐구 과학탐구"
                },
                {
                  "title": "3교시",
                  "description": "과학탐구 과학탐구"
                },
                {
                  "title": "4교시",
                  "description": "과학탐구 과학탐구"
                }
              ],
              "itemListAlignment": "left"
            }
          ]
        }
      }
    ]
  }
}
	return responsebody

@app.route('/sche', methods = ['POST'])
def sche():
	body = request.get_json()
	userID = body['userRequest']['user']['id']
	scheN = 0
	try:
		useridtable = UserIdData.all(formula=match({"userID":userID}))
		print(useridtable)
		id1 = useridtable[0]['id']
		schedulename = []
		scheduledatestart = []
		scheduledateend = []
		schedatastart = ""
		schedataend = ""
		print("Setting")
		if useridtable == 0 or useridtable == "false" or useridtable == "" or useridtable == "NaN" or useridtable == []:
			responseBody = {
		"version": "2.0",
		"template": {
			"outputs": [
				{
					"textCard": {
		  				"title": date + " 학사일정",
		  				"description": "먼저 사용자 등록을 통해 정보를 등록해 주세요! \n밑의 사용자 등록하기 메뉴를 통해 등록하거나 \'사용자 등록하기\'를 입력하세요." ,
		  				"buttons": [
			{
			  "action": "message",
			  "label": "사용자 등록하기",
			  "messageText": "사용자 등록하기"
			}
									]
								}
				}
						]
		}
	}
		else:
			print("school")
			for a in UserIdData.all():
				if id1 == a['id']:
					data = a['fields']
					if data['schoolcode'] == "S":
						Loading = Sschedule.all(sort=['datestart'])
						schooln = "삼남중학교"
						break
					elif data['schoolcode'] == "E":
						Loading = Eschedule.all(sort=['datestart'])
						schooln = "언양고등학교"
						break
					else:
						Loading = Sschedule.all(sort=['datestart'])
						schooln = "언양고등학교"
						break
			print(schooln)
			for a in Loading:
				schedatastart = a['fields']['datestart']
				schedataend = a['fields']['dateend']
				startday = "".join(schedatastart.split("-"))
				print(startday)
				endday = "".join(schedataend.split("-"))
				print(endday)
				if int(day) > int(startday):
					if int(day) > int(endday):
						scheN += 1
					else:
						break
				else:
					break
			print(scheN)
			
			for b in range(scheN, scheN + 5):
				schedulename.append(Loading[b]['fields']['schedule'])
				scheduledatestart.append(Loading[b]['fields']['datestart'])
				scheduledateend.append(Loading[b]['fields']['dateend'])
			
			print(schedulename)

			if scheduledatestart[0] == scheduledateend[0]:
				schedescr0 = scheduledatestart[0]
			else:
				schedescr0 = scheduledatestart[0] + " ~ " + scheduledateend[0]

			if scheduledatestart[1] == scheduledateend[1]:
				schedescr1 = scheduledatestart[1]
			else:
				schedescr1 = scheduledatestart[1] + " ~ " + scheduledateend[1]
			
			if scheduledatestart[2] == scheduledateend[2]:
				schedescr2 = scheduledatestart[2]
			else:
				schedescr2 = scheduledatestart[2] + " ~ " + scheduledateend[2]

			if scheduledatestart[3] == scheduledateend[3]:
				schedescr3 = scheduledatestart[3]
			else:
				schedescr3 = scheduledatestart[3] + " ~ " + scheduledateend[3]

			if scheduledatestart[4] == scheduledateend[4]:
				schedescr4 = scheduledatestart[4]
			else:
				schedescr4 = scheduledatestart[4] + " ~ " + scheduledateend[4]
			responseBody = {
  "version": "2.0",
  "template": {
    "outputs": [
      {
        "listCard": {
          "header": {
            "title": schooln + " 학사일정"
          },
          "items": [
            {
              "title": schedulename[0],
              "description": schedescr0
            },
            {
              "title": schedulename[1],
              "description": schedescr1
            },
            {
              "title": schedulename[2],
              "description": schedescr2
            },
            {
              "title": schedulename[3],
              "description": schedescr3
            },
            {
              "title": schedulename[4],
              "description": schedescr4
            }
	  ]
        }
      }
    ]
  }
}

	except:
		responseBody = {
		"version": "2.0",
		"template": {
			"outputs": [
				{
					"textCard": {
		  				"title": date + " 학사일정",
		  				"description": "먼저 사용자 등록을 통해 정보를 등록해 주세요! \n밑의 사용자 등록하기 메뉴를 통해 등록하거나 \'사용자 등록하기\'를 입력하세요." ,
		  				"buttons": [
			{
			  "action": "message",
			  "label": "사용자 등록하기",
			  "messageText": "사용자 등록하기"
			}
									]
								}
				}
						]
		}
	}

	return responseBody
				
			

# 동의서 작성
@app.route('/agree', methods = ['POST'])
def agree():
	responesebody = {
  "version": "2.0",
  "template": {
	"outputs": [
	  {
		"textCard": {
		  "title": "개인정보 수집 및 이용 동의서",
		  "description": "\'오늘 급식 뭐임\'(이하 \'서비스\')은 급식, 시간표, 학사 일정 확인 등을 위해 「개인정보 보호법」 제 15조 1항에 따라 보유 기간(25년 2월 28일)까지 사용자의 개인정보(암호화된 사용자 ID, 지역, 학교, 학년, 반)를 수집 및 이용합니다. 사용자는 서비스 이용에 필요한 최소한의 개인정보 수집 및 이용에 동의하지 않을 수 있으나, 동의를 거부 할 경우 서비스 이용이 불가합니다.\n아래 동의 버튼 클릭 시 해당 내용에 동의한 것으로 간주됩니다.",
		"buttons": [
			{
			  "action": "block",
			  "label": "동의",
			  "blockId" : "66486e1826296c3bea93d1c0"
			}
		]
		}
		  
	  }
	]
  }
}
	return responesebody
@app.route('/info', methods = ['POST'])
def info():
	responesebody = {
  "version": "2.0",
  "template": {
    "outputs": [
      {
        "textCard": {
          "title": "챗봇을 사용하기 전에, 사용자 정보를 입력해 주세요.",
          "description": "사용자 정보는 다음과 같은 형식으로 입력해 주세요.\n xx(지역) xx학교 x학년 x반\n예) 울산 언양고등학교 1학년 5반"
        }
      }
    ]
  }
}
	return responesebody

@app.route('/infocheck', methods = ['POST'])
def infocheck():
	starttime = datetime.utcnow().timestamp()
	body = request.get_json()
	userinfo = body['userRequest']['utterance']
	userID = body['userRequest']['user']['id']
	print(userinfo)
	try:
		useridtable = UserIdData.all(formula=match({"userID":userID}))
		print(useridtable)
		olderid = useridtable[0]['fields']['userID']
		id1 = useridtable[0]['id']
		if useridtable == 0 or useridtable == "false" or useridtable == "" or useridtable == "NaN" or useridtable == []:
			Newdata = {'userID': userID, 'Educode': "", 'schoolcode': "", 'schooltype':"", 'schoolname':'', 'gradecode': 0, 'classcode': 0, 'M1':'　　　　','M2':'　　　　','M3':'　　　　','M4':'　　　　','M5':'　　　　','M6':'　　　　','M7':'　　　　','T1':'　　　　','T2':'　　　　','T3':'　　　　','T4':'　　　　','T5':'　　　　','T6':'　　　　','T7':'　　　　','W1':'　　　　','W2':'　　　　','W3':'　　　　','W4':'　　　　','W5':'　　　　','W6':'　　　　','W7':'　　　　','H1':'　　　　','H2':'　　　　','H3':'　　　　','H4':'　　　　','H5':'　　　　','H6':'　　　　','H7':'　　　　','F1':'　　　　','F2':'　　　　','F3':'　　　　','F4':'　　　　','F5':'　　　　','F6':'　　　　','F7':'　　　　'}
			UserIdData.create(Newdata)
			print(Newdata)
		elif userID == olderid:
			UserIdData.update(id1, {'userID': userID, 'Educode': "", 'schoolcode': "", 'schooltype':"", 'schoolname':'', 'gradecode': 0, 'classcode': 0, 'M1':'　　　　','M2':'　　　　','M3':'　　　　','M4':'　　　　','M5':'　　　　','M6':'　　　　','M7':'　　　　','T1':'　　　　','T2':'　　　　','T3':'　　　　','T4':'　　　　','T5':'　　　　','T6':'　　　　','T7':'　　　　','W1':'　　　　','W2':'　　　　','W3':'　　　　','W4':'　　　　','W5':'　　　　','W6':'　　　　','W7':'　　　　','H1':'　　　　','H2':'　　　　','H3':'　　　　','H4':'　　　　','H5':'　　　　','H6':'　　　　','H7':'　　　　','F1':'　　　　','F2':'　　　　','F3':'　　　　','F4':'　　　　','F5':'　　　　','F6':'　　　　','F7':'　　　　'}, replace=True)
			print(olderid + " Updated!")
	except:
		Newdata = {'userID': userID, 'Educode': "", 'schoolcode': "", 'schooltype':"", 'schoolname':'', 'gradecode': 0, 'classcode': 0, 'M1':'　　　　','M2':'　　　　','M3':'　　　　','M4':'　　　　','M5':'　　　　','M6':'　　　　','M7':'　　　　','T1':'　　　　','T2':'　　　　','T3':'　　　　','T4':'　　　　','T5':'　　　　','T6':'　　　　','T7':'　　　　','W1':'　　　　','W2':'　　　　','W3':'　　　　','W4':'　　　　','W5':'　　　　','W6':'　　　　','W7':'　　　　','H1':'　　　　','H2':'　　　　','H3':'　　　　','H4':'　　　　','H5':'　　　　','H6':'　　　　','H7':'　　　　','F1':'　　　　','F2':'　　　　','F3':'　　　　','F4':'　　　　','F5':'　　　　','F6':'　　　　','F7':'　　　　'}
		UserIdData.create(Newdata)
		print(Newdata)
		
	try:
		schoolfind = userinfo.find("학교")
		gradefind = userinfo.find("학년")
		classfind = userinfo.find("반")
		if schoolfind == -1 or gradefind == -1 or classfind == -1:
			print("wrong format")
			raise Exception("wrong format")
		userarea = userinfo[0:2]
		userschool = userinfo[3:schoolfind+2]
		usergrade = userinfo[gradefind-1:gradefind]
		userclass = userinfo[classfind-1:classfind]
		userareacode = areacode[userarea]
		print(userareacode + userarea + userschool + usergrade + userclass)

		userareacode = areacode[userarea]
		params = {
			'KEY' : NEIS_Key,
			'Type' : 'json',
			'pIndex' : '1',
			'pSize' : '100',
			'ATPT_OFCDC_SC_CODE' : userareacode,
			'SCHUL_NM' : userschool
		}
		response = requests.get('https://open.neis.go.kr/hub/schoolInfo', params=params)
		contents = response.json()
		print(contents)
		contentstext = response.text
		print(contentstext)
		find = contentstext.find('해당하는 데이터가 없습니다.')
		print(find)
		print(contents['schoolInfo'][1]['row'][0])
		if find == -1:
			area = contents['schoolInfo'][1]['row'][0]['LCTN_SC_NM']
			print(area)
			school = contents['schoolInfo'][1]['row'][0]['SCHUL_NM']
			print(school)
			schoolcode = contents['schoolInfo'][1]['row'][0]['SD_SCHUL_CODE']
			print(schoolcode)
			schooltype = contents['schoolInfo'][1]['row'][0]['SCHUL_KND_SC_NM']
			print(schooltype)
			
			params = {
				'KEY' : NEIS_Key,
				'Type' : 'json',
				'pIndex' : '1',
				'pSize' : '100',
				'ATPT_OFCDC_SC_CODE' : userareacode,
				'SD_SCHUL_CODE' : schoolcode,
				'AY' : '2024'
			}
			response = requests.get('https://open.neis.go.kr/hub/classInfo', params=params)
			contents = response.json()
			contentstext = response.text
			find = contentstext.find('해당하는 데이터가 없습니다.')
			if find == -1:
				state = 0
				for a in contents['classInfo'][1]['row']:
					print(a)
					agrade = a['GRADE']
					aclass = a['CLASS_NM']
					if agrade == usergrade[0] and aclass == userclass[0]:
						state = 1
						strgrade = usergrade[0]
						strclass1 = userclass[0]
						grade = int(usergrade[0])
						class1 = int(userclass[0])
						if schooltype == "초등학교":
							type = "els"
						elif schooltype == "중학교":
							type = "mis"
						elif schooltype == "고등학교":
							type = "his"
						
						UserIdData.update(id1, {'userID':userID, 'Educode': userareacode, 'schoolcode': schoolcode, 'schooltype': type, 'schoolname':school, 'gradecode': grade, 'classcode': class1}, replace=True)
						break
				if state == 0:
					print("No Grade or Class")
					raise Exception("No Grade or Class")
			else:
				print("Can't find Grade")
				raise Exception("Can't find Grade")
		else:
			print("Can't find School")
			raise Exception("Can't find School")
		responsebody = {
  "version": "2.0",
  "template": {
	"outputs": [
	  {
		"textCard": {
		  "title": "입력한 정보가 맞는지 확인해 주세요",
		  "description": area + " " + school + " " + strgrade + "학년 " + strclass1 + "반",
		"buttons": [
			{
			  "action": "block",
			  "label": "맞아요!",
			  "blockId" : "664870174b66e33a2480f5b2"
			},
			{
			  "action": "block",
			  "label": "아니에요",
			  "blockId" : "66486e1826296c3bea93d1c0"
			}
		]
		}
		  
	  }
	]
  }
}

	except:
		responsebody = {
  "version": "2.0",
  "template": {
	"outputs": [
	  {
		"textCard": {
		  "title": "오류 발생",
		  "description": "오류 발생, 정보를 재입력하고 싶다면 \'재입력\' 버튼을, 급식이나 시간표를 조회하시려면 \'오늘 급식 뭐임?\' 또는 \'오늘 시간표 뭐임?\' 버튼을 눌러주세요.",
		"buttons": [
			{
			  "action": "block",
			  "label": "재입력",
			  "blockId" : "66486e1826296c3bea93d1c0"
			},
			{
			  "action": "block",
			  "label": "오늘 급식 뭐임?",
			  "blockId" : "65f6ee3a58611458d29a92c2"
			},
			{
			  "action": "block",
			  "label": "오늘 시간표 뭐임?",
			  "blockId" : "65fa21294fc74f623ccfa55a"
			}
		]
		}
		  
	  }
	]
  }
}
	endtime = datetime.utcnow().timestamp()
	loadingtime = endtime - starttime
	print(str(loadingtime) + "s 소요")
	print(responsebody)
	return responsebody

@app.route('/check', methods = ['POST'])
def check():
	responesebody = {
  "version": "2.0",
  "template": {
	"outputs": [
	  {
		"textCard": {
		  "title": "입력한 정보가 등록되었어요",
		"buttons": [
			{
			  "action": "message",
			  "label": "오늘 급식 뭐임?",
			  "messageText": "오늘 급식 뭐임?"
			},
			{
			  "action": "message",
			  "label": "오늘 시간표 뭐임?",
			  "messageText": "오늘 시간표 뭐임?"
			}
		]
		}
		  
	  }
	]
  }
}
	return responesebody


@app.route('/timetable', methods = ["POST"])
def timetable():
	starttime = datetime.utcnow().timestamp()
	body = request.get_json()
	userID = body['userRequest']['user']['id'] # ID 조회
	print(userID)
	try:
		UserData = UserIdData.all(formula=match({"userID": userID, "Educode": '-', "schoolcode": '-', "schooltype":'-', "schoolname": '-', "gradecode": '-', "classcode": '-', 'M1':'-','M2':'-','M3':'-','M4':'-','M5':'-','M6':'-','M7':'-','T1':'-','T2':'-','T3':'-','T4':'-','T5':'-','T6':'-','T7':'-','W1':'-','W2':'-','W3':'-','W4':'-','W5':'-','W6':'-','W7':'-','H1':'-','H2':'-','H3':'-','H4':'-','H5':'-','H6':'-','H7':'-','F1':'-','F2':'-','F3':'-','F4':'-','F5':'-','F6':'-','F7':'-'}, match_any=True))
		if UserData == 0 or UserData == "false" or UserData == "" or UserData == "NaN" or UserData == []:
			print("Can't Search Data")
			raise Exception("Can't Search Data")
		else:
			Educode = UserData[0]['fields']['Educode']
			schoolcode = UserData[0]['fields']['schoolcode']
			schooltype = UserData[0]['fields']['schooltype']
			schoolname = UserData[0]['fields']['schoolname']
			gradecode = UserData[0]['fields']['gradecode']
			classcode = UserData[0]['fields']['classcode']
			
			timetablelink = 'https://open.neis.go.kr/hub/'+schooltype+'Timetable'
			
			timetabledict = {'M1':'','M2':'','M3':'','M4':'','M5':'','M6':'','M7':'','T1':'','T2':'','T3':'','T4':'','T5':'','T6':'','T7':'','W1':'','W2':'','W3':'','W4':'','W5':'','W6':'','W7':'','H1':'','H2':'','H3':'','H4':'','H5':'','H6':'','H7':'','F1':'','F2':'','F3':'','F4':'','F5':'','F6':'','F7':''}
			for a in timetabledict.keys():
				newdict = {a : UserData[0]['fields'][a]}
				timetabledict.update(newdict)
			MTW_1 = timetabledict['M1'] + " " + timetabledict['T1'] + " " + timetabledict['W1']
			MTW_2 = timetabledict['M2'] + " " + timetabledict['T2'] + " " + timetabledict['W2']
			MTW_3 = timetabledict['M3'] + " " + timetabledict['T3'] + " " + timetabledict['W3']
			MTW_4 = timetabledict['M4'] + " " + timetabledict['T4'] + " " + timetabledict['W4']
			MTW_567 = timetabledict['M5'] + " " + timetabledict['T5'] + " " + timetabledict['W5'] + "\n" + timetabledict['M6'] + " " + timetabledict['T6'] + " " + timetabledict['W6'] + "\n" + timetabledict['M7'] + " " + timetabledict['T7'] + " " + timetabledict['W7']

			HF_1 = timetabledict['H1'] + " " + timetabledict['F1']
			HF_2 = timetabledict['H2'] + " " + timetabledict['F2']
			HF_3 = timetabledict['H3'] + " " + timetabledict['F3']
			HF_4 = timetabledict['H4'] + " " + timetabledict['F4']
			HF_567 = timetabledict['H5'] + " " + timetabledict['F5'] + "\n" + timetabledict['H6'] + " " + timetabledict['F6'] + "\n" + timetabledict['F7'] + " " + timetabledict['F7']
			
			responseBody = {
  "version": "2.0",
  "template": {
    "outputs": [
	    {
            "simpleText": {
                "text": schoolname + " " + gradecode + "학년 " + classcode + "반 " + date + " 시간표"
            }
          },
      {
        "carousel": {
          "type": "itemCard",
          "items": [
            {
              "title": MTW_567,
              "itemList": [
                {
                  "title": "　요일",
                  "description": " 월요일   화요일   수요일 "
                },
                {
                  "title": "1교시",
                  "description": MTW_1
                },
                {
                  "title": "2교시",
                  "description": MTW_2
                },
                {
                  "title": "3교시",
                  "description": MTW_3
                },
                {
                  "title": "4교시",
                  "description": MTW_4
                }
              ],
              "itemListAlignment": "left"
            },
            {
              "title": HF_567,
              "itemList": [
                {
                  "title": "　요일",
                  "description": " 목요일   금요일 "
                },
                {
                  "title": "1교시",
                  "description": HF_1
                },
                {
                  "title": "2교시",
                  "description": HF_2
                },
                {
                  "title": "3교시",
                  "description": HF_3
                },
                {
                  "title": "4교시",
                  "description": HF_4
                }
              ],
              "itemListAlignment": "left"
            }
          ]
        }
      }
    ]
  }
}
	except:
		responsebody = {
  "version": "2.0",
  "template": {
	"outputs": [
	  {
		"textCard": {
		  "title": "오류 발생",
		  "description": "오류 발생, 정보를 입력하고 싶다면 \'입력\' 버튼을, 급식이나 시간표를 조회하시려면 \'오늘 급식 뭐임?\' 또는 \'오늘 시간표 뭐임?\' 버튼을 눌러주세요.",
		"buttons": [
			{
			  "action": "block",
			  "label": "재입력",
			  "blockId" : "66486e1826296c3bea93d1c0"
			},
			{
			  "action": "block",
			  "label": "오늘 급식 뭐임?",
			  "blockId" : "65f6ee3a58611458d29a92c2"
			},
			{
			  "action": "block",
			  "label": "오늘 시간표 뭐임?",
			  "blockId" : "65fa21294fc74f623ccfa55a"
			}
		]
		}
		  
	  }
	]
  }
}
	return responseBody

@app.route('/newtimetable', methods = ["POST"])
def newtimetable():
	starttime = datetime.utcnow().timestamp()
	body = request.get_json()
	userID = body['userRequest']['user']['id'] # ID 조회
	print(userID)
	try:
		UserData = UserIdData.all(formula=match({"userID": userID, "Educode": '-', "schoolcode": '-', "schooltype":'-', "schoolname": '-', "gradecode": '-', "classcode": '-'}, match_any=True))
		if UserData == 0 or UserData == "false" or UserData == "" or UserData == "NaN" or UserData == []:
			print("Can't Search Data")
			raise Exception("Can't Search Data")
		else:
			
			Educode = UserData[0]['fields']['Educode']
			schoolcode = UserData[0]['fields']['schoolcode']
			schooltype = UserData[0]['fields']['schooltype']
			schoolname = UserData[0]['fields']['schoolname']
			gradecode = UserData[0]['fields']['gradecode']
			classcode = UserData[0]['fields']['classcode']
			print("Loading userinfo")
			
			timetabledict = {'M1':'　　　　','M2':'　　　　','M3':'　　　　','M4':'　　　　','M5':'　　　　','M6':'　　　　','M7':'　　　　','T1':'　　　　','T2':'　　　　','T3':'　　　　','T4':'　　　　','T5':'　　　　','T6':'　　　　','T7':'　　　　','W1':'　　　　','W2':'　　　　','W3':'　　　　','W4':'　　　　','W5':'　　　　','W6':'　　　　','W7':'　　　　','H1':'　　　　','H2':'　　　　','H3':'　　　　','H4':'　　　　','H5':'　　　　','H6':'　　　　','H7':'　　　　','F1':'　　　　','F2':'　　　　','F3':'　　　　','F4':'　　　　','F5':'　　　　','F6':'　　　　','F7':'　　　　'}

			Monday = timedelta(days=1-int(week))
			datetime_kst_M = datetime_kst + Monday
			day_M = datetime_kst_M.strftime("%Y%m%d")

			Tuesday = timedelta(days=2-int(week))
			datetime_kst_T = datetime_kst + Tuesday
			day_T = datetime_kst_T.strftime("%Y%m%d")

			Wednesday = timedelta(days=3-int(week))
			datetime_kst_W = datetime_kst + Wednesday
			day_W = datetime_kst_W.strftime("%Y%m%d")

			Thursday = timedelta(days=4-int(week))
			datetime_kst_H = datetime_kst + Thursday
			day_H = datetime_kst_H.strftime("%Y%m%d")
		
			Friday = timedelta(days=5-int(week))
			datetime_kst_F = datetime_kst + Friday
			day_F = datetime_kst_F.strftime("%Y%m%d")

			print("weekdays are available")
			
			Weeklist = {day_M:'M', day_T:'T', day_W:'W', day_H:'H', day_F:'F'}
			timetablelink = 'https://open.neis.go.kr/hub/'+schooltype+'Timetable'
			
			params = {
			'KEY' : NEIS_Key,
			'Type' : 'json',
			'pIndex' : '1',
			'pSize' : '100',
			'ATPT_OFCDC_SC_CODE' : Educode,
			'SD_SCHUL_CODE' : schoolcode,
			'AY' : '2024',
			'SEM' : '1',
			'GRADE' : gradecode,
			'CLASS_NM' : classcode,
			'TI_FROM_YMD' : day_M,
			'TI_TO_YMD' : day_F
			}
			
			response = requests.get(timetablelink, params=params)
			contentstext = response.text
			contents = response.json()
			print("load succesful")
			
			find = contentstext.find('해당하는 데이터가 없습니다.')
			
			if find == -1:
				contentslist = contents[schooltype+'Timetable'][1]['row']
				for a in contentslist:
					Weekday = a['ALL_TI_YMD']
					Weekdayfind = Weeklist[Weekday]
					class_time = Weekdayfind + a['PERIO']
					unpure_subject = a['ITRT_CNTNT']
					unpure_subject_list = list(unpure_subject)
					dellist = []
					for x in range(0, len(unpure_subject_list)):
						if unpure_subject_list[x] == "와" or unpure_subject_list[x] == "과":
							if unpure_subject_list[x+1] == " ":
								dellist.append(x)
								dellist.append(x+1)
					dellist_r = reversed(dellist)
					print(dellist_r)
					for y in dellist_r:
						del unpure_subject_list[y]
					for x in range(0, len(unpure_subject_list)):
						if unpure_subject_list[x] == "(" or unpure_subject_list[x] == ")" or unpure_subject_list[x] == "[" or unpure_subject_list[x] == "]" or unpure_subject_list[x] == " ":
							dellist.append(x)
					dellist_r = reversed(dellist)
					print(dellist_r)
					for y in dellist_r:
						del unpure_subject_list[y]
					print(unpure_subject_list)
					if len(unpure_subject_list) > 4:
						for y in range(0, len(unpure_subject_list)-4):
							del unpure_subject_list[4]
					if len(unpure_subject_list) == 2:
						unpure_subject_list.insert(-10,"　")
						unpure_subject_list.insert(10,"　")
					if len(unpure_subject_list) == 3:
						unpure_subject_list.insert(-10," ")
						unpure_subject_list.insert(10," ")
					
					print(unpure_subject_list)
					pured_subject = "".join(unpure_subject_list)
					print(class_time+" "+pured_subject)
					updatedict = {class_time : pured_subject}
					timetabledict.update(updatedict)
				
				MTW_1 = timetabledict['M1'] + " " + timetabledict['T1'] + " " + timetabledict['W1']
				MTW_2 = timetabledict['M2'] + " " + timetabledict['T2'] + " " + timetabledict['W2']
				MTW_3 = timetabledict['M3'] + " " + timetabledict['T3'] + " " + timetabledict['W3']
				MTW_4 = timetabledict['M4'] + " " + timetabledict['T4'] + " " + timetabledict['W4']
				MTW_567 = "5교시 " + timetabledict['M5'] + " " + timetabledict['T5'] + " " + timetabledict['W5'] + "\n6교시 " + timetabledict['M6'] + " " + timetabledict['T6'] + " " + timetabledict['W6'] + "\n7교시 " + timetabledict['M7'] + " " + timetabledict['T7'] + " " + timetabledict['W7']

				HF_1 = timetabledict['H1'] + " " + timetabledict['F1']
				HF_2 = timetabledict['H2'] + " " + timetabledict['F2']
				HF_3 = timetabledict['H3'] + " " + timetabledict['F3']
				HF_4 = timetabledict['H4'] + " " + timetabledict['F4']
				HF_567 = "5교시 " + timetabledict['H5'] + " " + timetabledict['F5'] + "\n" + timetabledict['H6'] + " " + timetabledict['F6'] + "\n7교시 " + timetabledict['F7'] + " " + timetabledict['F7']
				
				title = schoolname + " " + str(gradecode) + "학년 " + str(classcode) + "반 " + date + " NEIS 시간표"
				print("ready to response")
				responseBody = {
  "version": "2.0",
  "template": {
    "outputs": [
	    {
            "simpleText": {
                "text": title
            }
          },
      {
        "carousel": {
          "type": "itemCard",
          "items": [
            {
              "title": MTW_567,
              "itemList": [
                {
                  "title": "　요일",
                  "description": " 월요일   화요일   수요일 "
                },
                {
                  "title": "1교시",
                  "description": MTW_1
                },
                {
                  "title": "2교시",
                  "description": MTW_2
                },
                {
                  "title": "3교시",
                  "description": MTW_3
                },
                {
                  "title": "4교시",
                  "description": MTW_4
                }
              ],
              "itemListAlignment": "left"
            },
            {
              "title": HF_567,
              "itemList": [
                {
                  "title": "　요일",
                  "description": " 목요일   금요일 "
                },
                {
                  "title": "1교시",
                  "description": HF_1
                },
                {
                  "title": "2교시",
                  "description": HF_2
                },
                {
                  "title": "3교시",
                  "description": HF_3
                },
                {
                  "title": "4교시",
                  "description": HF_4
                }
              ],
              "itemListAlignment": "left"
            }
          ]
        }
      }
    ]
  }
}
				
	except:
		responseBody = {
  "version": "2.0",
  "template": {
	"outputs": [
	  {
		"textCard": {
		  "title": "오류 발생",
		  "description": "오류 발생, 정보를 입력하고 싶다면 \'입력\' 버튼을, 급식이나 시간표를 조회하시려면 \'오늘 급식 뭐임?\' 또는 \'오늘 시간표 뭐임?\' 버튼을 눌러주세요.",
		"buttons": [
			{
			  "action": "block",
			  "label": "재입력",
			  "blockId" : "66486e1826296c3bea93d1c0"
			},
			{
			  "action": "block",
			  "label": "오늘 급식 뭐임?",
			  "blockId" : "65f6ee3a58611458d29a92c2"
			},
			{
			  "action": "block",
			  "label": "오늘 시간표 뭐임?",
			  "blockId" : "65fa21294fc74f623ccfa55a"
			}
		]
		}
		  
	  }
	]
  }
}
	endtime = datetime.utcnow().timestamp()
	loadingtime = endtime - starttime
	print(str(loadingtime) + "s 소요")
	print(responseBody)
	return responseBody

@app.route('/meal', methods = ["POST"])
def meal():
	starttime = datetime.utcnow().timestamp()
	body = request.get_json()
	userID = body['userRequest']['user']['id'] # ID 조회
	print(userID)
	try:
		UserData = UserIdData.all(formula=match({"userID": userID, "Educode": '-', "schoolcode": '-', "schoolname": '-'}, match_any=True))
		if UserData == 0 or UserData == "false" or UserData == "" or UserData == "NaN" or UserData == []:
			print("Can't Search Data")
			raise Exception("Can't Search Data")
		else:
			Educode = UserData[0]['fields']['Educode']
			schoolcode = UserData[0]['fields']['schoolcode']
			schoolname = UserData[0]['fields']['schoolname']
			
			mealdict = {}
			output = []
			params = {
			'KEY' : NEIS_Key,
			'Type' : 'json',
			'pIndex' : '1',
			'pSize' : '100',
			'ATPT_OFCDC_SC_CODE' : Educode,
			'SD_SCHUL_CODE' : schoolcode,
			'MLSV_FROM_YMD' : day,
			'MLSV_TO_YMD' : day_2
			}
			
			response = requests.get(NEISmealurl, params=params)
			contentstext = response.text
			contents = response.json()
			
			find = contentstext.find('해당하는 데이터가 없습니다.')
			
			if find == -1:
				count = int(contents['mealServiceDietInfo'][0]['head'][0]['list_total_count'])
				for a in range(0, count):
					mealday = str(contents['mealServiceDietInfo'][1]['row'][a]['MLSV_YMD'])
					mealcontents = contents['mealServiceDietInfo'][1]['row'][a]['DDISH_NM']
					mealcontent = "\n".join(mealcontents.split('<br/>'))
					mealdict[mealday] = mealcontent
				mealdata = dict(sorted(mealdict.items()))
				for key, value in mealdata.items():
					keymonth = key[4:6]
					keyday = key[6:8]
					output.append({"title":keymonth + "월 " + keyday + "일" + " " + schoolname + " 급식", "description" : value})
						
			else:
				output = [{
		              "title": date + " " + schoolname + " 급식",
		              "description": "급식이 없어요!"
		           		 }]
				responseBody = {
	  			"version": "2.0",
	  			"template": {
	    			"outputs": [
	    			  {
	    				"carousel": {
	    				"type": "textCard",
	  			        "items": output
	  					}
	 			     }
	    						]
	  						}
				}
	except:
		print("Can't find info")
		responseBody = {
		"version": "2.0",
		"template": {
			"outputs": [
				{
					"textCard": {
		  				"title": date + " 시간표",
		  				"description": "먼저 사용자 등록을 통해 정보를 등록해 주세요! \n밑의 사용자 등록하기 메뉴를 통해 등록하거나 \'사용자 등록하기\'를 입력하세요." ,
		  				"buttons": [
			{
			  "action": "message",
			  "label": "사용자 등록하기",
			  "messageText": "사용자 등록하기"
			}
									]
								}
				}
						]
		}
	}
	
				
	endtime = datetime.utcnow().timestamp()
	loadingtime = endtime - starttime
	print(str(loadingtime) + "s 소요")
	print(responseBody)
	return responseBody
