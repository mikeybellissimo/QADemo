import streamlit as st

def run_css():
    st.markdown("""
        <style>
        .navbar {
            background-color: black;
            color: white;
            width: 100%;
            height: 50px;
            display:flex;
            text-align: center;
            align-items: center;
        }
                
        #navbarLeft{
            width: 25%; 
        }
        #navbarCenter{
            width: 50%; 
        }
        #navbarRight{
            width: 25%; 
        }
        
        .st-key-doneButton > .stButton > button {
            background-color: #228B22;
            width: 100%;
        }

        .st-emotion-cache-yw8pof {
            width: 100%;
            padding: 3rem 0rem 10rem;
            max-width: 100%;
        }
        </style>
        """, unsafe_allow_html=True)
