from typing import List, Literal, Optional

import pandas as pd 
from matplotlib import rc
import matplotlib.pyplot as plt

# rc('font', family='AppleGothic') # Mac 
rc('font', family='NanumGothic')
plt.rcParams['axes.unicode_minus'] = False

def draw_barplot_by_period(
        data: pd.DataFrame, 
        period: Literal["Y", "Q", "M"], 
        palette: List[str], 
        rot: Optional[int]=90
    ) -> None:
    """기간별로 나누어 리뷰 수에 대한 막대그래프를 연도별로 색을 구분하여 그려주는 함수

    Args:
        data (pd.DataFrame): datetime 열이 포함되어 있는 데이터프레임
        period (Literal['Y', 'Q', 'M']): 표현할 기간 유형
        palette (List[str]): 연도별 구분할 색상 팔레트
        rot (Optional[int], optional): xticklabels의 회전값. 기본값은 90
    """
    fig, ax = plt.subplots(figsize=(10, 3))

    # 연도별 데이터 분리
    period_data = data.groupby(data["date"].dt.to_period("Y"))
    xticks = []
    xticklabels = []
    for year, subdata in period_data:
        # 기간별 데이터 프레임
        group = subdata.groupby(subdata["date"].dt.to_period(period)).size()
        # bar graph 그리기
        ax.bar(group.index.astype("int64"), group.values, color=palette[str(year)], label=str(year))
        # x축 값과 라벨 저장
        xticks.extend(group.index.astype("int64"))
        xticklabels.extend(group.index)
        
    # 그래프 꾸미기
    period_dict = {"Y": "연도", "Q": "분기", "M": "월"}
    ax.set_title(f"{period_dict[period]}별 리뷰 수 막대그래프")
    ax.set_xticks(xticks, labels=xticklabels, rotation=rot)
    ax.legend(loc="best")

    plt.show()