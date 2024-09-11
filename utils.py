import os
from dotenv import load_dotenv
import sys

load_dotenv()
WORKDIR=os.getenv("WORKDIR")
os.chdir(WORKDIR)
sys.path.append(WORKDIR)

import time
from langchain_core.pydantic_v1 import BaseModel, Field, validator
import operator
from typing import TypedDict, Annotated, List, Literal
from langchain_core.messages import AnyMessage, HumanMessage
from langchain_openai.chat_models import ChatOpenAI
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_aws.chat_models import ChatBedrock
from constants import *
import re

class GraphConfig(BaseModel):
    """
    Initial configuration to trigger the AI system.

    Attributes:
    - qa_model: Select the model for the LLM. Options include 'openai', 'google', 'meta', or 'amazon'.
    - system_prompt: Select the prompt of your conversation.
    - temperature: Select the temperature for the model. Options range from 0 to 1.
    - using_summary_in_memory: If you want to summarize previous messages, place True. Otherwise, False.
    """
    qa_model: Literal[*AVAILABLE_MODELS]
    system_prompt: Literal[*CUSTOM_PROMPTS.keys()]
    temperature: float = Field(ge=0, le=1)
    using_summary_in_memory: bool = False
    
    @validator("temperature")
    def check_temperature(cls, temperature: float):
        if (temperature < 0.0) | (temperature > 1.0):
            raise ValueError("Temperature should be between 0 and 1")
    
        return temperature

class State(TypedDict):
    messages: Annotated[List[AnyMessage], operator.add]
    summary: str


class GraphInput(TypedDict):
    """
    The initial message that starts the AI system
    """
    messages: Annotated[List[AnyMessage], operator.add]

class GraphOutput(TypedDict):
    """
    The output of the AI System
    """
    messages: List[AnyMessage]


def _get_model(config: GraphConfig):
    desired_model = config['configurable'].get('qa_model', 'OpenAI: chatgpt-4o-latest')
    temperature = config['configurable'].get('temperature', 0)
    prompt_name = config['configurable'].get('system_prompt', 'Default-LLM')
    system_prompt = CUSTOM_PROMPTS[prompt_name]
    company, model_name = desired_model.split(':')[0].strip().lower(), desired_model.split(':')[-1].strip()

    if company == "openai":
        model = ChatOpenAI(temperature=temperature, model=model_name)
    elif company == "google":
        model = ChatGoogleGenerativeAI(temperature=temperature, model=model_name)
    elif company == 'groq':
        model = ChatGroq(temperature=temperature, model=model_name)
    elif company == 'amazon':
        model = ChatBedrock(model_id =model_name, model_kwargs = {'temperature':temperature})
    else:
        raise ValueError

    return model, system_prompt


def retrieve_model_name(model):
    try:
        model_name = model.model_name
    except:
        try:
            model_name = model.model
        except:
            model_name = model.model_id

    return model_name


def adding_delay_for_rate_limits(model):
    """
    Google API and Groq API free plans has limit rates so we avoid reaching them
    """
    model_name = retrieve_model_name(model)
    if re.search('gemini|llama', model_name) is not None:
        time.sleep(6)
