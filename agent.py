import os
from dotenv import load_dotenv
import sys

load_dotenv()
WORKDIR=os.getenv("WORKDIR")
os.chdir(WORKDIR)
sys.path.append(WORKDIR)

from langgraph.graph import StateGraph, END
from utils import State, GraphInput, GraphOutput, GraphConfig
from nodes import *

def defining_nodes(workflow: StateGraph):
    workflow.add_node("llm", answer_query)

    return workflow

def defining_edges(workflow: StateGraph):
    workflow.add_edge("llm",END)

    return workflow


workflow = StateGraph(State, 
                      input = GraphInput,
                      output = GraphOutput,
                      config_schema = GraphConfig)

workflow.set_entry_point("llm")
workflow = defining_nodes(workflow = workflow)
workflow = defining_edges(workflow = workflow)

app = workflow.compile()

if __name__ == '__main__':
    from langchain_core.messages import HumanMessage
    from langgraph.checkpoint.memory import MemorySaver
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)
    config = {"configurable": {"thread_id": "1",
                               "qa_model": "OpenAI: chatgpt-4o-latest",
                               "temperature": 0,
                               "system_prompt": "Default-LLM"}}
    while True:
        input_msg = input("Question: ")
        input_message = HumanMessage(content=input_msg)
        output = app.invoke({"messages": [input_message]}, config) 
        for m in output['messages'][-1:]:
            m.pretty_print()
