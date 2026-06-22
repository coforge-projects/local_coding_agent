from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pathlib import Path
import aiofiles

from agentic_codex.db.database import get_db
from agentic_codex.db.repos.project_repo import ProjectRepo
from agentic_codex.auth.auth_dependencies import get_current_user



router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
    dependencies=[Depends(get_current_user)]
)


#  GET ALL PROJECTS
@router.get("/")
async def list_projects(db: AsyncSession = Depends(get_db)):
    repo = ProjectRepo(db)
    return await repo.list_all()


#  CREATE PROJECT
@router.post("/")
async def create_project(data: dict, db: AsyncSession = Depends(get_db)):
    repo = ProjectRepo(db)
    project = await repo.create(data)

    # Create project folder
    project_dir = Path(f"./projects/{project.id}")
    project_dir.mkdir(parents=True, exist_ok=True)

    # Scaffold files
    (project_dir / "README.md").write_text(f"# {project.name}")
    (project_dir / "main.py").write_text("# Entry point")

    return project


#  GET PROJECT BY ID
@router.get("/{id}")
async def get_project(id: int, db: AsyncSession = Depends(get_db)):
    repo = ProjectRepo(db)
    project = await repo.get_by_id(id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project


#  DELETE PROJECT
@router.delete("/{id}")
async def delete_project(id: int, db: AsyncSession = Depends(get_db)):
    repo = ProjectRepo(db)
    project = await repo.get_by_id(id)

    if not project:
        raise HTTPException(status_code=404)

    await db.delete(project)
    await db.commit()

    return {"message": "deleted"}


#  GET FILE TREE
@router.get("/{id}/files")
async def list_files(id: int):
    base = Path(f"./projects/{id}")

    if not base.exists():
        raise HTTPException(status_code=404)

    def build_tree(path):
        return {
            "name": path.name,
            "type": "dir" if path.is_dir() else "file",
            "children": [build_tree(p) for p in path.iterdir()] if path.is_dir() else []
        }

    return build_tree(base)


#  READ FILE
@router.get("/{id}/file")
async def read_file(id: int, path: str):
    file_path = Path(f"./projects/{id}") / path

    if not file_path.exists():
        raise HTTPException(status_code=404)

    async with aiofiles.open(file_path, "r") as f:
        content = await f.read()

    return {"content": content}


#  WRITE FILE
@router.post("/{id}/file")
async def write_file(id: int, path: str, content: str):
    file_path = Path(f"./projects/{id}") / path
    file_path.parent.mkdir(parents=True, exist_ok=True)

    async with aiofiles.open(file_path, "w") as f:
        await f.write(content)

    return {"message": "saved"}