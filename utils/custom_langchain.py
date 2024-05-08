import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.callbacks import BaseCallbackHandler
from dotenv import load_dotenv
import os

def load_api():
    """ 환경변수에서 API KEY 불러오기 """
    load_dotenv()

    # check API KEY 
    if "OPENAI_API_KEY" not in os.environ:
        print("API KEY 정보가 없습니다. 확인 후 환경변수에 등록해주세요.")

class ChainSummary:
    """ 문서 요약 """
    def __init__(self, template):
        self.container = st.empty()
        self.template = template

        self.prompt = PromptTemplate.from_template(self.template)
        self.model = ChatOpenAI(
            temperature=0,
            model_name="gpt-3.5-turbo",
            streaming=True,
            callbacks=[CustomHandler(self.container)]
        )
        self.output_parser = StrOutputParser()

        self.chain = self.prompt | self.model | self.output_parser

    def invoke(self, inputs):
        with st.spinner(text="요약 중입니다...."):
            response = self.chain.invoke(inputs)

        return response
    
class ChainSimpleSummary:
    def __init__(self, template):
        self.template = template

        self.prompt = PromptTemplate.from_template(self.template)
        self.model = ChatOpenAI(
            temperature=0,
            model_name="gpt-3.5-turbo",
        )
        self.output_parser = StrOutputParser()

        self.chain = self.prompt | self.model | self.output_parser

    def invoke(self, inputs):
        response = self.chain.invoke(inputs)

        return response

class CustomHandler(BaseCallbackHandler):
    def __init__(self, container):
        self.container = container
        self.text = ""
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)        
    