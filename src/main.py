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
import logging_config

logger = logging.getLogger(__name__)
if os.getenv("LANGCHAIN_DEBUG_LOGGING") == 'True':
    set_debug(True)


if __name__ == '__main__':
    #model = ChatVertexAI(model="gemini-pro", temperature=0)
    #model = ChatGoogleGenerativeAI(model = 'gemini-1.5-pro', temperature = 0)
    #model = ChatOpenAI(model = 'gpt-4o', temperature = 0)
    model = ChatOpenAI(model = 'gpt-4o-mini', temperature = 0)
    memory = ConversationTokenBufferMemory(
        llm=model, 
        max_token_limit=64000
    )

    llm_chat = Chatbot(
        model = model,
        system_prompt= CUSTOM_PROMPTS['Default-LLM']
        #system_prompt = CUSTOM_PROMPTS['Python-Engineer']
    )

    while True:
        user_query = input("Put your question:\n")
        output = llm_chat(user_query,memory)
        print(f"Usage tokens: {output['total_tokens']}")
        memory.save_context(
            {'Past User Message': user_query},
            {'Past AI Message': output['content']}
        )
        logger.info(memory.load_memory_variables({}))