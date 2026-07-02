from typing import TypedDict, List, Dict


class AgentState(TypedDict):
    messages: List[Dict[str, str]]
    project_id: str
    plan: str
    response: str
    selected_tool_category: str

    success: bool
    validation_reason: str
    retry_count: int

    reflection: str
    needs_retry: bool