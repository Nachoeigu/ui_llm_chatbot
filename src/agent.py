import os
from dotenv import load_dotenv
import sys

load_dotenv()
WORKDIR=os.getenv("WORKDIR")
os.chdir(WORKDIR)
sys.path.append(WORKDIR)

from langgraph.graph import StateGraph, END
from src.utils import State, GraphInput, GraphOutput, GraphConfig
from src.nodes import *
from src.router import *

def defining_nodes(workflow: StateGraph):
    workflow.add_node("llm", answer_query)
    workflow.add_node("summarizing_memory", summarize_memory)

    return workflow

def defining_edges(workflow: StateGraph):
    workflow.add_conditional_edges(
        "llm",
        define_next_step)
    workflow.add_edge("summarizing_memory", END)

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
    from langchain_core.messages import HumanMessage, AIMessage
    from langgraph.checkpoint.memory import MemorySaver
    import uuid
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)
    config = {"configurable": {"thread_id": "1",
                               "qa_model": "OpenAI : chatgpt-4o-latest",
                               "temperature": 0,
                               "system_prompt": "Default-LLM",
                               "using_summary_in_memory": True}}
    while True:
        input_msg = input("Question: ")
        if input_msg.lower() in ['exit','quit','q']:
            break
        input_message = HumanMessage(content=input_msg, id = str(uuid.uuid4()))
        output = app.invoke({"messages": [input_message]}, config) 
        
        print("AI: ", [msg for msg in output['messages'] if isinstance(msg, AIMessage)][-1].content)
