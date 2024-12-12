import streamlit as st
import requests

def show_word_365():
    st.title("Edit Your Word Document")

    word_file = st.file_uploader("Upload Word File", type="docx")

    if word_file:
        st.write("Word file uploaded successfully!")

        # call backend example
        response = requests.post(
            "http://localhost:8000/api/word_365", 
            files={"file": word_file}
        )
        
        if response.status_code == 200:
            word_url = response.json().get("word_url")
            st.write("Click below to edit the document in Word 365:")
            st.markdown(f"[Edit Document]({word_url})", unsafe_allow_html=True)
        else:
            st.error("There was an error processing your Word file.")
