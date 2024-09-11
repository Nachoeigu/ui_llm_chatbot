import os
from dotenv import load_dotenv
import sys

load_dotenv()
WORKDIR=os.getenv("WORKDIR")
os.chdir(WORKDIR)
sys.path.append(WORKDIR)

from constants import *
from utils import State, GraphConfig
from typing import Literal
from langgraph.graph import END


def define_next_step(state: State, config: GraphConfig) -> Literal[END, "summarizing_memory"]:
    using_summary_in_memory = config['configurable'].get("using_summary_in_memory", False)
    if using_summary_in_memory == False:
        return END
    elif len(state['messages']) > 3:
        return "summarizing_memory"
