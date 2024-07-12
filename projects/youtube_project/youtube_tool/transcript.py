import deepl 
from youtube_tool.utils import *
from pathlib import Path

from pytube import Playlist, YouTube
from youtube_transcript_api import YouTubeTranscriptApi

def translate_with_deepl(transcript:str, target_lang="KO") -> str:
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

def extract_transcripts(url:str, savedir="output"):
    """유튜브 자막을 텍스트파일로 저장하는 함수

    Args:
        url (str): 플레이리스트 URL
        savedir (str): 저장할 디렉토리 (Default: )
    """
    # 저장 폴더 만들기
    savepath = Path(savedir)

    if not savepath.is_dir():
        savepath.mkdir(parents=True, exist_ok=True)

    # 정보 추출
    youtube = YouTube(url)
    video_id = youtube.video_id
    video_title = youtube.title.replace(":","")

    # 자막 추출
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["ko"], preserve_formatting=True)
        lang = "ko"
    except:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"], preserve_formatting=True)
        lang = "en"

    # 텍스트로 변환
    transcript_text = " ".join([x["text"] for x in transcript])

    # 영어면 번역
    if lang == "en":
        transcript_text = translate_with_deepl(transcript_text).replace(". ", "\n")

    # 저장
    with open(savepath / f"{video_title}.txt", 'w', encoding="utf-8") as txt_file:
        txt_file.write(transcript_text)

        print(f"SUCCESS SAVE FILE: {video_title}")


def extract_playlist_transcripts(url:str, savedir="output"):
    """플레이리스트의 자막들을 텍스트파일로 저장하는 함수

    Args:
        url (str): 플레이리스트 URL
        savedir (str): 저장할 디렉토리 (Default: )
    """
    # 저장 폴더 만들기
    savepath = Path(savedir)

    if not savepath.is_dir():
        savepath.mkdir(parents=True, exist_ok=True)

    # 플레이리스트 불러오기
    playlist = Playlist(url)

    for idx, video in enumerate(playlist,1):
        # 정보 추출
        youtube = YouTube(video)
        video_id = youtube.video_id
        video_title = youtube.title.replace(":","")

        # 자막 추출
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["ko"], preserve_formatting=True)
            lang = "ko"
        except:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"], preserve_formatting=True)
            lang = "en"

        # 텍스트로 변환
        transcript_text = " ".join([x["text"] for x in transcript])

        # 영어면 번역
        if lang == "en":
            transcript_text = translate_with_deepl(transcript_text).replace(". ", "\n")

        # 저장
        with open(savepath / f"{video_title}.txt", 'w', encoding="utf-8") as txt_file:
            txt_file.write(transcript_text)

        print(f"SUCCESS SAVE FILE: ({idx}/{len(playlist)}) {video_title}")