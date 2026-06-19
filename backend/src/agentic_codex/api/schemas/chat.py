from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    project_id: str
    conversation_id: Optional[str] = None
    message: str


class ChatMessage(BaseModel):
    id: str
    role: str
    content: str
    tokens_used: int


class ChatResponse(BaseModel):
    conversation_id: str
    message: ChatMessage