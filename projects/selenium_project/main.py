# main.py
import pandas as pd
from selenium_tool import *

def get_youtube_comment(url, n_scroll=5, save_path="./") -> pd.DataFrame:
    """Youtube 댓글을 수집하는 함수"""
    # video id 추출
    video_id = get_videoid(url)
    print(f"YOUTUBE ID: {video_id}")

    # 크롬 창 열기
    print(f"1. 크롬 창을 열고 있습니다.", end=" ")
    driver = open_chrome(url)
    print(type(driver))
    print(f">>>> 완료")

    # 스크롤 다운
    scroll_down(driver, n_scroll)

    # 딕셔너리 만들기 
    print(f"2. 댓글을 가져오는 중입니다.")
    comment_data_dict = crwaling_comment(driver)

    # 데이터 프레임으로 만들기
    print(f"3. 데이터프레임으로 변환 중입니다", end=" ")
    df_comments = pd.DataFrame(comment_data_dict)
    df_comments["videoID"] = video_id
    print(">>>> 완료")

    # .csv파일로 저장
    df_comments.to_csv(save_path + "youtube_comments_crawling.csv")

    return df_comments


if __name__ == "__main__":
    # 실행 예제
    url = "https://www.youtube.com/watch?v=0BWScn_OWPk"
    youtube_comments = get_youtube_comment(url,n_scroll=1)