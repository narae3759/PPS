# youtube_crawling.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium_tool.utils import *

from typing import Dict

def open_chrome(url) -> WebDriver:
    """크롬 창을 생성하여 url로 이동하는 함수"""
    # 크롬 창 열기
    options = Options()
    driver = webdriver.Chrome(options = options)

    # 창모드 전체화면으로 크기 늘리기
    driver.maximize_window()
    
    # 로딩시간
    loading(driver)
    
    # 유튜브 주소 접속하기
    driver.get(url)
    
    # 유튜브 로딩시간
    loading(driver, element=(By.ID, "below"))

    # 동영상 재생되면 멈춤
    video_pause(driver)

    return driver

def crwaling_comment(driver) -> Dict:
    """댓글 딕셔너리를 만드는 함수
    
    Returns:
        dict: {
            "UserID": [],
            "Comment": [],
            "Likes": []
        }
    """
    # 데이터를 담을 빈 딕셔너리 만들기
    comment_data_dict = {"UserID": [], "Comment":[],"Likes":[]}

    # 댓글 불러오기
    number_comments = driver.find_elements(By.CLASS_NAME, 'style-scope ytd-comment-view-model')
    print(f"-불러올 댓글 수: {len(number_comments)}")

    # loop를 통해 데이터 받기 및 저장하기
    cnt = 0
    print("-START", end=" ")
    for i in range(len(number_comments)):
        # 텍스트 추출
        user_id = driver.find_elements(By.CSS_SELECTOR, '#author-text')[i].text
        comment_text = driver.find_elements(By.CSS_SELECTOR, "#content-text")[i].text
        num_likes = driver.find_elements(By.XPATH, '//*[@id="vote-count-middle"]')[i].text

        # comment_data_dict 딕셔너리에 데이터 넣기
        comment_data_dict["UserID"].append(user_id[1:])
        comment_data_dict["Comment"].append(comment_text)
        comment_data_dict["Likes"].append(num_likes)

        # 로그 프린트
        cnt += 1
        if cnt > 0 and cnt % 20 == 0:
            print(cnt, end=" > ")
    print("End")

    return comment_data_dict
