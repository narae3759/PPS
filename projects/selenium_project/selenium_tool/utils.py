# utils.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from urllib.parse import parse_qs

def loading(driver, element=(By.TAG_NAME, "body")):
    """페이지가 로딩될 때까지 기다리는 함수"""
    # 로딩시간
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located(element))

def video_pause(driver):
    """비디오를 정지하는 함수"""
    video = driver.find_element(By.TAG_NAME, "video")
    ispause = driver.execute_script("return arguments[0].paused;", video)
    if not ispause:
        driver.execute_script("arguments[0].pause();", video)

def scroll_down(driver, n_scroll):
    """페이지를 n_scroll번 스크롤다운 하는 함수"""
    # 댓글창이 보여야 활성화 되기 때문에 살짝 내리는 과정 필요
    driver.execute_script("window.scrollTo(0, 280);")
    time.sleep(2)
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    for i in range(n_scroll):
        # 내린다
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(2)
        # 비교
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def get_videoid(url:str) -> str:
    """URL에서 videoid 추출하는 함수"""
    query = parse_qs(url.split('?')[-1])
    videoid = query["v"][0]

    return videoid