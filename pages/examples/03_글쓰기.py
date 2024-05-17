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
            <li> 사용자가 작성한 키워드를 기반으로 레시피를 추천합니다. </li>
            <li> 다양한 예제로 바꿀 예정입니다. </li>
            </div>
            """, unsafe_allow_html=True)

# col1, col2 = st.columns(2)

# with col1:
#     length = st.number_input(':sparkles: 글자 수 제한', value=100, step=50, format="%d")

keywords = st_tags(
    label="냉장고에 있는 재료를 입력해주세요.",
    text='Enter를 입력하세요',
    value=["단호박", "우유", "치즈"],
    maxtags = 10,
    key='1')

if button := st.button("Write", type="primary"):
    
    template = """
    INGREDIENTS로 만들 수 있는 다이어트 레시피를 FORMAT에 맞춰 알려주세요.
    준비물은 무게 단위까지 자세히 작성해야 합니다.

    INGREDIENTS: {ingredients}
    
    FORMAT:
    요리명:
    준비물: 
    칼로리:
    방법:
    1. 
    2. 
    ...
    """
    prompt = PromptTemplate.from_template(template)
    # container = st.empty()
    writebot = ChatOpenAI(
        model_name = "gpt-3.5-turbo",
        temperature = 0.5,
        # streaming = True,
        # callbacks = [CustomHandler(container)]
    )
    response = (prompt | writebot).stream({"ingredients":keywords})
    def stream_data():
        for chunk in response:
            yield chunk.content
    st.write_stream(stream_data)
