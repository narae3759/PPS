import streamlit as st
from utils.utils import read_mdfile, style_load
	
# llm 생성
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from utils.langchain_custom import CustomHandler

style_load()
###########################################################################
# Page 시작
###########################################################################

col1, col2 = st.columns(2)

with col1:
    line = st.number_input(':sparkles: 몇 줄로 요약할까요?', value=5, format="%d")

## example
example_txt = """서울 강동구 주택가에서 불이 나 주민 3명이 대피하는 일이 벌어졌다. 해당 화재는 반려묘가 전기레인지를 작동시켜 화재가 발생한 것으로 추정된다.

소방당국에 따르면 지난 17일 오전 10시 46분께 강동구 천호동의 6층짜리 주택 2층에서 화재가 발생했다. 화재는 약 40분 만에 진화됐다.

이번 화재로 인해 소방 인력 63명과 차량 17대가 출동했다. 이 과정에서 주민 3명이 자력으로 대피했다. 다행히 인명피해는 없었으나 약 300만원의 재산 피해가 발생한 것으로 추정된다.

소방 당국은 거주자가 집을 비운 사이 고양이가 전기레인지를 작동시켜 화재가 발생한 것으로 보고 자세한 사고 원인을 조사 중에 있다.

소방청에 따르면 지난 2020년부터 3년간 반려동물로 인한 화재는 2020년 103건, 2021년 127건, 2022년 157건 등으로 총 387건이 발생했으며, 14억 원의 재산피해가 발생했다.

주로 동물들이 전기레인지나 인덕션의 전원을 눌러 주변의 종이나 냄비 등에 착화돼 발생하거나 전선·콘센트를 동물들이 물어 합선 혹은 단락이 일어나고, 털과 배설물이 유입되어 누전으로 인한 화재가 발생하기도 한다.

특히 전원 버튼을 손가락으로 터치해 작동시키는 전기레인지의 경우 사람 손가락뿐 아니라 반려동물의 발바닥에도 반응한다는 제주도소방안전본부의 실험 결과가 있다. 지난 1일 대전광역시 서구에서도 반려묘에 의해 주방 전기레인지가 작동해 발생한 것으로 추정되는 화재가 일어난 바 있다.

높은 곳에 올라가는 것을 좋아하는 고양이의 특성상 주방 전기레인지에 뛰어 올라가는 일이 잦아 전기레인지를 작동시켜 화재로 이어지는 것으로 추정된다. 이에 최근 고양이를 키우는 가정에서는 사고를 방지하기 위해 전기레인지에 덮개를 씌우는 등 자구책을 마련하고 있다.

소방청 관계자는 외출 전 전기레인지를 비롯한 각종 콘센트의 전원을 차단하고, 전기레인지 주변에 불이 옮겨붙을 만한 물질을 제거하는 것이 좋다고 충고했다."""



prompt = st.text_area("요약할 텍스트를 입력하세요", value=example_txt, height=200)
st.write(f"{len(prompt)}자 입력 중...")

if button := st.button("Sumarize", type="primary"):
    
    message = [
            SystemMessage(
                content = f"{line}줄로 요약하는데 존댓말로 해주세요."
            ),
            HumanMessage(
                content = prompt
            ),
        ]
    
    container = st.empty()
    summbot = ChatOpenAI(
        model_name = "gpt-3.5-turbo",
        temperature = 0.5,
        streaming = True,
        callbacks = [CustomHandler(container)]
    )
    response = summbot.invoke(message)