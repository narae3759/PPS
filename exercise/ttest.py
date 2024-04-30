from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def main():
    # Chrome WebDriver 생성
    options = Options()
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    
    # 웹 페이지로 이동
    driver.get("https://www.naver.com")

    # 검색어 입력 
    input_box = driver.find_element(By.CSS_SELECTOR, "#query")
    input_box.send_keys("Python")
    driver.find_element(By.CSS_SELECTOR, "#search-btn").click()
    
    # 로드 될 때까지 대기
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    
    # driver.quit()

main()