from pymongo import MongoClient
import requests
import xmltodict
import json
from selenium import webdriver

import time
from bs4 import BeautifulSoup


client = MongoClient('localhost', 27017)
# client = MongoClient('mongodb://test:test@localhost', 27017)
db = client.animalLost


# app1.py & app2.py & app3.py

db.bohocenter.remove({})
db.dogs.remove({})
db.blogs.remove({})

# 블로그 크롤러 함수
def blog_crawler():
    # 브라우져 오픈
    # chromedriver = "C:/LSW/PYDATAexam/Webdriver/chromedriver"
    chromedriver = "C:/chromedriver/chromedriver.exe"
    # chromedriver = "/home/ubuntu/chromedriver"
    driver = webdriver.Chrome(chromedriver)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

    # 크롤링할 데이터를 저장할 리스트를 미리 만들어 두었습니다.
    url_list = []
    title_list = []
    writer_list = []
    blogname_list = []
    content_list = []
    date_list = []
    img_url_list = []
    index_list = list(range(0, len(title_list)))

    # 원하는 검색어를 이용하면 원하는 내용의 블로그 검색이 가능합니다.
    text = "유기견  센터"

    for i in range(1, 3):  # 1~(n-1)페이지까지의 블로그 내용을 읽어옴
        url = 'https://section.blog.naver.com/Search/Post.nhn?pageNo=' + str(
            i) + '&rangeType=ALL&orderBy=sim&keyword=' + text
        driver.get(url)
        time.sleep(1)
        # 한 페이지당 7개의 블로그 창이 뜨기때문에 페이지마다 7개의 데이터를 크롤링 해옵니다.
        for j in range(0, 7):
            # 블로그에 적은 글의 주소가 저장된 위치를 찾고 리스트에 저장합니다.
            links = driver.find_elements_by_css_selector(
                "#content > section > div.area_list_search > div > div > div.info_post > div.desc > a.desc_inner")
            link = links[j].get_attribute('href')
            url_list.append(link)

            # 블로그에 글쓴 사람의 닉네임의 위치를 찾고 리스트에 저장합니다.
            writers = driver.find_elements_by_css_selector(
                "#content > section > div.area_list_search > div > div > div.info_post > div.writer_info")
            writer = writers[j].find_element_by_css_selector('em').text
            writer_list.append(writer)

            # 블로그의 이름을 뽑아내고, 리스트에 저장합니다.
            blog_name = writers[j].find_element_by_css_selector('span').text
            blogname_list.append(blog_name)

            # 글쓴 날짜를 뽑아내고, 리스트에 저장합니다.
            write_date = writers[j].find_element_by_css_selector('.date').text
            date_list.append(write_date)

            # 블로그에 글의 제목의 위치를 찾습니다. 리스트에 저장합니다.
            titles = driver.find_elements_by_css_selector(
                "#content > section > div.area_list_search > div > div > div.info_post > div.desc > a.desc_inner > strong > span")
            title = titles[j].text
            title_list.append(title)

            # 블로그의 이미지 url의 위치를 찾고 저장합니다.
            # img_links=driver.find_elements_by_css_selector("#content > section > div.area_list_search > div > div > div.thumbnail_post > div > a.thumbnail_inner > img")
            # img_link=img_links[j].get_attribute('src')
            # img_url_list.append(img_link)

    # 상황에 따라 길어질 수 있으므로 수집이 끝나면 알 수 있도록 이를 출력해 줍니다.
    print("url 수집 끝, 해당 url 데이터 크롤링")

    text2 = "유기견 강아지"
    driver.get("https://search.naver.com/search.naver?sm=tab_hty.top&where=image&query=" + text2)  # 여기에 URL을 넣어주세요
    time.sleep(3)

    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    thumbnails = soup.select('div > div.thumb > a > img')

    for thumbnail in thumbnails[0:len(title_list)]:
        img = thumbnail['src']
        img_url_list.append(img)
        time.sleep(0.1)
    # 수집한 url마다 들어갑니다.
    for url in url_list:  # 수집한 url 만큼 반복
        driver.get(url)  # 해당 url로 이동
        driver.switch_to.frame('mainFrame')  # 찾아봐도 이해가 안되는 내용, 그냥 크롤링이 불가능 하므로 id가 mainframe인 창으로 이동하고
        # 본문의 내용을 찾아서
        overlays = ".se-main-container"
        contents = driver.find_elements_by_css_selector(overlays)
        # 리스트에 저장합니다.
        content_list.append(contents[0].text.replace("\n", " "))
        time.sleep(0.1)
    # 상황에 따라 길어질 수 있으므로 수집이 끝나면 알 수 있도록 이를 출력해 줍니다.
    print("본문 내용 수집이 완료되었습니다.")

    # MONGO DB에 저장합니다.
    client = MongoClient('localhost', 27017)
    # 이름이 db_animal인 DB를 이용합니다 없다면 만듭니다.
    db = client.animalLost
    for i in list(range(0, len(title_list))):
        doc = {'title': title_list[i], 'url': url_list[i], 'writer': writer_list[i], 'content': content_list[i],
               'date': date_list[i], 'img_url': img_url_list[i]}
        db.blogs.insert_one(doc)  # blogs라는 collections에 데이터들을 저장합니다. 끝!

    # MONGO DB에 저장합니다.
    client = MongoClient('localhost', 27017)
    # 이름이 db_animal인 DB를 이용합니다 없다면 만듭니다.
    db = client.animalLost
    for i in list(range(0, len(title_list))):
        doc = {'title': title_list[i], 'url': url_list[i], 'writer': writer_list[i], 'content': content_list[i],
               'date': date_list[i], 'img_url': img_url_list[i]}
        db.blogs.insert_one(doc)  # blogs라는 collections에 데이터들을 저장합니다. 끝!


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


#함수를 실행합니다. 
blog_crawler();