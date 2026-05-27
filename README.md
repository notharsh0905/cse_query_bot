# UIET CSE Department Assistant (RAG Bot)

A localized, 100% free, and privacy-focused RAG (Retrieval-Augmented Generation) conversational AI agent built to answer queries about the Computer Science and Engineering department using official academic documents.

# Project Overview

The UIET CSE Assistant reads official academic documents (like course syllabi, academic calendars, and department brochures) and uses Retrieval-Augmented Generation (RAG) to provide 100% accurate, hallucination-free answers based only on the provided documentation. 

Instead of relying on heavy cloud infrastructure or expensive APIs, this system is a customized SML (Small Model Language) pipeline designed to run entirely locally for free on consumer hardware (like a MacBook Air or an RTX Windows laptop).

# Tech Stack & Libraries Used

* **Frontend UI:** Streamlit (Native Python web application framework with live session state handling)
* **Local LLM Engine:** Ollama (Hosts and executes quantized models locally on your machine's hardware memory)
* **Underlying Brain:** Llama 3.2 (3B)
* **Vector DB:** Meta FAISS (Facebook AI Similarity Search for highly optimized dense vector clustering)
* **Embeddings Engine:** Sentence-Transformers (Maps paragraphs into dense vector spaces to capture semantic meaning)
* **Document Parser:** PyPDF (Lightweight pure-python PDF extraction library to parse and ingest text)

## Installation & Setup

### 1. Prerequisites
Install **Ollama** onto your computer from [ollama.com](https://ollama.com). Once installed, open your terminal/command prompt and run the model:

ollama pull llama3.2:3b

### 2. Environment Setup
Clone this repository to your computer, open your terminal inside the project directory, and initialize a virtual environment:

On macOS/Linux:

python3 -m venv venv,
source venv/bin/activate,
python3 -m pip install -r requirements.txt

On Windows:

python -m venv venv,
venv\Scripts\activate,
pip install -r requirements.txt

### 3. Running the Application
Ensure your source PDFs are placed inside the data/ directory, then start the application server:
python3 -m streamlit run app.py

The interface will automatically load in your browser at http://localhost:8501.
