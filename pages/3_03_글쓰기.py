import streamlit as st
from utils.utils import read_mdfile, style_load
	
# llm 생성
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from utils.langchain_custom import CustomHandler

style_load()    
###########################################################################
# Page 시작
###########################################################################

st.title("짧은 글쓰기")

length = st.slider(':sparkles: 글자 수 제한', 50, 500)
keyword = st.text_input("주제를 입력해주세요")
if button := st.button("Write", type="primary"):
    
    template = f"{keyword}를 주제로 명언을 {length}자 이내로 작성해주세요."
    prompt = PromptTemplate.from_template(template)
    # container = st.empty()
    writebot = ChatOpenAI(
        model_name = "gpt-3.5-turbo",
        temperature = 0.5,
        # streaming = True,
        # callbacks = [CustomHandler(container)]
    )
    response = (prompt | writebot).stream({"keyword":keyword, "length":length})
    def stream_data():
        for chunk in response:
            yield chunk.content
    st.write_stream(stream_data)
    