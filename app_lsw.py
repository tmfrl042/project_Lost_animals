import requests
from bs4 import BeautifulSoup
import json
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.db_animal

# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index_lswf.html')

# API 역할을 하는 부분
@app.route('/blog', methods=['GET'])
def read_blogs():
    blogs=list(db.blogs.find({},{'_id':False}))
    return jsonify({'blog_texts': blogs})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True, use_reloader=False)
