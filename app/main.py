from fastapi import FastAPI, HTTPException 
from pydantic import BaseModel
from app.redactor import redact_pii
from app.ai_client import get_ai_response
from app.database import log_interaction, leak_check 

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    safe_message = redact_pii(request.message)
    ai_answer = get_ai_response(safe_message)
    is_leak, score = leak_check(ai_answer)
    
    if is_leak:
        print(f"leakage! similarity score: {score:.2f}")
        log_interaction(request.message, safe_message, "[BLOCKED: SENSITIVE DATA DETECTED]")
        raise HTTPException(
            status_code=403, 
            detail="Security Policy Violation: The AI response contains unauthorized internal data."
        )
    
    log_interaction(request.message, safe_message, ai_answer)
    
    return {
        "status": "Securely Processed",
        "sent_to_ai": safe_message,
        "ai_response": ai_answer,
        "leakage_score": score 
    }