import streamlit as st

from utils import stprint


def app():
    st.title("Zusammenfassung")

    name = st.selectbox("Zusammenfassung für:", st.session_state.group.names)

    # get all expenses where name is in other_shares
    owe_money_to_others = []
    get_money_from = []
    for participant in st.session_state.group.participants:
        if participant.name == name:
            dept_book = participant.dept_book
            for other_name, amount in dept_book.items():
                if amount > 0:
                    get_money_from.append((other_name, amount))
                elif amount < 0:
                    owe_money_to_others.append((other_name, -amount))

    if not owe_money_to_others and not get_money_from:
        st.markdown(
            f"<h3 style='font-size:24px;'>Keine Schulden und keine Forderungen</h3>",
            unsafe_allow_html=True,
        )
    if owe_money_to_others:
        st.write("--------")
        st.markdown(
            f"<h3 style='font-size:24px;'>Du schuldest:</h3>",
            unsafe_allow_html=True,
        )
        text_col, money_col, button_col = st.columns([3, 1, 1])
        for other_name, amount in owe_money_to_others:
            text_col.markdown(
                f"<h3 style='font-size:18px; color: red;'>{other_name}</h3>",
                unsafe_allow_html=True,
            )
            money_col.markdown(
                f"<h3 style='font-size:18px; color: red;'>{amount:.2f} €</h3>",
                unsafe_allow_html=True,
            )
            if button_col.button("Bezahlen", key=other_name):
                st.session_state.group.pay_dept(name, other_name)
                st.session_state["payment_made"] = True
                st.rerun()

    if get_money_from:

        st.write("--------")
        st.markdown(
            f"<h3 style='font-size:24px;'>Dir schulden:</h3>",
            unsafe_allow_html=True,
        )
        name_col, money_col, _ = st.columns([3, 1, 1])
        for other_name, amount in get_money_from:
            name_col.markdown(
                f"<h3 style='font-size:18px; color: green;'>{other_name}</h3>",
                unsafe_allow_html=True,
            )
            money_col.markdown(
                f"<h3 style='font-size:18px; color: green;'>{amount:.2f} €</h3>",
                unsafe_allow_html=True,
            )
