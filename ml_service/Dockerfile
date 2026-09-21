FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ml_service/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ml_service/main.py .
COPY ml_service/models ./models

EXPOSE 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]