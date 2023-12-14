import streamlit as st
from typing import List


def form(name: str, details: List[str], submit: str):
    form_data = dict()
    with st.form(key=name, clear_on_submit=True):
        for detail in details:
            prompt = detail.replace("_", " ")
            form_data[detail] = st.text_input(prompt)

        is_submitted = st.form_submit_button(submit)
        if is_submitted:
            st.write("Gotten input!")


st.write("# Signup")

form(
    name="Signup",
    details=["name", "email", "password"],
    submit="Signup",
)
