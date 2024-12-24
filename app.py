import streamlit as st
from view_edit_event import view_edit_page
from create_event import create_event_page
from css import run_css
import custom_components

from agent import Extractor

# app setup
run_css()

navbar = custom_components.navbar()



if "initialized" not in st.session_state:
    # Relevant to User state  
    st.session_state["screen"] = "create_event"

    # App Operations Information
    st.session_state['initialized'] = True
    
    st.session_state["next_missing_data"] = None
    st.session_state["new_event_images"] = []

    st.session_state['camera_clear_hack'] = 0

#Extractor.extract("I want to create a new event")

#print(st.session_state)
if st.session_state.screen == "create_event":
    create_event_page()











# # dummy routing 
# if st.button("CREATE EVENT PAGE"):
#     st.session_state.screen = "view_edit"
#     view_edit_page("Michael.")
# if st.button("CREATE ACTUAL EVENT PAGE"):
#     st.session_state.screen = "create"
#     print(st.session_state)

# # state based generation



