import logging
from db_client import process_pdf_to_documents, add_documents_to_vector_store
from db_client import get_vector_store
from langchain_openai import AzureChatOpenAI
import os
from dotenv import load_dotenv
# from langchain_openai import OpenAI
from openai import OpenAI

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


# Azure OpenAI configuration
os.getenv("AZURE_OPENAI_ENDPOINT")
os.getenv("AZURE_OPENAI_API_KEY")
os.getenv("OPENAI_API_KEY")
# llm = AzureChatOpenAI(
#     azure_deployment="dzung-emb",
#     model="gpt-4o-mini",
#     api_version="2024-10-01",
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
        )
        logger.info("LLM call successful")
        return response
    except Exception as e:
        logger.error(f"Error calling LLM: {e}")
        raise e
    
if __name__ == "__main__":
    prompt = "What is the capital of France?"
    context = "The capital of France is Paris. The city is known for its art, fashion, and culture."
    response = call_llm(prompt, context)
    print(response.choices[0].message.content)