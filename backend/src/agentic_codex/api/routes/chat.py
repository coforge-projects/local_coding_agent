from fastapi import APIRouter
from agentic_codex.api.schemas.chat import ChatRequest, ChatResponse, ChatMessage
import uuid
from datetime import datetime

router = APIRouter()

# ✅ Store data: project → conversations → messages
projects = {}


@router.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest):
    project_id = payload.project_id
    conversation_id = payload.conversation_id
    message = payload.message

    # ✅ Ensure project exists
    if project_id not in projects:
        projects[project_id] = {}

    project_conversations = projects[project_id]

    # ✅ Create new conversation if needed
    if not conversation_id:
        conversation_id = str(uuid.uuid4())
        project_conversations[conversation_id] = []

    # ✅ Ensure conversation exists
    if conversation_id not in project_conversations:
        project_conversations[conversation_id] = []

    # ✅ Store user message
    project_conversations[conversation_id].append({
        "id": str(uuid.uuid4()),
        "role": "user",
        "content": message,
        "timestamp": datetime.utcnow().isoformat()
    })

    response_text = f"Echo: {message}"

    # ✅ Store assistant message
    project_conversations[conversation_id].append({
        "id": str(uuid.uuid4()),
        "role": "assistant",
        "content": response_text,
        "timestamp": datetime.utcnow().isoformat()
    })

    return ChatResponse(
        conversation_id=conversation_id,
        message=ChatMessage(
            id=str(uuid.uuid4()),
            role="assistant",
            content=response_text,
            tokens_used=10
        )
    )


@router.get("/projects/{project_id}/conversations/{conversation_id}")
async def get_conversation(project_id: str, conversation_id: str):
    if project_id not in projects:
        return {"detail": "Project not found"}

    if conversation_id not in projects[project_id]:
        return {"detail": "Conversation not found"}

    return {
        "conversation_id": conversation_id,
        "messages": projects[project_id][conversation_id]
    }


@router.get("/projects/{project_id}/conversations")
async def list_conversations(project_id: str):
    if project_id not in projects:
        return {"detail": "Project not found"}

    return {
        "project_id": project_id,
        "conversation_ids": list(projects[project_id].keys())
    }

@router.post("/projects")
async def create_project(name: str):
    if name in projects:
        return {"detail": "Project already exists"}

    projects[name] = {}
    return {"project_id": name}

@router.get("/projects")
async def list_projects():
    return {
        "projects": list(projects.keys())
    }