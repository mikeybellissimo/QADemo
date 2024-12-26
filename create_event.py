import streamlit as st
import tempfile 
from speech import speech_to_text
from streamlit_back_camera_input import back_camera_input

def create_event_page():
    def get_modified_raw_description():
        st.session_state.new_event_description_raw = st.session_state["raw_description_text_area"]
        

    recent_picture = back_camera_input( key=f"camera_{st.session_state.camera_clear_hack}")

    audio = st.audio_input("Describe the Issue", key=f"audio_{st.session_state.audio_input_hack}")
    
    
    if audio:
        st.session_state.new_event_description_raw += speech_to_text(audio)
        st.session_state.audio_input_hack += 1 

    if recent_picture:
        st.session_state.new_event_images.append(recent_picture)
        # This makes it so the camera resets after each picture instead of having to hit "Clear Photo" every time
        st.session_state.camera_clear_hack += 1
        st.rerun()
    
    raw_description = st.text_area("Raw Description", st.session_state.new_event_description_raw, placeholder="Issue Description", on_change=get_modified_raw_description, key="raw_description_text_area", label_visibility="hidden")
    
    for image in st.session_state.new_event_images:
        st.image(image)
    
