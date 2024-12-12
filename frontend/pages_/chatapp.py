import streamlit as st
import requests

def show_pdf_chat():
    st.title("Chat with Your PDF")

    # Upload PDF
    pdf_file = st.file_uploader("Upload PDF", type="pdf")
    
    if pdf_file:
        st.write("PDF uploaded successfully!")

        question = st.text_area("Ask a question about your PDF:")

        if question:
            # call backend example
            response = requests.post(
                "http://localhost:8000/api/pdf_chat", 
                files={"file": pdf_file},
                data={"question": question}
            )
            if response.status_code == 200:
                st.write("Answer: ", response.json().get("answer"))
            else:
                st.error("There was an error processing your question.")
