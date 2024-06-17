import streamlit as st
from streamlit_tags import st_tags
from custom_functions import *
	
# llm 생성
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.schema import AIMessage, HumanMessage, SystemMessage

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
- N행시란 WORD의 글자마다 짧은 글을 짓는 게임을 말합니다. 
- 글의 내용은 CONCEPT에 맞춰 EXAMPLES에 따라 N행시를 생성하세요.
- 마크다운의 리스트 형식으로 출력하세요

# WORD: {input}

# CONCEPT: {concept}

# EXAMPLES:
- 사: 사랑하는 사람과 함께
- 이: 이 세상 모든 것을 나누고파
- 다: 다정한 마음으로 행복을 만들어 함께하자
"""

template2 = """\
# INSTRUCTION
- 당신은 레시피를 추천해주는 역할입니다.
- INGREDIENTS는 현재 사용자가 가지고 있는 음식 재료입니다.
- INGREDIENTS가 먹을 수 없는 재료라면 그 재료의 이름과 함께 다시 요청해주세요.
- FORMAT에 맞춰 답변하세요.

# INGREDIENTS: {ingredients}

# FORMAT:<마크다운 리스트 형식으로 표현하세요>
- **요리명**: <볼드체로 표현하세요, 최종 소요시간을 괄호()로 표현해주세요>
- **난이도**: <'상/중/하'로 표현하세요>
- **재료**: <재료(무게)를 상세히 작성하세요>
- **칼로리**: <Kcal 단위로 작성하세요>
- **요리 순서**: <지속 시간과 행동을 상세히 작성하세요>
1. 
2. 
...
"""

template3 = """\
# INSTRUCTION
- 당신은 공공기관의 마케팅부서를 도와주는 역할입니다.
- TOPIC에서 주제를 추출한 후, 그에 대한 아이디어 10개를 제시합니다.
- COLUMNS에 따라 내용을 한국어 표로 작성하세요.

# TOPIC: {topic}

# COLUMNS:
- NO <아이디어 번호> 
- Title <아이디어 주제, 20자 이내로 작성하세요>
- Description <아이디어 상세 내용, 500자 이내로 작성하세요>
"""

templates = [template1, template2, template3]
#--------------------------------------------------------------------------
## Settings
#--------------------------------------------------------------------------
# 모델 생성 및 저장
if "gen_chain1" not in st.session_state:
    model = ChatOpenAI(model_name="gpt-3.5-turbo",streaming=True)
    for i, template in enumerate(templates):
        prompt = PromptTemplate.from_template(template)
        chain = prompt | model

        st.session_state[f"gen_chain{i+1}"] = chain
#--------------------------------------------------------------------------
## Functions
#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
## Header
#--------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["1️⃣ **N행시**", "2️⃣ **레시피 작성**", "3️⃣ **아이디어 기획**"])
#--------------------------------------------------------------------------
## Body 1 - N행시
#--------------------------------------------------------------------------
with tab1:
    with st.container(border=True):
        concept = st.radio(
            label="⭐ 출력 스타일을 선택하세요",
            options=["유머","명언","감성","건배사"],
            horizontal=True
        )

        word, tab1_button = one_line_btn(
            ratio=[0.75,0.25],
            placeholder="N행시할 단어를 입력하세요",
            btnlabel="Submit"
        )

    if tab1_button:
        if not word:
            st.error("단어가 입력되지 않았습니다.",icon="🚨")
        else:
            chain = st.session_state["gen_chain1"] | StrOutputParser()
            with st.container(border=True):
                text_align("<b>출력 결과</b>")
                vertical_space(5)
                container = st.empty()
                handler = CustomHandler(container)
                chain.invoke(
                    {"input": word, "concept":concept},
                    {"callbacks": [handler]}
                )

#--------------------------------------------------------------------------
## Body 2 - 레시피 작성
#--------------------------------------------------------------------------
with tab2:
    keywords = st_tags(
        label="냉장고에 있는 재료를 입력해주세요.",
        text='Enter를 입력하세요',
        value=["단호박", "우유", "치즈"],
        maxtags = 10)
    
    if tab2_button := st.button("Write", type="primary"):
        chain = st.session_state["gen_chain2"] | StrOutputParser()
        with st.container(border=True):
            text_align("<b>추천 레시피</b>")
            vertical_space(5)
            container = st.empty()
            handler = CustomHandler(container)
            response = chain.invoke(
                {"ingredients": keywords},
                {"callbacks": [handler]}
            )
            # print(response)

#--------------------------------------------------------------------------
## Body 3 - 아이디어 표로 작성
#--------------------------------------------------------------------------
with tab3:
    with st.container(border=True):
        topic, tab3_button = one_line_btn(
            ratio=[0.75,0.25],
            placeholder="마케팅 기획 목적을 작성하세요",
            btnlabel="Generate"
        )
    
    if tab3_button:
        chain = st.session_state["gen_chain3"] | StrOutputParser()
        with st.container(border=True):
            text_align("<b>홍보 아이디어 기획</b>")
            vertical_space(5)
            container = st.empty()
            handler = CustomHandler(container)
            response = chain.invoke(
                {"topic": topic},
                {"callbacks": [handler]}
            )
        
            vertical_space(10)
