		"label": "3반",
		"blockId": "65faa630d7cbb10c92facd52"
	  },
	{
		"messageText": "4반",
		"action": "block",
		"label": "4반",
		"blockId": "65faa630d7cbb10c92facd52"
	  },
	{
		"messageText": "5반",
		"action": "block",
		"label": "5반",
		"blockId": "65faa630d7cbb10c92facd52"
	  },
	{
		"messageText": "6반",
		"action": "block",
		"label": "6반",
		"blockId": "65faa630d7cbb10c92facd52"
	  },
	{
		"messageText": "7반",
		"action": "block",
		"label": "7반",
		"blockId": "65faa630d7cbb10c92facd52"
	  },
	{
		"messageText": "8반",
		"action": "block",
		"label": "8반",
		"blockId": "65faa630d7cbb10c92facd52"
	  },
	{
		"messageText": "9반",
		"action": "block",
		"label": "9반",
		"blockId": "65faa630d7cbb10c92facd52"
	  }
	  
	]
  }
}
	return responesebody

@app.route('/class1', methods = ['POST'])
def class1():
	body = request.get_json()
	userclass = body['userRequest']['utterance']
	userID = body['userRequest']['user']['id']
	useridtable = userIdData.all(formula=match({"userID":userID}))
	id1 = useridtable[0]['id']
	for a in userIdData.all():
		if id1 == a['id']:
			data = a['fields']
			uclass = userclass
			if userclass == "1반":
				userIdData.update(id1, {"classcode": 1})
			elif userclass == "2반":
				userIdData.update(id1, {"classcode": 2})
			elif userclass == "3반":
				userIdData.update(id1, {"classcode": 3})
			elif userclass == "4반":
				userIdData.update(id1, {"classcode": 4})
			elif userclass == "5반":
				userIdData.update(id1, {"classcode": 5})
			elif userclass == "6반":
				userIdData.update(id1, {"classcode": 6})
			elif userclass == "7반":
				userIdData.update(id1, {"classcode": 7})
			elif userclass == "8반":
				userIdData.update(id1, {"classcode": 8})
			elif userclass == "9반":
				userIdData.update(id1, {"classcode": 9})
			else:
				userIdData.update(id1, {"classcode": 0})

			if data['schoolcode'] == "S":
				uschool = "삼남중학교 "
			elif data['schoolcode'] == "E":
				uschool = "언양고등학교 "
			else:
				uschool = "지원하지 않는 학교 "
		
			if data['gradecode'] == "1":
				ugrade = "1학년 "
			elif data['gradecode'] == "2":
				ugrade = "2학년 "
			elif data['gradecode'] == "3":
				ugrade = "3학년 "
			else:
				ugrade = "지원하지 않는 학년 "
				
			description = str(uschool) + str(ugrade) + str(uclass)
			print(description)
	
			responesebody = {
  "version": "2.0",
  "template": {
	"outputs": [
	  {
		"textCard": {
		  "title": "입력한 정보가 맞는지 확인해 주세요",
		  "description": description,
		"buttons": [
			{
			  "action": "block",
			  "label": "맞아요!",
			  "blockId" : "65faaca1a64303558477aa63"
			},
			{
			  "action": "block",
			  "label": "아니에요",
			  "blockId" : "65faa5ef091618695a7fee9c"
			}
		]
		}
		  
	  }
	]
  }
}
			return responesebody
	

	except:
		responesebody = {
  "version": "2.0",
  "template": {
	"outputs": [
	  {
		"textCard": {
		  "title": "입력한 정보가 맞는지 확인해 주세요",
		  "description": "오류 발생, 아니에요 버튼을 눌러 다시 확인해 주세요",
		"buttons": [
			{
			  "action": "block",
			  "label": "맞아요!",
			  "blockId" : "65faaca1a64303558477aa63"
			},
			{
			  "action": "block",
			  "label": "아니에요",
			  "blockId" : "65faa5ef091618695a7fee9c"
			}
		]
		}
		  
	  }
	]
  }
}
	
	
		return responesebody

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
			  "label": "오늘 급식 뭐임?"
			},
			{
			  "action": "message",
			  "label": "오늘 시간표 뭐임?"
			}
		]
		}
		  
	  }
	]
  }
}
	return responesebody
