import streamlit as st
from view_edit_event import view_edit_page
from create_event import create_event_page
from css import run_css
import custom_components
from speech import speech_to_text
from agent import Extractor

# app setup
run_css()


# Initialization
if "initialized" not in st.session_state:
    # Relevant to User Inspection Information  
    st.session_state["area"] = None
    st.session_state["jobsite"] = None

    # App Operations Information
    st.session_state['initialized'] = True
    st.session_state["screen"] = "home"
    st.session_state["next_missing_data"] = None
    st.session_state["new_event_images"] = []
    st.session_state["new_event_description_raw"] = ""

    st.session_state['camera_clear_hack'] = 0
    st.session_state['audio_input_hack']= 0

# Top of every screen 
navbar = custom_components.navbar()




#Routing 
if st.session_state.screen == "home":
    audio = st.audio_input("Voice Assistant", key=f"audio_{st.session_state.audio_input_hack}")
    if audio:
        Extractor.extract(speech_to_text(audio))
        st.session_state.audio_input_hack += 1 
        st.rerun()
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



