import streamlit as st
from st_pages import Page, Section, show_pages, add_page_title
from utils.utils import read_mdfile
from utils.custom_langchain import load_api
import re

def load_style():
    """ Sets up the basic environment """
    # Load API KEY
    load_api() 
    
    # Apply css
    read_mdfile("./static/css.md")

    # Create sidebar
    sidebar()


def sidebar():
    """ Creates a sidebar with the specified content """
    add_page_title()
    show_pages(
        [
            Page("Home.py", "PPS AI & Data Lab LLM 실험실", "🧪"),
            Section(name="Examples", icon="📌"),
                Page("./pages/1_01_문서요약.py", "01. 문서요약"),
                Page("./pages/2_02_상담봇.py", "02. 상담봇"),
                Page("./pages/3_03_글쓰기.py", "03. 글쓰기"),
                Page("./pages/4_04_QA봇.py", "04. Q&A 봇"),
            Section(name="Projects", icon="💼"),
                Page("./pages/6_01_뉴스요약.py", "01. 오늘의 뉴스 요약"),
                Page("./pages/7_02_뉴스QA.py", "02. 오늘의 뉴스 QA"),
                # Page("./pages/8_03_test.py", "03. 유튜브 요약"),
        ]
    )


def vertical_space(size:int):
    """Create vertical blank spaces

    Args:
        size (int): height
    """
    st.container(height=size, border=False)


def text_align(text:str, type="center"):
    """Aligns the text with the specified alignment
    
    Args:
        text (str): The text to be aligned
        type (str, optional): The alignment style for the text. Can be one of the following: 'left', 'center'(default), 'right' 
    """
    st.markdown(f"""
               <div style="text-align:{type}">
               {text}
               </div>
               """, unsafe_allow_html=True)


def btn_container(type="right", ratio=None):
    """Adjusts the position of the button

    Args:
        button : A button provided by streamlit
        type (str, optional): The alignment style for the text. Can be one of the following: 'left', 'center', 'right'(default)
        ratio (list, optional): The length of the button. 

    Returns:
        columns[idx]: The container to insert the button into
    """
    if not ratio:
        if type=="center":
            ratio = [0.3,0.4,0.3]
            idx = 1
        elif type == "right":
            ratio = [0.7, 0.3]  
            idx = 1
        else:
            ratio = [0.3, 0.7]
            idx = 0
    
    columns = st.columns(ratio)
    
    return columns[idx]
    

def remove_blank(text:str):
    """Removes multiple whitespaces in a string.

    Returns:
        output: The text with multiple whitespaces removed
    """
    output = re.sub(r'\n{2,}', '\n', text).strip()

    return output


    
    

