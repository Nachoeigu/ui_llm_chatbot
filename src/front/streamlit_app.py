import os
from dotenv import load_dotenv
import sys

load_dotenv()
WORKDIR=os.getenv("WORKDIR")
os.chdir(WORKDIR)
sys.path.append(WORKDIR)

from constants import *
from src.model import Chatbot
from langchain.memory import ConversationTokenBufferMemory
from langchain.globals import set_debug
from langchain_openai.chat_models import ChatOpenAI
from langchain_google_vertexai import ChatVertexAI
import logging
import src.logging_config
import streamlit as st

logger = logging.getLogger(__name__)
if os.getenv("LANGCHAIN_DEBUG_LOGGING") == 'True':
    set_debug(True)

if __name__ == '__main__':
    if "llm_chat" not in st.session_state:
        #st.session_state.model = ChatVertexAI(model="gemini-pro", temperature=0)
        #st.session_state.model = ChatGoogleGenerativeAI(model = 'gemini-1.5-pro', temperature = 0)
        st.session_state.model = ChatOpenAI(model = 'gpt-4o', temperature = 0)
        #st.session_state.model = ChatOpenAI(model = 'gpt-3.5-turbo', temperature = 0)
        st.session_state.llm_chat = Chatbot(
            model = st.session_state.model,
            system_prompt = CUSTOM_PROMPTS['Python-Engineer']
        )
    if "memory" not in st.session_state:
        st.session_state.memory = ConversationTokenBufferMemory(
            llm=st.session_state.model, 
            max_token_limit=64000
        )

    if "token_usage" not in st.session_state:
        st.session_state.token_usage = 0

    st.title("🦜🔗 Chat with me!")

    with st.form("my_form"):
        logger.info(st.session_state.memory.chat_memory.messages)
        user_query = st.text_area("Enter your question:", "I would like to know more about...")
        submitted = st.form_submit_button("Submit")
        if submitted:
            output = st.session_state.llm_chat(
                user_query=user_query,
                memory=st.session_state.memory
            )
            st.session_state.memory.save_context(
                {'Past User Message': user_query},
                {'Past AI Message': output['content']}
            )
            st.session_state.token_usage += output['total_tokens']

            st.info(output)
