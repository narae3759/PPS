import streamlit as st
from st_pages import Page, Section, show_pages, add_page_title
from utils.utils import read_mdfile
from utils.custom_langchain import load_api

def vertical_space(size):
    st.container(height=size, border=False)

def text_align(text, type="center"):
    st.markdown(f"""
               <div style="text-align:{type}">
               {text}
               </div>
               """, unsafe_allow_html=True)

def button_align(label, type="right", ratio=None):
    if not ratio:
        if type=="center":
            ratio = [0.3,0.4,0.3]
            idx = 1
        elif type == "right":
            ratio = [0.8, 0.2]  
            idx = 1
        else:
            ratio = [0.2, 0.8]
            idx = 0
    
    columns = st.columns(ratio)
    button = columns[idx].button(
        label=label,
        use_container_width=True
    )

    return button
    
    

        
    

def sidebar():
    """ sidebar 목차 구성 """
    add_page_title()
    show_pages(
        [
            Page("Home.py", "PPS AI & Data Lab LLM 실험실", "🧪"),
            Section(name="Examples", icon="📌"),
                Page("./pages/1_01_문서요약.py", "01. 문서요약"),
                Page("./pages/2_02_상담봇.py", "02. 상담봇"),
                Page("./pages/3_03_글쓰기.py", "03. 글쓰기"),
                Page("./pages/4_04_QA봇.py", "04. Q&A 봇"),
                Page("./pages/6_test.py", "05. 테스트중입니다")
        ]
    )

def load_style():
    """ 전체 환경 Setting """
    # API KEY 불러오기
    load_api() 
    
    # 스타일 적용 
    read_mdfile("./static/css.md")

    # Sidebar 목차 구성
    sidebar()
    
    

