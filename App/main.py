# App
import streamlit as st

# UI Layout
st.write("My first Streamlit app 🎈")
my_upload = st.sidebar.file_uploader("Upload file", type=[".wav"])
