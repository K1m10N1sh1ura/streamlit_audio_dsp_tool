import streamlit as st
import os
import soundfile as sf
import numpy as np
from App import sidebar, plots

# Demo.wav beim allerersten Start laden
if "signals" not in st.session_state or not st.session_state.signals:
    demo_path = "Demo.wav"
    if os.path.exists(demo_path):
        data, samplerate = sf.read(demo_path)
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

st.set_page_config(page_title="AudioLab", layout="wide", initial_sidebar_state="expanded")

# Sidebar (Upload + Signal-Steuerung)
sidebar.render_sidebar()

# Plotbereich
plots.render_plot()