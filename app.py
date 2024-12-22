import streamlit as st

enable = st.checkbox("Enable camera")
picture = st.camera_input("Take a picture", disabled=not enable)

audio_value = st.audio_input("Record a voice message")

if audio_value:
    st.audio(audio_value)

if picture:
    st.image(picture)