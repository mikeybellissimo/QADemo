import streamlit as st
from st_components.location_prompt import prompt_for_location

def navbar():
    def set_jobsite():
        if st.session_state["raw_jobsite_text_input"] != None:
            st.session_state.location["jobsite"] = st.session_state["raw_jobsite_text_input"]
    def set_area():
        if st.session_state["raw_area_text_input"] != None:
            st.session_state.location["area"] = st.session_state["raw_area_text_input"]
    
    st.markdown('''<div class="navbar">
                        <div id = "navbarLeft">Menu</div>
                        <div id = "navbarCenter">Logo</div>
                        <div id = "navbarRight">User</div>
                    </div>''', unsafe_allow_html=True)
    with st.container(key="locationHeader"):
        
        if st.button(str(st.session_state.location["jobsite"]) + " - " + str(st.session_state.location["area"])):
            prompt_for_location()
       