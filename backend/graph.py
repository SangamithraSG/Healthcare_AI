from langgraph.graph import StateGraph, END
from backend.state import AgentState
from backend.agents import (
    orchestrator_node, appointment_node, lab_report_node, 
    safety_node, escalate_node, prescription_node, insurance_node
)

def route_intent(state: AgentState):
    if state.get("risk_score", 0.0) > 0.7:
        return "escalate"
        
    if state.get("current_intent") == "emergency":
        return "escalate"
    intent = state.get("current_intent")
    if intent == "appointment":
        return "appointment_agent"
    elif intent == "lab_report":
        return "lab_agent"
    elif intent == "prescription":
        return "prescription_agent"
    elif intent == "insurance":
        return "insurance_agent"
    return "escalate"  # Default fallback for unhandled domains

def route_safety(state: AgentState):
    if state.get("is_safe") is False:
        return "escalate"
    return END

workflow = StateGraph(AgentState)

workflow.add_node("orchestrator", orchestrator_node)
workflow.add_node("appointment_agent", appointment_node)
workflow.add_node("lab_agent", lab_report_node)
workflow.add_node("prescription_agent", prescription_node)
workflow.add_node("insurance_agent", insurance_node)
workflow.add_node("safety_agent", safety_node)
workflow.add_node("escalate", escalate_node)

workflow.set_entry_point("orchestrator")

workflow.add_conditional_edges("orchestrator", route_intent, {
    "appointment_agent": "appointment_agent",
    "lab_agent": "lab_agent",
    "prescription_agent": "prescription_agent",
    "insurance_agent": "insurance_agent",
    "escalate": "escalate"
})

workflow.add_edge("appointment_agent", "safety_agent")
workflow.add_edge("lab_agent", "safety_agent")
workflow.add_edge("prescription_agent", "safety_agent")
workflow.add_edge("insurance_agent", "safety_agent")

workflow.add_conditional_edges("safety_agent", route_safety, {
    "escalate": "escalate",
    END: END
})

workflow.add_edge("escalate", END)

app_graph = workflow.compile()
