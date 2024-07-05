import os
from dotenv import load_dotenv
import sys

load_dotenv()
WORKDIR=os.getenv("WORKDIR")
os.chdir(WORKDIR)
sys.path.append(WORKDIR)

from langchain.memory import ConversationBufferWindowMemory, ConversationTokenBufferMemory
from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain.globals import set_debug
from langchain_openai.chat_models import ChatOpenAI
from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts import ChatPromptTemplate

import logging
import logging_config


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
            template="{system_prompt}\n{user_query}\n{memory}",
            input_variables=["user_query","memory"],
            partial_variables={
                'system_prompt': self.system_prompt
            }
        )

    def __call__(self, user_query:str):
        return self.chain.invoke({'user_query':user_query,
                           'memory':memory})

if __name__ == '__main__':
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
        system_prompt = 'You are an expert in Sciences and know how to explain things to 5 years old kids'
    )

    while True:
        user_query = input("Put your question:\n")
        output = llm_chat.chain.invoke({
            'user_query': user_query,
            'memory': '' if not memory.chat_memory.messages else str(memory.chat_memory.messages)
        })
        logger.info(output)
        memory.save_context(
            {'user': user_query},
            {'ai_message': output}
        )
        logger.info(memory.load_memory_variables({}))
