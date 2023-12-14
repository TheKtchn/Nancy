from enum import Enum
from typing import List

import streamlit as st

if "user_data" not in st.session_state.keys():
    st.session_state.user_data = {"name": "", "email": "", "password": ""}

if "is_session" not in st.session_state.keys():
    st.session_state.is_session = False


class Pages(Enum):
    HOME = "Home"
    FINANCES = "Finances"
    BUDGET = "Budget"
    CHAT = "Chat"


if "current_page" not in st.session_state.keys():
    st.session_state.current_page = Pages.HOME


def form(name: str, details: List[str]):
    form_data = dict()
    with st.form(key=name, clear_on_submit=True):
        for detail in details:
            prompt = f"{detail.replace('_', ' ').title()}:"
            form_data[detail] = st.text_input(prompt)

        is_submitted = st.form_submit_button(name)
        if is_submitted:
            yield form_data


if st.session_state.current_page == Pages.HOME:
    st.write("# Signup")
    form(
        name="Signup",
        details=["name", "email", "password"],
    )

    st.write("# Login")
    form(
        name="Login",
        details=["existing_email", "existing_password"],
    )
