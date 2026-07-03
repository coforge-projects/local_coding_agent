# ============================================================
# MSA AUTH (COMMENTED TEMPORARILY - KEEP FOR FUTURE REUSE)
# ============================================================

# from fastapi import Depends, HTTPException, status
# from fastapi_azure_auth import SingleTenantAzureAuthorizationCodeBearer
# import os
#
# from agentic_codex.db.database import get_db
# from agentic_codex.services.user_service import get_or_create_user
#
# # ✅ Load env values
# AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")
# AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
#
# # ✅ Azure auth scheme (with scope)
# azure_scheme = SingleTenantAzureAuthorizationCodeBearer(
#     app_client_id=AZURE_CLIENT_ID,
#     tenant_id=AZURE_TENANT_ID,
#     scopes={
#         f"api://{AZURE_CLIENT_ID}/access_as_user": "Access API"
#     }
# )
#
# # ✅ Get current user (Azure → DB)
# async def get_current_user(
#     user=Depends(azure_scheme),
#     db=Depends(get_db)
# ):
#     azure_user = {
#         "user_id": user.oid,
#         "email": user.preferred_username,
#         "name": user.name,
#     }
#
#     print(f"✅ Authenticated user: {azure_user['email']}")
#
#     try:
#         db_user = await get_or_create_user(db, azure_user)
#         return db_user
#     except Exception as e:
#         print(f"⚠️ DB error (skipping user creation): {e}")
#         return azure_user
#
#
# # ✅ Role-based access control (MSA VERSION)
# def require_role(required_role: str):
#
#     def role_checker(user=Depends(get_current_user)):
#
#         user_role = getattr(user, "role", "user")
#
#         role_hierarchy = {
#             "owner": 3,
#             "editor": 2,
#             "viewer": 1,
#             "user": 1
#         }
#
#         if role_hierarchy.get(user_role, 0) < role_hierarchy.get(required_role, 0):
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail="Insufficient permissions",
#             )
#
#         return user
#
#     return role_checker


# ============================================================
# JWT AUTH (CURRENT ACTIVE AUTH)
# ============================================================

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy import text
import os

from agentic_codex.db.database import engine

security = HTTPBearer()

ALGORITHM = "HS256"


def _get_secret_key() -> str:
    secret_key = os.getenv("JWT_SECRET")
    if not secret_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="JWT_SECRET environment variable is not configured"
        )
    return secret_key


async def get_current_user(token: HTTPAuthorizationCredentials = Security(security)):
    try:
        payload = jwt.decode(
            token.credentials,
            _get_secret_key(),
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("user_id")
        token_version = payload.get("token_version")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        async with engine.begin() as conn:

            result = await conn.execute(
                text("""
                    SELECT token_version
                    FROM users
                    WHERE id = :user_id
                """),
                {"user_id": user_id}
            )

            db_user = result.fetchone()

            if not db_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found"
                )

            if db_user[0] != token_version:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has been revoked"
                )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


def require_role(required_role: str):

    def role_checker(user=Depends(get_current_user)):

        user_role = user.get("role", "user")

        role_hierarchy = {
            "owner": 3,
            "editor": 2,
            "viewer": 1,
            "user": 1
        }

        if role_hierarchy.get(user_role, 0) < role_hierarchy.get(required_role, 0):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )

        return user

    return role_checker