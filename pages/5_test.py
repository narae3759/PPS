import streamlit as st
from custom_functions import *
import re

load_style()
session_key = 'ex_qa_state'
###########################################################################
# Page 시작
###########################################################################
## Templates
template = """# INSTRUCTION
TEXT를 5줄로 요약해주세요. 각 문장은 높임말로 작성해주세요.

# TEXT: {text}
"""
#--------------------------------------------------------------------------
## Functions
#--------------------------------------------------------------------------
def set_action(session_key, action, page=None):
    if action == "Next":
        st.session_state[session_key] += 1
    elif action == "Back":
        st.session_state[session_key] -= 1
    elif action == "Move":
        st.session_state[session_key] = page

def check_url(url):
    url_pattern = r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[^\s]*$'
    check = True if re.match(url_pattern, url) else False
    
    return check 

#--------------------------------------------------------------------------
## Settings
#--------------------------------------------------------------------------
if session_key not in st.session_state:
    st.session_state[session_key] = 1

#--------------------------------------------------------------------------
## Header
#--------------------------------------------------------------------------
columns = st.columns([0.1,0.35,0.1,0.35,0.1])

type_dict = {0: "primary", 1: "secondary"}
type_key = 0 if st.session_state['ex_qa_state'] == 1 else 1

with columns[1].container():
    st.button(label="STEP1. 정보 입력", 
              on_click=set_action, args=[session_key, "Move",1],
              type=type_dict[type_key],
              use_container_width=True)
with columns[3].container():
    st.button(label="STEP2. 요약 및 Q&A", 
              on_click=set_action, args=[session_key,"Move",2],
              type=type_dict[1-type_key],
              use_container_width=True)

vertical_space(20)

#--------------------------------------------------------------------------
## Body
#--------------------------------------------------------------------------
if st.session_state[session_key] == 1:
    ### Form 1 - STEP1. 정보 입력
    with st.container(border=True):
        options = ["직접 입력", "URL", "File Upload"]
        opt_index = {opt:i for i, opt in enumerate(options)}

        # Radio Button
        radio = st.radio(
            label="입력 방식",
            options=options,
            horizontal=True
        )

        # Input Box
        radio_idx = opt_index[radio]
        if radio_idx == 0:
            content = st.text_area(
                height=300,
                label="텍스트",
                label_visibility="collapsed",
                placeholder="텍스트를 입력하세요"
            )
        elif radio_idx == 1:
            content = st.text_input(
                label="텍스트",
                label_visibility="collapsed",
                placeholder="https://www.google.com"
            )
            url_available = check_url(content)
        else:
            content = st.file_uploader(
                label="텍스트",
                label_visibility="collapsed"
            )

    # Save Data
    st.session_state['ex_qa_data'] = {
        "type": radio,
        "content": content
    }

    # Raise Error
    isdisabled = False
    if not content:
        isdisabled = True
        st.error("입력된 값이 존재하지 않습니다.", icon="🚨")
    elif radio_idx == 1 and not url_available:
        isdisabled = True
        st.error("올바른 URL 표현이 아닙니다.", icon="🚨")

    # Next Button
    st.button(
        label="STEP1. 요약 및 Q&A으로 이동",
        type="primary",
        disabled=isdisabled,
        on_click=set_action, args=[session_key,"Next"],
        use_container_width=True
    )
else:
    ### Form 2 - STEP2. 요약 및 Q&A
    #### Summary Container
    data = st.session_state["ex_qa_data"]

    # Raise Error
    if not data['content']:
        st.error("입력된 값이 존재하지 않습니다. STEP1부터 다시 하세요.", icon="🚨")

        # Back Button  
        st.button(
            label="STEP1. 정보 입력으로 이동",
            type="primary",
            on_click=set_action, args=[session_key,"Back"],
            use_container_width=True
        )
    else:
    # Summary Container
        with st.container(border=True):
            st.markdown("<div style='font-size:0.9rem;margin-bottom:0.5rem'>요약</div>", unsafe_allow_html=True)
            
            chain = ChainSummary(template)
            response = chain.invoke({"text": data["content"]})
            
            vertical_space(3)

    #### Question Container
    with st.container(border=True):
        # Input Box
        st.markdown("<div style='font-size:0.9rem;margin-bottom:0.5rem'>Question</div>", unsafe_allow_html=True)
        col1, col2 = st.columns([0.85,0.15])
        with col1:
            container = st.empty()

            question = st.text_input(
                label="Question",
                placeholder="질문을 입력하세요",
                label_visibility="collapsed"
            )

        # Enter Button
        with col2:
            enter_btn = st.button(
                label="Enter",
                use_container_width=True
            )


    # Back Button  
    st.button(
        label="다시하기",
        type="primary",
        on_click=set_action, args=[session_key,"Back"],
        use_container_width=True
    )
        

#--------------------------------------------------------------------------
## Form 1 - STEP1. 정보 입력
#--------------------------------------------------------------------------
# with st.spinner(text="이동 중"):

