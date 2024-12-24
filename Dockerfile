FROM python:3.10.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000 8501

# Lệnh CMD để chạy backend và frontend cùng lúc
CMD ["sh", "-c", "python backend/main.py & streamlit run frontend/app.py --server.port 8501 --server.enableCORS false --server.headless true"]
