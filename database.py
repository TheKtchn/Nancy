import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGODB_USERNAME = os.getenv("MONGODB_USERNAME")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
MONGODB_CLUSTER = os.getenv("MONGODB_CLUSTER")
DB_NAME = "nancy"

# Create a MongoDB client and database instance
uri = f"mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_CLUSTER}.vfhiusw.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client[DB_NAME]


# Function to check the database connection
def ping():
    try:
        client.admin.command("ping")
        return True
    except Exception as e:
        return False
