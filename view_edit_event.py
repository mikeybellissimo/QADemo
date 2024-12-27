import streamlit as st

def view_edit_page():
    st.write("Name: " + str(st.session_state.new_issue["name"]))
    st.write("Description: " + str(st.session_state.new_issue["description"]))
    st.write("Classification: " + str(st.session_state.new_issue["classification"]))
    st.write("Action: " + str(st.session_state.new_issue["action_to_resolve"]))