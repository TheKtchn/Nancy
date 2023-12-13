import os

import streamlit as st
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


def initialize_mongodb():
    """
    Function to initialize the MongoDB connection.

    Returns:
        MongoClient: The MongoDB client connected to the specified database.
    """
    # Retrieve MongoDB credentials and cluster information from environment variables
    MONGODB_USERNAME = os.getenv("MONGODB_USERNAME")
    MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
    MONGODB_CLUSTER = os.getenv("MONGODB_CLUSTER")

    # Create a MongoDB connection URI using the retrieved credentials and cluster information
    uri = f"mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_CLUSTER}.vfhiusw.mongodb.net/?retryWrites=true&w=majority"

    # Create a MongoDB client and select the database
    client = MongoClient(uri)

    return client  # Return the client


def ping(client):
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

    if st.button("Ping🔌"):
        connected = ping(client)
        if connected:
            st.success("Connected")
        else:
            st.error("Not connected")


if __name__ == "__main__":
    main()
