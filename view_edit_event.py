import streamlit as st
from datetime import datetime, timedelta
def view_edit_page():
    st.title("Review Issue")
    st.session_state.new_issue["name"] = st.text_input("Name: " , value= str(st.session_state.new_issue["name"]))
    st.session_state.new_issue["description"] = st.text_area("Description: " , value= str(st.session_state.new_issue["description"]))
    st.session_state.new_issue["classification"] = st.text_input("Classification: " , value= str(st.session_state.new_issue["classification"]))
    st.session_state.new_issue["action_to_resolve"] = st.text_input("Action: " , value= str(st.session_state.new_issue["action_to_resolve"]))
    if st.session_state.new_issue["due_datetime"] == "":
        due_dt = (datetime.now() + timedelta(hours=24))
    else:
        try:
            due_dt = st.session_state.new_issue["due_datetime"]
            due_dt = datetime.strptime(due_dt, "%Y-%m-%dT%H:%M")
        except:
            print("Time is being parsed improperly")
            due_dt = (datetime.now() + timedelta(hours=24))
    st.date_input("Due Date: ", value=due_dt)
    
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

    
    st.subheader("Attach Additional Images")  
    recent_picture = st.camera_input(label="Take a picture of an issue", label_visibility="hidden", key=f"camera_{st.session_state.camera_clear_hack}")
    
    if recent_picture:
        st.session_state.new_issue["new_event_images"].append(recent_picture)
        # This makes it so the camera resets after each picture instead of having to hit "Clear Photo" every time
        st.session_state.camera_clear_hack += 1
        st.rerun()