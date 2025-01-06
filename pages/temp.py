jobsite_input_text = st.text_input("Jobsite", value=str(st.session_state.location["jobsite"]))
area_input_text = st.text_input("Area", value=str(st.session_state.location['area']))
location_done_button = st.button("Done", key="doneButton" + "Location")
if location_done_button:
    
    if jobsite_input_text != "None":
        st.session_state.location['jobsite'] = jobsite_input_text
    if area_input_text != "None":
        st.session_state.location['area'] = area_input_text
    st.rerun()