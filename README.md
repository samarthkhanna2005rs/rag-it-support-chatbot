# RAG IT Support Chatbot

A high-performance Retrieval-Augmented Generation (RAG) chatbot designed to answer IT support queries based on local knowledge base documents. This project decouples the backend API from the frontend interface to allow for scalable cloud deployment.

## Tech Stack
* **Backend:** FastAPI, Python
* **AI Framework:** LangChain
* **LLM & Embeddings:** Qwen3 (1.7B) and Nomic-Embed-Text (via Ollama)
* **Vector Database:** Chroma
* **Frontend:** Streamlit

## Local Setup Instructions

### 1. Prerequisites
Ensure you have Python installed and [Ollama](https://ollama.ai/) running on your machine.
Pull the necessary models before starting:
```bash
ollama pull nomic-embed-text
ollama pull qwen3:1.7b
