#!/bin/bash

# Navigate to the directory of the script
cd "$(dirname "$0")"

# Activate the virtual environment
source venv/bin/activate

# Run the Streamlit app
echo "Running Streamlit app..."
streamlit run src/front/streamlit_app.py