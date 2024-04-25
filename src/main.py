import json
import os

import streamlit as st

from apollo.VectorStore import VectorStore


def get_ai_response(user_input: str) -> str:
    # Placeholder for AI response logic.
    return f"🤖 AI: I'm just echoing for now: {user_input}"


def main() -> None:
    st.set_page_config(page_title="Apollo", layout="wide")
    st.title("Apollo")

    vector_store = VectorStore()

    if "delete_status" not in st.session_state:
        st.session_state.delete_status = ""

    # Initialize chat state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Sidebar for document upload
    with st.sidebar:
        st.header("Upload a Document")
        uploaded_file = st.file_uploader("Choose a file (only PDF)", type=["pdf"])
        if uploaded_file is not None:
            try:
                with open("temp_file.pdf", "wb") as f:
                    f.write(uploaded_file.getvalue())

                try:
                    title = vector_store.extract_title(pdf_path="temp_file.pdf")
                    vector_store.push_document(
                        document_path="temp_file.pdf", title=title
                    )
                    st.success("File uploaded successfully!")
                except Exception as e:
                    st.error(f"Error while uploading the file. {e}")
            except Exception as e:
                st.error(f"Error while uploading the file. {e}")

            os.remove("temp_file.pdf")

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

    # Chat input using st.chat_input
    user_input = st.chat_input("Type your message here...", key="chat")

    # Process input and display chat
    if user_input:
        # Update chat history
        update_chat(user_input)
        # Clear the input field by forcing a rerun (Streamlit does not automatically clear st.chat_input)
        st.rerun()

    # Display chat messages
    display_chat()


def update_chat(user_input: str) -> None:
    """Updates the chat with user input and AI responses."""
    human_message = f"🧑 You: {user_input}"  # Adding an emoji for human messages
    st.session_state.messages.append(human_message)
    ai_response = get_ai_response(user_input)
    st.session_state.messages.append(ai_response)


def display_chat() -> None:
    """Displays chat messages using markdown for better styling."""
    chat_container = st.container()
    with chat_container:
        for message in reversed(st.session_state.messages):
            # Use st.markdown to allow for better formatting if needed
            st.markdown(f"{message}")


if __name__ == "__main__":
    main()
