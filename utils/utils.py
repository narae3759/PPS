import streamlit as st
from dotenv import load_dotenv
import os
from pathlib import Path
from st_pages import Page, Section, show_pages, add_page_title

def read_mdfile(file):
    md_text = Path(file).read_text(encoding="utf-8")
    st.markdown(md_text, unsafe_allow_html=True)
    
def sidebar():
    add_page_title()
    show_pages(
        [
            Page("Home.py", "PPS AI & Data Lab LLM 실험실", "🧪"),
            Section(name="Examples", icon="📌"),
                Page("./pages/1_01_문서요약.py", "01. 문서요약"),
                Page("./pages/2_02_상담봇.py", "02. 상담봇"),
                Page("./pages/3_03_글쓰기.py", "03. 글쓰기"),
            Section(name="Docs", icon="📚"),
                Page("./pages/4_04_test.py", "Langchain", ""),
        ]
    )

def style_load():
    # .env load 
    load_dotenv()

    # check API KEY 
    if "OPENAI_API_KEY" not in os.environ:
        print("API KEY 정보가 없습니다. 확인 후 환경변수에 등록해주세요.")
        
    sidebar()
    read_mdfile("./docs/css.md")
