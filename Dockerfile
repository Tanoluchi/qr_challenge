FROM python:3.10-slim

WORKDIR /code

COPY . /code

RUN apt-get update && apt-get install -y \
    python3-dev \
    gcc \
    libpq-dev jq unzip \
    build-essential \
    libffi-dev libc-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]