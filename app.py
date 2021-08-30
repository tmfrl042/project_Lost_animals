from flask import Flask, render_template, jsonify, request
from bson.objectid import ObjectId
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://test:test@3.38.98.101', 27017)
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


# nav2-content
# API 역할을 하는 부분
@app.route('/dogs', methods=['GET'])
def view_abdogs():
    dogs_notice = list(db.dogs.find({"SPECIES_NM": {'$regex': '개'}}, {'_id': False}).limit(30))
    return jsonify({'dogs_notices': dogs_notice})


# nav3-content
@app.route('/blog', methods=['GET'])
def read_blogs():
    blogs = list(db.blogs.find({}, {'_id': False}))
    return jsonify({'blog_texts': blogs})


# nav4-content
# 적재된 후기를 DB에서 불러오는 부분
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


@app.route('/delete', methods=['POST'])
def delete():
    print("삭제진입")
    id = request.form['id_give']
    confirmPassword = request.form['confirmPassword_give']

    print(id)
    print(confirmPassword)

    data = db.reviews.find_one({'_id': ObjectId(id)})
    currentPassword = data['password']

    print(data)
    print(currentPassword)

    if currentPassword != confirmPassword:
        return jsonify({'msg': '비밀번호가 일치하지 않습니다. 다시 입력해주세요!'})
    else:
        db.reviews.delete_one({'_id': ObjectId(id)})
        return jsonify({'msg': '삭제되었습니다.'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True, use_reloader=False)
