from typing import Tuple

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 함수
def loading(
        driver: WebDriver, 
        element: Tuple[str, str] = (By.TAG_NAME, "body")
    ) -> None:
    """페이지가 로딩될 때까지 기다리는 함수
    
    Args:
        driver (WebDriver): Selenium WebDriver 인스턴스
        element (Tuple[str, str], optional) 기다릴 요소를 지정하는 튜플
            첫번째 항목: By 클래스의 속성(ex. By.TAG_NAME, By.CLASS_NAME 등)
            두번째 항목: 첫번째 항목에 대한 값
            기본값: (By.TAG_NAME, "body")
    """
    # 로딩시간
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located(element))

def find_element_by_class(
        driver: WebDriver, 
        class_name: str
    ) -> WebElement | None:
    """WebElement를 찾지 못하면 None으로 반환하는 함수
    
    Args:
        driver (WebDriver): Selenium WebDriver 인스턴스
        class_name (str): 찾고자 하는 element의 클래스 이름
    Returns:
        WebElement | None: 찾은 WebElement 객체. 요소가 없으면 None으로 반환
    """
    try:
        element = driver.find_element(By.CLASS_NAME, class_name)
    except:
        element = None
    
    return element 