from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from datetime import datetime

from agentic_codex.auth.auth_dependencies import get_current_user
from agentic_codex.db.database import get_db
from agentic_codex.db.models import AuditLog

router = APIRouter(
    tags=["Audit"],
    dependencies=[Depends(get_current_user)]
)

# GET the audits from the project
@router.get("/projects/{id}/audit")
async def get_audit_logs(
    id: str,
    limit: int = 100,
    from_date: datetime | None = None,
    to_date: datetime | None = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(AuditLog).where(AuditLog.resource_id == id)

    if from_date and to_date:
        query = query.where(
            and_(
                AuditLog.created_at >= from_date,
                AuditLog.created_at <= to_date
            )
        )

    query = query.limit(limit)

    result = await db.execute(query)
    return result.scalars().all()