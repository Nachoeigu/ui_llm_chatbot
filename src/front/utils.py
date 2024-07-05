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

logger = logging.getLogger(__name__)

def format_message(message, is_user=True):
    style = USER_STYLE if is_user else AI_STYLE
    user_prefix = "🤓" if is_user else "🤖"
    return f"""<div style="{style}">{user_prefix} {message}</div>"""
    