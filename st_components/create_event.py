import streamlit as st
from speech import speech_to_text
from extractors.issue_extractor import IssueExtractor

from st_components.location_prompt import prompt_for_location
def create_event_page():
    def get_modified_raw_description():
        st.session_state.new_issue["new_event_description_raw"] = st.session_state["raw_description_text_area"]
    
    
    
        
    
    if st.session_state.location['jobsite'] == None or st.session_state.location['area'] == None:
        prompt_for_location()
    
    recent_picture = st.camera_input(label="Take a picture of an issue", label_visibility="hidden", key=f"camera_{st.session_state.camera_clear_hack}")

    audio = st.audio_input("Describe the Issue", key=f"audio_{st.session_state.audio_input_hack}")
    
    done_button = st.button("Review", key="doneButton")
    if audio:
        st.session_state.new_issue["audio"] = audio
        st.session_state.new_issue["new_event_description_raw"] += " " + speech_to_text(audio)
        st.session_state.audio_input_hack += 1 

    if recent_picture:
        st.session_state.new_issue["new_event_images"].append(recent_picture)
        # This makes it so the camera resets after each picture instead of having to hit "Clear Photo" every time
        st.session_state.camera_clear_hack += 1
        st.rerun()

    
    if st.session_state.new_issue["new_event_description_raw"] == "" and st.session_state.user_state["issue_description"] != None:
        st.session_state.new_issue["new_event_description_raw"] = st.session_state.user_state["issue_description"]

    raw_description = st.text_area("Raw Description", st.session_state.new_issue["new_event_description_raw"], placeholder="Issue Description", on_change=get_modified_raw_description, key="raw_description_text_area", label_visibility="hidden")
    
    
    if done_button:
        IssueExtractor.extract(st.session_state.new_issue["new_event_description_raw"])
        st.session_state.user_state['screen'] = "view_edit"
        st.rerun()

    for image in st.session_state.new_issue["new_event_images"]:
        st.image(image)
    
