import streamlit as st
from custom_functions import *
	
# llm 생성
from langchain import hub 
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

load_style()
session_key = "chat_history"
###########################################################################
# Page 시작
###########################################################################
# Insert Text
st.markdown("""
            <div class="info-container">
            📢 기능 설명(작업 중)
            <li> 사용자의 심리상담을 해주는 챗봇입니다. </li>
            <li> 대화 내용을 기억하여 대답할 수 있습니다. </li>
            <li> 상담이 아닌 특정 업무에 대한 챗봇으로 바꿀 예정입니다. </li>
            </div>
            """, unsafe_allow_html=True)
#--------------------------------------------------------------------------
## Settings
#--------------------------------------------------------------------------
if session_key not in st.session_state:
    st.session_state[session_key] = []

if "counseling_chain" in st.session_state:
    chat = st.session_state["counseling_chain"]
    memory = st.session_state["counseling_memory"]
else:
    # Chat 인스턴스 생성
    # prompt = PromptTemplate.from_template(template)
    memory = ConversationBufferMemory(return_messages=True, memory_key="chat_history")
    runnable = RunnablePassthrough.assign(
        chat_history = RunnableLambda(memory.load_memory_variables)
        | itemgetter("chat_history")
    )
    prompt = hub.pull("thinker/counseling_korean")
    model = ChatOpenAI(model_name="gpt-4o",streaming=True)
    chain = runnable | prompt | model | StrOutputParser()

    chat = Chat(chain, session_key)
    st.session_state["counseling_chain"] = chat
    st.session_state["counseling_memory"] = memory

#--------------------------------------------------------------------------
## Header & Body
#--------------------------------------------------------------------------

# 첫 채팅을 시작할 때 첫 인사 출력
if len(st.session_state[session_key]) == 0:
    greeting = "안녕하세요. 저는 심리 상담사입니다. 고민을 들어드릴게요😊"
    chat.greeting(greeting)
# 채팅 기록이 있을 때 기록된 채팅 출력
else:
    for history in st.session_state[session_key]:
        st.chat_message(history["role"]).markdown(history["content"])

question = st.chat_input(placeholder="메세지 입력")

# 채팅이 입력되었을 때
if question:
    # 입력된 채팅 출력
    chat.input_user(question)

    # 답변 출력
    answer = chat.input_assistant(question)
    # 메모리 저장
    memory.save_context(
        {"inputs": question},
        {"output": answer}
    )
    # 메모리 출력
    print(memory.load_memory_variables({}))
