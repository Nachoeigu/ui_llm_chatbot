@echo off
REM Navigate to the directory of the script
cd /d "%~dp0"

REM Activate the virtual environment
call venv\Scripts\activate.bat

REM Run the Streamlit app
echo Running Streamlit app...
streamlit run src/front/streamlit_app.py