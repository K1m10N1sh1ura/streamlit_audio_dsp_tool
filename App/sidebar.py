import streamlit as st
from App import state_handler

def render_sidebar():
    # Logo
    st.sidebar.image("audiolab_logo2.png", use_container_width=True)

    # Upload & Signal-Handling
    uploaded_files = st.sidebar.file_uploader(
        "",
        type=["wav"],
        accept_multiple_files=True
    )
    state_handler.handle_file_upload(uploaded_files)

    # Signal-Liste anzeigen
    st.sidebar.markdown("### Signals")
    for i, signal in enumerate(st.session_state.signals):
        col1, col2 = st.sidebar.columns([0.7, 0.3])

        # Textfeld links
        new_name = col1.text_input("", value=signal["name"], key=f"name_{i}")

        # Toggle rechts
        new_state = col2.toggle("Show", value=signal["active"], key=f"toggle_{i}")

        # Update
        st.session_state.signals[i]["name"] = new_name
        st.session_state.signals[i]["active"] = new_state
