from fastapi import Depends, HTTPException, status
from fastapi_azure_auth import SingleTenantAzureAuthorizationCodeBearer
import os

from agentic_codex.db.database import get_db
from agentic_codex.services.user_service import get_or_create_user

# ✅ Load env values
AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")
AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")

# ✅ Azure auth scheme (with scope)
azure_scheme = SingleTenantAzureAuthorizationCodeBearer(
    app_client_id=AZURE_CLIENT_ID,
    tenant_id=AZURE_TENANT_ID,
    scopes={
        f"api://{AZURE_CLIENT_ID}/access_as_user": "Access API"
    }
)


# ✅ Get current user (Azure → DB)
async def get_current_user(
    user=Depends(azure_scheme),
    db=Depends(get_db)
):
    azure_user = {
        "user_id": user.oid,
        "email": user.preferred_username,
        "name": user.name,
    }

    print(f"✅ Authenticated user: {azure_user['email']}")

    try:
        db_user = await get_or_create_user(db, azure_user)
        return db_user
    except Exception as e:
        print(f"⚠️ DB error (skipping user creation): {e}")
        return azure_user


# ✅ Role-based access control (REAL version)
def require_role(required_role: str):

    def role_checker(user=Depends(get_current_user)):
        # ✅ Use real role from DB (fallback if missing)
        user_role = getattr(user, "role", "user")

        role_hierarchy = {
            "owner": 3,
            "editor": 2,
            "viewer": 1,
            "user": 1  # default users = viewer level
        }

        if role_hierarchy.get(user_role, 0) < role_hierarchy.get(required_role, 0):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return user

    return role_checker
