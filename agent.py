import os
from dotenv import load_dotenv
import sys

load_dotenv()
WORKDIR=os.getenv("WORKDIR")
os.chdir(WORKDIR)
sys.path.append(WORKDIR)

from langgraph.graph import StateGraph
from utils import State, GraphInput, GraphOutput, GraphConfig
from nodes import *

def defining_nodes(workflow: StateGraph):
    workflow.add_node("llm", answer_query)
    workflow.add_node("human_feedback", read_human_feedback)

    return workflow

def defining_edges(workflow: StateGraph):
    workflow.add_edge("llm","human_feedback")
    workflow.add_edge("human_feedback","llm")

    return workflow


workflow = StateGraph(State, 
                      input = GraphInput,
                      output = GraphOutput,
                      config_schema = GraphConfig)

workflow.set_entry_point("llm")
workflow = defining_nodes(workflow = workflow)
workflow = defining_edges(workflow = workflow)

app = workflow.compile(
    interrupt_before=['human_feedback']
    )



if __name__ == '__main__':
    from langchain_core.messages import HumanMessage
    from langgraph.checkpoint.memory import MemorySaver
    app = workflow.compile(
        interrupt_before=['human_feedback'],
        checkpointer=MemorySaver()
    )

    human_input_msg = "Hi"
    
    configuration = {
        "configurable": {
            "thread_id": 42,
            "qa_model":"Groq: gemma-7b-it",
            "temperature":0,
            "system_prompt":"Default-LLM"
        }
    }

    for event in app.stream(
            input = {'messages': [HumanMessage(content=human_input_msg)]},
            config = configuration,
            stream_mode='values'):
        
        type_msg = event['messages'][-1].type
        msg = event['messages'][-1].content
        print(type_msg.upper() + f": {msg}")
