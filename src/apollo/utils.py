import json
import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()


users_str = os.getenv("webapp_users")

# Handle the case where the environment variable is not set
if users_str is None:
    users = {}
else:
    try:
        users = json.loads(users_str)
    except json.JSONDecodeError:
        users = {}


def check_password() -> bool:
    """Returns `True` if the user had a correct password."""

    def login_form() -> None:
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered() -> None:
        """Checks whether a password entered by the user is correct."""
        username = st.session_state["username"]
        password = st.session_state["password"]
        if username in users and users.get(username) == password:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True
    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False
