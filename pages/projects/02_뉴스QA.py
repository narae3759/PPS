import streamlit as st
from custom_functions import *
import json
from datetime import datetime 
from bs4 import BeautifulSoup, SoupStrainer

load_style()
session_key = 'chat_history'
###########################################################################
# Page 시작
###########################################################################
## Templates
#--------------------------------------------------------------------------
summary_template = """# INSTRUCTION
- 당신은 뉴스 정보를 전달하는 앵커입니다.
- ARTICLE을 5줄로 요약하여 완전한 문장으로 브리핑하세요.

# ARTICLE: {article}
"""
#--------------------------------------------------------------------------
## Functions
#--------------------------------------------------------------------------
def extract_naver_news(url:str):
    """Extracts only the article from the HTML

    Args:
        url (str): The URL of the article

    Returns:
        info_dict: A dictionary containing the article information
            {
                'press': '아이뉴스24',
                'title': "'쿠팡 와우 카드', 7개월 만에 50만장 발급…혜택 더 늘린다",
                'author': '구서윤 기자',
                'content': '업계 최고 수준의 적립 혜택 제공...
            }
    """
    info_dict = {}

    html = load_html(url)
    soup = BeautifulSoup(
        html, 
        parse_only=SoupStrainer('div', attrs={"class":"newsct"}), features="lxml")
    
    head = soup.find("div", attrs={"class":"media_end_head go_trans"})
    title = head.find("div", attrs={"class":"media_end_head_title"})
    author = head.find("div", attrs={"class":"media_end_head_journalist"})

    info_dict['press'] = head.img["title"]
    info_dict['title'] = remove_blank(title.text)
    info_dict['author'] = remove_blank(author.text).split("\n")[0]
    info_dict['content'] = remove_blank(soup.find("article").text)

    return info_dict

def save_user_chat(chat):
    """Stores user chat in session_state"""
    st.session_state[session_key].append({"role":"user", "message":chat})

def save_assistant_chat(chat):
    """Stores assistant chat in session_state"""
    st.session_state[session_key].append({"role":"assistant", "message":chat})

def print_chat_history():
    """Prints out the chat history of the session_state"""
    for chat in st.session_state[session_key]:
        st.chat_message(chat["role"]).markdown(chat["message"])

    return st.container()

def reset_chat_history():
    """Initialize the chat history of session_state"""
    st.session_state[session_key] = []
#--------------------------------------------------------------------------
## Settings
#--------------------------------------------------------------------------
if session_key not in st.session_state:
    st.session_state[session_key] = []

#--------------------------------------------------------------------------
## Header
#--------------------------------------------------------------------------
# Insert Text
st.markdown("""
            <div class="info-container">
            📢 기능 설명
            <li> 원하는 URL을 불러오면 간단히 요약해줍니다.</li>
            <li> 멀티 턴으로 대화할 수 있습니다.</li>
            </div>
            """, unsafe_allow_html=True)

# Setting Box
with st.expander(label=":three_button_mouse: URL을 입력해주세요",expanded=True):
    # Select Category
    columns = st.columns([0.85, 0.15])
    news_url = columns[0].text_input(
        label="텍스트",
        label_visibility="collapsed",
        placeholder="https://www.google.com"
        )
    
    # Click Button
    submit_btn = columns[1].button(
        label="Submit",
        type="primary",
        use_container_width=True
    )
    
#--------------------------------------------------------------------------
## Body
#--------------------------------------------------------------------------    
with st.container(border=True):
    # ChatBox Title
    st.markdown(":robot_face: PPS Bot (뉴스 이해를 도와주는 로봇입니다)")

    # When the Button is clicked
    if submit_btn:
        reset_chat_history()
        
        # Greeting Message - News Summary
        news_info = extract_naver_news(news_url)
        with st.chat_message("assistant"):
            summary = f"📌 {news_info['title']}\n\n"
            first_message = st.markdown(summary)
            chain = ChainSummary(summary_template)
            summary += chain.invoke({"article": news_info["content"]})
            save_assistant_chat(summary)
    # When the page is refreshed
    else:
        chat = print_chat_history()

    # Input Box
    if question := st.chat_input(placeholder="Enter Your Message"):
        chat.chat_message("user").markdown(question)
        save_user_chat(question)

        answer = "안녕하세요"
        chat.chat_message("assistant").markdown(answer)
        save_assistant_chat(answer)

    print(st.session_state[session_key])
    



