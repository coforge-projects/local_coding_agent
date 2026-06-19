from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from agentic_codex.db.models import Message

class MessageRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict):
        msg = Message(**data)
        self.db.add(msg)
        await self.db.commit()
        return msg

    async def list_last_n(self, conversation_id: int, n: int = 10):
        result = await self.db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.id.desc())
            .limit(n)
        )
        return result.scalars().all()