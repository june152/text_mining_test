# 정적 페이지
import requests as req
from bs4 import BeautifulSoup as bs
# 동적 페이지
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
# 시간 지연 모듈
import time
# json 모듈
import json

# 블로그 검색 url 베이스
url = 'https://search.naver.com/search.naver?ssc=tab.blog.all&sm=tab_jum&query='

# 키워드 입력
userInput = input("검색 키워드 입력 : ")
url += userInput

# 크롬 드라이버 실행
driver = webdriver.Chrome()
# 액션체인 생성
action = ActionChains(driver)
# url 입력
driver.get(url)
time.sleep(0.5)
# 다음 리스트 컴포넌트
moreDiv = driver.find_element(By.CSS_SELECTOR, '.mod_more_wrap2')
while 1:
    if moreDiv.get_attribute('style') == 'display: block;' :
        action.move_to_element(moreDiv).perform()
    else :
        break
    time.sleep(0.1)

# 검색결과 스크롤
ulComponent = driver.find_element(By.CSS_SELECTOR, '.lst_view')
# li 목록 추출
liList = ulComponent.find_elements(By.CSS_SELECTOR, '.bx')
# 초기 list size
listSize = len(liList)

# 네이버 블로그 베이스 url
blogBase = 'https://blog.naver.com'

contentText = ''

for i in range(0, listSize) :
    # li 중 style none 타입 제외
    if liList[i].get_attribute('style') == 'display: none;' :
        continue
    # 링크를 담은 컴포넌트 추출
    postComponent = liList[i].find_element(By.CSS_SELECTOR, '.title_link')
    # 포스트 링크
    postUrl = postComponent.get_attribute('href')
    # 네이버 블로그가 아닌 경우 스킵
    if 'naver' not in postUrl :
        continue
    # bs로 해당 링크 요청
    res = req.get(postUrl)
    html_text = res.text
    html = bs(html_text, 'html.parser')
    # i프레임 정보 추출
    iframe = html.find('iframe')
    # iframe이 None인 경우
    if iframe is None :
        continue
    # i프레임 src 추출
    iframeUrl = iframe.attrs['src']
    # 실제 포스터 요청
    postRes = req.get(blogBase + iframeUrl)
    post_text = postRes.text
    # 실제 포스터 파싱
    postContent = bs(post_text, 'html.parser')
    # 메인 컨텐츠 컴포넌트 추출
    mainContainer = postContent.find(class_='se-main-container')
    # 별개 형식인 경우 스킵
    if mainContainer is None:
        continue
    # 텍스트 컴포넌트 리스트
    textCompList = mainContainer.find_all(class_='se-text-paragraph')
    # 별개 형식인 경우 스킵
    if textCompList is None:
        continue
    # 텍스트 붙이기
    for tComp in textCompList :
        contentText += tComp.get_text()
    print(str(i+1), "번째 포스트 내용 추출 중...")

savePath = './exported/' + userInput + '.json'
textData = {
        "content" : contentText
    }
# 아스키 비활성화
jsonData = json.dumps(textData, ensure_ascii=False)
# 유니코드 표현불가문자 제거
jsonData = jsonData.replace("\u200b", "")
# utf-8로 인코딩
with open(savePath, 'w', encoding="utf-8") as json_file:
    json_file.write(jsonData)

time.sleep(1)

print(userInput, "키워드 결과 추출완료")