import streamlit as st

def show_sidebar():
    st.sidebar.title("Navigation")
    st.sidebar.radio("Go to", ["Dashboard", "Chat with PDF", "Power BI", "Edit Word"])
