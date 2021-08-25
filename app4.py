from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbpearl

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html')

## 적재된 후기를 DB에서 불러오는 부분
@app.route('/review', methods=['GET'])
def listing():
    reviews = list(db.reviews.find({}, {'_id': False}))
    return jsonify({'all_reviews': reviews})

## 후기작성 후 등록버튼 클릭시 DB에 정보저장하는 부분
@app.route('/review', methods=['POST'])
def saving():
    nickname_receive = request.form['nickname_give']
    title_receive = request.form['title_give']
    comment_receive = request.form['comment_give']
    password_receive = requests.form['password_give']

    doc = {
        'nickname': nickname_receive,
        'title': title_receive,
        'comment': comment_receive,
        'password': password_receive
    }
    db.reviews.insert_one(doc)

    return jsonify({'msg':'후기가 등록완료되었습니다.'})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)