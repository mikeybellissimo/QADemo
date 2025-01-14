import streamlit as st
from agents.location_extractor import LocationExtractor
from speech import speech_to_text

@st.dialog("Set Location")
def prompt_for_location():
    st.write("Please enter your location.")
    location_audio = st.audio_input("Describe the Issue", label_visibility="hidden", key=f"location_audio_{st.session_state.audio_input_hack}")
    if location_audio:
        LocationExtractor.extract(speech_to_text(location_audio))
        st.session_state.location_audio_input_hack += 1
        st.rerun()
        
    jobsite_input_text = st.text_input("Jobsite", value=str(st.session_state.location["jobsite"]))
    area_input_text = st.text_input("Area", value=str(st.session_state.location['area']))
    location_done_button = st.button("Done", key="doneButton" + "Location")
    if location_done_button:
        
        if jobsite_input_text != "None":
            st.session_state.location['jobsite'] = jobsite_input_text
        if area_input_text != "None":
            st.session_state.location['area'] = area_input_text
        st.rerun()