import os
from dotenv import load_dotenv

def load_api(api_name:str):
    """환경변수에서 API KEY를 불러오는 함수

    Args:
        api_name (str): api 환경변수 이름
    """
    load_dotenv()

    if api_name not in os.environ:
        print(f"{api_name} 정보가 없습니다. 확인 후 환경변수에 등록해주세요.")