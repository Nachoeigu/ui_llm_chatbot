import os
from dotenv import load_dotenv
import sys

load_dotenv()
WORKDIR=os.getenv("WORKDIR")
os.chdir(WORKDIR)
sys.path.append(WORKDIR)

from constants import *
from langchain.memory import ConversationTokenBufferMemory
from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain.globals import set_debug
from langchain_openai.chat_models import ChatOpenAI
from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

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
        self.parser = StrOutputParser()
        self.chain = self.prompt \
                        | self.model \
                            | self.parser         

    def __developing_prompt(self):
        return PromptTemplate(
            template="{system_prompt}\n Answer this: '{user_query}'\n{memory}",
            input_variables=["user_query","memory"],
            partial_variables={
                'system_prompt': self.system_prompt
            }
        )

    def __call__(self, user_query:str, memory:ConversationTokenBufferMemory):
        return self.chain.invoke({'user_query':user_query,
                           'memory':'' if not memory.chat_memory.messages else 'I will provide to you our chronological conversation history, use only if needed:'+str(memory.chat_memory.messages)})

