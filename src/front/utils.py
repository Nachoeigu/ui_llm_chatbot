import os
from dotenv import load_dotenv
import sys

load_dotenv()
WORKDIR=os.getenv("WORKDIR")
os.chdir(WORKDIR)
sys.path.append(WORKDIR)

from constants import USER_STYLE, AI_STYLE


def format_message(message, is_user=True):
    style = USER_STYLE if is_user else AI_STYLE
    user_prefix = "🤓" if is_user else "🤖"
    return f"""
    <div style="{style}">
        <strong>{user_prefix}</strong> {message}
    </div>
    """