import streamlit as st
from st_components.location_prompt import prompt_for_location

def navbar():
    st.markdown('''<div class="navbar">
                        <div id = "navbarLeft">Menu</div>
                        <div id = "navbarCenter">Logo</div>
                        <div id = "navbarRight">User</div>
                    </div>''', unsafe_allow_html=True)
    with st.container(key="locationHeader"):
        if st.button(str(st.session_state.location["jobsite"]) + " - " + str(st.session_state.location["area"])):
            prompt_for_location()
       