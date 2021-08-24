import requests
from bs4 import BeautifulSoup
import xmltodict
import json
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request



app = Flask(__name__)


client = MongoClient('localhost', 27017)
db = client.db15challenge

# dogs_notice = list(db.dogs.find({"SPECIES_NM": {'$regex':'개'}}, {'_id': False}))
# print(dogs_notice)
#

# db.dogs.drop()

# 내가 받은 인증키
mykey = "20a3a80ca32b4e62b4bd4c2f8ffe7e23"
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
# 1페이지만 가져옴 (한번에 가져올수 있는 api 데이터가 최대 1000개)
for i in range(1, 2):
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
    # 수많은 키중에서 이미지경로,공고고유번호,품종,체중,발견장소,공고시작일자,종료일자만 가져와서 중복없이 추가하기
    length = len(jsonDict['AbdmAnimalProtect']['row'])
    for m in range(0,length) :
        image = jsonDict['AbdmAnimalProtect']['row'][m].get('IMAGE_COURS')
        number = jsonDict['AbdmAnimalProtect']['row'][m].get('PBLANC_IDNTFY_NO')
        breed = jsonDict['AbdmAnimalProtect']['row'][m].get('SPECIES_NM')
        weight = jsonDict['AbdmAnimalProtect']['row'][m].get('BDWGH_INFO')
        discovery = jsonDict['AbdmAnimalProtect']['row'][m].get('DISCVRY_PLC_INFO')
        start = jsonDict['AbdmAnimalProtect']['row'][m].get('PBLANC_BEGIN_DE')
        end = jsonDict['AbdmAnimalProtect']['row'][m].get('PBLANC_END_DE')
        dogsDict = dict(IMAGE_COURS=image, PBLANC_IDNTFY_NO=number, SPECIES_NM=breed, BDWGH_INFO=weight, DISCVRY_PLC_INFO=discovery, PBLANC_BEGIN_DE=start, PBLANC_END_DE=end)
        countAll += 1
        if not number in animalList:
            animalList.append(number)
            db.dogs.insert_one(dogsDict)
    print(str(i)+"페이지db에저장성공")

# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index2.html')

# API 역할을 하는 부분
@app.route('/dogs', methods=['GET'])
def view_abdogs():
    dogs_notice = list(db.dogs.find({"SPECIES_NM": {'$regex':'개'}}, {'_id': False}))
    return jsonify({'dogs_notices': dogs_notice})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True, use_reloader=False)