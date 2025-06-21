import streamlit as st
import soundfile as sf
import io
import numpy as np

default_colors = ["#FF5733", "#33C1FF", "#9D33FF", "#33FF57", "#FF33A1"]

def handle_file_upload(uploaded_files):
    if "signals" not in st.session_state:
        st.session_state.signals = []

    # Schritt 1: Alle aktuell hochgeladenen Dateinamen sammeln
    current_file_names = set()
    if uploaded_files:
        current_file_names = {file.name for file in uploaded_files}

    # Schritt 2: signals aufräumen (alle Signale entfernen, deren Datei nicht mehr existiert)
    st.session_state.signals = [
        signal for signal in st.session_state.signals
        if signal.get("file_name") in current_file_names
    ]

    # Schritt 3: Neue Dateien hinzufügen
    existing_files = {signal.get("file_name") for signal in st.session_state.signals}

    if uploaded_files:
        for uploaded_file in uploaded_files:
            if uploaded_file.name not in existing_files:
                file_bytes = io.BytesIO(uploaded_file.read())
                data, samplerate = sf.read(file_bytes)
                data = data if data.ndim > 1 else np.expand_dims(data, axis=1)

                for i in range(data.shape[1]):
                    st.session_state.signals.append({
                        "name": f"{uploaded_file.name} - Ch{i+1}",
                        "file_name": uploaded_file.name,
                        "color": default_colors[len(st.session_state.signals) % len(default_colors)],
                        "data": data[:, i],
                        "fs": samplerate,  # ⬅️ Samplerate speichern
                        "active": True
                    })
