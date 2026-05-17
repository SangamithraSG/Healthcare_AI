import sys
import uuid
from dotenv import load_dotenv
load_dotenv()
from langchain_core.messages import HumanMessage
from backend.graph import app_graph
from backend.state import AgentState

def test_system(message, patient_id="test_pat_1"):
    state = {
        "patient_id": patient_id,
        "session_id": str(uuid.uuid4()),
        "messages": [HumanMessage(content=message)],
        "current_intent": "",
        "is_safe": True,
        "escalation_reason": "",
        "risk_score": 0.0
    }
    
    print(f"\n--- Testing Message: '{message}' ---")
    try:
        final_state = app_graph.invoke(state)
        print(f"Intent: {final_state.get('current_intent')}")
        print(f"Risk Score: {final_state.get('risk_score')}")
        if final_state.get('messages'):
            print(f"Final AI Message: {final_state['messages'][-1].content}")
        else:
            print("No messages in final state.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_system("I need a refill on my lisinopril.")
    test_system("Does my BlueCross policy cover blood tests?")
    test_system("My SSN is 123-45-6789 and I want to book an appointment.")
