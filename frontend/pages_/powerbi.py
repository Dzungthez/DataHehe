import streamlit as st
import requests

# def show_powerbi():
#     st.title("Tải CSV lên Power BI")

#     # Upload CSV
#     csv_file = st.file_uploader("Tải lên tệp CSV", type="csv")

#     if csv_file:
#         # Tạo key động cho mỗi tệp CSV dựa trên tên tệp
#         file_key = f"csv_{csv_file.name}"
#         st.write("Đang tải lên tệp...")

#         # Gửi file CSV tới backend
#         response = requests.post(
#             "http://localhost:8000/api/csv_powerbi",
#             files={"file": (csv_file.name, csv_file, "multipart/form-data")},
#         )

#         if response.status_code == 200:
#             # Nhận thông tin từ backend
#             response_data = response.json()
#             dataset_id = response_data.get("dataset_id")
            
#             if dataset_id:
#                 # Lấy danh sách các bảng từ dataset
#                 group_id = "ee1a45b8-f73e-41e2-b8b7-905ac52d4117"
#                 api_url = f"https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/tables"
#                 access_token = response_data.get("access_token")
                
#                 headers = {
#                     "Authorization": f"Bearer {access_token}",
#                     "Content-Type": "application/json",
#                 }
                
#                 tables_response = requests.get(api_url, headers=headers)

#                 if tables_response.status_code == 200:
#                     tables_info = tables_response.json()
#                     if tables_info:
#                         st.subheader("Danh sách các bảng:")
#                         for table in tables_info.get("value", []):
#                             st.write(f"Table Name: {table.get('name')}")
#                             st.json(table)
#                             st.write(f"{tables_info}")
#                     else:
#                         st.warning("Không có bảng nào trong dataset.")
#                 else:
#                     st.error(f"Không thể lấy thông tin bảng từ Power BI API: {tables_response.text}")
#             else:
#                 st.error("Không nhận được `dataset_id` từ backend.")
#         else:
#             st.error(f"Đã xảy ra lỗi trong quá trình xử lý: {response.text}")

# # Gọi hàm để hiển thị giao diện Streamlit
# show_powerbi()

def show_powerbi():
    st.title("Tải CSV lên Power BI")

#     # Upload CSV
    csv_file = st.file_uploader("Tải lên tệp CSV", type="csv")
    st.title("Nhúng báo cáo Power BI")

    # Hiển thị iframe trong Streamlit
    st.markdown(
        """
        <iframe 
            title="TeamsAttendanceReport" 
            width="600" 
            height="373.5" 
            src="https://app.powerbi.com/view?r=eyJrIjoiMGVjMmMxZGUtOTIzNC00ZWFkLWE3ZjItN2I5OTY2NmFlNTcwIiwidCI6IjVlMTU4ZTJhLTA1OTYtNGE2Yy04ODAxLTM1MDJhZWY0NTYzZiIsImMiOjEwfQ%3D%3D" 
            frameborder="0" 
            allowFullScreen="true">
        </iframe>
        """,
        unsafe_allow_html=True
    )
show_powerbi()
