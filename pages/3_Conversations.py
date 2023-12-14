import streamlit as st

from conversation_functions import add_chat, get_chats
from response import Response

if "username" not in st.session_state.keys():
    st.session_state.username = ""

cntnr = st.container(border=True)
cntnr.write(st.session_state.username)

if st.session_state.username:
    input_chat = st.chat_input("Say something...")
    add_chat_response: Response = add_chat(
        username=st.session_state.username, chat=input_chat
    )
    if add_chat_response.is_error:
        st.error(add_chat_response.message)
    else:
        st.success(add_chat_response.message)

    get_chats_response: Response = get_chats(username=st.session_state.username)
    if get_chats_response.is_error:
        st.error(get_chats_response.message)
    else:
        with st.chat_message("user"):
            number_of_chats = len(get_chats_response.data)
            for i in range(number_of_chats):
                print(type(get_chats_response.data))
                st.write(get_chats_response.data[i][f"{i+1}"])

else:
    st.info("Authenticate user to get details.")
