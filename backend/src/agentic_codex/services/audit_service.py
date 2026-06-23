from sqlalchemy.ext.asyncio import AsyncSession
from agentic_codex.db.models import AuditLog


class AuditService:

    async def log(
        self,
        db: AsyncSession,
        user_id: int,
        action: str,
        resource_type: str,
        resource_id: int,
        metadata: dict,
        ip: str
    ):
        log = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            metadata=str(metadata),
            ip_address=ip
        )

        db.add(log)
        await db.commit()