import streamlit as st
from utils.utils import *
from utils.custom_style import *
from utils.custom_langchain import *
import re
import json
from datetime import datetime 
from bs4 import BeautifulSoup, SoupStrainer

load_style()
session_key = 'news_data'
###########################################################################
# Page 시작
###########################################################################
## Templates
#--------------------------------------------------------------------------
template = """# INSTRUCTION
- 다음 TEXT를 FORMAT에 맞춰 5줄로 요약하세요.
- 다음 FORMAT에 맞춰 작성하세요.
- 요점 정리는 bullet form으로 작성하고 온점(.)으로 종결하세요.
- 태그는 최대 3개이며, 키워드 앞에 '\#'를 붙이세요.


# TEXT: {text}

# FORMAT:
🔖 태그1, 태그2, ...

📌 요점 정리
- 요약1
- 요약2
- ...
"""
#--------------------------------------------------------------------------
## Functions
#--------------------------------------------------------------------------
def generate_url(choice:str):
    """Generate a URL based on the selected category

    Args:
        choice (str): The text of the selected radio button

    Returns:
        url: The generated URL
    """
    category = ["경제","사회","생활/문화","세계","과학"]
    url_category = {x: i+101 for i, x in enumerate(category)}

    url = f"https://news.naver.com/section/{url_category[choice]}"

    return url

def extract_article_list(url:str, cnt:int):
    """Extracts a portion of HTML containing the article list

    Args:
        url (str): The URL where the article list
        int (int): The number of articles

    Returns:
        divlist: The HTML content related to the article
    """
    article = []
    html = load_html(url)

    only_read = SoupStrainer("div", attrs={"class":"section_article as_headline _TEMPLATE"})           # 필요한 부분만 긁어온다.
    soup = BeautifulSoup(html, 'html.parser', parse_only=only_read)
    divlist = soup.find_all('li', class_=lambda x: "_SECTION_HEADLINE" in x)
    
    return divlist[:min(len(divlist), cnt)]

def create_info_dict(div):
    """Converts the information extracted from the article into a dictionary

    Args:
        div : The HTML content related to the article

    Returns:
        info_dict: A dictionary containing the article information
            {
                "thumb": "https://mimgnews.pstatic.net/image/origin/374/2024/05/02/382003.jpg?type=nf220_150",
                "url": "https://n.news.naver.com/mnews/article/374/0000382003",
                "title": "내년 의대증원 규모 1500명 안팎…소송전 '변수'",
                "press": "SBS Biz",
                "content": "[앵커]의대들이.... ",
                "summary": "- 내년 의대 ..."
            }
    """
    info_dict = {}
    try:
        info_dict['thumb'] = div.img["data-src"]
    except:
        info_dict['thumb'] = ''
    info_dict['url'] = div.find('a', attrs={"class":"sa_text_title"})["href"]
    info_dict['title'] = div.strong.text
    info_dict['press'] = div.find('div', attrs={"class":"sa_text_press"}).text
    info_dict['content'] = extract_article(info_dict['url'])

    return info_dict

def extract_article(url:str):
    """Extracts only the article from the HTML

    Args:
        url (str): The URL of the article

    Returns:
        article: The article text extracted from the HTML
    """
    html = load_html(url)
    soup = BeautifulSoup(html, parse_only=SoupStrainer('article'), features="lxml")
    # Multi-space removal
    article = re.sub(r'\n{2,}', '\n', soup.text).strip()

    return article

def create_article_expander(number:int, info_dict:dict):
    """Creates a st.expander for the the article

    Args:
        number (int): The index number of the article
        info_dict (dict): A dictionary containing the article information
            {
                "thumb": "https://mimgnews.pstatic.net/image/origin/374/2024/05/02/382003.jpg?type=nf220_150",
                "url": "https://n.news.naver.com/mnews/article/374/0000382003",
                "title": "내년 의대증원 규모 1500명 안팎…소송전 '변수'",
                "press": "SBS Biz",
                "content": "[앵커]의대들이.... ",
                "summary": "- 내년 의대 ..."
            }
    """
    title = f"**{number}. {info_dict['title']}**"

    with st.expander(label=title, expanded=True):
        col1, col2 = st.columns([0.3,0.7])

        with col1:
            st.markdown(f"""
                        <a href={info_dict['url']}>
                            <img src={info_dict['thumb']} width='100%'/>
                        </a>
                        """, unsafe_allow_html=True)

        with col2:
            chain = ChainSummary(template)
            response = chain.invoke({"text": info_dict["content"]})
            info_dict['summary'] = response

def create_article_expander_no_stream(number:int, info_dict:dict):
    """Creates a st.expander for the the article

    Args:
        number (int): The index number of the article
        info_dict (dict): A dictionary containing the article information
            {
                "thumb": "https://mimgnews.pstatic.net/image/origin/374/2024/05/02/382003.jpg?type=nf220_150",
                "url": "https://n.news.naver.com/mnews/article/374/0000382003",
                "title": "내년 의대증원 규모 1500명 안팎…소송전 '변수'",
                "press": "SBS Biz",
                "content": "[앵커]의대들이.... ",
                "summary": "- 내년 의대 ..."
            }
    """
    title = f"**{number}. {info_dict['title']}**"
    
    with st.expander(label=title, expanded=True):
        col1, col2 = st.columns([0.3,0.7])

        with col1:
            st.markdown(f"""
                        <a href={info_dict['url']}>
                            <img src={info_dict['thumb']} width='100%'/>
                        </a>
                        """, unsafe_allow_html=True)

        with col2:
            st.markdown(info_dict['summary'])


def download_btn(container, data:dict, type="json"):
    """Creates a download button element

    Args:
        container: The container where the button will be inserted
        data (dict): The dictionary to be stored
        type (str, optional): The type of file saving method. Can be one of the following: 'json'(default), 'csv'
    """
    if type == "json":
        container.download_button(
            label="Download json",
            data=json.dumps(data, ensure_ascii=False),
            file_name="articles.json",
            mime='application/json',
            on_click=save_data,
            args=[json.dumps(data)],
            use_container_width=True
        )
    else:
        container.download_button(
            label="Download csv",
            data=json2csv(data),
            file_name="articles.csv",
            mime='text/csv',
            on_click=save_data,
            args=[json.dumps(data)],
            use_container_width=True
        )

def save_data(data):
    """Saves data to the st.session_state

    Args:
        data (str): The JSON-formatted data to be converted into a string
    """
    st.session_state[session_key] = data
#--------------------------------------------------------------------------
## Settings
#--------------------------------------------------------------------------
if session_key not in st.session_state:
    st.session_state[session_key] = ''

#--------------------------------------------------------------------------
## Header
#--------------------------------------------------------------------------
# Insert Text
st.markdown("""
            <div class="info-container">
            📢 기능 설명
            <li> 네이버 뉴스를 기반으로 기사를 불러옵니다.</li>
            <li> 썸네일을 누르면 해당 기사 링크로 연결됩니다.</li>
            <li> 모든 요약은 개조식 문장으로 처리됩니다.</li>
            <li> 요약된 내용은 json, csv로 저장이 가능합니다.</li>
            </div>
            """, unsafe_allow_html=True)

# Setting Box
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

    # Setting Save Method
    save_type = columns[1].selectbox(
        label=":three: 저장 방식",
        options=["json", "csv"],
    )

    # Click Button
    search_btn = st.button(
        label="News 불러오기",
        type="primary",
        use_container_width=True
    )

#--------------------------------------------------------------------------
## Body
#--------------------------------------------------------------------------

# Generate URL
today = datetime.now()
url = generate_url(choice)

# When the Button is clicked
if search_btn:
    with st.container(border=True):
        # Body-header
        download = btn_container(type="right")
        st.markdown(f"### {today.year}년 {today.month}월 {today.day}일 오늘의 헤드라인 뉴스({choice})")
        success = st.container()

        # Total Spinner
        with st.spinner():
            article_list = extract_article_list(url, max_cnt)

            # Insert Message 
            st.markdown(f"{len(article_list)}개의 헤드라인 뉴스를 가져옵니다.")
            
            article_json = {
                'date': today.strftime("%Y년 %m월 %d일"),
                'category': choice,
                'articles': []
            }
            for number, article in enumerate(article_list, 1):
                article_info = create_info_dict(article)
                article_json['articles'].append(article_info)
                
                # Create article container
                create_article_expander(number, article_info)

        # Success Message
        download_btn(download, data=article_json, type=save_type)
        success.success("모든 뉴스 요약이 완료되었습니다.", icon="✅")

# When the download button is pressed and the page is refreshed
elif data := st.session_state[session_key]:
    article_json = json.loads(data)
    article_list = article_json['articles']
    
    with st.container(border=True):
        # Body-header
        download = btn_container(type="right")
        st.markdown(f"### {today.year}년 {today.month}월 {today.day}일 오늘의 헤드라인 뉴스({choice})")
        success = st.container()

        # Insert Message 
        st.markdown(f"{len(article_json)}개의 헤드라인 뉴스를 가져옵니다.")
        
        for number, article_info in enumerate(article_list, 1):
            # Create article container
            create_article_expander_no_stream(number, article_info)
            
        # Success Message
        download_btn(download, data=article_json, type=save_type)
        success.success(":white_check_mark: 모든 뉴스 요약이 완료되었습니다.")



