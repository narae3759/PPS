import streamlit as st
from pathlib import Path 

def read_mdfile(file):
    md_text = Path(file).read_text(encoding="utf-8")
    st.markdown(md_text, unsafe_allow_html=True)


