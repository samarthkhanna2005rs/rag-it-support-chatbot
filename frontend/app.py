import streamlit as st
import requests
import os

# 1. Define a dynamic backend URL
# This checks for an environment variable first, but defaults to your local setup for testing.
BACKEND_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000")

st.title("IT Support RAG Chatbot")

question = st.text_input("Ask an IT Support Question")

if st.button("Submit"):
    if question:
        try:
            # 2. Use the dynamic URL
            response = requests.post(
                f"{BACKEND_URL}/chat",
                json={"question": question}
            )
            
            # 3. Handle potential server errors gracefully
            response.raise_for_status() 
            data = response.json()

            st.subheader("Answer")
            st.write(data.get("answer", "No answer found in response."))
            
        except requests.exceptions.RequestException as e:
            # This prevents the whole app from crashing if the backend is asleep or offline
            st.error(f"Failed to connect to the backend API. Error: {e}")