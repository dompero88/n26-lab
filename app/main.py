from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
import re

app = FastAPI()

# Configuration: Ollama IP from environment variables
OLLAMA_HOST = os.getenv("OLLAMA_ENDPOINT", "http://172.31.23.1:11434")

class PromptRequest(BaseModel):
    user_input: str

def sanitize_pii(text: str) -> str:
    """
    Sanitizes sensitive information (PII) from the text.
    Currently masks IBANs using a standard pattern.
    """
    if not text:
        return ""
    # Simplified IBAN masking regex
    return re.sub(r'[A-Z]{2}\d{2}[A-Z0-9]{12,}', '[REDACTED_IBAN]', text)

@app.get("/")
def home():
    return {"status": "ok", "service": "AI-Security-Guardrail"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/analyze")
def analyze(request: PromptRequest):
    # 1. INGRESS SECURITY: Prompt Injection Detection
    # Basic check for common injection patterns
    forbidden_phrases = ["ignore previous instructions", "system override", "disregard all rules"]
    user_input_lower = request.user_input.lower()
    
    if any(phrase in user_input_lower for phrase in forbidden_phrases):
        raise HTTPException(status_code=403, detail="Security Violation: Potential Injection Detected")

    # 2. INGRESS DATA GOVERNANCE: PII Masking on input
    safe_prompt = sanitize_pii(request.user_input)

    # 3. AI INFERENCE (Call to EC2 Inference Layer)
    try:
        payload = {
            "model": "tinyllama",
            "prompt": f"Analyze this transaction risk: {safe_prompt}",
            "stream": False
        }
        
        # Timeout set to 60s to account for model loading/latency
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate", 
            json=payload, 
            timeout=60 
        )
        
        response.raise_for_status()
        
        # Extract raw response
        raw_ai_response = response.json().get("response", "")

        # 4. EGRESS SECURITY: PII Masking on output (The "Final Shield")
        # We sanitize the AI output to prevent accidental data leakage
        sanitized_ai_response = sanitize_pii(raw_ai_response)
        
        return {"ai_response": sanitized_ai_response}
        
    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=504, 
            detail="AI Service Timeout: The model is taking too long to respond."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"AI Service Unreachable: {str(e)}"
        )