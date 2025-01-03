import streamlit as st
import pandas as pd



def display_tasks_page():
    
    conn = st.connection('dummy_db', type='sql')
    data = conn.query('SELECT name, color, Upper(name), Lower(name), UPPer(color) from dum', ttl=1)#pd.DataFrame({'name':['Mikey','Clari','Oso'], 'color':['White','Morena','White']})
    st.dataframe(data)

