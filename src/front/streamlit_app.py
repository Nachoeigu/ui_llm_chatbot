import os
from dotenv import load_dotenv
import sys

load_dotenv()
WORKDIR=os.getenv("WORKDIR")
os.chdir(WORKDIR)
sys.path.append(WORKDIR)

from src.front.utils import format_message
from constants import *
from langchain_core.messages import AIMessage, HumanMessage
from src.model import Chatbot
from langchain.memory import ConversationTokenBufferMemory
from langchain.globals import set_debug
from langchain_openai.chat_models import ChatOpenAI
from langchain_google_vertexai import ChatVertexAI
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
import logging
import src.logging_config
import streamlit as st

logger = logging.getLogger(__name__)
if os.getenv("LANGCHAIN_DEBUG_LOGGING") == 'True':
    set_debug(True)

if __name__ == '__main__':
    if "llm_chat" not in st.session_state:
        #st.session_state.model = ChatOpenAI(model = 'gpt-3.5-turbo', temperature = 0)
        st.session_state.model = ChatGoogleGenerativeAI(model = 'gemini-1.5-pro', temperature = 0)
        st.session_state.llm_chat = Chatbot(
            model = st.session_state.model,
            system_prompt = BASIC_PROMPT #CUSTOM_PROMPTS['Python-Engineer']
        )
    if "memory" not in st.session_state:
        st.session_state.memory = ConversationTokenBufferMemory(
            llm=st.session_state.model, 
            max_token_limit=64000
        )

    if "token_usage" not in st.session_state:
        st.session_state.token_usage = 0

    if "user_query" not in st.session_state:
        st.session_state.user_query = ""

    st.title("🦜🔗 Chat with me!")

    st.header("Chat history: Memory of the LLM")
    for message in st.session_state.memory.chat_memory.messages:
        if isinstance(message, HumanMessage):
            st.markdown(format_message(message.content, True), unsafe_allow_html=True)
        if isinstance(message, AIMessage):
            st.markdown(format_message(message.content, False), unsafe_allow_html=True)

    st.markdown(f"**Total Consumed Tokens:** {st.session_state.token_usage}")
    with st.form(key='submission'):
        user_query = st.text_area("Put your question:", st.session_state.user_query)
        submitted = st.form_submit_button("Submit")
        if submitted:
            output = st.session_state.llm_chat(
                user_query=user_query,
                memory=st.session_state.memory
            )
            st.session_state.memory.save_context(
                {'input': user_query},
                {'output': output['content']}
            )
            logger.info(f"Consumption of tokens in this message:\n{output['total_tokens']}")
            st.session_state.token_usage += output['total_tokens']
            logger.info(f"Consumption of tokens in total conversation:\n{st.session_state.token_usage}")
            st.session_state.user_query = ""
            st.info(output['content'])
            logger.info(st.session_state.memory.chat_memory.messages)
            st.rerun()
