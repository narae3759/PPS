import streamlit as st
from custom_functions import *
	
# llm 생성
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.schema import AIMessage, HumanMessage, SystemMessage

load_style()
###########################################################################
# Page 시작
###########################################################################
## 인사
st.chat_message("assistant").markdown("안녕하세요. PPS 상담봇입니다. 고민이 있다면 언제든 말해주세요:smile:")

## STEP1. messages 생성
if "messages" not in st.session_state:
	st.session_state.messages = []

## STEP2. messages 출력
for chat in st.session_state.messages:
	with st.chat_message(chat["role"]):
		st.markdown(chat["content"])

if prompt := st.chat_input("채팅을 입력하세요(ex. 나 오늘 우울해)"):
	
    chat = [
        SystemMessage(
            content = """
            당신은 상대방의 사연을 듣고 상담해주는 심리상담사 로봇입니다.
            상대방의 말에 공감해주고, 해결책이 있다면 찾아주세요. 
            500자 이내로 상대방의 CHAT에 존댓말로 이모지와 함께 답변해주세요.
            """
        ),
        HumanMessage(
            content = prompt
        ),
    ]
	
    ## STEP3. user 
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role":"user", "content":prompt})

    ## STEP4. assistant 
    with st.chat_message("assistant"):
        container = st.empty()
        chatbot = ChatOpenAI(
            model_name = "gpt-3.5-turbo",
            temperature = 0.5,
            streaming = True,
            callbacks = [CustomHandler(container)]
        )
        response = chatbot.invoke(chat).content      
    st.session_state.messages.append({"role":"assistant", "content":response})