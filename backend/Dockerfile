# ---------- Base Image ----------
FROM python:3.12-slim

# ---------- Environment ----------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---------- Working Directory ----------
WORKDIR /app

# ---------- System Dependencies ----------
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# ---------- Install Python Dependencies ----------
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# ---------- Copy Project ----------
COPY . .

# ---------- Create Persistent Vector DB Directory ----------
RUN mkdir -p /app/data/vectordb

# ---------- Expose Port ----------
EXPOSE 8000

# ---------- Start FastAPI ----------
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]