from fastapi import FastAPI
from pydantic import BaseModel
from backend.graph import app_graph
from backend.database import ESCALATION_QUEUE
from langchain_core.messages import HumanMessage
import os
from dotenv import load_dotenv

# Load keys safely
load_dotenv()

# ==========================================
# HOUR 1: LANGSMITH CONNECTION
# ==========================================
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Healthcare-Agentic-AI"
# Ensure GROQ_API_KEY and LANGCHAIN_API_KEY are exported in the shell

app = FastAPI(title="Healthcare Agentic AI System")

class ChatRequest(BaseModel):
    session_id: str
    patient_id: str
    message: str

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    initial_state = {
        "messages": [HumanMessage(content=req.message)],
        "session_id": req.session_id,
        "patient_id": req.patient_id,
        "current_intent": None,
        "risk_score": 0.0,
        "is_safe": True,
        "escalation_reason": None
    }
    
    # LangGraph Execution
    final_state = app_graph.invoke(initial_state)
    
    return {
        "response": final_state["messages"][-1].content,
        "is_safe": final_state.get("is_safe"),
        "risk_score": final_state.get("risk_score"),
        "escalation_reason": final_state.get("escalation_reason")
    }

@app.get("/escalations")
async def get_escalations():
    return {"escalations": ESCALATION_QUEUE}

if __name__ == "__main__":
    import uvicorn
    print("Starting FastAPI app...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
