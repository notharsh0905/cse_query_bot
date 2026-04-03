import streamlit as st
from sentence_transformers import SentenceTransformer
import faiss
from pypdf import PdfReader
import numpy as np
import os
import ollama

# ---------------- SYSTEM PROMPT ----------------
SYSTEM_PROMPT = """
You are an intelligent and helpful AI assistant designed for the Department Chatbot of CSJMU (Chhatrapati Shahu Ji Maharaj University), Kanpur.

Answer ONLY using the provided context.

If answer not found say:
"I could not find the answer in the provided documents."

Keep answers simple and student friendly.
"""

# ---------------- UI ----------------
st.set_page_config(page_title="Smart Assistant", layout="wide")
st.title("🤖 CSE Smart Assistant (PDF + Manual + Default Data)")

# ---------------- SESSION STATE ----------------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- CLEAR HISTORY ----------------
if st.button("🗑️ Clear Chat History"):
    st.session_state.history = []

# ---------------- PDF UPLOAD ----------------
uploaded_file = st.file_uploader("📄 Upload PDF (optional)", type="pdf")

# ---------------- LOAD DEFAULT DATA ----------------
def load_default_data():
    text = ""
    if os.path.exists("data"):
        for file in os.listdir("data"):
            path = os.path.join("data", file)

            if file.endswith(".txt"):
                with open(path, "r", encoding="utf-8") as f:
                    text += f.read() + "\n"

            elif file.endswith(".pdf"):
                reader = PdfReader(path)
                for page in reader.pages:
                    t = page.extract_text()
                    if t:
                        text += t + "\n"
    return text

# ---------------- MANUAL DATA ----------------
def load_manual_data():
    return """
SLM department timing is 9 AM to 5 PM.
HOD of SLM department is Dr. XYZ.
CSE department offers subjects like DBMS, OS, CN, AI.
Lab facilities include programming lab, networking lab.
"""

# ---------------- PDF TEXT ----------------
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        t = page.extract_text()
        if t:
            text += t + "\n"
    return text

# ---------------- CHUNKING ----------------
def split_text(text, chunk_size=700, overlap=100):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks

# ---------------- SYSTEM SETUP ----------------
@st.cache_resource
def setup_system(text_chunks):
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = embedder.encode(text_chunks)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))

    return text_chunks, embedder, index

# ---------------- DATA SELECTION ----------------
manual_text = load_manual_data()
default_text = load_default_data()

if uploaded_file:
    st.info("📄 Using uploaded PDF + manual data")
    pdf_text = extract_text_from_pdf(uploaded_file)
    combined_text = pdf_text + "\n" + manual_text
else:
    st.info("📚 Using default data + manual data")
    combined_text = default_text + "\n" + manual_text

# ---------------- CHUNK ----------------
text_chunks = split_text(combined_text)

# ---------------- SETUP ----------------
if text_chunks:
    docs, embedder, index = setup_system(text_chunks)

    query = st.text_input("💬 Ask your question:")

    if query:
        q_emb = embedder.encode([query])
        distances, idx = index.search(np.array(q_emb), 3)

        relevant_chunks = [docs[i] for i in idx[0]]
        context = "\n".join(relevant_chunks)

        if distances[0][0] > 2.5:
            response = "❌ Answer not found in the available data."
            st.warning(response)

        else:
            prompt = f"""
{SYSTEM_PROMPT}

Context:
{context}

Question:
{query}

Answer:
"""

            response = ollama.chat(
                model="llama3.2:3b",
                messages=[{"role": "user", "content": prompt}]
            )["message"]["content"]

            if response == "" or len(response) < 3:
                response = "Answer not found"

            st.success(response)

        st.session_state.history.append((query, response))

# ---------------- CHAT HISTORY ----------------
st.subheader("🕘 Chat History")

if len(st.session_state.history) == 0:
    st.info("No chat history yet.")
else:
    for q, a in st.session_state.history[::-1]:
        st.markdown(f"**🧑 You:** {q}")
        st.markdown(f"**🤖 Bot:** {a}")
        st.markdown("---")