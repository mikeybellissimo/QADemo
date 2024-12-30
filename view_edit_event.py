import streamlit as st
from datetime import datetime, timedelta
def view_edit_page():
    st.write("Name: " + str(st.session_state.new_issue["name"]))
    st.write("Description: " + str(st.session_state.new_issue["description"]))
    st.write("Classification: " + str(st.session_state.new_issue["classification"]))
    st.write("Action: " + str(st.session_state.new_issue["action_to_resolve"]))
    if st.session_state.new_issue["due_datetime"] == "":
        due_dt = (datetime.now() + timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M")
    else:
        due_dt = st.session_state.new_issue["due_datetime"]
    st.write("Due Date: " + str(due_dt))
    
    if st.session_state.new_issue["audio"] == None:
        audio = st.audio_input("Attach Audio", key=f"audio_{st.session_state.audio_input_hack}")
        if audio:
            st.session_state.new_issue["audio"] = audio
    else:
        st.audio(st.session_state.new_issue["audio"])
    for im, ind in zip(st.session_state.new_issue["new_event_images"], range(len(st.session_state.new_issue["new_event_images"]))):
        st.image(im)
        if st.button("Delete", key="removeButton" + str(ind)):
            del st.session_state.new_issue["new_event_images"][ind]
            st.rerun()
        
    