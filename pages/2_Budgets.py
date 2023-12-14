from datetime import date, timedelta

import streamlit as st

from budget_functions import add_budget, delete_budget, get_budgets, update_budget
from response import Response

if "username" not in st.session_state.keys():
    st.session_state.username = ""

cntnr = st.container(border=True)
cntnr.write(st.session_state.username)


if st.session_state.username:
    budget = dict()

    today = date.today()
    upper_bound = today + timedelta(days=3 * 30)

    with st.form(key="Add Budget", clear_on_submit=True):
        budget["item"] = st.text_input("Enter item:")
        budget["amount"] = st.number_input("Enter amount:")
        due_date_str = st.date_input(
            "Enter date:",
            min_value=today,
            max_value=upper_bound,
            format="DD/MM/YYYY",
        )
        due_date = due_date_str.strftime("%d/%m/%Y")

        is_submitted = st.form_submit_button("Add")
        if is_submitted:
            add_budget_response: Response = add_budget(
                username=st.session_state.username,
                budget=budget,
            )
            if not add_budget_response.is_error:
                st.success(add_budget_response.message)
            else:
                st.error(add_budget_response.message)

    with st.form(key="Update Budget", clear_on_submit=True):
        budget["item"] = st.text_input("Enter item:")
        budget["amount"] = st.number_input("Enter amount:")
        due_date_str = st.date_input(
            "Enter date:",
            min_value=today,
            max_value=upper_bound,
            format="DD/MM/YYYY",
        )
        budget["due_date"] = due_date_str.strftime("%d/%m/%Y")

        is_submitted = st.form_submit_button("Update")
        if is_submitted:
            update_budget_response: Response = update_budget(
                username=st.session_state.username,
                budget=budget,
            )
            if not update_budget_response:
                st.success(update_budget_response.message)
            else:
                st.error(update_budget_response.message)

    with st.form(key="Delete Budget", clear_on_submit=True):
        item = st.text_input("Enter item:")

        is_submitted = st.form_submit_button("Delete")
        if is_submitted:
            delete_budget_response: Response = delete_budget(
                username=st.session_state.username,
                item=item,
            )
            if not delete_budget_response:
                st.success(delete_budget_response.message)
            else:
                st.error(delete_budget_response.message)

    st.write("### Budgets")
    get_budgets_response: Response = get_budgets(username=st.session_state.username)
    if get_budgets_response.is_error:
        st.error(get_budgets_response.message)
    else:
        st.dataframe(get_budgets_response.data)

else:
    st.info("Authenticate user to get details.")
