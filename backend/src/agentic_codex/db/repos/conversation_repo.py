from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from agentic_codex.db.models import Conversation

class ConversationRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict):
        convo = Conversation(**data)
        self.db.add(convo)
        await self.db.commit()
        return convo

    async def list_by_project(self, project_id: int):
        result = await self.db.execute(
            select(Conversation).where(
                Conversation.project_id == project_id
            )
        )
        return result.scalars().all()