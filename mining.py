from collections import Counter
import json
from konlpy.tag import Okt
from wordcloud import WordCloud
from PIL import Image
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import nltk

userInput = input("추출된 키워드 데이터 입력 : ")

# 경로
filePath = "./exported/" + userInput + ".json"

data = {}

# 파일 읽기
try:
    with open(filePath, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        
        # print(data["content"])
        
        # 토큰화 모듈
        tokenizer = Okt()
        raw_pos_tagged = tokenizer.pos(data["content"], norm=True, stem=True)
        # print(raw_pos_tagged)
        
        delList = ['를', '이', '은', '는', '있다', '하다', '에', '되다', '보다', '좋다', '오다', '정말', '그냥', '오늘', '이다', '지금', '많다', '적다', '먹다', '자다', '받다', '말다'
                   , '없다', '있다', '가다', '그렇다', '싶다', '들어가다', '나오다', '많이', '또한', '편하다', '후기', '도움', '해주다', '경우', '하지만', '요즘', '잦다', '찾다', '가장'
                   , '대해', '정도', '생각', '필요하다', '중요하다', '피곤하다', '아니다', '맞다', '모두', '없이', '방법', '담다', '바로', '높다', '낮다', '다양하다', '우리', '이제'
                   , '그리고', '그런데', '그러나', '않다', '그래서', '챙기다', '고르다', '시키다', '괜찮다', '드리다', '마시다', '알아보다', '다른', '이렇게', '힘들다', '일어나다', '걱정'
                   , '나타나다', '느끼다', '어렵다', '때문', '들다', '사실', '지치다', '평소', '간편하다', '이야기', '꾸준하다', '이번', '같다', '어떻다', '살펴보다', '알다', '불리다'
                   , '자주', '피로하다', '마시다', '돼다', '건강하다', '미리', '되어다', '위해', '너무', '느껴지다', '크다', '작다', '쓰다', '함께', '하루', '대한', '늘다', '줄다'
                   , '늘어나다', '줄어들다', '주다', '풍부하다', '좋아하다', '쉬다', '이미', '알려지다', '생기다', '선택']
        
        wordCleaned = []
        for word in raw_pos_tagged:
            if not word[1] in ["Josa", "Eomi", "Punctuation", "Foreign"]:   # Foreign == ”, “ 와 같이 제외되어야할 항목들
                if (len(word[0]) != 1) & (word[0] not in delList): # 한 글자로 이뤄진 단어들을 제외 & 원치 않는 단어들을 제외, 대신 "안, 못"같은 것까지 같이 지워져서 긍정,부정을 파악해야 되는경우는 제외하지 않는다.
                    if(("http" not in word[0]) & ("ㅋ" not in word[0])) :
                        wordCleaned.append(word[0])
        
        # Counter 메소드 이용 소팅 및 사전화
        resultSet = Counter(wordCleaned)
        wordDict = dict(resultSet)
        # print(wordDict)
        # sortedWordDict = sorted(wordDict.items(), key=lambda x:x[1], reverse=True)
        # print(sortedWordDict)
        
        # 그래프에 한글 폰트 설정
        font_name = matplotlib.font_manager.FontProperties(fname="C:/Windows/Fonts/malgun.ttf").get_name() # NanumGothic.otf
        matplotlib.rc('font', family=font_name)
        
        # 막대그래프
        word_frequency = nltk.FreqDist(wordCleaned)
        df = pd.DataFrame(list(word_frequency.values()), word_frequency.keys())
        result = df.sort_values([0], ascending = False)
        result = result[:50]
        result.plot(kind='bar', legend=False, figsize=(15,5))
        plt.show()
        
        # 워드클라우드
        # word_cloud = WordCloud(font_path='C:/Windows/Fonts/malgun.ttf',
        #                        width=2000, height=1000,
        #                     #    background_color='white',
        #                        max_font_size=120).generate_from_frequencies(wordDict)
        
        # word_cloud.generate_from_frequencies(wordDict)
        
        # plt.figure(figsize=(15,15))
        # plt.imshow(word_cloud)
        # plt.axis("off")
        # plt.tight_layout(pad=0)
        # plt.show()
        
except FileNotFoundError:
    print("해당 파일이 없습니다.")
except UnicodeDecodeError:
    print(userInput , "을(를) 읽을 수 없습니다. 인코딩이 일치하지 않습니다.")