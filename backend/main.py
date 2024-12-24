from fastapi import FastAPI, Depends
from api.pdf_chat import router as pdf_chat_router
from db_client import get_vector_store

app = FastAPI()

# Khởi tạo Vector Store một lần
vector_store = get_vector_store()

def get_global_vector_store():
    """
    Dependency để cung cấp vector_store toàn cục cho các route.
    """
    return vector_store

# Đăng ký các router
app.include_router(
    pdf_chat_router, 
    prefix="/api", 
    tags=["PDF Chat"], 
    dependencies=[Depends(get_global_vector_store)]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
