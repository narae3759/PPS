import streamlit as st
from custom_functions import *

load_style()
	
# llm 생성
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema import AIMessage, HumanMessage, SystemMessage

###########################################################################
# Page 시작
###########################################################################
from custom_functions.page_custom import page_header, page_body
import json

if 'current_state' not in st.session_state:
    st.session_state['current_state'] = 1

page_header()
page_body()

