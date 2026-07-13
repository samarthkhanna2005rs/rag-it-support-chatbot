import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate

app = FastAPI(title="IT Support RAG API")

# --- 1. CORS Configuration ---
# This allows your Vercel frontend to communicate with this backend.
# In production, replace "*" with your actual Vercel domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. Environment Variables ---
# Defaults to localhost for your local testing, but allows cloud configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")

# Embeddings
embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
    base_url=OLLAMA_BASE_URL
)

# Vector DB
vectorstore = Chroma(
    persist_directory="vectorstore",
    embedding_function=embeddings
)

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 2}
)

# LLM
llm = ChatOllama(
    model="qwen3:1.7b",
    temperature=0,
    base_url=OLLAMA_BASE_URL
)

# Request schema
class ChatRequest(BaseModel):
    question: str

# --- 3. Health Check Endpoint ---
# Cloud providers like Render need this to know your server successfully started
@app.get("/")
def read_root():
    return {"status": "Backend is running", "message": "Welcome to the RAG IT Support API"}


@app.post("/chat")
def chat(request: ChatRequest):
    docs = retriever.invoke(request.question)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    template = """
You are an IT Support Assistant.

Answer ONLY using the provided context.

Context:
{context}

Question:
{question}
"""

    prompt = ChatPromptTemplate.from_template(template)

    final_prompt = prompt.format(
        context=context,
        question=request.question
    )

    response = llm.invoke(final_prompt)

    return {
        "question": request.question,
        "answer": response.content
    }