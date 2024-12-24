import streamlit as st
import requests

def show_powerbi():
    st.title("Tải CSV lên Power BI")

    # Upload CSV
    csv_file = st.file_uploader("Tải lên tệp CSV", type="csv")

    if csv_file:
        # Tạo key động cho mỗi tệp CSV dựa trên tên tệp
        file_key = f"csv_{csv_file.name}"
        st.write("Đang tải lên tệp...")

        # Gửi file CSV tới backend
        response = requests.post(
            "http://localhost:8000/api/csv_powerbi",
            files={"file": (csv_file.name, csv_file, "multipart/form-data")},
        )

        if response.status_code == 200:
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
        else:
            st.error(f"Đã xảy ra lỗi trong quá trình xử lý: {response.text}")

# Gọi hàm để hiển thị giao diện Streamlit
show_powerbi()
