import requests
from bs4 import BeautifulSoup
import xmltodict
import json
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.animalLost

db.bohocenter.remove({})

# 내가 받은 인증키
mykey = "63b2c36d704e439dbcb63c3368650bb9"
# 요청주소
url_base = "https://openapi.gg.go.kr/AbdmAnimalProtect?pSize=1000&KEY="
mid_url = url_base + mykey

animalList = []
countAll = 0
cotinueCount = 0

#최대 페이지 몇인지 확인
pageNum = 1
while True:
    url = mid_url + "&pIndex=" + str(pageNum)
    req = requests.get(url).text
    xml_parse = xmltodict.parse(req)
    jsonDict = json.loads(json.dumps(xml_parse))
    if not "AbdmAnimalProtect" in jsonDict:
        #print("Page가 없어! 마지막 페이지 : " + str(pageNum-1))
        break
    pageNum += pageNum

# 한번에 가져올수 있는 api 데이터가 최대 1000개여서 페이지 돌면서 1000개씩 가져오기
for i in range(1, pageNum-2):
    url = mid_url + "&pIndex="+ str(i)
    # 주소받아와서 xml부분 가져오기
    req = requests.get(url).text

    # xml 파싱 후 json으로
    xml_parse = xmltodict.parse(req)
    jsonDict = json.loads(json.dumps(xml_parse))

   #키 있는지 확인
    if not "AbdmAnimalProtect" in jsonDict:
        # print("Key가 없어!")
        break

    # 수많이 키중에서 시군,보호소명,주소,전화번호만 가져와서 중복없이 추가하기
    length = len(jsonDict['AbdmAnimalProtect']['row'])
    for m in range(0,length) :
        sido = "경기도"
        sigun = jsonDict['AbdmAnimalProtect']['row'][m].get('SIGUN_NM')
        name = jsonDict['AbdmAnimalProtect']['row'][m].get('SHTER_NM')
        add= jsonDict['AbdmAnimalProtect']['row'][m].get('PROTECT_PLC')
        telno = jsonDict['AbdmAnimalProtect']['row'][m].get('SHTER_TELNO')
        centerDict = dict(SIDO_NM=sido, SIGUN_NM=sigun, SHTER_NM=name,PROTECT_PLC=add,SHTER_TELNO=telno)
        countAll += 1
        if not name in animalList:
            animalList.append(name)
            db.bohocenter.insert_one(centerDict)

    print(str(i)+"페이지db에저장성공")

# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')

# API 역할을 하는 부분
@app.route('/center', methods=['GET'])
def view_center():
    bohocenter = list(db.bohocenter.find({}, {'_id': False}))
    return jsonify({'bohocenters': bohocenter})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True, use_reloader=False)
