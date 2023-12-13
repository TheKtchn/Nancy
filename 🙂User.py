import time  # Import the time module

import streamlit as st

from database import ping
from response import Response
from user_functions import login_user_form, logout_user_form, signup_user_form

DB_NAME = "nancy"

if "is_session" not in st.session_state:
    st.session_state.is_session = False


def show_success_message(message, timeout=3):
    success_placeholder = st.empty()
    success_placeholder.success(message)
    time.sleep(timeout)
    success_placeholder.empty()


def show_error_message(message, timeout=3):
    error_placeholder = st.empty()
    error_placeholder.error(message)
    time.sleep(timeout)
    error_placeholder.empty()


def signup_section():
    st.write("### User Signup")
    user_signup_form = {
        "name": st.text_input("Enter your name:", ""),
        "email": st.text_input("Enter your email:", ""),
        "password": st.text_input("Enter your password:", "", type="password"),
    }

    if st.button("Signup"):
        if ping():
            if not st.session_state.is_session:
                rspnse: Response = signup_user_form(user_signup_form=user_signup_form)
                if not rspnse.is_error:
                    show_success_message(rspnse.message)
                    st.session_state.user_data = rspnse.data
                    st.session_state.is_session = True

                    user_signup_form = {
                        "name": st.text_input("Enter your name:", ""),
                        "email": st.text_input("Enter your email:", ""),
                        "password": st.text_input(
                            "Enter your password:", "", type="password"
                        ),
                    }
                else:
                    show_error_message(rspnse.message)
            else:
                show_error_message("User already logged in.")
        else:
            show_error_message("Could not connect to the database.")


def login_section():
    st.write("### User Login")
    user_login_form = {
        "email": st.text_input("Enter existing email:", ""),
        "password": st.text_input("Enter password:", "", type="password"),
    }

    if st.button("Login"):
        if ping():
            if not st.session_state.is_session:
                rspnse: Response = login_user_form(user_login_form=user_login_form)
                if not rspnse.is_error:
                    show_success_message(rspnse.message)
                    st.session_state.user_data = rspnse.data
                    st.session_state.is_session = True

                    user_login_form = {
                        "email": st.text_input("Enter existing email:", ""),
                        "password": st.text_input(
                            "Enter password:", "", type="password"
                        ),
                    }
                else:
                    show_error_message(rspnse.message)
            else:
                show_error_message("User already logged in.")
        else:
            show_error_message("Could not connect to the database.")


def logout_section():
    if st.button("Logout"):
        if ping():
            if not st.session_state.is_session:
                rspnse: Response = logout_user_form()
                st.session_state.user_data = rspnse.data
                st.session_state.is_session = False
            else:
                show_error_message("User already logged in.")
        else:
            show_error_message("Could not connect to the database.")


def main():
    signup_section()
    login_section()
    logout_section()


if __name__ == "__main__":
    main()
