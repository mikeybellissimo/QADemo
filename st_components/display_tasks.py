import streamlit as st
import pandas as pd
from speech import speech_to_text
from agents.user_state_extractor import StateExtractor

def display_tasks_page():
    
    conn = st.connection('dummy_db', type='sql')
    data = conn.query(st.session_state.query['select_query'], ttl=1)
    st.dataframe(data)

    audio = st.audio_input("Voice Assistant", key=f"audio_{st.session_state.audio_input_hack}")
    if audio:
        StateExtractor.extract(speech_to_text(audio))
        print(st.session_state.query['select_query'])
        st.session_state.audio_input_hack += 1 
        st.rerun()