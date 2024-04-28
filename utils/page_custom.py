import streamlit as st 
import json

def set_action(action, click=None):
    if action == "Next":
        st.session_state['current_state'] += 1
    if action == "Back":
        st.session_state['current_state'] -= 1
    else:
        st.session_state['current_state'] = click

def page_header():
    col1, col2, col3, col4 = st.columns([0.5,0.8,0.8,0.5])

    type_one = 'primary' if st.session_state['current_state'] == 1 else 'secondary'
    type_two = 'primary' if st.session_state['current_state'] == 2 else 'secondary'

    with col2:
        st.button("STEP1. 정보 입력", on_click=set_action, args=["Click", 1], type=type_one)

    with col3:
        st.button("STEP2. 요약 및 Q&A", on_click=set_action, args=["Click", 2], type=type_two)

def raise_error(choice_num):
    if choice_num == 1:
        error_message = "입력된 텍스트가 없습니다."
    elif choice_num == 2:
        error_message = "입력된 URL이 없습니다."
    elif choice_num == 3:
        error_message = "업로드된 파일이 없습니다."
    else:
        error_message = "입력된 값이 없습니다. STEP1부터 다시 시작하세요."
            
    st.error(error_message, icon="🚨")

def save_info(choice, content):
    data = {
        "type": choice,
        "content": content
    }

    with open("./utils/temp.json", 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)

    print("저장 완료!!!!")

def input_form():
    with st.container(border=True):
        radio_options = {"Write": 1, "URL": 2, "Upload File": 3}

        choice = st.radio(
            label="입력 방식",
            options = radio_options.keys(),
            horizontal=True
        )

        choice_num = radio_options[choice]
        if choice_num == 1:
            content = st.text_area(
                label = "텍스트를 입력하세요.",
                height = 200,
                placeholder = "텍스트를 입력하세요."
            )
        elif choice_num == 2:
            content = st.text_input(
                label = "URL을 입력하세요.",
                placeholder="https://www.streamlit.io"
            )
        elif choice_num == 3:
            content = st.file_uploader(
                label = "파일을 업로드하세요."
            )
        
        if not content:
            raise_error(choice_num)
        else:
            save_info(choice, content)
            st.button("Next", on_click=set_action, args=["Next"], type="primary", use_container_width=True)
            
def read_info():
    with open("./utils/temp.json", 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    return data

def result_form():  
    data = read_info()  
    content = data['content']

    st.button("다시하기", 
              on_click=set_action, args=["Back"], 
              type="primary")
    
    with st.container(border=True, height=250):
        st.markdown("<div style='text-align:center'><h4>Summary</h4><div>", unsafe_allow_html=True)
        st.write(content)

    result = st.text_input(
        label="Question",
        placeholder="질문을 입력하세요"
    )

def test():
    with st.form(key="myform"):
        radio_options = {"Write": 1, "URL": 2, "Upload File": 3}

        choice = st.radio(
            label="입력 방식",
            options = radio_options.keys(),
            horizontal=True
        )

        choice_num = radio_options[choice]
        if choice_num == 1:
            content = st.text_area(
                label = "텍스트를 입력하세요.",
                height = 200,
                placeholder = "텍스트를 입력하세요."
            )
        elif choice_num == 2:
            content = st.text_input(
                label = "URL을 입력하세요.",
                placeholder="https://www.streamlit.io"
            )
        elif choice_num == 3:
            content = st.file_uploader(
                label = "파일을 업로드하세요."
            )

        content = st.form_submit_button(
            label="Next",
            on_click=set_action, args=["Next"],
            use_container_width=True,
            type="primary"
        )

        print(content)

def page_body():
    if st.session_state['current_state'] == 1:
        # test()
        input_form()
    else:
        result_form()

        st.markdown("""
        <style>
        .custom-button {
        background-color: #4CAF50;
        color: white;
        padding: 14px 20px;
        margin: 8px 0;
        border: none;
        cursor: pointer;
        width: 100%;
        }
        .custom-button:hover {
        opacity: 0.8;
        }
        </style>
        <button class="custom-button">Custom Button</button>
        """, unsafe_allow_html=True)

        
