import os
import logging
from datetime import datetime
from pathlib import Path
import shutil

from email import policy
from email.message import EmailMessage
from email.parser import BytesParser

from typing import Dict
from bs4 import BeautifulSoup

import pdfkit

# Logger 설정
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class Eml2Pdf:
    """EML 파일을 PDF로 변환해주는 클래스"""

    def __init__(self, filepath:str, wkhtmltopdf_path:str):
        """Eml2Pdf 초기화 함수

        Args:
            filepath (str): eml 파일 경로
            wkhtmltopdf_path (str): wkhtmltopdf.exe의 경로
        """
        # 파일 경로 설정
        path = Path(filepath)
        self.files = []

        ## 예외 처리
        if not (path.is_file() or path.is_dir()):
            logger.error(f"eml 파일 경로를 찾을 수 없습니다.(PATH: {filepath})", exc_info=False)
        else:         
            ## 파일일 경우
            if path.is_file():
                self.directory = path.parent
                self.files = [path]
            ## 폴더일 경우
            elif path.is_dir():
                self.directory = path
                self.files = path.glob("*.eml")
    
            ## 기타 경로 설정
            self.output_dir = self.directory.parent / "outputs"
            self.image_dir = self.directory / "images"
            if not self.image_dir.is_dir():
                os.mkdir(self.image_dir)
        
        # PDFkit 설정
        if not os.path.isfile(wkhtmltopdf_path):
            logger.error("wkhtmltopdf.exe 경로를 찾을 수 없습니다.", exc_info=False)
        else:
            self.config = pdfkit.configuration(
                wkhtmltopdf=wkhtmltopdf_path
            )
            self.options = {
                "encoding": "UTF-8",
                "enable-local-file-access": None
            }

    def _get_message(self, filepath) -> EmailMessage:
        """eml에서 message를 추출하는 함수

        Returns:
            EmailMessage : eml 파일에서 추출한 message 객체
        """
        try:
            with open(filepath, 'rb') as eml_file:
                message = BytesParser(policy=policy.default).parse(eml_file)
        except:
            message = None

        return message
    
    def _get_headers(self) -> Dict :
        """message에서 header 정보를 추출하는 함수
        
        Returns:
            Dict : message 객체에서 추출한 header 정보 딕셔너리
        """
        header_list = ["Subject", "To", "From", "Cc", "BCc", "Date", "AttachedFiles"]
        headers = {key: "" for key in header_list}

        for key in headers:
            if key in self.message:
                headers[key] = self.message[key].replace('<', '&lt;').replace('>', '&gt;')
            else:
                headers[key] = ""

        return headers
    
    def _get_content(self) -> str:
        """message에서 본문 정보를 추출하는 함수
        본문 정보는 텍스트, 이미지, 첨부파일로 이루어져 있으며
        _get_headers의 AttachedFiles를 업데이트 한다.

        Returns:
            str : message 객체에서 추출한 본문 html 텍스트
        """
        img_sources = {}
        attached_files = []
        self.headers = self._get_headers()

        # message 순회
        for part in self.message.walk():
            content_type = part.get_content_type()
            disposition = part.get_content_disposition()
            filename = part.get_filename()

            # 텍스트 추출
            if content_type == "text/html":
                try:
                    html_content = part.get_payload(decode=True).decode()
                except:
                    html_content = part.get_payload(decode=True).decode("CP949")
            # 이미지 추출
            if disposition == "inline":
                cid = part.get("Content-ID").strip("<>")

                file_path = self.image_dir / part.get_filename()
                with open(file_path, 'wb') as img_file:
                    img_file.write(part.get_payload(decode=True))
                
                img_sources[cid] = file_path.resolve()
            # 첨부파일 추출
            elif disposition == "attachment":
                attached_files.append(f"- {filename}")
        
        # src 이미지 경로 업데이트
        soup = BeautifulSoup(html_content, features="lxml")
        img_tags = soup.find_all("img")
        for img in img_tags:
            cid = img["src"].lstrip("cid:")
            img["src"] = img_sources[cid]
        html_content = str(soup)

        self.headers["AttachedFiles"] = '\n'.join(attached_files)

        return html_content
    
    def eml2html(self) -> str:
        """message 내용을 html로 변환하는 함수
        
        Returns:
            str : message 객체에서 추출한 정보로 만든 최종 html 텍스트
        """
        html_content = self._get_content()
        html_header = f"""
        <div class="header">
            <p style='font-size:24px;'><strong>제목:</strong> {self.headers['Subject']}</p>
            <p><strong>보낸사람:</strong> {self.headers['From']}</p>
            <p><strong>받는사람:</strong> {self.headers['To']}</p>
            <p><strong>참조:</strong> {self.headers['Cc']}</p>
            <p><strong>숨은참조:</strong> {self.headers['BCc']}</p>
            <p><strong>보낸날짜:</strong> {self.headers['Date']}</p>
            <p><strong>첨부파일:</strong><br> {self.headers['AttachedFiles']}</p>
        </div>
        """
        

        html_text = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: 맑은 고딕; }}
                .header {{ font-size: 13px; }}
            </style>
        </head>
        <body>
            <hr>
            {html_header}
            <hr>    
            {html_content}
        </body>
        </html>
        """

        return html_text
    
    def html2pdf(self, filename):
        """html 텍스트를 pdf로 저장하는 함수"""
        self.html_text = self.eml2html()

        # 보낸날짜 추출
        send_date = self.headers["Date"]
        format = "%a, %d %b %Y %H:%M:%S %z"
        insert_date = datetime.strptime(send_date, format).strftime("(%y%m%d)")
        savepath = self.output_dir / f"{insert_date + filename}.pdf"

        # Output 디렉토리 생성하는 함수
        if not os.path.isdir(self.output_dir):
            os.mkdir(self.output_dir)
        
        # PDF 저장
        pdfkit.from_string(
            self.html_text,
            savepath,
            configuration=self.config,
            options=self.options
        )

        return savepath

    def run(self):
        try:
            # 파일 변환
            idx = 1
            for filepath in self.files:
                self.message = self._get_message(filepath)
                if self.message:
                    filename = filepath.stem
                    savepath = self.html2pdf(filename)
                    
                    # 로그 
                    logger.debug(f"SUCCESS! {idx}. SAVE_PATH: {savepath}")
                    idx += 1
            
            # image 폴더 삭제
            try:
                shutil.rmtree(self.image_dir)
            except:
                pass

        except StopIteration:
            logger.error("변환할 eml 파일이 없습니다.", exc_info=False)

        except Exception as e:
            print(e.__class__.__name__, e)
            # pass


if __name__ == "__main__":
    # 사용 예시
    wkhtmltopdf="C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"
    eml_filepath = 'eml_folder/[피피에스] 사업 공고 전달의 건.eml'
    eml_dir = 'inputs'

    tool = Eml2Pdf(eml_dir, wkhtmltopdf)
    tool.run()
