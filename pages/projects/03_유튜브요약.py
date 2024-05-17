import streamlit as st
import json
from datetime import datetime 
from bs4 import BeautifulSoup, SoupStrainer
from custom_functions import *

load_style()
session_key = 'chat_history'
###########################################################################
# Page 시작
###########################################################################
## Templates
#--------------------------------------------------------------------------
template = """# INSTRUCTION
- 당신은 뉴스 정보를 전달하는 기자입니다.
- TRANSCRIPT을 FORMAT에 맞춰 한국어로 요약하세요.
- 대화의 주제에 따라 소제목으로 구분하며 그 내용을 작성합니다.
- 요약은 bullet form으로 작성하고 온점(.)으로 종결하세요.

# TRANSCRIPT: {transcript}

# FORMAT:
**소제목1**
- 내용1
- 내용2
- ...
**소제목2**
- 내용1
- 내용2
- ...
...
"""
#--------------------------------------------------------------------------
## Functions: module - youtubetool
#--------------------------------------------------------------------------
from custom_functions.youtubetool import *

#--------------------------------------------------------------------------
## Settings
#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
## Header
#--------------------------------------------------------------------------
# Insert Text
st.markdown("""
            <div class="info-container">
            📢 기능 설명
            <li> 유튜브에서 지원하고 있는 자막을 추출하고, 요약합니다.</li>
            <li> 영어 자막일 시 요약할 때 한국어로 번역됩니다.</li>
            <li> 모든 요약은 개조식 문장으로 처리됩니다.</li>
            <li> 현재 요약 가능한 시간은 30분 이내입니다.(보완 예정)</li>
            <li> Q&A 기능을 추가할 얘정입니다.</li>
            </div>
            """, unsafe_allow_html=True)

# Setting Box
with st.expander(label=":computer: Youtube URL을 입력해주세요",expanded=True):
    # Select Category
    columns = st.columns([0.85, 0.15])
    youtube_url = columns[0].text_input(
        label="텍스트",
        label_visibility="collapsed",
        value="https://www.youtube.com/watch?v=DQacCB9tDaw",
        placeholder="Youtube URL을 입력하세요."
        )
    
    # Click Button
    submit_btn = columns[1].button(
        label="Submit",
        type="primary",
        use_container_width=True
    )
#--------------------------------------------------------------------------
## Body
#--------------------------------------------------------------------------    

# When the Button is clicked
if submit_btn:
    # Embed Youtube Link
    video_container = container_align(type="center", ratio=[0.1,0.8,0.1])
    video_container.video(youtube_url)

    success = st.container()
    
    # Output Box
    with st.container(border=True):
        youtube = YoutubeTool(youtube_url)

        # Print Summary Text
        st.markdown("📋 요약")
        with st.container(border=True):
            # Extracts the script from YouTube.
            with st.spinner("유튜브에서 자막을 추출하는 중입니다..."):
                transcript = youtube.extract_transcript_deepl()
            
            # Summarizes the transcript extracted from YouTube.
            with st.spinner("유튜브 내용을 요약 중입니다..."):
                text_align(youtube.title)
                st.markdown("---")
                chain = ChainSummary(template)
                response = chain.invoke({"transcript": transcript})
        
        # Success Message
        success.success("✅ 요약 완료!")



