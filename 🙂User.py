import os

import streamlit as st
from pymongo import MongoClient
from response import Response
from user_functions import signup_user_form_st

DB_NAME = "nancy"
st.session_state.is_session = False


@st.cache
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
    """
    Streamlit app to check the connection to a MongoDB database.
    """
    st.title("Streamlit MongoDB Client Connection")

    # Initialize MongoDB connection
    client = initialize_mongodb()

    st.title("User Registration")

    name = st.text_input("Enter your name:", "")
    email = st.text_input("Enter your email:", "")
    password = st.text_input("Enter your password:", "", type="password")

    if st.button("Register"):
        if not st.session_state.is_session:
            rspnse: Response = signup_user_form_st()
            if not rspnse.is_error:
                st.success("User registered.")
                st.session_state.user_data = {
                    "name": name,
                    "email": email,
                    "password": password,
                }
                st.session_state.is_session = True
                
            else:
                st.error(f"Could not register user.\n{rspnse.message}")

        else:
            st.error("User in session.")


if __name__ == "__main__":
    main()
