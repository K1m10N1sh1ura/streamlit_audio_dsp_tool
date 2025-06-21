import streamlit as st
from App import sidebar, plots

st.set_page_config(page_title="AudioLab", layout="wide")

# Sidebar (Upload + Signal-Steuerung)
sidebar.render_sidebar()

# Plotbereich
plots.render_plot()