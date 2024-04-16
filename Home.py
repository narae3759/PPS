# python -m streamlit run script.py
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
## author
st.markdown('''<div style="text-align:right;font-size:12;">
                <b>작성자: 김나래 연구원<b>
            </div>''', unsafe_allow_html=True)



## Reference
st.divider()
st.markdown("### 📃 Reference")

tab1, tab2 = st.tabs(["✨ Streamlit", "🦜️ Langchain"])
with tab1:
    st.markdown(
        """
        * 🔗 [Streamlit 공식 문서](https://docs.streamlit.io/develop/api-reference/chat)
        * 🔗 [Streamlit Components 모음](https://streamlit.io/components)
        * 🔗 [Streamlit Sidebar github](https://github.com/blackary/st_pages)
        """
    )
with tab2:
    st.markdown(
        """
        * 🔗 [Langchain 공식 문서](https://python.langchain.com/docs/get_started/introduction)
        * 🔗 [Langchain 번역 문서(written by 테디노트)](https://wikidocs.net/book/14314)
        * 🔗 [Langchain 강의(모두의 AI)](https://www.youtube.com/watch?v=WWRCLzXxUgs)
        """
    )
