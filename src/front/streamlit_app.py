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
    if "prompt" not in st.session_state:
        st.session_state.prompt = 'Default-LLM'
    if "llm_chat" not in st.session_state:
        st.session_state = model_selection(st.session_state, 'OpenAI: gpt-4o-mini', 0.5, st.session_state.prompt)
    if "memory" not in st.session_state:
        st.session_state.memory = ConversationTokenBufferMemory(llm=st.session_state.model)

    if "user_query" not in st.session_state:
        st.session_state.user_query = ""

    selected_prompt = st.selectbox("Choose system prompt", CUSTOM_PROMPTS, index=0)
    selected_model = st.selectbox("Choose model", AVAILABLE_MODELS, index=4)
    temperature = st.slider("Adjust Temperature", min_value=0.0, max_value=1.0, value=0.5, step=0.1)
    if st.button("Clean Memory", type = 'primary'):
        st.session_state.memory = ConversationTokenBufferMemory(llm=st.session_state.model)


    if (selected_model != st.session_state.model_name)|(st.session_state.temperature != temperature)|(st.session_state.prompt != selected_prompt):
        st.session_state = model_selection(st.session_state, selected_model, temperature, selected_prompt)

    st.title("🦜🔗 Chat with me!")
    saving_memory_in_file(st.session_state.memory.chat_memory.messages)
    logger.info(f"Model settings:\n- Prompt:{st.session_state.llm_chat.system_prompt}\n- Model name:{st.session_state.llm_chat.model}\n- Temperature:{st.session_state.temperature}")
    for message in st.session_state.memory.chat_memory.messages:
        if isinstance(message, HumanMessage):
            st.markdown(format_message(message.content, True), unsafe_allow_html=True)
        if isinstance(message, AIMessage):
            st.markdown(format_message(message.content, False), unsafe_allow_html=True)
    
    typing_placeholder = st.empty()
    with st.form(key='submission'):
        user_query = st.text_area("Put your question:", st.session_state.user_query)
        submitted = st.form_submit_button("Submit")
        if submitted:
            typing_placeholder.markdown(f"**Generating response...**")
        
            output = st.session_state.llm_chat(
                user_query=user_query,
                memory=st.session_state.memory
            )
            typing_placeholder.empty()
            st.session_state.memory.save_context(
                {'input': user_query},
                {'output': output}
            )
            st.session_state.user_query = " "
            st.info(output)
            st.rerun()
        
