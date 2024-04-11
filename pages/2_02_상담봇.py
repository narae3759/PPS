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
st.title("상담봇")

## 인사
st.chat_message("assistant").markdown("안녕하세요. PPS 상담봇입니다. 고민이 있다면 언제든 말해주세요:smile:")

## STEP1. messages 생성
if "messages" not in st.session_state:
	st.session_state.messages = []

## STEP2. messages 출력
for chat in st.session_state.messages:
	with st.chat_message(chat["role"]):
		st.markdown(chat["content"])

if prompt := st.chat_input("Message Chatbot..."):
	
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