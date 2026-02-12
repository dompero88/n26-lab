from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
import re

app = FastAPI()

# Legge l'IP di Ollama dalle variabili d'ambiente (iniettate da ECS)
OLLAMA_HOST = os.getenv("OLLAMA_ENDPOINT", "http://localhost:11434")

class PromptRequest(BaseModel):
    user_input: str

def sanitize_pii(text: str) -> str:
    # Maschera IBAN (Regex semplificata)
    return re.sub(r'[A-Z]{2}\d{2}[A-Z0-9]{12,}', '[REDACTED_IBAN]', text)

@app.get("/")
def health_check():
    return {"status": "ok", "service": "N26-AI-Guardrail"}

@app.post("/analyze")
def analyze(request: PromptRequest):
    # 1. Security Guardrail: Prompt Injection
    if "ignore previous instructions" in request.user_input.lower():
        raise HTTPException(status_code=403, detail="Security Violation: Injection Detected")

    # 2. Data Governance: PII Masking
    safe_prompt = sanitize_pii(request.user_input)

    # 3. AI Inference (Chiamata a EC2 B)
    try:
        payload = {
            "model": "tinyllama",
            "prompt": f"Analyze this transaction risk: {safe_prompt}",
            "stream": False
        }
        response = requests.post(f"{OLLAMA_HOST}/api/generate", json=payload, timeout=10)
        return {"ai_response": response.json().get("response")}
    except Exception as e:
        return {"error": "AI Service Unreachable", "details": str(e)}
