# python -m streamlit run Home.py
# python ../PPS-note/auto_updating.py
import streamlit as st
from custom_functions.utils import read_mdfile
from custom_functions.custom_style import load_style

load_style()
###########################################################################
# Page 시작
###########################################################################

## 설명
st.image("https://imgur.com/MjLsmXQ.png")
read_mdfile("./docs/home.md")
