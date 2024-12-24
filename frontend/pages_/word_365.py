import webbrowser
from datetime import datetime
import json
import os
import msal
import streamlit as st
import requests

APP_ID = "c9e7a750-a477-4f65-b4ef-2269c8518df3"
DIR_ID = "5e158e2a-0596-4a6c-8801-3502aef4563f"
USERNAME = "22028046@vnu.edu.vn"
PASSWORD = "Chichich11"
AUTHORITY_URL = f"https://login.microsoftonline.com/{DIR_ID}"
SCOPES = ["Files.ReadWrite"]

GRAPH_API_ENDPOINT = 'https://graph.microsoft.com/v1.0'

def get_access_token():
    token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "https://graph.microsoft.com/.default",
        "grant_type": "client_credentials",
    }
    response = requests.post(token_url, data=payload)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        st.error(f"Failed to get access token: {response.status_code} - {response.text}")
        return None
# Tải file lên thư viện tài liệu SharePoint
def upload_file_to_sharepoint(access_token, file_name, file_data):
    upload_url = f"https://graph.microsoft.com/v1.0/sites/{SITE_ID}/drives/{DOCUMENT_LIBRARY}/root:/{file_name}:/content"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/octet-stream",
    }
    response = requests.put(upload_url, headers=headers, data=file_data)
    if response.status_code == 201:
        st.success("File uploaded successfully!")
        return response.json()
    else:
        st.error(f"Failed to upload file: {response.status_code} - {response.text}")
        return None


 
def show_word_365():
    st.title("Edit Your Word Document in Word 365")

    word_file = st.file_uploader("Upload Word File", type="docx")

    if word_file:
        st.write("Uploading Word file to OneDrive...")
        if st.button("Upload File"):
            st.info("Getting access token...")
            access_token = get_access_token()
            
            if access_token:
                st.info("Uploading file to SharePoint...")
                upload_response = upload_file_to_sharepoint(access_token, uploaded_file.name, uploaded_file.read())
                
                if upload_response:
                    st.json(upload_response)  # Hiển thị thông tin file đã upload
        
show_word_365()
