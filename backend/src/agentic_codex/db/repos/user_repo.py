from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from agentic_codex.db.models import User

class UserRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def upsert(self, azure_oid: str, email: str, name: str):
        result = await self.db.execute(
            select(User).where(User.azure_oid == azure_oid)
        )
        user = result.scalar_one_or_none()

        if user:
            user.email = email
            user.name = name
        else:
            user = User(
                azure_oid=azure_oid,
                email=email,
                name=name
            )
            self.db.add(user)

        await self.db.commit()
        return user