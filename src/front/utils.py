import os
from dotenv import load_dotenv
import sys

load_dotenv()
WORKDIR=os.getenv("WORKDIR")
os.chdir(WORKDIR)
sys.path.append(WORKDIR)

from constants import USER_STYLE, AI_STYLE
import logging
import src.logging_config
import streamlit as st
from langchain_openai.chat_models import ChatOpenAI
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