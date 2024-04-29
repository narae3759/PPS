# python -m streamlit run Home.py
import streamlit as st
from utils.utils import read_mdfile
from utils.custom_style import load_style

load_style()
###########################################################################
# Page 시작
###########################################################################
## author
st.markdown('''<div style="text-align:right;font-size:12;">
                <b>작성자: 김나래 연구원<b>
            </div>''', unsafe_allow_html=True)

## Docs 링크
st.markdown("📌 LLM 소개, 기능 테스트를 위한 사이트입니다.")
st.markdown("📌 간략한 예제를 준비했으며 앞으로 기능들을 구체적으로 개발할 예정입니다.")
st.markdown("📌 공부한 내용을 따로 정리하고 있습니다.(📚 Docs 보러가기 [↗](https://github.com/narae3759/PPS/wiki), 업데이트 예정입니다.)")

## 설명
read_mdfile("./docs/home.md")
