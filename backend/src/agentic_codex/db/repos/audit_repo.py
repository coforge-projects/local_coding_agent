from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from agentic_codex.db.models import AuditLog

class AuditRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def insert(self, data: dict):
        log = AuditLog(**data)
        self.db.add(log)
        await self.db.commit()
        return log

    async def list_by_project(self, project_id: int):
        result = await self.db.execute(
            select(AuditLog).where(
                AuditLog.resource_id == project_id
            )
        )
        return result.scalars().all()
