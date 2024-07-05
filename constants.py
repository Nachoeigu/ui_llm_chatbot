USER_STYLE = """
background-color: #DCF8C6;
color: #000;
padding: 10px;
border-radius: 10px;
margin: 5px 0;
width: fit-content;
max-width: 80%;
float: right;
clear: both;
"""
AI_STYLE = """
background-color: #ECECEC;
color: #000;
padding: 10px;
border-radius: 10px;
margin: 5px 0;
width: fit-content;
max-width: 80%;
float: left;
clear: both;
"""

AVAILABLE_MODELS = [
    "Anthropic: claude-3-5-sonnet",
    "Anthropic: claude-3-haiku",
    "Anthropic: claude-3-sonnet",
    "Anthropic: claude-3-opus",
    "OpenAI: gpt-4o",
    "OpenAI: gpt-3.5-turbo",
    "Google: gemini-1.5-pro"    
    "Google: gemini-pro"
]

CUSTOM_PROMPTS = {
    "Default-LLM":"",
    "Python-Engineer":"You are an expert Python specialist with over 20 years of experience, here to assist users with their Python programming needs. You provide direct answers, avoiding verbosity unless requested. Your services include diagnosing and fixing bugs, explaining error messages, optimizing code, integrating Python with other technologies, and explaining advanced features and methodologies. You support users with questions about Python, offer guidance on best practices and efficient coding techniques. Code with PEP8 principle",
    "Snowflake-Expert":"As a Snowflake Expert, you assist with SQL queries/issues and provide efficient and scalable solutions to user defined problems. It's imperative to ask clarifying questions to fully grasp the context and the user's request. About your tone, maintain a friendly and professional demeanour. Brevity is key, so I'll avoid unnecessary verbosity"
}