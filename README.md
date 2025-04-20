# AI Journalist Agent

An automated article generation tool that uses AI to research, analyze, and write high-quality articles on any topic.

## Overview

AI Journalist Agent is a Streamlit web application that leverages CrewAI and LangChain to create a multi-step journalistic workflow. The application can:

1. Research topics using SerperDev search
2. Analyze and summarize found sources
3. Write well-structured articles tailored to specific styles and audiences

## Features

- **🔍 AI-powered Research**: Automatically finds relevant and authoritative sources on any topic
- **📊 Content Analysis**: Extracts and summarizes key information from web sources
- **✍️ Smart Article Generation**: Creates structured, well-written articles with proper formatting
- **🎨 Customizable Outputs**: Configure article length, style, and target audience
- **📱 User-Friendly Interface**: Simple, intuitive Streamlit interface with progress tracking

## Installation

1. Clone this repository
```bash
git clone https://github.com/yourusername/ai-journalist.git
cd ai-journalist
```

2. Install required packages
```bash
pip install -r requirements.txt
```

3. Set up API keys
   - Get an OpenAI API key from [OpenAI](https://openai.com)
   - Get a SerperDev API key from [Serper](https://serper.dev)

## Usage

1. Run the Streamlit application
```bash
streamlit run app.py
```

2. Enter your API keys in the sidebar
3. Configure your article settings:
   - Choose between GPT-3.5-Turbo (faster) or GPT-4o (higher quality)
   - Set article length (300-1000 words)
   - Choose number of sources (2-5)
   - Select article style (Informative, Persuasive, Narrative, etc.)
   - Specify target audience (optional)
4. Enter your article topic and click "Generate Article"
5. Watch as the AI researches, analyzes, and writes your article in real-time
6. Download the finished article as a Markdown file

## Project Structure

```
ai-journalist/
├── app.py                  # Streamlit frontend interface
├── backend.py              # Backend logic with AI agents
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

## Requirements

- Python 3.8+
- OpenAI API key
- SerperDev API key
- Dependencies listed in requirements.txt:
  - streamlit
  - crewai
  - langchain
  - langchain_openai
  - langchain_community
  - newspaper3k

## How It Works

The application follows a three-step process:

1. **Research Phase**: The AI agent searches for relevant sources using SerperDev and returns formatted links
2. **Analysis Phase**: The agent fetches content from each source URL and summarizes key information
3. **Writing Phase**: Using the research and analysis, the agent crafts a well-structured article in the requested style


---
