from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request
# import requests
# from bs4 import BeautifulSoup
# import xmltodict
# import json
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time
# from bs4 import BeautifulSoup
# import sys
# import os
# import pandas as pd
# import numpy as np

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


# app1.py & app2.py
"""
db.bohocenter.remove({})
db.dogs.remove({})

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
        image = jsonDict['AbdmAnimalProtect']['row'][m].get('IMAGE_COURS')
        number = jsonDict['AbdmAnimalProtect']['row'][m].get('PBLANC_IDNTFY_NO')
        breed = jsonDict['AbdmAnimalProtect']['row'][m].get('SPECIES_NM')
        weight = jsonDict['AbdmAnimalProtect']['row'][m].get('BDWGH_INFO')
        discovery = jsonDict['AbdmAnimalProtect']['row'][m].get('DISCVRY_PLC_INFO')
        start = jsonDict['AbdmAnimalProtect']['row'][m].get('PBLANC_BEGIN_DE')
        end = jsonDict['AbdmAnimalProtect']['row'][m].get('PBLANC_END_DE')
        centerDict = dict(SIDO_NM=sido, SIGUN_NM=sigun, SHTER_NM=name,PROTECT_PLC=add,SHTER_TELNO=telno)
        dogsDict = dict(IMAGE_COURS=image, PBLANC_IDNTFY_NO=number, SPECIES_NM=breed, BDWGH_INFO=weight, DISCVRY_PLC_INFO=discovery, PBLANC_BEGIN_DE=start, PBLANC_END_DE=end)

        countAll += 1
        if not name in animalList:
            animalList.append(name)
            db.bohocenter.insert_one(centerDict)

        if not number in animalList:
            animalList.append(number)
            db.dogs.insert_one(dogsDict)
    print(str(i)+"페이지db에저장성공")
"""
# app3.py
"""
chromedriver="C:/LSW/PYDATAexam/Webdriver/chromedriver"
driver=webdriver.Chrome(chromedriver)
url_list = []
title_list = []
writer_list = []
blogname_list=[]
content_list = []
date_list=[]
text = "유기견 보호소"

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

for i in range(1, 3):  # 1~2페이지까지의 블로그 내용을 읽어옴
    url = 'https://section.blog.naver.com/Search/Post.nhn?pageNo='+ str(i) + '&rangeType=ALL&orderBy=sim&keyword=' + text
    driver.get(url)
    time.sleep(1)
    for j in range(0, 7): # 각 블로그 주소 저장
        links=driver.find_elements_by_css_selector("#content > section > div.area_list_search > div > div > div.info_post > div.desc > a.desc_inner")
        writers=driver.find_elements_by_css_selector("#content > section > div.area_list_search > div > div > div.info_post > div.writer_info")
        titles=driver.find_elements_by_css_selector("#content > section > div.area_list_search > div > div > div.info_post > div.desc > a.desc_inner > strong > span")

        link = links[j].get_attribute('href')
        url_list.append(link)
        title=titles[j].text
        title_list.append(title)
        writer=writers[j].find_element_by_css_selector('em').text
        writer_list.append(writer)
        blog_name=writers[j].find_element_by_css_selector('span').text
        blogname_list.append(blog_name)
        write_date=writers[j].find_element_by_css_selector('.date').text
        date_list.append(write_date)
#print(len(url_list))
print("url 수집 끝, 해당 url 데이터 크롤링")

for url in url_list: # 수집한 url 만큼 반복
    driver.get(url) # 해당 url로 이동

    driver.switch_to.frame('mainFrame')
    overlays = ".se-main-container" # 내용 크롤링

    contents = driver.find_elements_by_css_selector(overlays)
    content_list.append(contents[0].text.replace("\n"," "))

df1 = pd.DataFrame({'index':list[],'title': title_list,'writer': writer_list, 'content': content_list,'date':date_list})
print(df1)    


k=list(range(1,len(title_list)+1))
print(k)


# CSV파일로 저장하기
df1.to_csv("test_db.csv",index=False,encoding="utf-8-sig")
# CSV파일 읽기
df1 = pd.read_csv("test.csv")

"""

# nav2-content
# API 역할을 하는 부분
@app.route('/dogs', methods=['GET'])
def view_abdogs():
    dogs_notice = list(db.dogs.find({"SPECIES_NM": {'$regex': '개'}}, {'_id': False}).limit(10))
    return jsonify({'dogs_notices': dogs_notice})


# nav3-content
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
