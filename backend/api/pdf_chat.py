import logging
from fastapi import APIRouter, UploadFile, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
from db_client import process_pdf_to_documents, add_documents_to_vector_store
from db_client import get_vector_store
from langchain_openai import AzureChatOpenAI
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Initialize FastAPI Router
router = APIRouter()

# Azure OpenAI configuration
os.getenv("AZURE_OPENAI_ENDPOINT")
os.getenv("AZURE_OPENAI_API_KEY")
os.getenv("OPENAI_API_KEY")

# llm = AzureChatOpenAI(
#     azure_deployment="gpt-4o-mini",
#     api_version="gpt-4o-mini-2024-07-18",
#     temperature=0,
#     max_tokens=None,
#     timeout=None,
#     max_retries=2,
# )
llm = OpenAI()

def call_llm(prompt, context: str) -> str:
    """
    Gọi Azure Chat OpenAI để tạo câu trả lời.
    """
    message = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant. You are given a user question and relevant context. "
                "Provide the answer to the user question based on the context. "
                "If context is irrelevant or missing, answer based on the question only."
            ),
        },
        {"role": "user", "content": f"Question: {prompt}\nContext: {context}"},
    ]
    try:
        response = llm.chat.completions.create(
            model="gpt-4o-mini",
            messages=message,
            temperature=0
        ).choices[0].message.content
        logger.info("LLM call successful")
        return response
    except Exception as e:
        logger.error(f"Error calling LLM: {e}")
        return "Error calling LLM"


@router.post("/create_collection")
async def create_collection(file: UploadFile, vector_store=Depends(get_vector_store)):
    """
    API để thêm tài liệu vào Vector Store. Không cần tham số tên collection.
    """
    if not file.filename.endswith(".pdf"):
        logger.warning(f"Invalid file format: {file.filename}")
        raise HTTPException(status_code=400, detail="Chỉ hỗ trợ file PDF.")

    try:
        # Lưu file PDF tạm thời
        temp_dir = "temp_uploads"
        os.makedirs(temp_dir, exist_ok=True)
        pdf_path = os.path.join(temp_dir, file.filename)
        with open(pdf_path, "wb") as f:
            f.write(await file.read())

        # Xử lý PDF thành các documents
        documents = process_pdf_to_documents(pdf_path)
        logger.info(f"Processed PDF {file.filename} into {len(documents)} documents.")

        # Thêm documents vào Vector Store mặc định
        add_documents_to_vector_store(vector_store, documents)
        logger.info(f"Added {len(documents)} documents to vector store.")

        # Xóa file tạm
        os.remove(pdf_path)
        logger.info(f"Temporary file {pdf_path} removed.")

        return JSONResponse(content={"message": "Collection updated with the uploaded PDF."})

    except Exception as e:
        logger.error(f"Error processing file {file.filename}: {e}")
        raise HTTPException(status_code=500, detail=f"Lỗi khi xử lý file PDF: {str(e)}")


@router.post("/pdf_chat")
async def pdf_chat(question: str = Form(...), vector_store=Depends(get_vector_store)):
    """
    API xử lý tìm kiếm trong VectorDB và trả lời câu hỏi.
    """
    try:
        # Thực hiện tìm kiếm câu trả lời
        results = vector_store.similarity_search(query=question, k=3)
        logger.info(f"Similarity search returned {len(results)} results for query: {question}")

        if results:
            context = "\n".join([f"Context {i}: {doc.page_content}" for i, doc in enumerate(results)])
            response = call_llm(question, context)
        else:
            logger.warning(f"No results found for query: {question}")
            context = ""
            response = call_llm(question, context)

        logger.info(f"Generated response for question: {question}")
        return JSONResponse(content={"answer": response, "context": context})

    except Exception as e:
        logger.error(f"Error processing question '{question}': {e}")
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý: {str(e)}")
