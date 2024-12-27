import streamlit as st

def navbar():
    st.markdown('''<div class="navbar">
                        <div id = "navbarLeft">Menu</div>
                        <div id = "navbarCenter">Logo</div>
                        <div id = "navbarRight">User</div>
                    </div>''', unsafe_allow_html=True)
    st.text("Jobsite: " + str(st.session_state.user_state["jobsite"]))
    st.text("Area: " + str(st.session_state.user_state["area"]))
