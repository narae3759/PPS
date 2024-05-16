import streamlit as st
from custom_functions import *

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate 
from langchain_core.output_parsers import StrOutputParser 

load_style()
###########################################################################
# Page 시작
###########################################################################
## Templates 
#--------------------------------------------------------------------------
options = ["Template1(단순 요약)", "Template2(리스트 요약)", "Template3(커스텀 요약)"]

opt_index = {opt:i for i, opt in enumerate(options)}
templates = {i:opt for i, opt in enumerate(options)}

templates[0] = """# INSTRUCTION
TEXT를 {line}줄로 요약해주세요. 각 문장은 높임말로 작성해주세요.

# TEXT: {text}
"""

templates[1] = """# INSTRUCTION
- 다음 TEXT를 FORMAT에 맞춰 {line}줄로 요약해주세요.
- 정량적으로 표현될 수 있는 요약을 맨 앞에 배치해주세요.

# TEXT: {text}

# FORMAT:
- 요약1
- 요약2
- 요약3
"""

templates[2] = """# INSTRUCTION
- 다음 TEXT를 FORMAT에 맞춰 {line}줄로 요약해주세요.

# TEXT: {text}

# FORMAT:
1. 요약:
2. 원인:
3. 결과:
"""
#--------------------------------------------------------------------------
## Header
#--------------------------------------------------------------------------
# Insert Text
st.markdown("""
            <div class="info-container">
            📢 기능 설명
            <li> LLM은 문서를 요약할 수 있습니다. </li>
            <li> Template을 통해 원하는 형식으로 출력이 가능합니다. </li>
            <li> 텍스트 입력, URL 입력, PDF 입력 모두 가능합니다. (웹 보완 예정) </li>
            </div>
            """, unsafe_allow_html=True)

# Setting Box
with st.expander(label=":gear: Settings",expanded=True):

    col1, col2 = st.columns(2)

    ### Select Options
    with col1:
        with st.container(border=True, height=250):
            line = st.number_input(
                label=':one: 몇 줄로 요약할까요?', 
                value=5, 
                format="%d"
            )
            
            radios = st.radio(
                label=":two: 요약 템플릿을 선택하세요",
                options=options
            )
    ### Template Example
    with col2:
        with st.container(border=True, height=250):
            st.markdown("<div style='font-size:0.9rem'>🎈 Examples</div>", unsafe_allow_html=True)
            tabs = st.tabs(["Template1", "Template2", "Template3"])
            for i in range(3):
                isdisable = False if i == 2 else True
                tabs[i].text_area(
                    label="요약 템플릿",
                    value=templates[i],
                    label_visibility="collapsed",
                    key=f"template{i}",
                    height=130,
                    disabled=isdisable
                )
                
    ### TextBox
    with open("./exercise/example.txt", 'r', encoding='utf-8') as f:
        example_text = f.read()

    with st.container(border=True):
        content = st.text_area(
            label=":three: 요약하고 싶은 텍스트를 입력하세요",
            value=example_text,
            height=200
        )

### click button 
button = st.button(
    label="텍스트 요약하기",
    use_container_width=True,
    type="primary"
)
#--------------------------------------------------------------------------
## Body
#--------------------------------------------------------------------------

# When the Button is clicked
if button:
    with st.container(border=True):
        # Title
        text_align("Summary")
        vertical_space(3)

        # Summary
        chain = ChainSummary(templates[opt_index[radios]])
        response = chain.invoke({"line": line, "text": content})
