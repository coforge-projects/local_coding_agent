from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from agentic_codex.db.models import Conversation


class ConversationRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ✅ Create new conversation
    async def create(self, data: dict):
        convo = Conversation(**data)
        self.db.add(convo)
        await self.db.commit()
        await self.db.refresh(convo)
        return convo

    # ✅ Get conversation by ID (IMPORTANT for chat flow)
    async def get_by_id(self, conversation_id):
        result = await self.db.execute(
            select(Conversation).where(
                Conversation.id == conversation_id
            )
        )
        return result.scalars().first()

    # ✅ List all conversations for a project
    async def list_by_project(self, project_id):
        result = await self.db.execute(
            select(Conversation).where(
                Conversation.project_id == project_id
            )
        )
        return result.scalars().all()