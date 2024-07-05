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
#model = ChatVertexAI(model="gemini-pro", temperature=0)
#model = ChatGoogleGenerativeAI(model = 'gemini-1.5-pro', temperature = 0)
#model = ChatOpenAI(model = 'gpt-4o', temperature = 0)
model = ChatOpenAI(model = 'gpt-3.5-turbo', temperature = 0)
memory = ConversationTokenBufferMemory(
    llm=model, 
    max_token_limit=64000
)

llm_chat = Chatbot(
    model = model,
    system_prompt = BASIC_PROMPT #CUSTOM_PROMPTS['Python-Engineer']
)
logger.info('starting')

if __name__ == '__main__':


    st.title("🦜🔗 Chat with me!")

    with st.form("my_form"):
        logger.info(memory.chat_memory.messages)
        user_query = st.text_area("Enter your question:", "I would like to know more about...")
        submitted = st.form_submit_button("Submit")
        if submitted:
            output = llm_chat(user_query=user_query,memory=memory)
            memory.save_context(
                {'Past User Message': user_query},
                {'Past AI Message': output}
            )
            st.info(output)

