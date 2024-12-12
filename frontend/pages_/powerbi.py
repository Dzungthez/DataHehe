import streamlit as st
import requests

def show_powerbi():
    st.title("Power BI Visualization")

    # Upload CSV
    csv_file = st.file_uploader("Upload CSV File", type="csv")

    if csv_file:
        st.write("CSV uploaded successfully!")

        # Call backend example
        response = requests.post(
            "http://localhost:8000/api/csv_powerbi", 
            files={"file": csv_file}
        )
        
        if response.status_code == 200:
            powerbi_url = response.json().get("powerbi_url")
            st.write("Here is your Power BI report:")
            st.markdown(f'<iframe width="800" height="600" src="{powerbi_url}"></iframe>', unsafe_allow_html=True)
        else:
            st.error("There was an error processing your CSV file.")
