def show_dashboard():
    import streamlit as st

    # Title Section
    st.title("Dashboard")

    # Main Dashboard Content
    st.markdown("### Welcome to the Main Dashboard!")
    st.markdown(
        "Here, as a user, you can manage your data and access the different tools available in our website."
    )

    # Tools Section
    st.markdown("## Available Tools")

    # Chat with PDF
    st.markdown("### 1. Chat with PDF")
    st.write("Interact with PDF documents using our advanced chat tool.")

    # Power BI Visualization
    st.markdown("### 2. Power BI Visualization")
    st.write("Visualize your data and gain insights using Power BI dashboards.")

    # Edit Word Document
    st.markdown("### 3. Edit Word Document")
    st.write("Edit and customize your Word documents directly within the app.")