from fastapi import FastAPI
from api.pdf_chat import router as pdf_chat_router


app = FastAPI()

# Đăng ký các router
app.include_router(pdf_chat_router, prefix="/api", tags=["PDF Chat"])

# Chạy ứng dụng (nếu chạy trực tiếp từ file này)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)