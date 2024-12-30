import streamlit as st
import tempfile
import openai


def call_speech_api(audio_path):
    
    client = openai.OpenAI(api_key=st.secrets["open_ai_api"])
    
    audio_file= open(audio_path, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )

    return transcription.text 


def speech_to_text(audio):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio.getvalue())
        tmp.close()
        transcribed_text = call_speech_api(tmp.name)
        #st.write(transcribed_text)
    return transcribed_text

    
