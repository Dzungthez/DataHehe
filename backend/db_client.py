import os
from dotenv import load_dotenv
from langchain_astradb import AstraDBVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

# Load environment variables từ .env file
load_dotenv()

def get_vector_store() -> AstraDBVectorStore:
    """
    Khởi tạo AstraDB Vector Store với OpenAI Embeddings.
    """
    ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
    ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")

    if not ASTRA_DB_API_ENDPOINT or not ASTRA_DB_APPLICATION_TOKEN:
        raise RuntimeError(
            "ASTRA_DB_API_ENDPOINT và ASTRA_DB_APPLICATION_TOKEN phải được định nghĩa trong .env."
        )

    return AstraDBVectorStore(
        collection_name="astra_vector_langchain",
        embedding=OpenAIEmbeddings(),
        api_endpoint=ASTRA_DB_API_ENDPOINT,
        token=ASTRA_DB_APPLICATION_TOKEN,
    )

def process_pdf_to_documents(pdf_path: str, chunk_size: int = 500, chunk_overlap: int = 50) -> list[Document]:
    """
    Đọc file PDF, chia nhỏ nội dung, và chuyển thành danh sách Document.
    """
    loader = PyPDFLoader(pdf_path)
    raw_documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    documents = text_splitter.split_documents(raw_documents)

    return documents

def add_documents_to_vector_store(vector_store: AstraDBVectorStore, documents: list[Document]) -> None:
    """
    Thêm danh sách Document vào Vector Store.
    """
    ids = [str(i) for i in range(len(documents))]
    vector_store.add_documents(documents=documents, ids=ids)
    print(f"Đã thêm {len(documents)} tài liệu vào Vector Store.")

def search_documents(vector_store: AstraDBVectorStore, query: str, k: int = 1) -> list[str]:
    """
    Tìm kiếm các tài liệu tương tự trong Vector Store.
    """
    results = vector_store.similarity_search(query=query, k=k)
    return [doc.page_content for doc in results]

def delete_document_from_vector_store(vector_store: AstraDBVectorStore, document_id: str) -> None:
    """
    Xóa tài liệu khỏi Vector Store theo ID.
    """
    vector_store.delete(ids=[document_id])
    print(f"Đã xóa tài liệu với ID: {document_id}")
