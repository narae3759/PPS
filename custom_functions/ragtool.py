import os
import json 
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from bs4 import SoupStrainer 
from langchain import hub 
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

import logging 
logging.basicConfig(level=logging.INFO)

class NewsRAG:
    def __init__(self, keyword):
        self.keyword = keyword
        self.text_splitter = RecursiveCharacterTextSplitter
        self.vectorstore = Chroma 
        self.embeddings = OpenAIEmbeddings 
        self.prompt = hub.pull("rlm/rag-prompt")
        self.model = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0
        )

        self.urls = self._search_naver_news()
        self.retriever = self._make_retriever()
        self.chain = (
            {"context": self.retriever | self.format_docs, 
            "question": RunnablePassthrough()}
            | self.prompt
            | self.model
            | StrOutputParser()
        )

    def _search_naver_news(self):
        # Make Request URL
        base_url = "https://openapi.naver.com/v1/search/news?"
        params = {
            "query": self.keyword,
            "display": 20,
            "sort": "sim"
        }
        headers = {
            "X-Naver-Client-Id": os.getenv("NAVER_CLIENT_ID"),
            "X-Naver-Client-Secret": os.getenv("NAVER_SECRET_KEY")
        }

        url = base_url + urlencode(params)
        
        # Get response 
        request = Request(url, headers=headers)
        response = urlopen(request)

        # Get Text
        response_text = response.read().decode("utf-8")
        response_json = json.loads(response_text)

        # Extract URL
        urls = [url["link"] for url in response_json["items"] if "naver" in url["link"]]

        return urls

    def _load_documents(self):
        loader = WebBaseLoader(
            web_paths=tuple(self.urls),
            bs_kwargs=dict(
                parse_only=SoupStrainer(
                    class_=["media_end_head_headline","go_trans _article_content"]
                )
            )
        )

        docs = loader.load()

        return docs

    def _split_text(self):
        docs = self._load_documents()
        splitter = self.text_splitter(chunk_size=1000, chunk_overlap=200)
        splits = splitter.split_documents(docs)

        return splits
    
    def _make_retriever(self):
        vs = self.vectorstore.from_documents(
            documents=self._split_text(),
            embedding=self.embeddings()
        )

        retriever = vs.as_retriever()

        return retriever
    
    @staticmethod
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    def invoke(self, question):
        answer = self.chain.invoke(question)

        return answer

# class NewsRAG:
#     def __init__(self, keyword):
#         self.keyword = keyword
#         self.text_splitter = RecursiveCharacterTextSplitter
#         self.vectorstore = Chroma 
#         self.embeddings = OpenAIEmbeddings 
#         self.prompt = hub.pull("rlm/rag-prompt")
#         self.model = ChatOpenAI(
#             model_name="gpt-3.5-turbo",
#             temperature=0
#         )

#         self.urls = self._search_naver_news()
#         self.retriever = self._make_retriever()
#         self.chain = (
#             {"context": self.retriever | self.format_docs, 
#             "question": RunnablePassthrough()}
#             | self.prompt
#             | self.model
#             | StrOutputParser()
#         )

#     def _search_naver_news(self):
#         # Make Request URL
#         base_url = "https://openapi.naver.com/v1/search/news?"
#         params = {
#             "query": self.keyword,
#             "display": 20,
#             "sort": "sim"
#         }
#         headers = {
#             "X-Naver-Client-Id": os.getenv("NAVER_CLIENT_ID"),
#             "X-Naver-Client-Secret": os.getenv("NAVER_SECRET_KEY")
#         }

#         url = base_url + urlencode(params)
        
#         # Get response 
#         request = Request(url, headers=headers)
#         response = urlopen(request)

#         # Get Text
#         response_text = response.read().decode("utf-8")
#         response_json = json.loads(response_text)

#         # Extract URL
#         urls = [url["link"] for url in response_json["items"] if "naver" in url["link"]]

#         return urls

#     def _load_documents(self):
#         loader = WebBaseLoader(
#             web_paths=tuple(self.urls),
#             bs_kwargs=dict(
#                 parse_only=SoupStrainer(
#                     class_=["media_end_head_headline","go_trans _article_content"]
#                 )
#             )
#         )

#         docs = loader.load()

#         return docs

#     def _split_text(self):
#         docs = self._load_documents()
#         splitter = self.text_splitter(chunk_size=1000, chunk_overlap=200)
#         splits = splitter.split_documents(docs)

#         return splits
    
#     def _make_retriever(self):
#         vs = self.vectorstore.from_documents(
#             documents=self._split_text(),
#             embedding=self.embeddings()
#         )

#         retriever = vs.as_retriever()

#         return retriever
    
#     @staticmethod
#     def format_docs(docs):
#         return "\n\n".join(doc.page_content for doc in docs)
    
#     def invoke(self, question):
#         answer = self.chain.invoke(question)

#         return answer

if __name__ == "__main__":
    keyword = "훈련병 사망"

    rag = NewsRAG(keyword)
    answer = rag.invoke("훈련병은 왜 사망했어?")
    print(answer)

