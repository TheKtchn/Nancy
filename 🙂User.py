import os

import streamlit as st
from pymongo import MongoClient

from response import Response
from user_functions import login_user_form, signup_user_form

DB_NAME = "nancy"

if "is_session" not in st.session_state:
    st.session_state.is_session = False
# if "is_pinging" not in st.session_state:
#     st.session_state.is_pinging = False


def initialize_mongodb():
    """
    Function to initialize the MongoDB connection.

    Returns:
        MongoClient: The MongoDB client connected to the specified database.
    """
    MONGODB_USERNAME = st.secrets["MONGODB_USERNAME"]
    MONGODB_PASSWORD = st.secrets["MONGODB_PASSWORD"]
    MONGODB_CLUSTER = st.secrets["MONGODB_CLUSTER"]

    uri = f"mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_CLUSTER}.vfhiusw.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri)

    return client


def ping(client: MongoClient):
    """
    Check the connection to the MongoDB server by pinging the admin database.

    Args:
        client (MongoClient): The MongoDB client.

    Returns:
        bool: True if the connection is successful, False otherwise.
    """
    try:
        client.admin.command("ping")
        return True
    except Exception as e:
        return False


def main():
    client = initialize_mongodb()
    # st.session_state.is_pinging = ping(client=client)

    st.write("### User Signup")
    user_signup_form = {
        "name": st.text_input("Enter your name:", ""),
        "email": st.text_input("Enter your email:", ""),
        "password": st.text_input("Enter your password:", "", type="password"),
    }

    if st.button("Signup"):
        if not st.session_state.is_session:
            rspnse: Response = signup_user_form(user_signup_form=user_signup_form)
            if not rspnse.is_error:
                st.success(rspnse.message)
                st.session_state.user_data = rspnse.data
                st.session_state.is_session = True

            else:
                st.error(rspnse.message)

        else:
            st.error(rspnse.message)

    st.write("### User Login")
    user_login_form = {
        "email": st.text_input("Enter your email:", ""),
        "password": st.text_input("Enter your password:", "", type="password"),
    }

    if st.button("Login"):
        if not st.session_state.is_session:
            rspnse: Response = login_user_form(user_login_form=user_login_form)
            if not rspnse.is_error:
                st.success(rspnse.message)
                st.session_state.user_data = rspnse.data
                st.session_state.is_session = True

            else:
                st.error(rspnse.message)

        else:
            st.error(rspnse.message)


if __name__ == "__main__":
    main()
