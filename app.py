import requests
from bs4 import BeautifulSoup
import xmltodict
import json
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.animalLost


# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')


# nav1-content
# API 역할을 하는 부분
@app.route('/center', methods=['GET'])
def view_center():
    bohocenter = list(db.bohocenter.find({}, {'_id': False}))
    return jsonify({'bohocenters': bohocenter})


db.bohocenter.remove({})

# # 내가 받은 인증키
# mykey = "63b2c36d704e439dbcb63c3368650bb9"
# # 요청주소
# url_base = "https://openapi.gg.go.kr/AbdmAnimalProtect?pSize=1000&KEY="
# mid_url = url_base + mykey
#
# animalList = []
# countAll = 0
# cotinueCount = 0
#
# # 최대 페이지 몇인지 확인
# pageNum = 1
# while True:
#     url = mid_url + "&pIndex=" + str(pageNum)
#     req = requests.get(url).text
#     xml_parse = xmltodict.parse(req)
#     jsonDict = json.loads(json.dumps(xml_parse))
#     if not "AbdmAnimalProtect" in jsonDict:
#         # print("Page가 없어! 마지막 페이지 : " + str(pageNum-1))
#         break
#     pageNum += pageNum
#
# # 한번에 가져올수 있는 api 데이터가 최대 1000개여서 페이지 돌면서 1000개씩 가져오기
# for i in range(1, pageNum - 2):
#     url = mid_url + "&pIndex=" + str(i)
#     # 주소받아와서 xml부분 가져오기
#     req = requests.get(url).text
#
#     # xml 파싱 후 json으로
#     xml_parse = xmltodict.parse(req)
#     jsonDict = json.loads(json.dumps(xml_parse))
#
#     # 키 있는지 확인
#     if not "AbdmAnimalProtect" in jsonDict:
#         # print("Key가 없어!")
#         break
#
#     # 수많이 키중에서 시군,보호소명,주소,전화번호만 가져와서 중복없이 추가하기
#     length = len(jsonDict['AbdmAnimalProtect']['row'])
#     for m in range(0, length):
#         sido = "경기도"
#         sigun = jsonDict['AbdmAnimalProtect']['row'][m].get('SIGUN_NM')
#         name = jsonDict['AbdmAnimalProtect']['row'][m].get('SHTER_NM')
#         add = jsonDict['AbdmAnimalProtect']['row'][m].get('PROTECT_PLC')
#         telno = jsonDict['AbdmAnimalProtect']['row'][m].get('SHTER_TELNO')
#         centerDict = dict(SIDO_NM=sido, SIGUN_NM=sigun, SHTER_NM=name, PROTECT_PLC=add, SHTER_TELNO=telno)
#         countAll += 1
#         if not name in animalList:
#             animalList.append(name)
#             db.bohocenter.insert_one(centerDict)
#
#     print(str(i) + "페이지db에저장성공")
#

# nav2-content
# API 역할을 하는 부분
@app.route('/dogs', methods=['GET'])
def view_abdogs():
    dogs_notice = list(db.dogs.find({"SPECIES_NM": {'$regex': '개'}}, {'_id': False}))
    return jsonify({'dogs_notices': dogs_notice})


# # 내가 받은 인증키
# mykey = "20a3a80ca32b4e62b4bd4c2f8ffe7e23"
# # 요청주소
# url_base = "https://openapi.gg.go.kr/AbdmAnimalProtect?pSize=1000&KEY="
# mid_url = url_base + mykey
# animalList = []
# countAll = 0
# cotinueCount = 0
# # 최대 페이지 몇인지 확인
# pageNum = 1
# while True:
#     url = mid_url + "&pIndex=" + str(pageNum)
#     req = requests.get(url).text
#     xml_parse = xmltodict.parse(req)
#     jsonDict = json.loads(json.dumps(xml_parse))
#     if not "AbdmAnimalProtect" in jsonDict:
#         # print("Page가 없어! 마지막 페이지 : " + str(pageNum-1))
#         break
#     pageNum += pageNum
# # 1페이지만 가져옴 (한번에 가져올수 있는 api 데이터가 최대 1000개)
# for i in range(1, 2):
#     url = mid_url + "&pIndex=" + str(i)
#     # 주소받아와서 xml부분 가져오기
#     req = requests.get(url).text
#     # xml 파싱 후 json으로
#     xml_parse = xmltodict.parse(req)
#     jsonDict = json.loads(json.dumps(xml_parse))
#     # 키 있는지 확인
#     if not "AbdmAnimalProtect" in jsonDict:
#         # print("Key가 없어!")
#         break
#     # 수많은 키중에서 이미지경로,공고고유번호,품종,체중,발견장소,공고시작일자,종료일자만 가져와서 중복없이 추가하기
#     length = len(jsonDict['AbdmAnimalProtect']['row'])
#     for m in range(0, length):
#         image = jsonDict['AbdmAnimalProtect']['row'][m].get('IMAGE_COURS')
#         number = jsonDict['AbdmAnimalProtect']['row'][m].get('PBLANC_IDNTFY_NO')
#         breed = jsonDict['AbdmAnimalProtect']['row'][m].get('SPECIES_NM')
#         weight = jsonDict['AbdmAnimalProtect']['row'][m].get('BDWGH_INFO')
#         discovery = jsonDict['AbdmAnimalProtect']['row'][m].get('DISCVRY_PLC_INFO')
#         start = jsonDict['AbdmAnimalProtect']['row'][m].get('PBLANC_BEGIN_DE')
#         end = jsonDict['AbdmAnimalProtect']['row'][m].get('PBLANC_END_DE')
#         dogsDict = dict(IMAGE_COURS=image, PBLANC_IDNTFY_NO=number, SPECIES_NM=breed, BDWGH_INFO=weight,
#                         DISCVRY_PLC_INFO=discovery, PBLANC_BEGIN_DE=start, PBLANC_END_DE=end)
#         countAll += 1
#         if not number in animalList:
#             animalList.append(number)
#             db.dogs.insert_one(dogsDict)
#     print(str(i) + "페이지db에저장성공")


# nav3-content
# API 역할을 하는 부분
@app.route('/blog', methods=['GET'])
def read_blogs():
    blogs=list(db.blogs.find({},{'_id':False}))
    return jsonify({'blog_texts': blogs})

# nav4-content
## 적재된 후기를 DB에서 불러오는 부분
@app.route('/review', methods=['GET'])
def getReview():
    data = list(db.reviews.find({}))
    resData = []
    for d in data:
        idx = d['_id']

        nickname = d['nickname']
        title = d['title']
        comment = d['comment']
        password = d['password']

        dset = {
            'id': str(idx),
            'nickname': nickname,
            'title': title,
            'comment': comment,
            'password': password,
        }
        resData.append(dset)

    return jsonify({'all_reviews': resData})


# 후기작성 후 등록버튼 클릭시 DB에 정보저장하는 부분
@app.route('/review', methods=['POST'])
def saving():
    nickname_receive = request.form['nickname_give']
    title_receive = request.form['title_give']
    comment_receive = request.form['comment_give']
    password_receive = request.form['password_give']

    doc = {
        'nickname': nickname_receive,
        'title': title_receive,
        'comment': comment_receive,
        'password': password_receive
    }
    db.reviews.insert_one(doc)

    return jsonify({'msg': '후기가 등록완료되었습니다.'})


# 후기 수정, 삭제 버튼 클릭 시 DB저장된 ID와 입력한 아이디가 같으면 update, delete 하는 부분
@app.route('/update', methods=['POST'])
def update():
    print(request.form)
    id = request.form['id_give']
    confirmPassword = request.form['confirmPassword_give']
    # data = db.reviews.find_one({'_id': id})
    print(id)
    print(confirmPassword)
    # if confirmPassword == data['password']:
    #     db.reviews.update_one({'nickname': nickname_receive}, {'$set': {'like': new_like}})
    #     return jsonify({'msg': '성공!'})
    return jsonify({'msg': '실패!'})


# @app.route('/delete', methods=['POST'])
# def delete():
#     print(request.form)
#     id = request.form['id_give']
#     password = request.form['password_give']
#     # data = db.reviews.find_one({'_id': id})
#     print(id)
#     print(password)
#     # if password == data['password']:
#     #     # db.reviews.update_one({'name': name_receive}, {'$set': {'like': new_like}})
#     #     return jsonify({'msg': '성공!'})
#     return jsonify({'msg': '실패!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True, use_reloader=False)
