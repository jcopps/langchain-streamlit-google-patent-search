"""Python file to serve as the frontend"""
import sys
import os
import re

sys.path.append(os.path.abspath("."))

import streamlit as st
import time
from demo_app.components.sidebar import sidebar
from langchain.chains import ConversationChain

from langchain.text_splitter import NLTKTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI

from langchain.document_loaders import UnstructuredPDFLoader
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

from demo_app.patent_downloader import PatentDownloader


def load_docs(document_path):
    loader = UnstructuredPDFLoader(document_path)

    documents = loader.load()
    text_splitter = NLTKTextSplitter(chunk_size=1000)
    return text_splitter.split_documents(documents)


def load_chain(file_name=None):
    """Logic for loading the chain you want to use should go here."""
    docs = load_docs(file_name)
    st.write("Length: ", len(docs))
    st.write(docs[0])
    st.write(docs[-1])
    vectordb = Chroma.from_documents(
        docs, HuggingFaceEmbeddings(), persist_directory="."
    )
    vectordb.persist()
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        input_key="question",
        output_key="answer",
    )
    return ConversationalRetrievalChain.from_llm(
        OpenAI(temperature=0),
        vectordb.as_retriever(search_kwargs={"k": 6}),
        return_source_documents=True,
        memory=memory,
    )


def extract_patent_number(url):
    pattern = r"/patent/([A-Z]{2}\d+)"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None


def download_pdf():
    """Logic for validating and downloading the google patent as a PDF"""
    patent_downloader = PatentDownloader()

    patent_downloader.download(patent=patent_number)
    return "{}.pdf".format(patent_number)


def get_text():
    input_text = st.text_input("You: ", "Hello, how are you?", key="input")
    return input_text


if __name__ == "__main__":

    st.set_page_config(
        page_title="Patent Chat: Google Patents Chat Demo",
        page_icon="📖",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.header("📖 Patent Chat: Google Patents Chat Demo")
    sidebar()

    if not st.session_state.get("open_api_key_configured"):
        st.error("Please configure your API Keys!")
    if not st.session_state.get("patent_link_configured"):
        st.error("Please set the patent link!")
    else:
        patent_link = st.session_state.get("PATENT_LINK")
        patent_number = extract_patent_number(patent_link)
        st.write("Patent number: ", patent_number)

        pdf_path = "{}.pdf".format(patent_number)
        if os.path.isfile(pdf_path):
            st.write("File already downloaded.")
        else:
            pdf_path = download_pdf()
            st.write("File downloaded.")
        chain = load_chain(pdf_path)

        if "messages" not in st.session_state:
            st.session_state["messages"] = [
                {"role": "assistant", "content": "How can I help you?"}
            ]

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if user_input := st.chat_input("What is your question?"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": user_input})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""

                with st.spinner("CHAT-BOT is at Work ..."):

                    assistant_response = chain({"question": user_input})
                # Simulate stream of response with milliseconds delay
                st.write(assistant_response)
                for chunk in assistant_response["answer"].split():
                    full_response += chunk + " "
                    time.sleep(0.05)
                    # Add a blinking cursor to simulate typing
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )
