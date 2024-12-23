from fastapi import APIRouter, UploadFile, Form
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/pdf_chat")
async def pdf_chat(file: UploadFile, question: str = Form(...)):
    """
    API xử lý chat với file PDF.
    Hiện tại trả về mặc định 'hello'.
    """
    # Đọc nội dung file (nếu cần)
    content = await file.read()

    # Trả về phản hồi mặc định
    return JSONResponse(content={"answer": "hello"})
