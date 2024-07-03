# 리뷰 분석기(Review Analyzer) 개발 프로젝트

## 📋 프로젝트명: [서울신라호텔 더 파크뷰](https://pcmap.place.naver.com/restaurant/13166754/review/visitor)의 네이버 리뷰 분석

### 🔍 프로젝트 배경

* 최근 음식점에서 진행하는 리뷰 이벤트의 형태가 인스타그램 해시태그에서 네이버 영수증 리뷰로 변화함.
* 캐치테이블, 카카오맵 등 타 사이트에 비해 네이버 리뷰의 수가 많음.
* 리뷰 외 추가적인 정보(ex. 방문 목적, n번째 방문 등)수집이 가능함.

    ![](https://imgur.com/AqHDcXA.png)
    
### 🔍 프로젝트 목표

* 맛, 서비스, 가격 카테고리에 따른 긍/부정을 분석
* 설정한 카테고리 외에 추가적으로 나타나는 특징들이 있는지 분석
* 데이터를 보지 않아도 알 수 있는 호텔 뷔페에 대한 일반적인 반응 외에 알 수 있는 특징들에 대해 분석
* 추후 원하는 URL에 맞게 리뷰를 분석할 수 있도록 기능을 확장할 예정

## 📋 프로젝트 과정

### 1. 데이터 수집

* 네이버 리뷰 크롤링 모듈 개발(`review_analyzer/crawler.py`)<br>
    : 네이버 리뷰 URL, 목표 수집량을 입력하면 리뷰 데이터를 수집한다. 

    ![](https://imgur.com/2yboKO0.png)

* 총 206개의 데이터 수집 
    ![](https://imgur.com/7uyxkam.png)


### 2. 데이터 전처리

* 데이터 탐색
    - 정보가 너무 적어 사용하지 않음 `additional_info`, `auth_method`
    - 아이디, 방문 날짜, n번째 방문이 잘 맞지 않아 사용하지 않음. `n_visit` 

* 전처리 과정
    1. 중복 제거
    2. `date`열을 `date`와 `weekday`로 분리(ex. 2024년 6월 7일 -> 2024-06-07, 금요일)
    3. 필요없는 문자 제거(특수문자, 모음, 자음 등)
    4. `review` 결측치 제거
    5. `review` 교정
        1) 맞춤법 검사했으나 신조어의 의미가 달라져 쓰지 않음(❌ Pyhanspell)
        2) 두 개의 라이브러리를 비교하여 띄어쓰기 교정(Pykospacing, ✅ Soyspacing)
    6. `review` 길이를 통해 이상치 제거
        1) IQR를 기준으로 상한값 설정
        2) 하한값은 의미가 다양해지는 구간을 탐색하여 사용자가 직접 설정함

* 리뷰 형태소 분석
    * 불용어, 신조어, 가중치 등 여러 기능이 포함되어 있는 Kiwi 형태소 분석기 선택
    * Kiwi에서 제공하는 stopwords 이용하여 불용어 제거
    * 의미가 있다고 생각하는 체언(N), 용언(V)만 분석에 사용

### 3. 데이터 탐색 

* 시기별로 특정한 패턴이 보이지는 않으나, 연말과 연초에 많이 방문하는 것으로 보임.

    ![](https://imgur.com/a1cIkFU.png)

* 2022년까지 계속 리뷰 수가 증가하다가 2023년에 다소 줄어듦.

    ![](https://imgur.com/FDKv0RT.png)



### 4. 데이터 분석

## 📋 결론

## References 

* [GitHub, Pykospacing](https://github.com/haven-jeon/PyKoSpacing)
* [GiHub, Soyspacing](https://github.com/lovit/soyspacing?tab=readme-ov-file)
* [ratsgo Blog, Soyspacing Model Download](https://ratsgo.github.io/embedding/downloaddata.html)





