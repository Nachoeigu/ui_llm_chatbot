import os
from dotenv import load_dotenv
import sys
from datetime import datetime
import json

load_dotenv()
WORKDIR=os.getenv("WORKDIR")
os.chdir(WORKDIR)
sys.path.append(WORKDIR)

from constants import USER_STYLE, AI_STYLE, CUSTOM_PROMPTS
from langchain_core.messages import AIMessage, HumanMessage
import logging
from src.model import Chatbot
import src.logging_config
import streamlit as st
from langchain_openai.chat_models import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic

logger = logging.getLogger(__name__)

def format_message(message, is_user=True):
    style = USER_STYLE if is_user else AI_STYLE
    user_prefix = "🤓" if is_user else "🤖"
    return f"""<div style="{style}">{user_prefix} {message}</div>"""
    

def provide_model(selected_model:str, temperature:float=0) -> tuple:
    company, model_name = selected_model.split(':')[0].strip(), selected_model.split(':')[-1].strip()

    if company == 'OpenAI':
        return ChatOpenAI(model = model_name, temperature = temperature)
    elif company == 'Google':
        return ChatGoogleGenerativeAI(model = model_name, temperature = temperature)
    elif company == 'Anthropic':
        return ChatAnthropic(model = model_name, temperature = temperature)
    elif company == 'Groq':
        return ChatGroq(model = model_name, temperature = temperature)
    


def model_selection(session_state, selected_model:str, temperature:float, selected_prompt:str):
    session_state.model_name = selected_model
    session_state.temperature = temperature
    session_state.prompt = selected_prompt
    session_state.model = provide_model(selected_model=session_state.model_name,
                                            temperature=session_state.temperature)
    session_state.llm_chat = Chatbot(model=st.session_state.model,
                                        system_prompt=CUSTOM_PROMPTS[session_state.prompt])

    return session_state

def message_to_dict(message):
    if isinstance(message, HumanMessage):
        return {'role': 'human', 'content': message.content}
    elif isinstance(message, AIMessage):
        return {'role': 'AI', 'content': message.content}
    else:
        raise TypeError(f"Object of type {type(message)} is not JSON serializable")

def saving_memory_in_file(memory):
    history = [message_to_dict(msg) for msg in memory]
    filename = f"chat_history/{datetime.now().strftime('%Y%m%d')}.json"
    with open(filename, 'w') as f:
        json.dump(history, f, indent=4)