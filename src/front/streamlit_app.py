import os
from dotenv import load_dotenv
import sys

load_dotenv()
WORKDIR = os.getenv("WORKDIR")
os.chdir(WORKDIR)
sys.path.append(WORKDIR)

from src.front.utils import format_message, model_selection, saving_memory_in_file
from constants import AVAILABLE_MODELS, CUSTOM_PROMPTS
from langchain_core.messages import AIMessage, HumanMessage
from langchain.memory import ConversationTokenBufferMemory
from langchain.globals import set_debug
import logging
import src.logging_config
import streamlit as st

logger = logging.getLogger(__name__)
if os.getenv("LANGCHAIN_DEBUG_LOGGING") == 'True':
    set_debug(True)

if __name__ == '__main__':
    st.set_page_config(
        initial_sidebar_state="expanded",
        page_title="AI Chatbot",
        page_icon="⚡",
        layout="wide"
    )
    if "prompt" not in st.session_state:
        st.session_state.prompt = 'Default-LLM'
        
    if "llm_chat" not in st.session_state:
        st.session_state = model_selection(st.session_state, 'OpenAI: gpt-4o-mini', 0.5, st.session_state.prompt)
    if "memory" not in st.session_state:
        st.session_state.memory = ConversationTokenBufferMemory(llm=st.session_state.model, max_token_limit=300000)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "input_question" not in st.session_state:
        st.session_state.input_question = ''

    selected_prompt = st.selectbox("**CHOOSE SYSTEM PROMPT**", CUSTOM_PROMPTS, index=0)
    selected_model = st.selectbox("**CHOOSE MODEL**", AVAILABLE_MODELS, index=7)
    temperature = st.slider("**SET TEMPERATURE**", min_value=0.0, max_value=1.0, value=0.5, step=0.1)
    if st.button("Clean Memory", type = 'primary'):
        st.session_state.memory = ConversationTokenBufferMemory(llm=st.session_state.model)


    if (selected_model != st.session_state.model_name)|(st.session_state.temperature != temperature)|(st.session_state.prompt != selected_prompt):
        st.session_state = model_selection(st.session_state, selected_model, temperature, selected_prompt)
    saving_memory_in_file(st.session_state.memory.chat_memory.messages)
    logger.info(f"Model settings:\n- Prompt:{st.session_state.llm_chat.system_prompt}\n- Model name:{st.session_state.llm_chat.model}\n- Temperature:{st.session_state.temperature}")
    with st.chat_message("system"):
        if st.session_state.prompt == 'Default-LLM':
            pass
        else:
            st.markdown(CUSTOM_PROMPTS[st.session_state.prompt])

    for message in st.session_state.memory.chat_memory.messages:
        if isinstance(message, HumanMessage):
            role = "user"
        elif isinstance(message, AIMessage):
            role = "assistant"
        with st.chat_message(role):
            st.markdown(message.content)    
    if user_query := st.chat_input("Put your messages here..."):
        # Display user message in chat message container
        st.chat_message("user").markdown(user_query)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_query})

        response = f"Echo: {user_query}"
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            output = st.session_state.llm_chat(
                user_query=user_query,
                memory=st.session_state.memory
            )
            st.markdown(output)
        
        st.session_state.memory.save_context(
                {'input': user_query},
                {'output': output}
            )
            
        st.rerun()

