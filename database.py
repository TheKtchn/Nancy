import streamlit as st
from pymongo import MongoClient

# Retrieve MongoDB credentials and cluster information from environment variables
MONGODB_USERNAME = st.secrets["MONGODB_USERNAME"]
MONGODB_PASSWORD = st.secrets["MONGODB_PASSWORD"]
MONGODB_CLUSTER = st.secrets["MONGODB_CLUSTER"]

# Set the MongoDB database name
DB_NAME = "nancy"

# Create a MongoDB connection URI using the retrieved credentials and cluster information
uri = f"mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_CLUSTER}.vfhiusw.mongodb.net/?retryWrites=true&w=majority"

# Create a MongoDB client and select the database
client = MongoClient(uri)
db = client[DB_NAME]


def ping():
    """
    Check the connection to the MongoDB server by pinging the admin database.

    Returns:
        bool: True if the connection is successful, False otherwise.
    """
    try:
        client.admin.command("ping")
        return True
    except Exception as e:
        return False


# Usage example
if __name__ == "__main__":
    if ping():
        print("Connected to MongoDB successfully!")
    else:
        print("Failed to connect to MongoDB.")
