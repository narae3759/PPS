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
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
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

st.title("짧은 글쓰기")

length = st.slider(':sparkles: 글자 수 제한', 50, 500)
keyword = st.text_input("주제를 입력해주세요")
if button := st.button("Write", type="primary"):
    
    template = f"{keyword}를 주제로 명언을 {length}자 이내로 작성해주세요."
    prompt = PromptTemplate.from_template(template)
    # container = st.empty()
    writebot = ChatOpenAI(
        model_name = "gpt-3.5-turbo",
        temperature = 0.5,
        # streaming = True,
        # callbacks = [CustomHandler(container)]
    )
    response = (prompt | writebot).stream({"keyword":keyword, "length":length})
    def stream_data():
        for chunk in response:
            yield chunk.content
    st.write_stream(stream_data)
    