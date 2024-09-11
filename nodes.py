import os
from dotenv import load_dotenv
import sys

load_dotenv()
WORKDIR=os.getenv("WORKDIR")
os.chdir(WORKDIR)
sys.path.append(WORKDIR)

from constants import *
from utils import State
from langchain_core.messages import SystemMessage
from utils import GraphConfig, _get_model, adding_delay_for_rate_limits

def answer_query(state: State, config: GraphConfig) -> State:
    model, system_prompt = _get_model(config = config)
    adding_delay_for_rate_limits(model)
    output = model.invoke([SystemMessage(content = system_prompt)] + state['messages'])

    return {
        "messages": [output]
    }

def read_human_feedback(state: State) -> State:
    pass
