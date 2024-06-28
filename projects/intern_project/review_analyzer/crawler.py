import logging
import time
import json
import pandas as pd
from pathlib import Path, WindowsPath
from typing import List, Literal, Optional
from review_analyzer.selenium_tool import *

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Logger 설정
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 터미널에 출력할 수 있게 함
handler = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class ReviewCrawler:
    """네이버 리뷰를 크롤링하는 클래스

    Attributes:
        url (str): 크롤링할 네이버 리뷰 페이지 URL
        n_target (Optional[int]): 목표로 하는 리뷰 수집 개수. 기본값은 200.
        sort_type (Literal["latest", "recommended"]): 리뷰 정렬 방식(최신순, 추천순)
        no_data (bool): 리뷰 데이터를 추가 수집할 수 있는 상태 유무. 기본값은 False
        driver (Optional[WebDriver]): Selenium WebDriver 인스턴스. _open_chrome 메서드에 의해 생성됨
        json_data (List[Dict[str,str]]): json 형식의 리뷰 데이터. _crawling 메서드에 의해 생성됨 
        data (pd.DataFrame): DataFrame 형식의 리뷰 데이터. _crawling 메서드에 의해 생성됨
    
    Methods:
        run(): 리뷰 크롤링 실행
        save_data(save_path): 리뷰 데이터를 save_path에 저장

    Private Methods:
        _open_chrome(): Chrome 브라우저를 생성
        _sort_and_scroll(): 리뷰 정렬 및 더보기 클릭
        _crawling(reviews): 리뷰 데이터 추출 및 수집
        _add_crawling(n_click): 리뷰 데이터 추가 수집
    """

    def __init__(
        self, 
        url: str, 
        n_target: Optional[int] = 200, 
        sort_type: Literal["latest", "recommended"] = "latest"
    ):
        self.url = url 
        self.n_target = n_target
        self.sort_type = sort_type 
        self.no_data = False
        self.driver = None 
        self.json_data = []
        self.data = None
    

    def _open_chrome(self) -> WebDriver:
        """Chrome 브라우저를 생성하는 메서드

        Returns:
            WebDriver : Selenium WebDriver 인스턴스
        """
        # 크롬창 열기
        options = Options()
        driver = webdriver.Chrome(options = options)

        # 창모드 전체화면으로 크기 늘리기
        driver.maximize_window()

        # 로딩시간: 페이지 로딩
        loading(driver)

        # 네이버 리뷰 주소 접속하기
        driver.get(self.url)

        # 로딩시간: 페이지 로딩
        loading(driver)

        return driver

    def _sort_and_scroll(self) -> List[WebElement]:
        """리뷰 정렬 방식과 더보기를 클릭하는 메서드

        Returns:
            List[WebElement] : 리뷰에 해당하는 WebElement 객체 리스트
        """
        # 최신순으로 정렬
        if self.sort_type == "latest":
            self.driver.find_elements(By.CLASS_NAME, "zMIkw")[-1].click()

        # 목표 수집 댓글 수를 결정하는 경우
        while True:
            more_btn = find_element_by_class(self.driver, "fvwqf")

            # 더 보기 버튼 안보이면 break
            if not more_btn: 
                self.no_data = True
                break
            
            more_btn.click()
            time.sleep(0.5)

            # 목표 리뷰 개수 도달하면 break
            reviews = self.driver.find_elements(By.CLASS_NAME, "owAeM")
            if len(reviews) > self.n_target:
                # print("목표 리뷰 개수 도달")
                break
        
        # 전체 리뷰 추출
        reviews = self.driver.find_elements(By.CLASS_NAME, "owAeM")
        
        return reviews

    def _crawling(self, reviews: List[WebElement]) -> None:
        """리뷰 데이터 추출 및 수집하는 메서드

        Args:
            reviews (List[WebElement]): 리뷰에 해당하는 WebElement 객체 리스트
        """
        for review in reviews:
            review_json = {}

            text_area = review.find_elements(By.CLASS_NAME, "xHaT3")
            # 긴 글일 경우 내용 더보기 클릭
            if len(text_area) == 2:
                text_area[0].click()
                time.sleep(1)

            content = review.find_element(By.CLASS_NAME, "zPfVt")
            # 텍스트가 없으면 수집하지 않기
            if not content.text:
                continue
            
            # 세부 정보 추출
            info_content = ""
            if find_element_by_class(review, "MnhVd"):
                additional_infos = review.find_elements(By.CLASS_NAME, "xalSr")
                info_content = ", ".join([x.text for x in additional_infos])
            
            # 리뷰 데이터 저장
            review_json["reviewer"] = review.find_element(By.CLASS_NAME, "P9EZi").text
            review_json["review"] = content.text
            review_json["additional_info"] = info_content

            visit_keys = ["date", "n_visit", "auth_method"]
            visit_info = review.find_elements(By.CLASS_NAME, "CKUdu")
            for key, info in zip(visit_keys, visit_info):
                review_json[key] = info.text.split("\n")[-1].strip()

            # 데이터에 추가
            self.json_data.append(review_json)

    def _add_crawling(self, n_click: int) -> None:
        """리뷰 데이터를 추가 수집하는 메서드

        Args:
            n_click (int): 더보기 버튼 클릭 수
        """
        for _ in range(n_click):
            more_btn = find_element_by_class(self.driver, "fvwqf")

            # 더 보기 버튼 안보이면 break
            if not more_btn: break
            
            more_btn.click()
            time.sleep(0.5)
        
        reviews = self.driver.find_elements(By.CLASS_NAME, "owAeM")[-n_click*10:]
        self._crawling(reviews)

    def run(self) -> None:
        """전체 리뷰 크롤링을 실행하는 함수"""
        logger.debug(f"==========START CRAWLING==========")
        logger.debug(f"URL: {self.url}")

        self.driver = self._open_chrome()
        reviews = self._sort_and_scroll()

        logger.debug(f"{len(reviews)}개의 리뷰를 추출합니다. >>> 텍스트인 리뷰만 수집됩니다.")

        self._crawling(reviews)
        logger.debug(f"수집된 리뷰는 {len(self.json_data)}개 입니다.")
        
        n_add = self.n_target - len(self.json_data)
        if self.no_data:
            logger.debug(f"더 이상 수집할 데이터가 없습니다.")
        elif n_add > 0:
            n_click = int(n_add // 10) + 1
            logger.debug(f"목표 수집량을 위해 추가 수집합니다.")
            self._add_crawling(n_click)
        
        self.data = pd.json_normalize(self.json_data)
        logger.debug(f"최종 수집된 리뷰는 {len(self.json_data)}개 입니다.")
        logger.debug(f"========== END  CRAWLING==========")

    def save_data(self, save_path: str) -> None:
        """리뷰 데이터를 save_path에 저장하는 메서드

        Args:
            save_path (str): 저장할 파일 경로
        """
        if isinstance(save_path, WindowsPath):
            save_path = save_path.as_posix()

        if save_path[-4:] == "json":
            with open(save_path, "w", encoding="utf-8") as json_file:
                json.dump(self.json_data, json_file, indent=4, ensure_ascii=False)
        else:
            self.data.to_csv(save_path, index=False, encoding="utf-8")

        logger.debug(f"SUCCESS! PATH: {save_path}")


if __name__ == "__main__":
    # url = "https://pcmap.place.naver.com/restaurant/1804344332/review/visitor" # 리뷰 적은 곳
    url = "https://pcmap.place.naver.com/restaurant/13166754/review/visitor" # 리뷰 많은 곳

    # 리뷰 분석기 인스턴스 생성
    crawler = ReviewCrawler(url, n_target=200)
    
    # 리뷰 분석기 실행
    crawler.run()

    # 리뷰 데이터 저장
    crawler.save_data("data/naver_review_raw_data.json")
    crawler.save_data("data/naver_review_raw_data.csv")