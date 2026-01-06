import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import os

# Configure page
st.set_page_config(
    page_title="ALPHA - School Chatbot",
    page_icon="🎓",
    layout="wide"
)

# Initialize Gemini API
@st.cache_resource
def init_gemini():
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

# Extract text from PDFs
@st.cache_data
def load_pdf_content():
    pdf_files = ["Information.pdf", "fees_2024-25 (1).pdf", "Latest results.pdf"]
    all_content = ""
    
    for pdf_file in pdf_files:
        if os.path.exists(pdf_file):
            try:
                reader = PdfReader(pdf_file)
                content = f"\n\n=== Content from {pdf_file} ===\n\n"
                for page in reader.pages:
                    content += page.extract_text() + "\n"
                all_content += content
            except Exception as e:
                st.warning(f"Could not read {pdf_file}: {str(e)}")
        else:
            st.warning(f"File not found: {pdf_file}")
    
    return all_content

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Main UI
st.title("🎓 ALPHA - School Information Assistant")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("About ALPHA")
    st.info("""
    **ALPHA** is your intelligent school assistant that can answer questions about:
    
    - 📚 General school information
    - 💰 Fees structure (2024-25)
    - 🏆 Latest academic results
    - 📋 Admission process
    - 🎯 Programs and facilities
    
    Simply type your question below!
    """)
    
    st.markdown("---")
    
    if st.button("🔄 Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.caption("Powered by Google Gemini AI")

# Load school data
try:
    model = init_gemini()
    school_data = load_pdf_content()
    
    if not school_data.strip():
        st.error("⚠️ No PDF files found. Please upload the school information PDFs to the app directory.")
        st.stop()
    
except Exception as e:
    st.error(f"Error initializing the chatbot: {str(e)}")
    st.stop()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about the school..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Create context-aware prompt
                full_prompt = f"""You are ALPHA, a helpful and friendly school information assistant. 
                
Use the following school information to answer the student/parent's question accurately and concisely:

{school_data}

Important guidelines:
- Answer based ONLY on the information provided above
- If the information is not available in the documents, politely say so
- Be friendly, professional, and helpful
- Provide specific details like fees, dates, or results when asked
- Format your response in a clear, easy-to-read manner

Question: {prompt}

Answer:"""
                
                response = model.generate_content(full_prompt)
                answer = response.text
                
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
            except Exception as e:
                error_msg = f"I apologize, but I encountered an error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Footer
st.markdown("---")
st.caption("💡 Tip: You can ask about fees, admission process, results, facilities, or any other school-related information!")
