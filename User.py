import streamlit as st

from response import Response
from user_functions import authenticate_user, remove_user

if "username" not in st.session_state.keys():
    st.session_state.username = ""

with st.form(key="Authentication", clear_on_submit=True):
    username = st.text_input("Enter username: ")

    is_submitted = st.form_submit_button("Authenticate")
    if is_submitted:
        r: Response = authenticate_user(username)

        if not r.is_error:
            st.success(r.message)
            st.session_state.username = username
        else:
            st.error(r.message)


if st.button("Logout", type="primary"):
    st.session_state.username = ""

if st.button("Delete User", type="primary"):
    r: Response = remove_user(username=st.session_state.username)
    if not r.is_error:
        st.success(r.message)
    else:
        st.error(r.message)

    st.session_state.username = ""

cntnr = st.container(border=True)
cntnr.write(st.session_state.username)
