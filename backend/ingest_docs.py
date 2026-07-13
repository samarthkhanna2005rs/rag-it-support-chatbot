import os

from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# Use environment variable for the LLM URL
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
DATA_DIR = "data"
all_docs = []

print("Starting document ingestion...")

# Load files
if not os.path.exists(DATA_DIR):
    print(f"Error: Directory '{DATA_DIR}' not found.")
else:
    for filename in os.listdir(DATA_DIR):
        filepath = os.path.join(DATA_DIR, filename)

        if filename.endswith(".txt"):
            loader = TextLoader(filepath)
            docs = loader.load()
            all_docs.extend(docs)

        elif filename.endswith(".pdf"):
            loader = PyPDFLoader(filepath)
            docs = loader.load()
            all_docs.extend(docs)

    print(f"\nDocuments loaded: {len(all_docs)}")

    # Chunking
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(all_docs)
    print(f"Chunks created: {len(chunks)}")

    # Embeddings
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text",
        base_url=OLLAMA_BASE_URL
    )

    # Vectorstore
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="vectorstore"
    )

    print("\nVectorstore updated successfully.")