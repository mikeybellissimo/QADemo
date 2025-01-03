import streamlit as st
from location_prompt import prompt_for_location

def navbar():
    def set_jobsite():
        if st.session_state["raw_jobsite_text_input"] != None:
            st.session_state.user_state["jobsite"] = st.session_state["raw_jobsite_text_input"]
    def set_area():
        if st.session_state["raw_area_text_input"] != None:
            st.session_state.user_state["area"] = st.session_state["raw_area_text_input"]
    
    st.markdown('''<div class="navbar">
                        <div id = "navbarLeft">Menu</div>
                        <div id = "navbarCenter">Logo</div>
                        <div id = "navbarRight">User</div>
                    </div>''', unsafe_allow_html=True)
    with st.container(key="locationHeader"):
        if st.button(str(st.session_state.user_state["jobsite"]) + " - " + str(str(st.session_state.user_state["area"]))):
            prompt_for_location()
        #st.text_input("Jobsite: ",label_visibility="hidden",  value= str(st.session_state.user_state["jobsite"]), on_change=set_jobsite, key="raw_jobsite_text_input")
        #st.text_input("Area: ", label_visibility="hidden",  value = str(st.session_state.user_state["area"]), on_change=set_area, key="raw_area_text_input")
