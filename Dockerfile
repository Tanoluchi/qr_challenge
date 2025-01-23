FROM python:3.10-slim

WORKDIR /code

COPY . /code

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.src.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8084"]