import os
from dotenv import load_dotenv
import sys

load_dotenv()
WORKDIR=os.getenv("WORKDIR")
os.chdir(WORKDIR)
sys.path.append(WORKDIR)

from constants import *
from langchain_core.chat_history import InMemoryChatMessageHistory

from langchain.memory import ConversationTokenBufferMemory
from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain.globals import set_debug
from langchain_openai.chat_models import ChatOpenAI
from langchain_google_vertexai import ChatVertexAI
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain.output_parsers import PydanticOutputParser
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory

import logging
import src.logging_config


logger = logging.getLogger(__name__)
if os.getenv("LANGCHAIN_DEBUG_LOGGING") == 'True':
    set_debug(True)


class Chatbot:

    def __init__(self, model, system_prompt:str=''):
        self.model = model
        self.system_prompt = system_prompt
        self.prompt = self.__developing_prompt()
        self.history = InMemoryChatMessageHistory()
        self.parser = StrOutputParser()
        self.chain = self.prompt \
                        | self.model \
                            | self.parser
        
        self.chain_with_memory = RunnableWithMessageHistory(
            self.chain,
            lambda input: self.history,
            history_messages_key="chat_history",
        )

    def __developing_prompt(self):
        return ChatPromptTemplate(
            [
                ('system',self.system_prompt),
                ("placeholder", "{chat_history}"),
                ("human", "{input}"),
            ]
            )

    def __call__(self, user_query:str, memory:ConversationTokenBufferMemory):
        self.history = InMemoryChatMessageHistory(messages = memory.buffer_as_messages)
        return self.chain_with_memory.invoke({'input':user_query}, config = {'configurable': {'session_id': 'localhost'}})
