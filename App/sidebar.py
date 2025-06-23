import streamlit as st
from . import state_handler
import os
import soundfile as sf
import numpy as np

def render_sidebar():
    # Logo
    st.sidebar.image("audiolab_logo2.png", use_container_width=True)

    # Upload & Signal-Handling
    uploaded_files = st.sidebar.file_uploader(
        "",
        type=["wav"],
        accept_multiple_files=True
    )

    # Demo.wav laden, wenn keine Signale und keine Uploads
    if (
        ("signals" not in st.session_state or not st.session_state.signals)
        and not uploaded_files
        and os.path.exists("Demo.wav")
    ):
        data, samplerate = sf.read("Demo.wav")
        data = data if data.ndim > 1 else np.expand_dims(data, axis=1)
        default_colors = ["#FF5733", "#33C1FF", "#9D33FF", "#33FF57", "#FF33A1"]
        st.session_state.signals = []
        for i in range(data.shape[1]):
            st.session_state.signals.append({
                "name": f"Demo.wav - Ch{i+1}",
                "file_name": "Demo.wav",
                "color": default_colors[i % len(default_colors)],
                "data": data[:, i],
                "fs": samplerate,
                "active": True
            })

    state_handler.handle_file_upload(uploaded_files)

    # Signal-Liste anzeigen
    st.sidebar.markdown("### Signals")
    for i, signal in enumerate(st.session_state.signals):
        col1, col2 = st.sidebar.columns([0.7, 0.3])

        # Textfeld links
        new_name = col1.text_input("", value=signal["name"], key=f"name_{i}")

        # Play/Pause Button
        play_key = f"play_{i}"
        if play_key not in st.session_state:
            st.session_state[play_key] = False
        if col2.button("▶️" if not st.session_state[play_key] else "⏸️", key=f"play_button_{i}"):
            st.session_state[play_key] = not st.session_state[play_key]

        if st.session_state[play_key]:
            st.sidebar.audio(signal["data"], sample_rate=signal["fs"])

        # Update
        st.session_state.signals[i]["name"] = new_name

    st.sidebar.markdown("---")
    button_html = """
<a href="https://coff.ee/k1m10n1sh1ura" target="_blank">
    <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 51px !important;width: 217px !important;" >
</a>
"""
    st.sidebar.markdown(button_html, unsafe_allow_html=True)
