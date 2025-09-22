FROM python:3.11-slim

WORKDIR /app

# 安裝 PostgreSQL 客戶端工具和必要依賴
RUN apt-get update && \
    apt-get install -y postgresql-client && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 確保 start.sh 有執行權限
RUN chmod +x start.sh

CMD ["./start.sh"]
