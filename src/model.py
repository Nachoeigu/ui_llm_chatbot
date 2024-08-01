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
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain.output_parsers import PydanticOutputParser
from langchain_core.messages import AIMessage, HumanMessage

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
                            | {'content': self.parser, 'total_tokens': RunnableLambda(lambda model_output: model_output.to_json()['kwargs']['usage_metadata']['total_tokens']) }

    def __developing_prompt(self):
        return PromptTemplate(
            template="{system_prompt}\n Answer this: '{user_query}'{memory}",
            input_variables=["user_query","memory"],
            partial_variables={
                'system_prompt': self.system_prompt
            }
        )

    def __call__(self, user_query:str, memory:ConversationTokenBufferMemory):
        return self.chain.invoke({'user_query':user_query,
                           'memory':'' if not memory.chat_memory.messages else '\nBELOW OUR CHRONOLOGICAL CHAT HISTORY (use only if needed):\n ```\n'+ '\n'.join([f"USER: {msg.content}" if isinstance(msg, HumanMessage) else f"AI: {msg.content}" for msg in memory.chat_memory.messages]) + '\n´´´'})


if __name__ == '__main__':
    from langchain_openai.chat_models import ChatOpenAI
    from langchain_google_vertexai import ChatVertexAI
    #model = ChatOpenAI(model = 'gpt-4o', temperature = 0)
    model = ChatGoogleGenerativeAI(model = 'gemini-1.5-pro', temperature = 0)
    output = Chatbot(model = model, system_prompt=CUSTOM_PROMPTS['Default-LLM'])('hi', memory = ConversationTokenBufferMemory(llm = model, max_token_limit=10000))

