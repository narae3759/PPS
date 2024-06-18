import streamlit as st
from custom_functions import *

# llm 생성
from operator import itemgetter
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

load_style()
session_key = "news_history"
###########################################################################
# Page 시작
###########################################################################
# Insert Text
st.markdown("""
            <div class="info-container">
            📢 기능 설명(작업 중)
            <li> 키워드와 관련된 뉴스를 검색하여 질문에 답할 수 있습니다. </li>
            <li> 대화 내용을 기억하여 대답할 수 있습니다. </li>
            <li> 검색 영역을 넓혀나갈 예정입니다. </li>
            </div>
            """, unsafe_allow_html=True)
#--------------------------------------------------------------------------
## Settings
#--------------------------------------------------------------------------
if session_key not in st.session_state:
    st.session_state[session_key] = []

if "search_chain" in st.session_state:
     chat = st.session_state["search_chain"]
     memory = st.session_state["search_chain"]
else:
     memory = ConversationBufferMemory(return_messages=True, memory_key="news_history")
     runnable = RunnablePassthrough.assign(
          news_history = RunnableLambda(memory.load_memory_variables)
          | itemgetter("news_history")
     )
#--------------------------------------------------------------------------
## Header
#--------------------------------------------------------------------------
with st.expander(label=":mag: Search", expanded=True):
    # Select Category
    columns = st.columns([0.85, 0.15])
    keyword = columns[0].text_input(
        label="텍스트",
        label_visibility="collapsed",
        placeholder="검색어를 입력하세요"
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
for chat in st.session_state[session_key]:
	with st.chat_message(chat["role"]):
		st.markdown(chat["content"])

if submit_btn:
    with st.spinner("Please wait..."):
        chain = ragtool.NewsRAG(keyword)

    st.success("Complete!", icon="✔️")

    greeting = "안녕하세요. 뉴스를 기반으로 답하는 QA 로봇입니다. 무엇이 궁금하신가요?"
    st.chat_message("assistant").markdown(greeting)
    st.session_state[session_key].append({"role":"assistant", "content":greeting})

    question = st.chat_input(placeholder="채팅을 입력하세요")

    if question:
        st.chat_message("user").markdown(question)
        st.session_state[session_key].append({"role":"user", "content":question})

        answer = chain.invoke(question)
        st.chat_message("assistant").markdown(answer)

        st.session_state[session_key].append({"role":"assistant", "content":answer})

        


    