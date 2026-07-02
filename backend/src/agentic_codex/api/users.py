from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from agentic_codex.db.database import get_db
# from agentic_codex.auth.auth_dependencies import get_current_user
from agentic_codex.db.models import User, ProjectMember


router = APIRouter(
    tags=["Users"],
    # dependencies=[Depends(get_current_user)]
)


#  CURRENT USER
@router.get("/users/me")
# async def get_me(user=Depends(get_current_user)):
#     return user
async def get_me():
    return {
        "message": "MSA login temporarily disabled",
        # "user": user
    }


#  ADD MEMBER
@router.post("/projects/{id}/members")
async def add_member(
    id: str,
    email: str,
    db: AsyncSession = Depends(get_db)
):
    #  Find user by email
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    #  Check if already member
    existing = await db.execute(
        select(ProjectMember).where(
            ProjectMember.project_id == id,
            ProjectMember.user_id == user.id
        )
    )

    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="User already a member")

    #  Add member
    member = ProjectMember(
        project_id=id,
        user_id=user.id,
        role="member"
    )

    db.add(member)
    await db.commit()

    return {"message": "Member added", "user_id": user.id}


#  GET MEMBERS
@router.get("/projects/{id}/members")
async def list_members(
    id: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User)
        .join(ProjectMember, User.id == ProjectMember.user_id)
        .where(ProjectMember.project_id == id)
    )

    members = result.scalars().all()

    return members


#  REMOVE MEMBER
@router.delete("/projects/{id}/members/{uid}")
async def remove_member(
    id: str,   
    uid: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ProjectMember).where(
            ProjectMember.project_id == id,
            ProjectMember.user_id == uid
        )
    )

    member = result.scalar_one_or_none()

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    await db.delete(member)
    await db.commit()

    return {"message": "Member removed"}
