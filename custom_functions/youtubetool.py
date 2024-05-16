import os
from urllib.parse import parse_qs
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import deepl 
from .utils import *

class YoutubeTool():
    """유튜브를 저장, 자막 추출 및 번역하는 클래스

    Args:
        url (str): 유튜브 링크
        path (str): 저장할 디렉토리
    """
    def __init__(self, url:str, path=None):
        self.youtube = YouTube(url)
        self.title = self.youtube.title
        self.path = self.path if path else './'
        self.transcript = ''

        # URL 파싱
        query = parse_qs(url.split("?")[-1])
        self.video_id = query["v"][0]    

        # 지원되는 자막 언어 확인
        self.transcript_list = YouTubeTranscriptApi.list_transcripts(self.video_id)
        self.available_langs = list(set([lang.language_code for lang in self.transcript_list]))
        print(f"지원되는 자막: {self.available_langs}")

        # 경로 탐색 후 디렉토리 생성
        if not os.path.exists(self.path):
            os.mkdirs(self.path)


    def download(self, type="both", filename=None, extension="mp4"):
        """유튜브를 다운로드 하는 함수

        Args:
            type (str, optional): 추출할 스트림 방식. both(Default), video, audio
            filename (str): 저장할 파일 이름
            extension (str, optional): 저장할 파일 확장자
        """
        filename = filename if filename else self.title

        # type에 맞는 파라미터 탐색
        filter_key = {"both": {"progressive":True, "file_extension":extension},
                      "video": {"only_video":True, "file_extension":extension},
                      "audio": {"only_audio":True}}
        
        # 필터링
        youtube = YouTube(url)
        if type == "audio":
            stream = youtube.streams.filter(**filter_key[type]).first()
        else:
            stream = youtube.streams.filter(**filter_key[type]).order_by("resolution").desc().first()

        # 다운로드
        if not stream:
            print("오디오 스트림을 찾을 수 없습니다.")
        else:      
            stream.download(self.path, f"{filename}.{extension}")

    def extract_transcript(self, lang=None, save=False, filename=None):
        """유튜브에서 사용자가 원하는 언어에 맞춰 추출하는 함수

        Args:
            lang (str, optional): 추출하고 싶은 자막 언어
            save (bool) : 저장 여부(Default: False)
            filename (str, optional): 저장하고 싶은 파일 이름

        Returns:
            full_script (str): 추출된 자막 텍스트
        """
        lang = lang if lang else self.available_langs[0]
        filename = filename if filename else self.title

        # 스크립트 추출
        if lang in self.available_langs[0]:
            self.transcript = self.transcript_list.find_transcript([lang]).fetch()
        else:
            transcript_default = self.transcript_list.find_transcript([self.available_langs[0]]).fetch()
            self.transcript = transcript_default.translate(lang).fetch()
        
        # 스크립트 텍스트 병합
        full_script = " ".join([script["text"] for script in self.transcript])

        # 파일 저장
        if save:
            with open(f'{filename}({lang}).txt', 'w', encoding='utf-8') as f:
                f.write(full_script)

        return full_script

    def extract_transcript_deepl(self, lang=None, save=False, filename=None):
        """유튜브에서 사용자가 원하는 언어에 맞춰 추출하는 함수(번역 시 deepl 사용)

        Args:
            lang (str, optional): 추출하고 싶은 자막 언어
            save (bool) : 저장 여부(Default: False)
            filename (str, optional): 저장하고 싶은 파일 이름

        Returns:
            full_script (str): 추출된 자막 텍스트
        """
        lang = lang if lang else self.available_langs[0]
        filename = filename if filename else self.title

        # 지원하는 언어일 때
        if lang in self.available_langs[0]:
            # 스크립트 추출
            self.transcript = self.transcript_list.find_transcript([lang]).fetch()
            
            # 스크립트 텍스트 병합
            full_script = " ".join([script["text"] for script in self.transcript])
        
        # 지원하지 않는 언어일 때 
        else:
            # 기본 스크립트 추출
            transcript_default = self.transcript_list.find_transcript([self.available_langs[0]]).fetch()
            
            # 기본 스크립트 텍스트 병합
            default_script = " ".join([script["text"] for script in transcript_default])

            # 번역
            full_script = translate_with_deepl(default_script, target_lang=lang)

        # 파일 저장
        if save:
            with open(f'{filename}({lang}).txt', 'w', encoding='utf-8') as f:
                f.write(full_script)

        return full_script

def translate_with_deepl(transcript:str, target_lang="KO"):
    """DeepL로 번역하는 함수

    Args:
        transcript (str): 번역할 텍스트
        target_lang (str, optional): 번역하고 싶은 언어(Default: "KO")

    Returns:
        result.text (str): 번역된 텍스트
    """
    # API KEY 불러오기
    load_api("DEEPL_API_KEY")

    # 번역하기
    target_lang = "EN-US" if target_lang=="en" else target_lang.upper()
    translator = deepl.Translator(os.getenv("DEEPL_API_KEY"))
    result = translator.translate_text(transcript, target_lang=target_lang)

    return result.text

# 실행
if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=DQacCB9tDaw"
    
    youtube = YoutubeTool(url)
    # youtube.download()
    # transcript = youtube.extract_transcript_deepl('ko')
    # transcript = youtube.extract_transcript_deepl('ko')
