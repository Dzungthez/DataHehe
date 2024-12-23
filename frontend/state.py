# state.py
import streamlit as st

def initialize_state():
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "uploaded_files" not in st.session_state:
        st.session_state["uploaded_files"] = []
