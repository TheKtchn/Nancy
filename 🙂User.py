import streamlit as st
import time  # Import the time module

from database import ping
from response import Response
from user_functions import login_user_form, logout_user_form, signup_user_form

DB_NAME = "nancy"
from enum import Enum

class Pages(Enum):
    HOME = "Home"
    FINANCES = "Finances"
    BUDGET = "Budget"
    CHAT = "Chat"


if "is_session" not in st.session_state:
    st.session_state.is_session = False

if "user_data" not in st.session_state:
    st.session_state.user_data = {
        "name": "",
        "email": "",
        "password": "",
    }

if "current_page" not in st.session_state:
    st.session_state.current_page = Pages.HOME


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


def signup():
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

                    user_signup_form["name"] = ""
                    user_signup_form["email"] = ""
                    user_signup_form["password"] = ""
                else:
                    show_error_message(rspnse.message)
            else:
                show_error_message("User already logged in.")
        else:
            show_error_message("Could not connect to the database.")


def login():
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

                    user_login_form["email"] = ""
                    user_login_form["password"] = ""
                else:
                    show_error_message(rspnse.message)
            else:
                show_error_message("User already logged in.")
        else:
            show_error_message("Could not connect to the database.")


def logout():
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




def test():
    if st.button("Test"):
        st.session_state.current_page = Pages.FINANCES

def test_page():
    st.write("Here is a test page for you, yh.")
    if st.button("Home"):
        st.session_state.current_page = Pages.HOME

def home():
    signup()
    login()
    logout()
    test()
    
if __name__ == "__main__":
    if st.session_state.current_page == Pages.HOME:
        home()

    if st.session_state.current_page == Pages.FINANCES:
        test_page()

    
