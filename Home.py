import streamlit as st
from dotenv import load_dotenv
import os

# .env load 
load_dotenv()

# check API KEY 
if "OPENAI_API_KEY" not in os.environ:
    print("API KEY 정보가 없습니다. 확인 후 환경변수에 등록해주세요.")
	
# llm 생성
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain_core.callbacks import BaseCallbackHandler

class CustomHandler(BaseCallbackHandler):
    def __init__(self, container):
        self.container = container
        self.text = ""
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

###########################################################################
# Page 시작
###########################################################################
## Title
st.title("PPS AI & Data Lab 실험실")

## author
st.markdown("**author: 김나래 연구원**")

## GitLab
st.markdown("## Docs")

# from pathlib import Path
# def read_mdfile(file):
#     md_text = Path(file).read_text(encoding="utf-8")
#     st.markdown(md_text)
    
# read_mdfile("./docs/Streamlit/01. Streamlit 기초.md")