from conversation_manager import ConversationManager
from response import Response


def add_chat(
    username: str,
    chat: str,
):
    r = Response()

    if not chat:
        r.is_error = True
        r.message = "Chat can't be empty."
        return r

    conversation_mngr = ConversationManager(username)
    conversation_id = conversation_mngr.get_conversation_count() + 1
    create_conversation_result = conversation_mngr.create_conversation(
        {str(conversation_id): chat}
    )

    if create_conversation_result is None:
        r.is_error = True
        r.message = "Chat could not be added."
    else:
        r.message = "Added chat."

    return r


def get_chats(username):
    r = Response()

    conversation_mngr = ConversationManager(username)
    retrieve_conversations_result = conversation_mngr.retrieve_conversations()

    if retrieve_conversations_result is None:
        r.is_error = True
        r.message = "User does not have any chats."
    else:
        r.data = retrieve_conversations_result

    return r
