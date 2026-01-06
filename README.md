# school-chatbot
school AI chatbot for - official purpose only.
# 🎓 ALPHA - School Information Chatbot

An intelligent chatbot built with Streamlit and Google Gemini AI that answers questions about school information, fees, and academic results.

## Features

- 💬 Natural language conversation interface
- 📚 Answers questions from school information PDFs
- 💰 Provides fee structure details (2024-25)
- 🏆 Shares latest academic results
- 🎯 Context-aware responses based on school documents

## Setup Instructions

### 1. Prerequisites
- Python 3.8 or higher
- Google Gemini API key ([Get it here](https://makersuite.google.com/app/apikey))

### 2. Installation

Clone or download this repository and install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Add Your PDF Files

Place the following PDF files in the root directory:
- `Information.pdf` - General school information
- `fees_2024-25 (1).pdf` - Fee structure
- `Latest results.pdf` - Academic results

### 4. Configure Secrets

Create a `.streamlit/secrets.toml` file in your project directory:

```toml
GEMINI_API_KEY = "your-api-key-here"
```

**For Streamlit Cloud deployment:**
1. Go to your app settings
2. Navigate to "Secrets"
3. Add: `GEMINI_API_KEY = "your-api-key-here"`

### 5. Run Locally

```bash
streamlit run streamlit_app.py
```

## Deployment on Streamlit Cloud

1. Push your code to GitHub (don't include secrets.toml)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Add your `GEMINI_API_KEY` in the Secrets section
5. Upload your PDF files to the repository
6. Deploy!

## Usage

Simply type your questions in the chat interface:
- "What are the admission fees for grade 10?"
- "Tell me about the latest exam results"
- "What facilities does the school offer?"
- "What is the fee structure for this year?"

## Technologies Used

- **Streamlit** - Web interface
- **Google Gemini AI** - Natural language processing
- **PyPDF2** - PDF text extraction
- **Python** - Backend logic

## Notes

- The chatbot only answers based on information in the provided PDF files
- Chat history is maintained during the session
- Clear chat history using the sidebar button

## License

MIT License - Feel free to modify and use for your school!

---

**Powered by Google Gemini AI** 🤖
