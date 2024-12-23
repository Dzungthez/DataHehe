import streamlit as st
import requests

import requests
import streamlit as st

# Hàm lấy Access Token từ Azure AD
def get_access_token(client_id, client_secret, tenant_id):
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://analysis.windows.net/powerbi/api/.default",
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json().get("access_token")

# Nhúng báo cáo Power BI
def embed_powerbi_report(access_token, embed_url):
    st.markdown(
        f"""
        <iframe width="100%" height="600" src="{embed_url}" frameborder="0" allowFullScreen="true"></iframe>
        """,
        unsafe_allow_html=True
    )

# Thông tin cấu hình Azure AD
client_id = "327aa5cb-392c-4774-bbfe-468ed06bd746"  # Client ID từ Azure AD
client_secret = "a6e94ae8-da2e-4d60-a2dc-4ffca32f08a8"  # Client Secret từ Azure AD
tenant_id = "5e158e2a-0596-4a6c-8801-3502aef4563f"  # Tenant ID từ Azure AD
embed_url = "YOUR_EMBED_URL"  # URL báo cáo Power BI

# Lấy Access Token
access_token = get_access_token(client_id, client_secret, tenant_id)

# Nhúng báo cáo
embed_powerbi_report(access_token, embed_url)

def push_data_to_powerbi(access_token, dataset_id, table_name, rows):
    url = f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/tables/{table_name}/rows"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = requests.post(url, headers=headers, json={"rows": rows})
    return response.status_code, response.json()

# Ví dụ dữ liệu
rows = [
    {"column1": "Value1", "column2": "Value2"},
    {"column1": "Value3", "column2": "Value4"}
]

# Gửi dữ liệu
status, result = push_data_to_powerbi(access_token, "DATASET_ID", "TABLE_NAME", rows)
print(status, result)


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
