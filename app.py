def load_context ():
  context = ""
  filenames = ["information.pdf","fees_2024-25","latest results.pdf"]
  for name in filenames:
    try:
      with open(name, "r") as f:
           context +=
  f"\n{f.read()}"
        except:
          continue
          return context
          {
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "mount_file_id": "1oqjyl6eQnx3DqsOKjIX7bRKv3B1XpiL-",
      "authorship_tag": "ABX9TyPHL/NAs6ssPinlGEL8tp0Q",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/fidastar/school-chatbot/blob/main/app.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!pip install -q -U langchain-google-genai langchain-community langchain-chroma pypdf streamlit\n",
        "!npm install -g localtunnel"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "g9UpfezbwrlY",
        "outputId": "e4859e50-1f2d-4393-8bce-5d5e57c50b44"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "\u001b[1G\u001b[0K⠙\u001b[1G\u001b[0K⠹\u001b[1G\u001b[0K⠸\u001b[1G\u001b[0K⠼\u001b[1G\u001b[0K⠴\u001b[1G\u001b[0K⠦\u001b[1G\u001b[0K⠧\u001b[1G\u001b[0K⠇\u001b[1G\u001b[0K⠏\u001b[1G\u001b[0K⠋\u001b[1G\u001b[0K⠙\u001b[1G\u001b[0K⠹\u001b[1G\u001b[0K⠸\u001b[1G\u001b[0K⠼\u001b[1G\u001b[0K⠴\u001b[1G\u001b[0K⠦\u001b[1G\u001b[0K⠧\u001b[1G\u001b[0K⠇\u001b[1G\u001b[0K⠏\u001b[1G\u001b[0K⠋\u001b[1G\u001b[0K⠙\u001b[1G\u001b[0K⠹\u001b[1G\u001b[0K⠸\u001b[1G\u001b[0K⠼\u001b[1G\u001b[0K\n",
            "changed 22 packages in 2s\n",
            "\u001b[1G\u001b[0K⠼\u001b[1G\u001b[0K\n",
            "\u001b[1G\u001b[0K⠼\u001b[1G\u001b[0K3 packages are looking for funding\n",
            "\u001b[1G\u001b[0K⠼\u001b[1G\u001b[0K  run `npm fund` for details\n",
            "\u001b[1G\u001b[0K⠼\u001b[1G\u001b[0K"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "%%writefile app.py\n",
        "import os\n",
        "import streamlit as st\n",
        "from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings\n",
        "from langchain_community.document_loaders import PyPDFLoader\n",
        "from langchain_text_splitters import RecursiveCharacterTextSplitter\n",
        "from langchain_chroma import Chroma\n",
        "from langchain_core.prompts import ChatPromptTemplate\n",
        "\n",
        "# 1. SETUP\n",
        "os.environ[\"GOOGLE_API_KEY\"] = st.secrets[\"GEMINI_API_KEY\"]\n",
        "\n",
        "st.set_page_config(page_title=\"ALPHA AI\", page_icon=\"🏫\")\n",
        "\n",
        "# 2. THE KNOWLEDGE BASE (The Librarian)\n",
        "@st.cache_resource\n",
        "def setup_alpha_brain():\n",
        "    files = [\"school_info.pdf\", \"fee_structure.pdf\", \"latest_result.pdf\"]\n",
        "    all_docs = []\n",
        "    for file in files:\n",
        "        if os.path.exists(file):\n",
        "            loader = PyPDFLoader(file)\n",
        "            all_docs.extend(loader.load())\n",
        "\n",
        "    if not all_docs:\n",
        "        return None\n",
        "\n",
        "    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)\n",
        "    chunks = splitter.split_documents(all_docs)\n",
        "    embeddings = GoogleGenerativeAIEmbeddings(model=\"models/embedding-001\")\n",
        "    return Chroma.from_documents(chunks, embeddings)\n",
        "\n",
        "# 3. INTERFACE\n",
        "st.title(\"I am ALPHA\")\n",
        "st.divider()\n",
        "\n",
        "with st.spinner(\"ALPHA is studying the school records...\"):\n",
        "    vectorstore = setup_alpha_brain()\n",
        "\n",
        "if \"messages\" not in st.session_state:\n",
        "    st.session_state.messages = [{\"role\": \"assistant\", \"content\": \"Hello! I am ALPHA. Ask me anything about our school!\"}]\n",
        "\n",
        "for msg in st.session_state.messages[-5:]:\n",
        "    with st.chat_message(msg[\"role\"]):\n",
        "        st.markdown(msg[\"content\"])\n",
        "# ... (rest of your code above remains the same)\n",
        "\n",
        "# 4. BRAIN LOGIC\n",
        "# Move the input bar OUTSIDE of any 'if' statements to ensure it always shows\n",
        "prompt = st.chat_input(\"How can I help you?\")\n",
        "\n",
        "if prompt:\n",
        "    st.session_state.messages.append({\"role\": \"user\", \"content\": prompt})\n",
        "    with st.chat_message(\"user\"):\n",
        "        st.markdown(prompt)\n",
        "\n",
        "    with st.chat_message(\"assistant\"):\n",
        "        if vectorstore:\n",
        "            # (Your AI logic here...)\n",
        "            llm = ChatGoogleGenerativeAI(model=\"gemini-1.5-flash\", temperature=0.1)\n",
        "            search_results = vectorstore.similarity_search(prompt, k=3)\n",
        "            context_text = \"\\n\\n\".join([doc.page_content for doc in search_results])\n",
        "            system_prompt = f\"You are ALPHA, a school assistant. Use this context: {context_text}\"\n",
        "            response = llm.invoke([(\"system\", system_prompt), (\"human\", prompt)])\n",
        "            answer = response.content\n",
        "        else:\n",
        "            answer = \"Error: Please upload PDFs to the 📂 icon.\"\n",
        "\n",
        "        st.markdown(answer)\n",
        "        st.session_state.messages.append({\"role\": \"assistant\", \"content\": answer})\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "CgGDT8p7wvNa",
        "outputId": "7cc30dcf-49db-46f3-f1d4-e682ec825dd9"
      },
      "execution_count": 1,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Writing app.py\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "print(\"Your Tunnel Password (IP) is:\")\n",
        "!curl ipv4.icanhazip.com\n",
        "!python3 -m streamlit run app.py & npx pinggy -p 8501 -t"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "MRc91CxR74fP",
        "outputId": "c1322fc1-57f8-42c5-e305-25074dc2147c"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Your Tunnel Password (IP) is:\n",
            "34.10.113.114\n",
            "\u001b[1G\u001b[0K⠙\u001b[1G\u001b[0K⠹\n",
            "Collecting usage statistics. To deactivate, set browser.gatherUsageStats to false.\n",
            "\u001b[0m\n",
            "\u001b[1G\u001b[0K⠸\u001b[1G\u001b[0K⠼\u001b[1G\u001b[0K⠴\u001b[1G\u001b[0K⠦\u001b[1G\u001b[0K⠧\u001b[1G\u001b[0K⠇\u001b[1G\u001b[0K⠏\u001b[1G\u001b[0K⠋\u001b[1G\u001b[0K⠙\u001b[1G\u001b[0K⠹\u001b[1G\u001b[0K⠸\u001b[1G\u001b[0K⠼\u001b[1G\u001b[0K⠴\u001b[1G\u001b[0K⠦\u001b[1G\u001b[0K⠧\u001b[1G\u001b[0K\u001b[1G\u001b[0JNeed to install the following packages:\n",
            "pinggy@0.3.0\n",
            "Ok to proceed? (y) \u001b[20G\u001b[0m\n",
            "\u001b[34m\u001b[1m  You can now view your Streamlit app in your browser.\u001b[0m\n",
            "\u001b[0m\n",
            "\u001b[34m  Local URL: \u001b[0m\u001b[1mhttp://localhost:8501\u001b[0m\n",
            "\u001b[34m  Network URL: \u001b[0m\u001b[1mhttp://172.28.0.12:8501\u001b[0m\n",
            "\u001b[34m  External URL: \u001b[0m\u001b[1mhttp://34.10.113.114:8501\u001b[0m\n",
            "\u001b[0m\n",
            "\u001b[34m  Stopping...\u001b[0m\n",
            "^C\n"
          ]
        }
      ]
    }
  ]
}
