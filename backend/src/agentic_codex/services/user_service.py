from sqlalchemy import select
from agentic_codex.db.database import AsyncSessionLocal
from agentic_codex.db.models import User
from sqlalchemy import select
from agentic_codex.db.models import User


async def get_or_create_user(db, azure_user):
    """
    Upsert user based on Azure OID
    """

    print(f"Checking user in DB: {azure_user['email']}")

    result = await db.execute(
        select(User).where(User.azure_oid == azure_user["user_id"])
    )
    user = result.scalar_one_or_none()

    if not user:
        print("User not found, creating new user...")

        user = User(
            azure_oid=azure_user["user_id"],
            email=azure_user["email"],
            name=azure_user["name"],
            role="user"
        )

        db.add(user)
        await db.commit()
        await db.refresh(user)

        print("User created successfully")

    else:
        print("User already exists")

    return user
