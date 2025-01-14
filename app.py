import streamlit as st
from st_components.view_edit_issue import view_edit_page
from st_components.create_issue import create_issue_page
from st_components.display_tasks import display_tasks_page
from css import run_css
import custom_components
from speech import speech_to_text
from agents.user_state_extractor import StateExtractor
from agents.location_extractor import LocationExtractor

# app setup
run_css()

# Initialization
if "initialized" not in st.session_state:
    # User State Information
    st.session_state["user_state"] = {}
    st.session_state.user_state["screen"] = "home"
    st.session_state.user_state["issue_description"] = None
    

    # Location Information
    st.session_state["location"] = {}
    st.session_state.location["jobsite"] = None
    st.session_state.location["area"] = None

    # Create New Issue State
    st.session_state["new_issue"] = {}
    st.session_state.new_issue["name"] = None
    st.session_state.new_issue["description"] = None
    st.session_state.new_issue["classification"] = None
    st.session_state.new_issue["action_to_resolve"] = None
    st.session_state.new_issue["new_event_images"] = []
    st.session_state.new_issue["new_event_description_raw"] = ""
    st.session_state.new_issue["due_datetime"] = None
    st.session_state.new_issue["audio"] = None

    # Query
    st.session_state['query'] = {}
    st.session_state.query['select_query'] = "SELECT * FROM issue LIMIT 10"

    # App Operations Information
    st.session_state['initialized'] = True
    st.session_state["next_missing_data"] = None
    st.session_state['camera_clear_hack'] = 0
    st.session_state['audio_input_hack']= 0
    st.session_state['location_audio_input_hack']= 0

    



# Top of every screen 
navbar = custom_components.navbar()


#Routing 
if st.session_state.user_state["screen"] == "home":
    st.header("Placeholder Home Screen")
    audio = st.audio_input("Voice Assistant", key=f"audio_{st.session_state.audio_input_hack}")
    if audio:
        st.session_state.new_issue["audio"] = audio
        StateExtractor.extract(speech_to_text(audio))
        st.session_state.audio_input_hack += 1 
        st.rerun()

if st.session_state.user_state["screen"] == "create_issue":
    create_issue_page()

if st.session_state.user_state["screen"] == "view_edit":
    view_edit_page()

if st.session_state.user_state['screen'] == "display_tasks":
    display_tasks_page()
    

# Example input
# There is a big ass crack on the tv screen. The things still working thankfully but it looks like we got it that way when they shipped it. We should see if we can get a manufacturing warranty