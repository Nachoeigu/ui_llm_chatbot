import os
from dotenv import load_dotenv
import sys

load_dotenv()
WORKDIR=os.getenv("WORKDIR")
os.chdir(WORKDIR)
sys.path.append(WORKDIR)

from constants import *
from src.utils import State
from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage
from src.utils import GraphConfig, _get_model, adding_delay_for_rate_limits


def answer_query(state: State, config: GraphConfig) -> State:
    model, system_prompt = _get_model(config = config)
    adding_delay_for_rate_limits(model)
    if state.get("summary", "") != "":
        output = model.invoke([SystemMessage(content = system_prompt + f'\nConsider the following summary of the conversation: <summary> {state["summary"]} </summary>')] + state['messages'])
    else:
        output = model.invoke([SystemMessage(content = system_prompt)] + state['messages'])

    return {
        "messages": [output]
    }

def summarize_memory(state: State, config: GraphConfig) -> State:
    summary = state.get("summary", "")
    if summary != "":
        summary_message = f"Extend the summary by taking into account the new messages above.\nThis is the past summary, adapt it adding info of the new messages: {summary}\n\n"
    else:
        summary_message = "Create a summary of the conversation above:"

    model, _ = _get_model(config = config)
    adding_delay_for_rate_limits(model)
    system_prompt = SystemMessage(content = "You are a helpful assistant, an expert in summarizing conversations to reduce token usage. Your task is to create concise summaries of the key points from the conversation while retaining essential details. Keep your summary short, clear, and focused on the main ideas. Remove any redundant information and avoid unnecessary details. Be mindful of token limits, but ensure the core meaning is preserved.")
    messages = [system_prompt] + state["messages"] + [HumanMessage(content=summary_message)]
    response = model.invoke(messages)
    
    return {"summary": response.content, "messages": [RemoveMessage(id=m.id) for m in state["messages"][:-2]]}
