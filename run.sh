#!/bin/bash

# Load environment variables from .env file securely
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

export LANGCHAIN_TRACING_V2="true"
export LANGCHAIN_PROJECT="healthcare-agentic-ai"

# Start the FastAPI backend in the background
uvicorn main:app --reload --port 8000 &

# Start the Streamlit frontend
streamlit run streamlit_app.py
