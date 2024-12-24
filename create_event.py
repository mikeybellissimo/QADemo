import streamlit as st
import tempfile 
def create_event_page():
    recent_picture = st.camera_input(label="Take a picture of an issue", label_visibility="hidden", key=f"camera_{st.session_state.camera_clear_hack}")

    audio = st.audio_input("Describe the Issue")
    
    
    if audio:
        file_name = "output.wav"

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio.getvalue())
            tmp.close()
            transcribed_text = speech_to_text(tmp.name)
            st.success(f"You said: {transcribed_text}")

    if recent_picture:
        st.session_state.new_event_images.append(recent_picture)
        # This makes it so the camera resets after each picture instead of having to hit "Clear Photo" every time
        st.session_state.camera_clear_hack += 1
        st.rerun()

    for image in st.session_state.new_event_images:
        st.image(image)
        
