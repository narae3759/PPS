from typing import List, Dict, Literal, Optional, Tuple, Union, Set

import pandas as pd 
import numpy as np
from matplotlib import rc
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# rc('font', family='AppleGothic') # Mac 
rc('font', family='NanumGothic')
plt.rcParams['axes.unicode_minus'] = False
from wordcloud import WordCloud
from collections import Counter

def search_review(
        data: pd.DataFrame, 
        column: str, 
        keyword: str
    ) -> pd.DataFrame:
    """키워드가 포함되어 있는 열

    Args:
        data (pd.DataFrame): 검색할 데이터프레임
        column (str): 검색할 열
        keyword (str): 검색할 키워드

    Returns:
        pd.DataFrame: 키워드가 포함된 리뷰들을 데이터프레임으로 반환
    """
    data[column] = data[column].fillna("")
    check_contain = data[column].str.contains(keyword)
    results = data.loc[check_contain,["review"]]

    return results

def compare_wordcloud(
        worddict1: Dict[str, Dict[str,int]], 
        worddict2: Dict[str, Dict[str,int]], 
        column: Literal['N', 'V'], 
        titles: List[str]
    ) -> Dict[int, Dict[str,int]]:
    """두 개의 딕셔너리에 대해 차집합을 추출하여 워드클라우드를 그려주는 함수

    Args:
        worddict1 (Dict[str, Dict[str,int]]): 첫 번째 키워드 딕셔너리
        worddict2 (Dict[str, Dict[str,int]]): 두 번째 키워드 딕셔너리
        column (Literal['N', 'V']): 비교할 품사 유형
        titles (List[str]): 워드클라우드에 입력할 제목

    Returns:
        Dict[int, Dict[str,int]]: 차집합 단어들의 키워드 딕셔너리
    """

    def filtering(words:Dict[str,int], only:Set[str]):
        """차집합 키워드만 필터링해주는 함수"""
        cloud_data = {}
        for key, value in words.items():
            if len(key) < 2 or value < 2:
                continue 

            if key in only:
                cloud_data[key] = value

        return cloud_data

    wc = WordCloud(
        font_path='./data/NanumSquareNeo-cBd.ttf', 
        background_color='white',
        width=1920,
        height=1080
    )
    column_dict = {"N": "용언(N)", "V": "체언(V)"}

    # 품사에 대한 키워드 딕셔너리 추출
    words1 = worddict1[column]
    words2 = worddict2[column]

    # 차집합 구하기
    only1 = words1.keys() - words2.keys()
    only2 = words2.keys() - words1.keys()

    # 차집합 키워드만 추출한 키워드 딕셔너리
    cloud_data1 = filtering(words1, only1)
    cloud_data2 = filtering(words2, only2)

    fig, ax = plt.subplots(1, 2, figsize=(14,5))

    # 워드 클라우드 그리기
    cloud1 = wc.generate_from_frequencies(cloud_data1)

    ax[0].imshow(cloud1, interpolation="bilinear")
    ax[0].set_title(f"{titles[0]}년에만 있는 {column_dict[column]} 키워드", fontweight="bold")

    cloud2 = wc.generate_from_frequencies(cloud_data2)

    ax[1].imshow(cloud2, interpolation="bilinear")
    ax[1].set_title(f"{titles[1]}년에만 있는 {column_dict[column]} 키워드", fontweight="bold")

    return {0: cloud_data1, 1: cloud_data2}

class WordCloudTool:
    """워드클라우드를 그리기 위한 Tool 클래스

    Attributes:
        data (pd.DataFrame): 워드클라우드를 그리기 위한 데이터프레임
        column_dict (Dict[str,str]): 품사 정보 딕셔너리
        exclude_words (Optional[List[str]], optional): 제외할 키워드. 기본값은 []
        wc (WordCloud): 워드클라우드 객체
        word_dict (Dict[int, Dict[str,int]]): 데이터프레임에서 추출된 키워드 딕셔너리

    Methods:
        draw(group, title, crange, min_length): 워드클라우드를 그리는 함수

    Private Methods: 
        _check_exclude(keyword)
            : keyword가 exclude_words에 포함되는지 확인하는 메서드
        _make_dictionary()
            : data에서 column을 추출하여 키워드 딕셔너리를 만드는 메서드
        _filtering_dict(column, crange, min_length)
            : 키워드 딕셔너리에서 조건에 맞게 추출하는 메서드
    """

    def __init__(
            self, 
            data: pd.DataFrame, 
            exclude_words: Optional[List[str]]=[]
        ):
        self.data = data
        self.column_dict = {"N": "용언(N)", "V": "체언(V)"}
        self.exclude_words = exclude_words
        self.word_dict = self._make_dictionary()
        self.wc = WordCloud(
            font_path='./data/NanumSquareNeo-cBd.ttf', 
            background_color='white',
            width=1920,
            height=1080
        )


    def _check_exclude(self, keyword:str) -> bool:
        """keyword가 exclude_words에 포함되는지 확인하는 메서드

        Args:
            keyword (str): 체크할 키워드

        Returns:
            bool: keyword가 exclude_words에 포함되어 있으면 True, 아니면 False
        """
        check = [word in keyword for word in self.exclude_words]

        if sum(check) > 0:
            return True
        else:
            return False
        
    def _make_dictionary(self):
        """data에서 column을 추출하여 키워드 딕셔너리를 만드는 메서드

        Returns:
            Dict[str, Counter]: 키워드 딕셔너리
        """
        word_dict = {}
        for column in self.column_dict:
            words = []
            for word in self.data[column]:
                if str(word) == "nan" or self._check_exclude(word):
                    continue
                words += str(word).split()
        
            counter = Counter(words)
            word_dict[column] = counter
    
        return word_dict
    
    def _filtering_dict(
            self, 
            column: str, 
            crange: Tuple[int, Union[int,float]], 
            min_length: int
        ) -> Dict[str, int]:
        """키워드 딕셔너리에서 조건에 맞게 추출하는 메서드

        Args:
            column (str): 품사에 해당하는 열 이름
            crange (Tuple[int, Union[int,float]]): 추출할 키워드 딕셔너리의 카운트 범위
            min_length (int): 키워드의 최소 길이

        Returns:
            Dict[str, int]: 추출된 키워드 딕셔너리
        """
        cmin, cmax = crange
        cloud_data = {}
        for key, value in self.word_dict[column].items():
            if len(key) < min_length:
                continue
            
            if value > cmin and value < cmax:
                cloud_data[key] = value
        
        return cloud_data

    def draw(
            self, 
            group: Optional[Literal["all","N","V"]]="all", 
            titles: Optional[Union[str,List[str]]]=None, 
            crange: Optional[Tuple[int, Union[int,float]]]=(0, np.inf), 
            min_length: Optional[int]=1
        ) -> None:
        """키워드 딕셔너리에서 조건에 맞게 추출하는 메서드

        Args:
            group (Optional[Literal["all","N","V"]], optional)
                : 출력할 품사를 나타내는 열 이름. 기본값은 "all"
            titles (Optional[Union[str,List[str]]], optional)
                : 워드클라우드에 표시할 제목. 기본값은 None
            crange (Optional[Tuple[int, Union[int,float]]], optional)
                : 워드클라우드에 나타낼 키워드 빈도수 범위. 기본값은 (0, np.inf)
            min_length (Optional[int], optional)
                : 워드클라우드에 나타낼 키워드 최소 길이. 기본값은 1
        """

        if group == "all":
            fig, ax = plt.subplots(1, 2, figsize=(14,7))

            for i, column in enumerate(self.column_dict):
                cloud_data = self._filtering_dict(column, crange, min_length)
                cloud = self.wc.generate_from_frequencies(cloud_data)

                ax[i].imshow(cloud, interpolation="bilinear")
                if titles:
                    ax[i].set_title(titles[i])
        else:
            fig, ax = plt.subplots(figsize=(7,5))

            cloud_data = self._filtering_dict(group, crange, min_length)
            cloud = self.wc.generate_from_frequencies(cloud_data)

            ax.imshow(cloud, interpolation="bilinear")
            if titles:
                ax.set_title(titles)
            
        plt.show()

