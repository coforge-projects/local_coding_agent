from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from agentic_codex.db.models import Project


class ProjectRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ✅ Create new project
    async def create(self, data: dict):
        project = Project(**data)
        self.db.add(project)
        await self.db.commit()
        await self.db.refresh(project)
        return project

    # ✅ Get project by ID (fixed)
    async def get_by_id(self, project_id):
        result = await self.db.execute(
            select(Project).where(Project.id == project_id)
        )
        return result.scalars().first()

    # ✅ List all projects
    async def list_all(self):
        result = await self.db.execute(select(Project))
        return result.scalars().all()
