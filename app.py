import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate

# 1. SETUP & API KEY
# This pulls the key from the Streamlit "Secrets" you set up earlier
if "GEMINI_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GEMINI_API_KEY"]
else:
    st.error("Please add your GEMINI_API_KEY to Streamlit Secrets.")

st.set_page_config(page_title="ALPHA AI", page_icon="🏫")

# 2. THE KNOWLEDGE BASE (The Librarian)
@st.cache_resource
def setup_alpha_brain():
    # Make sure these filenames match your GitHub files EXACTLY (case-sensitive)
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

    # Splitting the text into smaller searchable chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(all_docs)
    
    # Creating the vector database (the brain)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    return Chroma.from_documents(chunks, embeddings)

# Initialize the brain
vectorstore = setup_alpha_brain()

# 3. INTERFACE & CHAT HISTORY
st.title("I am ALPHA")
st.caption("School Exhibition AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. CHAT LOGIC
prompt = st.chat_input("How can I help you?")

if prompt:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if vectorstore:
            with st.spinner("Analyzing school documents..."):
                # Search for the most relevant info in the PDFs
                search_results = vectorstore.similarity_search(prompt, k=3)
                context_text = "\n\n".join([doc.page_content for doc in search_results])
                
                # Setup the AI to answer using the context
                llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.1)
                
                system_prompt = (
                    "You are ALPHA, a helpful school assistant. "
                    "Use the following school records to answer the student's question accurately. "
                    "If the answer isn't in the context, say you don't know politely.\n\n"
                    f"Context:\n{context_text}"
                )
                
                response = llm.invoke([("system", system_prompt), ("human", prompt)])
                answer = response.content
        else:
            answer = "I'm sorry, I can't find the school documents. Please check the file names in the repository."

        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
