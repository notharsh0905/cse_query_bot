'''import streamlit as st
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import Chroma
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# Page Config
st.set_page_config(page_title="CSE Dept Chatbot", page_icon="🎓")
st.title("🎓 CSE Department Assistant")

# Initialize LLM and Vector DB (Cached so it's fast)
@st.cache_resource
def load_rag_system():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vector_store = Chroma(persist_directory="cse_vector_db", embedding_function=embeddings)
    llm = ChatOllama(model="llama3.2:3b", temperature=0)
    
    system_prompt = (
    "You are the official Assistant for the UIET Kanpur CSE Department. "
    "Your knowledge base is the provided 91-page department document which includes "
    "syllabus details for all subjects (including Chemistry, Physics, and Maths) "
    "that CSE students must study.\n\n"
    "RULES:\n"
    "1. Use the provided context to answer the question accurately.\n"
    "2. If the information is in the context (even if it's about Chemistry or Physics), answer it.\n"
    "3. Only if the information is completely missing from the document (like SpaceX), "
    "say: 'That information is not in the department records.'\n\n"
    "Context:\n{context}"
)
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    qa_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(vector_store.as_retriever(search_kwargs={"k": 5}), qa_chain)

rag_chain = load_rag_system()

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Ask about the CSE department..."):
    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant message (Streaming look)
    with st.chat_message("assistant"):
        response = rag_chain.invoke({"input": prompt})
        answer = response["answer"]
        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})'''