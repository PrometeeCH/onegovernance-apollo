import json
import os

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

from apollo.chat import Chat
from apollo.utils import check_password
from apollo.VectorStore import VectorStore


def main() -> None:
    if not check_password():
        st.stop()
    st.set_page_config(page_title="Apollo", layout="wide")
    st.title("Apollo - AI Specialized in Commodities.")

    vector_store = VectorStore()

    if "delete_status" not in st.session_state:
        st.session_state.delete_status = ""

    # Initialize chat state
    if st.session_state.get("chat") is None:
        st.session_state.chat = Chat()

    chat = st.session_state.chat

    # Sidebar for document upload
    with st.sidebar:
        st.header("Upload Documents")
        uploaded_files = st.file_uploader(
            "Choose files (PDF or TXT)", type=["pdf", "txt"], accept_multiple_files=True
        )
        if uploaded_files is not None:
            for uploaded_file in uploaded_files:
                # Determine the file extension to handle file appropriately
                file_type = uploaded_file.name.split(".")[-1].lower()
                file_path = f"temp_file_{uploaded_file.name}"  # Name temp file with original name

                # Write the uploaded file to a temporary file
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getvalue())

                try:
                    if file_type == "pdf":
                        # Extract title from PDF and push the document
                        title = vector_store.extract_title(pdf_path=file_path)
                        vector_store.push_document(document_path=file_path, title=title)
                    elif file_type == "txt":
                        # Assume the first line of the text file is the title
                        with open(file_path, "r") as f:
                            title = f.readline().strip()
                        vector_store.push_document(document_path=file_path, title=title)

                    st.success(f"File '{uploaded_file.name}' uploaded successfully!")

                except Exception as e:
                    st.error(f"Error while uploading '{uploaded_file.name}'. {e}")

                os.remove(file_path)  # Clean up the temporary file after processing

        # Display documents in the index
        st.header("Uploaded Documents")
        for doc in vector_store.fetch_documents(max_results=20):
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                metadata = json.loads(doc["metadata"])
                st.text(metadata["title"])
            with col2:
                if st.button("✖", key=doc["id"]):
                    result = vector_store.delete_document(doc["id"])
                    if isinstance(result, str) and len(result) > 0:  # Error case
                        st.session_state.delete_status = (
                            f"Failed to delete document: {result}"
                        )
                    else:
                        st.session_state.delete_status = (
                            "Document deleted successfully!"
                        )
                        st.rerun()  # Rerun to refresh the document list

    st.sidebar.text(st.session_state.delete_status)

    # Handle chat and user interaction
    for message in chat.messages:
        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.write(message.content)
        elif isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.write(message.content)

    prompt = st.chat_input("Say something...")
    if prompt:
        with st.spinner("..."):
            chat.add_message(prompt)
            st.rerun()


if __name__ == "__main__":
    main()
