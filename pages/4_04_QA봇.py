import streamlit as st

from utils.utils import read_mdfile, style_load

style_load()
	
# llm 생성
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from utils.langchain_custom import CustomHandler

###########################################################################
# Page 시작
###########################################################################
from utils.page_custom import page_header, page_body
import json

if 'current_state' not in st.session_state:
    st.session_state['current_state'] = 1

page_header()
page_body()

