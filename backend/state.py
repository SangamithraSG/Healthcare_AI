from typing import TypedDict, Annotated, List, Optional
from langchain_core.messages import AnyMessage
import operator

class AgentState(TypedDict):
    messages: Annotated[List[AnyMessage], operator.add]
    current_intent: Optional[str]
    risk_score: float
    session_id: str
    patient_id: str
    is_safe: bool
    escalation_reason: Optional[str]
