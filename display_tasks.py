import streamlit as st
import pandas as pd



def display_tasks_page():
    
    conn = st.connection('dummy_db', type='sql')
    data = conn.query('SELECT * from issues', ttl=1)
    st.dataframe(data)

