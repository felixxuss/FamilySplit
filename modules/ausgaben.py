import streamlit as st

from modules.classes import Expense


def app():
    st.header("Ausgabe hinzufügen")
    name_col, shares_col, amount_col = st.columns([2, 1, 2])

    payed_by_name = name_col.selectbox("Name", st.session_state.group.names)

    max_shares = st.session_state.group.get_shares_by_name(payed_by_name)
    own_shares = shares_col.number_input(
        "Anteile", min_value=0, max_value=max_shares, step=1, value=max_shares
    )
    amount = amount_col.number_input("Betrag in €", min_value=0.0, step=0.01, value=0.0)
    note = st.text_input("Notiz", "")

    with st.expander("Anteile"):
        for participant in st.session_state.group.participants:
            if participant.name == payed_by_name:
                continue
            other_name_col, other_share_col = st.columns([2, 1])
            other_name_col.write(participant.name)
            other_share_col.number_input(
                "Anteile",
                min_value=0,
                max_value=participant.shares,
                step=1,
                value=participant.shares,
                label_visibility="collapsed",
                key=f"{participant.name}_other_share",
            )

    add_button = st.button(label="Hinzufügen")

    # save the expense
    if add_button:
        if not note:
            st.toast("Bitte eine Notiz hinzufügen.")
        else:
            # get other_shares by keys
            other_shares = {}
            for participant in st.session_state.group.participants:
                name = participant.name
                # get value of number-input by key
                share = st.session_state.get(f"{name}_other_share", None)
                # share is only None if the participant is the payed_by participant
                # when share is 0, the participant is not included in other shares
                if share:
                    other_shares[name] = share

            expense = Expense(payed_by_name, own_shares, other_shares, amount, note)
            st.session_state.group.add_expense_to_participants(payed_by_name, expense)

    st.write("--------")

    st.header("Übersicht")
    for expense in st.session_state.group.all_expenses:
        name = expense.payed_by
        amount = expense.amount
        note = expense.note
        with st.expander(f"{name} hat {amount:.2f} € für {note} bezahlt"):
            name_col, share_col, amount_col = st.columns([2, 1, 2])
            name_col.markdown(
                "<h3 style='font-size:24px;'>Name</h3>", unsafe_allow_html=True
            )
            share_col.markdown(
                "<h3 style='font-size:24px;'>Anteile</h3>", unsafe_allow_html=True
            )
            amount_col.markdown(
                "<h3 style='font-size:24px;'>Betrag</h3>", unsafe_allow_html=True
            )
            for true_share in expense.true_shares:
                name_col, share_col, amount_col = st.columns([2, 1, 2])
                name_col.write(true_share[0])
                share_col.write(f"{true_share[1]}")
                amount_col.write(f"{true_share[2]:.2f} €")

            if st.button("Ausgabe löschen", key=expense.ID):
                if not st.session_state.get("payment_made"):
                    st.session_state.group.remove_expense(expense.ID)
                    st.rerun()
                else:
                    st.toast(
                        "Es wurde bereits eine Bezahlung getätigt. Es können keine Ausgaben mehr gelöscht werden."
                    )
