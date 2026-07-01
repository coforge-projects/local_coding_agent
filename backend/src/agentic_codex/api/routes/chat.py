from fastapi import APIRouter, Depends
from agentic_codex.api.schemas.chat import ChatRequest, ChatResponse, ChatMessage
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

# ✅ DB
from agentic_codex.db.database import get_db
from agentic_codex.db.repos.message_repo import MessageRepo
from agentic_codex.db.repos.conversation_repo import ConversationRepo
from agentic_codex.db.repos.project_repo import ProjectRepo

# ✅ Supervisor
from agentic_codex.agents.supervisor import Supervisor

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest, db: AsyncSession = Depends(get_db)):
    project_id = payload.project_id
    conversation_id = payload.conversation_id
    message = payload.message

    message_repo = MessageRepo(db)
    conversation_repo = ConversationRepo(db)
    project_repo = ProjectRepo(db)

    # ✅ PROJECT HANDLING
    project = None

    try:
        project_uuid = str(uuid.UUID(str(project_id)))
        project = await project_repo.get_by_id(project_uuid)
    except Exception:
        project = None

    # ✅ create project if invalid or not found
    if not project:
        project_uuid = str(uuid.uuid4())

        project = await project_repo.create({
            "id": project_uuid,
            "name": f"Project-{project_id}",
            "desc": "Auto-created project",
            "owner_id": None,
            "language": "python"
        })

    project_id = str(project.id)

    # ✅ CONVERSATION
    if not conversation_id:
        convo = await conversation_repo.create({
            "id": str(uuid.uuid4()),
            "project_id": project_id,
            "user_id": None,
            "title": "New Conversation"
        })

        conversation_id = str(convo.id)

    else:
        convo = await conversation_repo.get_by_id(conversation_id)

        if not convo:
            return {"detail": "Conversation not found"}

    # ✅ SAVE USER MESSAGE
    await message_repo.create({
        "id": str(uuid.uuid4()),
        "conversation_id": str(conversation_id),
        "role": "user",
        "content": message,
        "tokens_used": 0
    })

    # ✅ FETCH HISTORY
    history = await message_repo.list_last_n(
        conversation_id,
        n=10
    )

    messages = [
        {
            "role": msg.role,
            "content": msg.content
        }
        for msg in reversed(history)
    ]

    # ✅ SUPERVISOR (LANGGRAPH FLOW)
    supervisor = Supervisor(project_id=project_id)

    response_text = await supervisor.run(messages)

    # ✅ SAVE RESPONSE
    await message_repo.create({
        "id": str(uuid.uuid4()),
        "conversation_id": str(conversation_id),
        "role": "assistant",
        "content": response_text,
        "tokens_used": 0
    })

    return ChatResponse(
        conversation_id=str(conversation_id),
        message=ChatMessage(
            id=str(uuid.uuid4()),
            role="assistant",
            content=response_text,
            tokens_used=10
        )
    )