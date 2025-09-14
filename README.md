# Flatopia

We're building Flatopia to help migrant workers find better opportunities overseas.

## About

Flatopia is an AI-powered immigration and study abroad advisor that helps people explore migration opportunities and study abroad options for themselves and their families.

## Features

- 🤖 Intelligent conversation based on Groq API
- 📚 RAG (Retrieval Augmented Generation) technology
- 🔍 Vector database support
- 💬 Multi-turn conversation memory
- 🌐 Web interface and API
- ⚡ High performance and low latency

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

```bash
cp env.example .env
# Edit .env file and add your Groq API key
```

### 3. Run Application

```bash
# Start Web Interface
streamlit run app.py

# Or start API Service
uvicorn api.main:app --reload
```

## Project Structure

```
Flatopia/
├── api/                 # FastAPI backend
├── core/               # Core functionality modules
├── data/               # Data storage  
├── prompts/            # Prompt templates
├── utils/              # Utility functions
├── app.py             # Streamlit frontend
└── requirements.txt   # Dependency management
```

## Tech Stack

- **Backend**: FastAPI, Groq API
- **Frontend**: Streamlit
- **Vector Database**: ChromaDB
- **Embedding Model**: sentence-transformers
- **LLM**: Groq (Llama 3)

## License

MIT License

## Team Members

- Daniel
- Bhargava  
- Owen
- Francisco
- Klein
- Irfan
