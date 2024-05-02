import streamlit as st
from utils.custom_style import *
from utils.custom_langchain import *
import re
import json
from datetime import datetime 

load_style()
session_key = 'news_data'
###########################################################################
# Page 시작
###########################################################################
## Templates
template = """# INSTRUCTION
- 다음 TEXT를 FORMAT에 맞춰 5줄로 요약해주세요.
- 정량적으로 표현될 수 있는 요약을 맨 앞에 배치해주세요.

# TEXT: {text}

# FORMAT:
- 요약1
- 요약2
- 요약3
"""
#--------------------------------------------------------------------------
## Functions
#--------------------------------------------------------------------------
import requests 
from bs4 import BeautifulSoup, SoupStrainer

def load_html(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("찾을 수 없는 페이지입니다.")
    else:
        html = response.text

    return html

def extract_article(url):
    html = load_html(url)
    soup = BeautifulSoup(html, parse_only=SoupStrainer('article'), features="lxml")
    article = re.sub(r'\n{2,}', '\n', soup.text)

    return article

def naver_news_extract_urls(url, cnt=None):
    news = []
    html = load_html(url)

    only_read = SoupStrainer("div", attrs={"class":"section_article as_headline _TEMPLATE"})           # 필요한 부분만 긁어온다.
    soup = BeautifulSoup(html, 'html.parser', parse_only=only_read)
    parsing_div = soup.find_all('li', class_=lambda x: "_SECTION_HEADLINE" in x )
    if not cnt:
        cnt = len(parsing_div)
    else:
        cnt = min(len(parsing_div), cnt)

    st.markdown(f"{cnt}개의 헤드라인 뉴스를 가져옵니다.")
    
    for num, div in enumerate(parsing_div[:cnt]):
        news_info = {}
        try:
            news_info['thumb'] = div.img["data-src"]
        except:
            news_info['thumb'] = ''
        news_info['url'] = div.find('a', attrs={"class":"sa_text_title"})["href"]
        news_info['title'] = div.strong.text
        news_info['press'] = div.find('div', attrs={"class":"sa_text_press"}).text
        news_info['content'] = extract_article(news_info['url'])

        # print(news_info)

        title = f"**{num+1}. {news_info['title']}**"
        print(title)
        with st.expander(label=title, expanded=True):
            col1, col2 = st.columns([0.3,0.7])

            with col1:
                st.markdown(f"""
                            <a href={news_info['url']}>
                                <img src={news_info['thumb']} width='100%'/>
                            </a>
                            """, unsafe_allow_html=True)

            with col2:
                chain = ChainSummary(template)
                response = chain.invoke({"text": news_info["content"]})
                news_info['summary'] = response

                news.append(news_info)

    return news

#--------------------------------------------------------------------------
## Settings
#--------------------------------------------------------------------------
if session_key not in st.session_state:
    st.session_state[session_key] = ''

with st.expander(label=":gear: Settings",expanded=True):
    # Select Category
    choice = st.radio(
        label=":one: 분야",
        options=["경제","사회","생활/문화","과학","세계"],
        horizontal=True
    )

    # Setting Number
    columns = st.columns(2)
    max_cnt = columns[0].number_input(
        label=":two: 가져올 뉴스 개수",
        value=5, min_value=1, max_value=10,
        format="%d"
    )

    is_save = columns[1].selectbox(
        label=":three: 저장 방식",
        options=["저장 안함", "json"],
    )

    search_btn = st.button(
        label="News 불러오기",
        type="primary",
        use_container_width=True
    )
#--------------------------------------------------------------------------
## Body
#--------------------------------------------------------------------------
today = datetime.now()

category = ["경제","사회","생활/문화","세계","과학"]
url_category = {x: i+101 for i, x in enumerate(category)}

url = f"https://news.naver.com/section/{url_category[choice]}"

def save_data(data):
    st.session_state[session_key] = data

if search_btn:
    page = st.container(border=True)
    with page:
        btn_space = st.empty()
        st.markdown(f"### {today.year}년 {today.month}월 {today.day}일 오늘의 헤드라인 뉴스({choice})")
        memo = st.container()

        with st.spinner():
            news = naver_news_extract_urls(url, max_cnt)
        
        save_btn = btn_space.download_button(
            label="Download json",
            data=json.dumps(news,ensure_ascii=False),
            file_name="news.json",
            mime='application/json',
            on_click=save_data,
            args=[json.dumps(news)]
        )

        memo.success(":white_check_mark: 모든 뉴스 요약이 완료되었습니다.")

elif text := st.session_state[session_key]:

    data = json.loads(text)
    with st.container(border=True):
        btn_space = st.empty()
        st.markdown(f"### {today.year}년 {today.month}월 {today.day}일 오늘의 헤드라인 뉴스({choice})")

        st.success(":white_check_mark: 모든 뉴스 요약이 완료되었습니다.")
        st.markdown(f"{len(data)}개의 헤드라인 뉴스를 가져옵니다.")
        
        for article in data:
            element = st.expander(
                label=article['title'],
                expanded=True
            )

            columns = element.columns([0.3,0.7])

            columns[0].markdown(f"""
                                <a href={article['url']}>
                                    <img src={article['thumb']} width='100%'/>
                                </a>
                                """, unsafe_allow_html=True)

            columns[1].markdown(article['summary'])

