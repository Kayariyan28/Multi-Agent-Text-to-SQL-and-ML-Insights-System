FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY main.py .

ENV PYTHONUNBUFFERED=1
ENV LANGCHAIN_TRACING_V2=true  # For LangSmith

CMD ["python", "main.py"]
