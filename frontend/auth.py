
# def login():
#     auth_url = app.get_authorization_request_url(
#         scopes=["User.Read"],
#         redirect_uri=REDIRECT_URI,
#     )
#     st.write(f"[Login with Azure AD]({auth_url})")

# def handle_redirect():
#     code = st.experimental_get_query_params().get("code", [None])[0]
#     if code:
#         result = app.acquire_token_by_authorization_code(
#             code,
#             scopes=["User.Read"],
#             redirect_uri=REDIRECT_URI,
#         )
#         if "access_token" in result:
#             st.session_state.user = result["id_token_claims"]
#             st.rerun()
#     else:
#         st.write("Authentication failed. Try again.")

# def logout():
#     if "user" in st.session_state:
#         del st.session_state.user
#         st.rerun()

# def is_authenticated():
#     return "user" in st.session_state


import msal
import streamlit as st
from msal import ConfidentialClientApplication
from dotenv import load_dotenv
import os

load_dotenv()

# Lấy giá trị từ biến môi trường
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")
REDIRECT_URI = os.getenv("REDIRECT_URI")


app = ConfidentialClientApplication(
    CLIENT_ID,
    authority=f"https://login.microsoftonline.com/{TENANT_ID}",
    client_credential=CLIENT_SECRET,
)

def login():
    auth_url = app.get_authorization_request_url(
        scopes=["User.Read"],
        redirect_uri=REDIRECT_URI,
    )
    st.write(f"[Login with Azure AD]({auth_url})")
def handle_redirect():
    query_params = st.query_params
    code = query_params.get("code")
    if isinstance(code, list):
        code = code[0]
    if code:
        result = app.acquire_token_by_authorization_code(
            code,
            scopes=["User.Read"],
            redirect_uri=REDIRECT_URI,
        )
        if "access_token" in result:
            st.session_state.user = result["id_token_claims"]
            st.rerun()

    st.info("Please log in to access the app")
        

def logout():
    if "user" in st.session_state:
        del st.session_state.user
        st.success("Logged out successfully.")
        st.rerun()

def is_authenticated():
    return "user" in st.session_state