from langchain_core.callbacks import BaseCallbackHandler
from dotenv import load_dotenv
import os

def load_api():
    """ API KEY 셋팅 """
    load_dotenv()

    # check API KEY 
    if "OPENAI_API_KEY" not in os.environ:
        print("API KEY 정보가 없습니다. 확인 후 환경변수에 등록해주세요.")


class CustomHandler(BaseCallbackHandler):
    def __init__(self, container):
        self.container = container
        self.text = ""
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)        
    