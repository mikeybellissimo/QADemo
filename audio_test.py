import streamlit as st
import speech_recognition as sr
import tempfile
import time


# Recognizer for voice input
recognizer = sr.Recognizer()

# Voice-to-Text Function
def speech_to_text(audio_path):
    start_time = time.time()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        return text + " AND THE TIME IT TOOK WAS: " + str(time.time()-start_time)
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand the audio."
    except sr.RequestError as e:
        return f"Error with speech recognition: {e}"


# Handle User Input
audio = st.audio_input("Describe the Issue")

if audio:
    file_name = "output.wav"

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio.getvalue())
        tmp.close()
        transcribed_text = speech_to_text(tmp.name)
        st.success(f"You said: {transcribed_text}")
    
    
