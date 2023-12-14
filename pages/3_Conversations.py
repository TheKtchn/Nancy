import streamlit as st

from conversation_functions import add_chat, get_chats
from response import Response

if "username" not in st.session_state.keys():
    st.session_state.username = ""

cntnr = st.container(border=True)
cntnr.write(st.session_state.username)

if st.session_state.username:
    get_chats_response: Response = get_chats(username=st.session_state.username)
    if get_chats_response.is_error:
        st.error(get_chats_response.message)
    else:
        for chat in get_chats_response.data:
            st.write(chat)

else:
    st.info("Authenticate user to get details.")
