FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Security: Utente non-root
RUN useradd -m appuser
USER appuser

# Espone la porta 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
