import re

# ==========================================
# HOUR 5: EMERGENCY DETECTION REGEX
# ==========================================
EMERGENCY_REGEX = re.compile(r"\b(suicide|chest pain|heart attack|can't breathe|stroke|overdose|emergency)\b", re.IGNORECASE)

def calculate_risk(intent: str, message: str) -> float:
    risk = 0.0
    if intent == "lab_report":
        risk += 0.8
    elif intent == "prescription":
        risk += 0.9
    elif intent == "appointment":
        risk += 0.2
    elif intent == "general":
        risk += 0.5
    
    # Emergency check overrides
    if EMERGENCY_REGEX.search(message):
        risk = 1.0
        
    return min(risk, 1.0)
