# chatapp.py
import streamlit as st
import requests
import os
from state import initialize_state

def save_uploaded_file(uploaded_file):
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    file_path = os.path.join(data_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def show_pdf_chat():
    initialize_state()

    st.title("Chat with Your PDF")

    # Tạo layout với 4 phần: khoảng trắng bên trái, chat chính, upload file, khoảng trắng bên phải
    spacer_left, chat_col, files_col, spacer_right = st.columns([0.5, 3, 2, 0.5])

    with chat_col:
        # Chat header
        st.header("Ask AI")

        # Hiển thị lịch sử chat trong container
        chat_container = st.empty()  # Container rỗng để quản lý lịch sử chat
        with chat_container.container():
            for message in st.session_state["messages"]:
                if message["role"] == "user":
                    # Hiển thị tin nhắn của người dùng bên phải
                    st.markdown(
                        f"""
                        <div style="text-align: right; margin-bottom: 10px;">
                            <div style="display: inline-block; background-color: #d9fdd3; padding: 10px; border-radius: 10px;">
                                <strong>You:</strong> {message["content"]}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                elif message["role"] == "assistant":
                    # Hiển thị tin nhắn của hệ thống bên trái
                    st.markdown(
                        f"""
                        <div style="text-align: left; margin-bottom: 10px;">
                            <div style="display: inline-block; background-color: #e6f7ff; padding: 10px; border-radius: 10px;">
                                <strong>AI:</strong> {message["content"]}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        # Thanh nhập liệu (ở cuối giao diện)
        prompt = st.text_input("Type your question here", key="chat_input")
        if st.button("Send", key="send_button"):
            if prompt:
                # Thêm tin nhắn của người dùng vào session_state
                st.session_state["messages"].append({"role": "user", "content": prompt})

                # Trả lời của hệ thống
                if st.session_state["uploaded_files"]:
                    # Gửi yêu cầu đến backend
                    response = requests.post(
                        "http://localhost:8000/api/pdf_chat",
                        files={"file": open(os.path.join("data", st.session_state['uploaded_files'][-1]), "rb")},
                        data={"question": prompt}
                    )
                    if response.status_code == 200:
                        answer = response.json().get("answer", "No answer available.")
                    else:
                        answer = "Error processing the question."
                else:
                    answer = "Please upload a PDF file to ask document-specific questions."

                # Thêm tin nhắn của hệ thống vào session_state
                st.session_state["messages"].append({"role": "assistant", "content": answer})

                # Cập nhật giao diện chat
                chat_container.empty()  # Làm mới container để hiển thị tin nhắn mới
                with chat_container.container():
                    for message in st.session_state["messages"]:
                        if message["role"] == "user":
                            st.markdown(
                                f"""
                                <div style="text-align: right; margin-bottom: 10px;">
                                    <div style="display: inline-block; background-color: #d9fdd3; padding: 10px; border-radius: 10px;">
                                        <strong>You:</strong> {message["content"]}
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                        elif message["role"] == "assistant":
                            st.markdown(
                                f"""
                                <div style="text-align: left; margin-bottom: 10px;">
                                    <div style="display: inline-block; background-color: #e6f7ff; padding: 10px; border-radius: 10px;">
                                        <strong>AI:</strong> {message["content"]}
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

    with files_col:
        # Sidebar upload file
        st.header("Uploaded Files")
        pdf_file = st.file_uploader("Upload PDF", type="pdf")

        if pdf_file and pdf_file.name not in st.session_state["uploaded_files"]:
            file_path = save_uploaded_file(pdf_file)
            st.session_state["uploaded_files"].append(pdf_file.name)
            st.success(f"Uploaded successfully: {pdf_file.name}")

        # Hiển thị danh sách file đã tải lên
        if st.session_state["uploaded_files"]:
            for file_name in st.session_state["uploaded_files"]:
                st.write(f"📄 {file_name}")
        else:
            st.write("No files uploaded yet.")
