from database import db


class ConversationManager:
    def __init__(self, username) -> None:
        self.conversations = db["conversations"][username]

    def create_conversation(self, query):
        result = self.conversations.insert_one(query)
        return result

    def retrieve_conversations(self):
        conversation_records = [record for record in self.conversations.find()]
        return conversation_records

    def update_conversation(self, conversation_id, response):
        query = {"conversation_id": conversation_id}
        result = self.conversations.update_one(query, {"$set": response})
        return result

    def get_conversation_count(self):
        return len(self.retrieve_conversations())

    def delete_user_conversations(self):
        result = db.drop_collection(self.conversations)
        return result
