# # backend.py (FastAPI server)

# from fastapi import FastAPI, File, UploadFile
# import msal
# import requests
# import csv
# import json
# import os
# from dotenv import load_dotenv
# import logging
# import pandas as pd

# # Cấu hình logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Load environment variables
# load_dotenv()

# # Azure AD configuration
# APP_ID = "c9e7a750-a477-4f65-b4ef-2269c8518df3"
# DIR_ID = "5e158e2a-0596-4a6c-8801-3502aef4563f"
# USERNAME = "22028046@vnu.edu.vn"
# PASSWORD = "Chichich11"
# AUTHORITY_URL = f"https://login.microsoftonline.com/{DIR_ID}"
# SCOPES = ["https://analysis.windows.net/powerbi/api/.default"]

# # Get Access Token from Power BI
# def get_access_token():
#     try:
#         client = msal.PublicClientApplication(APP_ID, authority=AUTHORITY_URL)
#         response = client.acquire_token_by_username_password(
#             username=USERNAME,
#             password=PASSWORD,
#             scopes=SCOPES,
#         )
#         if "access_token" in response:
#             return response["access_token"]
#         else:
#             raise Exception(f"Failed to get access token: {response}")
#     except Exception as e:
#         raise Exception(f"Error while fetching access token: {str(e)}")

# # Convert CSV file to JSON
# def csv_to_json(csv_file_path):
#     try:
#         with open(csv_file_path, mode="r", encoding="utf-8") as file:
#             # Giả sử bạn sử dụng pandas để chuyển đổi CSV thành JSON
#             import pandas as pd
#             df = pd.read_csv(file)
#             print(df.head())
#             json_data = df.to_json(orient="records")
#             return json_data
#     except Exception as e:
#         print(f"Lỗi khi chuyển đổi CSV thành JSON: {e}")
#         return None

# app = FastAPI()

# @app.post("/api/csv_powerbi")
# async def upload_csv_to_powerbi(file: UploadFile = File(...)):
#     try:
#         # Lưu tệp CSV tạm thời
#         temp_file_path = f"temp_{file.filename}"
#         logger.info(f"Đang lưu tệp CSV tạm thời tại {temp_file_path}")
#         with open(temp_file_path, "wb") as temp_file:
#             temp_file.write(await file.read())
#         logger.info(f"Tệp {file.filename} đã được lưu tạm thời.")

#         # Lấy access token từ Power BI
#         logger.info("Đang lấy access token từ Power BI.")
#         access_token = get_access_token()
#         if not access_token:
#             logger.error("Không thể lấy access token.")
#             return {"error": "Không thể lấy access token"}

#         # Tham số Power BI
#         group_id = "ee1a45b8-f73e-41e2-b8b7-905ac52d4117"  # Group ID
#         dataset_id = "fdb2cdeb-cb3c-4076-aaf7-50af17a3a0a5"  # Dataset ID
#         table_name = "date"  # Tên bảng
#         report_id = "9a895cc8-466c-490a-a441-014a2d2b29b3"
#         dataset_endpoint = f"https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/tables/{table_name}/rows"

#         headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

#         # Chuyển đổi CSV thành JSON
#         logger.info("Đang chuyển đổi tệp CSV thành JSON.")
#         json_data = csv_to_json(temp_file_path)
#         print("Converted JSON data:", json_data)
        
#         if not json_data:
#             logger.error("Dữ liệu CSV không thể chuyển thành JSON.")
#             return {"error": "Dữ liệu CSV không thể chuyển thành JSON"}

#         # Tải lên Power BI
#         logger.info("Đang tải dữ liệu lên Power BI.")
#         response = requests.post(dataset_endpoint, headers=headers, data=json_data)
#         print("Response status code:", response.status_code)
#         print("Response content:", response.text)
        
#         # Kiểm tra kết quả từ Power BI
#         if response.status_code == 200:
#             logger.info("Dữ liệu đã được tải lên Power BI thành công.")
#             # Trả về URL báo cáo Power BI
#             report_url = f"https://app.powerbi.com/groups/{group_id}/reports/{report_id}/ReportSection"
#             return {"powerbi_url": report_url}
#         else:
#             error_message = response.json().get('error', 'Unknown error')
#             logger.error(f"Lỗi khi tải lên Power BI: {error_message}")
#             return {"error": f"Lỗi khi tải lên Power BI: {error_message}"}
#     except Exception as e:
#         logger.error(f"Đã xảy ra lỗi: {str(e)}")
#         return {"error": f"Đã xảy ra lỗi: {str(e)}"}
#     finally:
#         # Dọn dẹp tệp tạm thời
#         if os.path.exists(temp_file_path):
#             os.remove(temp_file_path)
#             logger.info(f"Tệp tạm thời {temp_file_path} đã được xóa.")

# @app.get("/api/csv_powerbi")
# async def get_csv_powerbi():
#     return {"message": "This endpoint only accepts POST requests for CSV uploads."}