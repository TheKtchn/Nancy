from response import Response
from session_manager import SessionManager


def add_chat(
    session_mngr: SessionManager,
    chat: str,
):
    response = Response()

    # Check if an active session is ongoing
    if not session_mngr.is_session:
        response.is_error = True
        response.message = "No active session is ongoing."
        return response

    if chat:
        response.is_error = True
        response.message = "Chat can't be empty."
        return response

    conversation_id = session_mngr.conversation_mngr.get_conversation_count()
    create_conversation_result = session_mngr.conversation_mngr.create_conversation(
        {conversation_id: chat}
    )

    if create_conversation_result is None:
        response.is_error = True
        response.message = "Chat could not be added."

    else:
        response.message = "Added chat."

    return response


def get_chats(session_mngr: SessionManager):
    response = Response()

    # Check if an active session is ongoing
    if not session_mngr.is_session:
        response.is_error = True
        response.message = "No active session is ongoing."
        return response

    chats = session_mngr.conversation_mngr.retrieve_conversations()
    if chats:
        response.message = chats

    else:
        response.message = "User does not have any chats."

    return response


def add_reply(session_mngr: SessionManager, reply: dict):
    response = Response()

    # Check if an active session is ongoing
    if not session_mngr.is_session:
        response.is_error = True
        response.message = "No active session is ongoing."
        return response

    conversation_id = reply["conversation_id"]
    r = reply["response"]

    update_conversations_result = session_mngr.conversation_mngr.update_conversation(
        conversation_id=conversation_id,
        response=r,
    )

    if update_conversations_result:
        response.message = "Updated conversation."

    else:
        response.is_error = True
        response.message = "Could not update conversation."

    return response
