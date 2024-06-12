import streamlit as st 
from custom_functions.langchain_tool import *
from langchain_community.callbacks import StreamlitCallbackHandler


class Chat:
    def __init__(self, chain, session_key):
        self.session_key = session_key
        self.chain = chain

    def greeting(self, message):
        st.chat_message("assistant").markdown(message)
        st.session_state[self.session_key].append({
            "role": "assistant",
            "content": message
        })

    def input_user(self, message):
        st.chat_message("user").markdown(message)
        st.session_state[self.session_key].append({
            "role": "user",
            "content": message
        })

    def input_assistant(self, question):
        with st.chat_message("assistant"):
            container = st.empty()
            handler = CustomHandler(container)
            answer = self.chain.invoke(
                {"input": question},
                {"callbacks": [handler]}
            )
            # print(answer)

        st.session_state[self.session_key].append({
            "role": "assistant",
            "content": answer
        })

        return answer


        