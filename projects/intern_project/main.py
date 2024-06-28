from review_analyzer import * 
from pathlib import Path

def main():
    # url = "https://pcmap.place.naver.com/restaurant/1804344332/review/visitor" # 리뷰 적은 곳
    url = "https://pcmap.place.naver.com/restaurant/13166754/review/visitor" # 리뷰 많은 곳

    # 리뷰 분석기 인스턴스 생성
    crawler = ReviewCrawler(url, n_target=200)

    # 리뷰 분석기 실행
    crawler.run()

    # 리뷰 데이터 저장
    path = Path("./projects/intern_project/data")
    filename = "naver_review_raw_data"
    try:
        crawler.save_data(path / f"{filename}.json")
        crawler.save_data(path / f"{filename}.csv")
    except:
        crawler.save_data(f"./{filename}.json")
        crawler.save_data(f"./{filename}.csv")

# python main.py
if __name__ == "__main__":
    main()