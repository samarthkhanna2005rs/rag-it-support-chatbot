# RAG IT Support Chatbot

A high-performance Retrieval-Augmented Generation (RAG) chatbot designed to answer IT support queries based on local knowledge base documents. This project decouples the backend API from the frontend interface to allow for scalable cloud deployment.

## 🚀 Tech Stack

* **Backend:** FastAPI, Python
* **AI Framework:** LangChain
* **LLM:** Qwen3 (1.7B) via Ollama
* **Embeddings:** Nomic-Embed-Text via Ollama
* **Vector Database:** Chroma
* **Frontend:** Streamlit

---

## 🛠️ Local Setup Instructions

### 1. Prerequisites
Ensure you have Python (3.9+) installed and [Ollama](https://ollama.ai/) running on your machine. 

Before starting the application, pull the necessary lightweight models:
```bash
ollama pull nomic-embed-text
ollama pull qwen3:1.7b
```

### 2. Install Dependencies
Clone the repository, create a virtual environment, and install the required packages:

```bash
# Create and activate virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate
# On Mac/Linux:
# source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 3. Initialize the Vector Database
Add your `.txt` and `.pdf` files to the `data/` folder, then build the local Chroma database by running the ingestion script:

```bash
python backend/ingest_docs.py
```
*Note: You should see a success message indicating your documents were chunked and stored.*

### 4. Run the Application
You will need two separate terminal windows (with the virtual environment activated in both) to run the backend and frontend simultaneously.

**Terminal 1: Start the API Backend**
```bash
uvicorn backend.main:app --reload --port 8000
```
*The API will be available at `http://127.0.0.1:8000`*

**Terminal 2: Start the UI Frontend**
```bash
streamlit run frontend/app.py
```
*The UI will automatically open in your browser at `http://localhost:8501`*

---

## ☁️ Deployment Architecture

This project is structured to separate concerns for production deployment:

* **Frontend:** The UI dynamically connects to the backend via the `BACKEND_API_URL` environment variable. 
* **Backend:** The FastAPI application includes CORS middleware, allowing it to securely accept cross-origin requests from hosted frontends.

**Recommended Hosting:**
* Deploy the FastAPI backend on a containerized service like **Render** or **Railway**.
* For **Vercel** deployment, the `frontend/app.py` (Streamlit) should be rebuilt in a serverless-friendly framework like **React/Next.js**, while pointing its API calls to the hosted backend URL. Alternatively, host the current frontend on **Streamlit Community Cloud**.
