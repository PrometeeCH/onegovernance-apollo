import streamlit as st


def get_ai_response(user_input: str) -> str:
    # Placeholder for AI response logic.
    return f"🤖 AI: I'm just echoing for now: {user_input}"


def main() -> None:
    st.set_page_config(page_title="Apollo", layout="wide")
    st.title("Apollo")

    # Sidebar for document upload
    with st.sidebar:
        st.header("Document Upload")
        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            st.success("File uploaded successfully!")

    # Initialize chat state
    if "messages" not in st.session_state:
        st.session_state.messages = []

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
