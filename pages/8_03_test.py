import streamlit as st
from utils.utils import *
from utils.custom_style import *
from utils.custom_langchain import *
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

#--------------------------------------------------------------------------
## Functions
#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
## Settings
#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
## Header
#--------------------------------------------------------------------------
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
    st.video("https://www.youtube.com/watch?v=DQacCB9tDaw")

#  * 다운로드 과정은 Progress 또는 Toast가 좋을 듯 하다.
#  유튜브의 자막을 받아서
#  벡터 스토어에 넣고
#  요약을 해서 
#  합치는 걸 나타내기

