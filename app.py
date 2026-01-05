import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

# 1. SETUP & API KEY
# This pulls from your Streamlit "Secrets" dashboard
if "GEMINI_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GEMINI_API_KEY"]
else:
    st.error("Missing API Key! Please add GEMINI_API_KEY to your Streamlit Secrets.")

st.set_page_config(page_title="ALPHA AI", page_icon="🏫")

# 2. THE KNOWLEDGE BASE
@st.cache_resource
def setup_alpha_brain():
    # Make sure these names match your GitHub files EXACTLY
    files = ["Information.pdf", "fees_2024-25 (1).pdf", "Latest results.pdf"]
    all_docs = []
    
    for file in files:
        if os.path.exists(file):
            try:
                loader = PyPDFLoader(file)
                all_docs.extend(loader.load())
            except Exception as e:
                st.warning(f"Error loading {file}: {e}")

    if not all_docs:
        return None

    # Process documents for searching
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(all_docs)
    # Change this line in your setup_alpha_brain function:
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=st.secrets["GEMINI_API_KEY"]  # Add this part!
)
return Chroma.from_documents(chunks, embeddings)

# Start the 'brain'
vectorstore = setup_alpha_brain()

# 3. INTERFACE
st.title("I am ALPHA")
st.caption("Official School Exhibition AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. CHAT LOGIC
prompt = st.chat_input("Ask me anything about the school:")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if vectorstore:
            with st.spinner("Thinking..."):
                # RAG: Search the PDF data
                search_results = vectorstore.similarity_search(prompt, k=3)
                context_text = "\n\n".join([doc.page_content for doc in search_results])
                
                llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.1)
                system_prompt = f"You are ALPHA, a school assistant. Use this context to answer: {context_text}"
                
                response = llm.invoke([("system", system_prompt), ("human", prompt)])
                answer = response.content
        else:
            answer = "I don't have access to the school documents right now."

        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
