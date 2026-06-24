from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from agentic_codex.db.models import Message


class MessageRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ✅ Create new message
    async def create(self, data: dict):
        msg = Message(**data)
        self.db.add(msg)
        await self.db.commit()
        await self.db.refresh(msg)
        return msg

    # ✅ Get last N messages (correct ordering)
    async def list_last_n(self, conversation_id, n: int = 10):
        result = await self.db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.id.desc())   # ✅ works but kept consistent
            .limit(n)
        )
        return result.scalars().all()

    # ✅ Optional: get ALL messages (useful later)
    async def list_all(self, conversation_id):
        result = await self.db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.id.asc())
        )
        return result.scalars().all()
