# chatapp.py
import streamlit as st
import requests
import os
import asyncio
from state import initialize_state

def save_uploaded_file(uploaded_file):
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    file_path = os.path.join(data_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

async def send_question(prompt):
    """
    Async function gửi câu hỏi đến backend API.
    """
    try:
        response = requests.post(
            "http://localhost:8000/api/pdf_chat",
            data={"question": prompt},
        )
        if response.status_code == 200:
            json_response = response.json()
            return json_response.get("answer", "No answer available."), json_response.get("context", "")
        else:
            return f"Error: {response.json().get('detail', 'Unknown error')}", ""
    except Exception as e:
        return f"Error: {str(e)}", ""


def show_pdf_chat():
    initialize_state()

    st.title("Chat with Your PDF")

    # Bố cục giao diện
    spacer_left, chat_col, files_col, spacer_right = st.columns([0.5, 3, 2, 0.5])

    # Khu vực Chat
    with chat_col:
        st.header("Ask AI")

        # Hiển thị container chat
        chat_container = st.empty()
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
                    # Hiển thị context dưới dạng dropdown
                    if "context" in message:
                        with st.expander("Show Context"):
                            st.text(message["context"])

        # Input người dùng
        if "chat_input" not in st.session_state:
            st.session_state["chat_input"] = ""

        chat_input = st.text_input(
            "Type your question here",
            value=st.session_state["chat_input"],
            key="chat_input_key",
            placeholder="Press Enter to send...",
        )

        if st.button("Send", key="send_button"):
            if chat_input:
                # Thêm câu hỏi của người dùng vào session_state
                st.session_state["messages"].append({"role": "user", "content": chat_input})

                # Gửi câu hỏi và hiển thị spinner
                with st.spinner("Waiting for AI response..."):
                    answer, context = asyncio.run(send_question(chat_input))

                # Lưu câu trả lời và context vào session_state
                st.session_state["messages"].append({
                    "role": "assistant",
                    "content": answer,
                    "context": context if context else "No context available"
                })

                # Xóa input sau khi gửi
                st.session_state["chat_input"] = ""

                # Làm mới container chat
                chat_container.empty()
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
                            # Hiển thị context dưới dạng dropdown
                            if "context" in message:
                                with st.expander("Show Context"):
                                    st.text(message["context"])

    # Khu vực tải lên file
    with files_col:
        st.header("Uploaded Files")
        pdf_file = st.file_uploader("Upload PDF", type="pdf")

        if pdf_file and st.button("Create Collection", key="create_collection_button"):
            file_path = save_uploaded_file(pdf_file)
            with open(file_path, "rb") as f:
                response = requests.post(
                    "http://localhost:8000/api/create_collection",
                    files={"file": f},
                )
            if response.status_code == 200:
                st.success("Collection created successfully!")
            else:
                st.error(f"Error: {response.json().get('detail', 'Unknown error')}")

        if st.session_state.get("collection_name"):
            st.write("Current Collection: Default")

