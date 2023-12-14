from datetime import date, timedelta

import streamlit as st

from response import Response
from transactions_and_balance_functions import (
    add_transaction,
    get_balance,
    get_transactions,
    set_balance,
)

if "username" not in st.session_state.keys():
    st.session_state.username = ""

cntnr = st.container(border=True)
cntnr.write(st.session_state.username)

if st.session_state.username:
    transaction = dict()

    today = date.today()
    lower_bound = today - timedelta(days=3 * 30)

    with st.form(key="Add Transaction", clear_on_submit=True):
        transaction["description"] = st.text_input("Enter description:")
        transaction["amount"] = st.number_input("Enter amount:")
        transaction["category"] = st.radio(
            "Select category:",
            ["Income", "Expense"],
        )
        date_str: date = st.date_input(
            "Enter date:",
            min_value=lower_bound,
            max_value=today,
            format="DD/MM/YYYY",
        )
        transaction["date"] = date_str.strftime("%d/%m/%Y")

        is_submitted = st.form_submit_button("Add")
        if is_submitted:
            add_transaction_response: Response = add_transaction(
                username=st.session_state.username,
                transaction=transaction,
            )
            if not add_transaction_response.is_error:
                st.success(add_transaction_response.message)
            else:
                st.error(add_transaction_response.message)

    with st.form(key="Set Balance", clear_on_submit=True):
        amount = st.number_input("Enter amount:")

        is_submitted = st.form_submit_button("Set")
        if is_submitted:
            set_balance_response: Response = set_balance(
                username=st.session_state.username, amount=amount
            )
            if not set_balance_response.is_error:
                st.success(set_balance_response.message)
            else:
                st.error(set_balance_response.message)

    st.write("### Balance")
    get_balance_response: Response = get_balance(username=st.session_state.username)
    if get_balance_response.is_error:
        st.error(get_balance_response.message)
    else:
        cntnr = st.container(border=True)
        cntnr.write(get_balance_response.data)

    st.write("### Transactions")
    get_transactions_response: Response = get_transactions(
        username=st.session_state.username
    )
    if get_transactions_response.is_error:
        st.error(get_transactions_response.message)
    else:
        st.dataframe(get_transactions_response.data)


else:
    st.info("Authenticate user to get details.")
