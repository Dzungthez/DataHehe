# app.py
import streamlit as st
from pages_.dashboard import show_dashboard
from pages_.chatapp import show_pdf_chat
from pages_.powerbi import show_powerbi
from pages_.word_365 import show_word_365
from state import initialize_state

# Cấu hình bố cục trang
st.set_page_config(layout="wide")

def main():
    initialize_state()  # Khởi tạo session state

    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", ["Dashboard", "Chat with Files", "Power BI", "Edit Doc"])

    if selection == "Dashboard":
        show_dashboard()
    elif selection == "Chat with Files":
        show_pdf_chat()
    elif selection == "Power BI":
        show_powerbi()
    elif selection == "Edit Doc":
        show_word_365()

if __name__ == "__main__":
    main()
