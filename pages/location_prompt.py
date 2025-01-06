import streamlit as st
from extractors.location_extractor import LocationExtractor
from speech import speech_to_text

@st.dialog("Set Location")
def prompt_for_location():
    location_audio = st.audio_input("Describe the Issue", label_visibility="hidden", key=f"location_audio_{st.session_state.audio_input_hack}")
    if location_audio:
        LocationExtractor.extract(speech_to_text(location_audio))
        st.session_state.location_audio_input_hack += 1
        st.rerun()
    