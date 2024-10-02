import streamlit as st

from modules import ausgaben, teilnehmer, zusammenfassung
from modules.classes import Group

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Pages", ("Teilnehmer", "Ausgaben", "Zusammenfassung"), label_visibility="collapsed"
)

if not st.session_state.get("group"):
    st.session_state["group"] = Group()

    # add some participants for testing
    # st.session_state.group.add_participant("Müller", 6)
    # st.session_state.group.add_participant("Kremser", 3)
    # st.session_state.group.add_participant("Raue", 4)

if page == "Teilnehmer":
    teilnehmer.app()
elif page == "Ausgaben":
    ausgaben.app()
elif page == "Zusammenfassung":
    zusammenfassung.app()
