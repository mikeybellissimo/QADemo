import streamlit as st
import speech_recognition as sr
import tempfile
import time
import openai

# Recognizer for voice input
recognizer = sr.Recognizer()

def call_speech_api(audio_path):
    
    client = openai.OpenAI(api_key=st.secrets["open_ai_api"])

    audio_file= open(audio_path, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )

    return transcription.text 

# # Voice-to-Text Function
# def call_speech_api(audio_path):
#     start_time = time.time()
#     with sr.AudioFile(audio_path) as source:
#         audio = recognizer.record(source)
#     try:
#         text = recognizer.recognize_google(audio)
#         return text
#     except sr.UnknownValueError:
#         return "Sorry, I couldn't understand the audio."
#     except sr.RequestError as e:
#         return f"Error with speech recognition: {e}"


def speech_to_text(audio):
    file_name = "output.wav"

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio.getvalue())
        tmp.close()
        transcribed_text = call_speech_api(tmp.name)
        #st.write(transcribed_text)
    return transcribed_text

    
