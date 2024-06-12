import streamlit as st
from custom_functions import *

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate 
from langchain_core.output_parsers import StrOutputParser 

load_style()
###########################################################################
# Page 시작
###########################################################################
# Insert Text
st.markdown("""
            <div class="info-container">
            📢 기능 설명(작업 중)
            <li> 입력된 텍스트를 읽고 요약해주는 기능입니다. </li>
            <li> 템플릿에 따라 요약 형태를 바꿀 수 있습니다. </li>
            <li> 입력 형식을 다양화 할 예정입니다. </li>
            </div>
            """, unsafe_allow_html=True)
#--------------------------------------------------------------------------
## Template Examples
#--------------------------------------------------------------------------
template1 = """\
# INSTRUCTION
TEXT를 {line}줄로 요약해주세요.

# TEXT: {input}
"""

template2 = """\
# INSTRUCTION
- 다음 TEXT를 FORMAT에 맞춰 {line}줄로 요약해주세요.
- 정량적으로 표현될 수 있는 요약을 맨 앞에 배치해주세요.

# TEXT: {input}

# FORMAT:
- 요약1
- 요약2
- ...
"""

template3 = """\
# INSTRUCTION
- 다음 TEXT를 FORMAT에 맞춰 {line}줄로 요약해주세요.

# TEXT: {input}

# FORMAT:
1. 요약: <200자 이내로 요약하세요>
2. 원인:
3. 결과:
"""

template_dict = {
    "Template 1": template1,
    "Template 2": template2,
    "Template 3": template3,
    "Custom": "직접 입력해보세요",
}
#--------------------------------------------------------------------------
## Settings
#--------------------------------------------------------------------------
# 모델 불러오기
if "summary_chain" in st.session_state:
    chain = st.session_state["summary_chain"]
# 모델 생성 및 저장
else:
    prompt = PromptTemplate.from_template(template1)
    model = ChatOpenAI(model_name="gpt-4o",streaming=True)
    chain = prompt | model | StrOutputParser()

    st.session_state["summary_chain"] = chain
#--------------------------------------------------------------------------
## Functions
#--------------------------------------------------------------------------
def tab_container(tab, template, disabled=True):
    """tab의 text_area를 삽입하는 함수

    Args:
        tab (streamlit.delta_generator.DeltaGenerator): streamlit의 탭 컨테이너
        template (str): text_area에 삽입할 문자열
        disabled (bool, optional): 편집 가능 유무. Defaults to True.

    Returns:
        str: template 변수와 동일
    """
    prompt = tab.text_area(
        label="template", 
        height=270,
        value=template, 
        disabled=disabled,
        label_visibility="collapsed"
    )

    return prompt
#--------------------------------------------------------------------------
## Header
#--------------------------------------------------------------------------
# Template Examples Tab표현하기
with st.expander(label="Template Examples"):
    tabs = st.tabs(template_dict.keys())
    for i, (_, value) in enumerate(template_dict.items()):
        if i < len(template_dict) - 1:
            tab_container(tabs[i], value)
        else:
            example = tab_container(tabs[i], value, disabled=False)

# Setting 창
with st.expander(label=":gear: Settings", expanded=True):
    with st.container(border=True):
        # Line 입력
        line = st.number_input(
            label="1️⃣ 몇 줄로 요약할까요?",
            value = 5,
            max_value = 10
        )

        # Template 선택
        template = st.radio(
            label="2️⃣ 적용할 템플릿을 선택하세요",
            options = template_dict.keys(),
            horizontal=True
        )
    
    # 요약할 텍스트 입력
    with st.container(border=True):
        content = st.text_area(
            label="3️⃣ 요약할 텍스트를 입력하세요",
            height=300
        )

    # 요약 버튼
    button = st.button(
        label="Summary",
        type="primary",
        use_container_width=True
    )
#--------------------------------------------------------------------------
## Body
#--------------------------------------------------------------------------
if button:
    # 요약 출력 창
    with st.container(border=True):
        text_align("<b>Summary</b>")
        vertical_space(5)
        container = st.empty()
        handler = CustomHandler(container)
        chain.first.template = template_dict[template]
        chain.invoke(
            {"input": content, "line": line},
            {"callbacks": [handler]}
        )