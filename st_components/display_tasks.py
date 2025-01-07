import streamlit as st
import pandas as pd
from agents.query_extractor import QueryExtractor
from speech import speech_to_text

def display_tasks_page():
    
    conn = st.connection('dummy_db', type='sql')
    data = conn.query(st.session_state.query['select_query'], ttl=1)
    st.dataframe(data)

    audio = st.audio_input("Voice Assistant", key=f"audio_{st.session_state.audio_input_hack}")
    if audio:
        st.session_state.new_issue["audio"] = audio
        #LocationExtractor.extract(speech_to_text(audio))
        QueryExtractor.extract(speech_to_text(audio))
        print(st.session_state.query['select_query'])
        st.session_state.audio_input_hack += 1 
        st.rerun()