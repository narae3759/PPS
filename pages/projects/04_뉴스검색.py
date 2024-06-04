import streamlit as st
from custom_functions import *

load_style()
session_key = "news_qa_msgs"
###########################################################################
# Page 시작
###########################################################################
## Templates
#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
## Functions
#--------------------------------------------------------------------------


#--------------------------------------------------------------------------
## Settings
#--------------------------------------------------------------------------
if session_key not in st.session_state:
    st.session_state[session_key] = []
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

        


    