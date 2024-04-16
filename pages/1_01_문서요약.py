import streamlit as st
from utils.utils import read_mdfile, style_load
	
# llm 생성
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from utils.langchain_custom import CustomHandler

style_load()
###########################################################################
# Page 시작
###########################################################################

st.title("문서 요약하기")

line = st.slider(':sparkles: 몇 줄로 요약할까요?', 0, 10)
prompt = st.text_area("요약할 텍스트를 입력하세요", height=200)
st.write(f"{len(prompt)}자 입력 중...")
if button := st.button("Sumarize", type="primary"):
    
    message = [
            SystemMessage(
                content = f"{line}줄로 요약하는데 존댓말로 해주세요."
            ),
            HumanMessage(
                content = prompt
            ),
        ]
    
    container = st.empty()
    summbot = ChatOpenAI(
        model_name = "gpt-3.5-turbo",
        temperature = 0.5,
        streaming = True,
        callbacks = [CustomHandler(container)]
    )
    response = summbot.invoke(message)