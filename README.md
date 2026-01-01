# GitHub Agent - Learn Agent Creation with Python

A simple AI agent that automates GitHub operations through natural language commands. 

## What This Project Does

This agent uses a local LLM to understand user commands and automatically:
- Create GitHub repositories
- Add files to repositories
- Handle GitHub operations via REST API

## How to Use This for Learning

This project demonstrates core agent concepts:
1. **Natural Language Processing**: Uses llama.cpp to parse user intent
2. **Structured Output**: Converts commands to JSON actions
3. **API Integration**: Executes actions via GitHub REST API
4. **Agent Loop**: Continuously listens and responds to commands

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv .venv`
3. Activate it: `source .venv/bin/activate`
4. Install dependencies: `pip install llama-cpp-python python-dotenv requests`
5. Download a GGUF model and place it in `models/model.gguf`
6. Create `.env` file (see `.env.example`)
7. Run: `python terminal_chat.py`

## Example Commands

```
You: create a repo called my-test-project
You: add a file README.md with "Hello World" to my-test-project
```

