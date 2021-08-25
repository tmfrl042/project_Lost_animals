from flask import Flask, render_template, jsonify, request
app = Flask(__name__)
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbpearl


## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index4.html')


## 적재된 후기를 DB에서 불러오는 부분
@app.route('/review', methods=['GET'])
def getReview():
    data = list(db.reviews.find({}))
    resData =[]
    for d in data:
        idx = d['_id']

        nickname = d['nickname']
        title = d['title']
        comment = d['comment']
        password = d['password']

        dset={"id": str(idx),
              "nickname":nickname,
              "title":title,
              "comment":comment,
              "password":password\
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

    return jsonify({'msg':'후기가 등록완료되었습니다.'})


# 후기작성 후 등록버튼 클릭시 DB에 정보저장하는 부분
@app.route('/update', methods=['POST'])
def update():
    print(request.form)
    id = request.form['id_give']
    password = request.form['password_give']
    # data = db.reviews.find_one({'_id': id})
    print(id)
    print(password)
    # if password == data['password']:
    #     # db.reviews.update_one({'name': name_receive}, {'$set': {'like': new_like}})
    #     return jsonify({'msg': '성공!'})
    return jsonify({'msg': '실패!'})



if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)