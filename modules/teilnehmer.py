import streamlit as st


def app():
    # Title
    st.title("Teilnehmer hinzufügen")

    # Form for adding a new participant
    with st.form("add_participant"):
        name_col, share_col = st.columns([3, 1])
        name = name_col.text_input("Name")
        shares = share_col.number_input("Mitglieder", min_value=1, step=1)
        add_button = st.form_submit_button(label="Hinzufügen")

        # If the form is submitted and valid input is provided
        if add_button:
            if name:
                st.session_state.group.add_participant(name, shares)
            else:
                st.toast("Bitte einen Namen eingeben.")

    # Display available participants
    if not st.session_state.group.has_participants:
        return

    st.header("Verfügbare Teilnehmer")
    # show headers for each column
    col1, col2, col3 = st.columns([3, 1, 1])
    col1.markdown("<h3 style='font-size:24px;'>Name</h3>", unsafe_allow_html=True)
    col2.markdown("<h3 style='font-size:24px;'>Mitglieder</h3>", unsafe_allow_html=True)
    for participant in st.session_state.group.participants:
        name = participant.name
        col1, col2, col3 = st.columns([3, 1, 1])

        col1.write(name)
        col2.write(str(participant.shares))
        if col3.button("löschen", key=name):
            can_delete = True
            expenses = st.session_state.group.all_expenses
            if expenses:
                for expense in expenses:
                    if expense.payed_by == name or name in expense.other_shares:
                        st.toast(
                            f"{name} kann nicht gelöscht werden, da eine Anteil an einer Ausgabe existiert."
                        )
                        can_delete = False
                        break

            # Remove participant from the list
            if can_delete:
                st.session_state.group.remove_participant(name)
                st.rerun()
