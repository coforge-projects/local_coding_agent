from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from agentic_codex.db.database import get_db
from agentic_codex.db.models import Conversation, Message
from agentic_codex.auth.auth_dependencies import get_current_user

router = APIRouter(
    tags=["Conversations"],
    dependencies=[Depends(get_current_user)]
)

#  GET conversations by project
@router.get("/projects/{id}/conversations")
async def get_conversations(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Conversation).where(Conversation.project_id == id)
    )
    return result.scalars().all()


#  GET messages by conversation
@router.get("/conversations/{id}/messages")
async def get_messages(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Message).where(Message.conversation_id == id)
    )
    return result.scalars().all()