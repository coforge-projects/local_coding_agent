from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from agentic_codex.db.database import create_tables

from agentic_codex.auth.auth_dependencies import get_current_user, require_role
from agentic_codex.auth.jwt import create_access_token

from agentic_codex.api.routes.chat import router as chat_router

from agentic_codex.api import projects, users , conversations, audit  # importing api's

from fastapi import HTTPException
from sqlalchemy import text
from agentic_codex.db.database import engine
import uuid


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Backend is running ✅"}


#-----------------------------

@app.post("/login")
async def login(email: str, password: str):
    try:
        async with engine.begin() as conn:
            query = text("""
                SELECT id, email, password, role, token_version
                FROM users
                WHERE email = :email
            """)
            
            result = await conn.execute(query, {"email": email})
            user = result.fetchone()

            if not user:
                raise HTTPException(status_code=401, detail="Invalid credentials")

            user_password = user[2]

            if user_password != password:
                raise HTTPException(status_code=401, detail="Invalid credentials")

           
            token = create_access_token({
            "user_id": user[0],
            "email": user[1],
            "role": user[3],
            "token_version": user[4]
              })


            return {
                "access_token": token,
                "token_type": "bearer"
            }
    except Exception as e:
        print("Login error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")
    

 

@app.post("/signup")
async def signup(email: str, name: str, password: str):
    try:
        async with engine.begin() as conn:
            # check existing user
            query = text("""
                SELECT email FROM users WHERE email = :email
            """)
            result = await conn.execute(query, {"email": email})
            existing_user = result.fetchone()

            if existing_user:
                raise HTTPException(status_code=400, detail="User already exists")

            user_id = str(uuid.uuid4())
            azure_oid = str(uuid.uuid4())  

            insert_query = text("""
                INSERT INTO users (id, email, name, role, password, azure_oid)
                VALUES (:id, :email, :name, 'user', :password, :azure_oid)
            """)

            await conn.execute(insert_query, {
                "id": user_id,
                "email": email,
                "name": name,
                "password": password,
                "azure_oid": azure_oid
            })

            return {"message": "User created successfully"}

    except Exception as e:
        print("Signup error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")




@app.post("/logout")
async def logout(user=Depends(get_current_user)):
    user_id = user.get("user_id")

    async with engine.begin() as conn:
        await conn.execute(
            text("""
                UPDATE users
                SET token_version = token_version + 1
                WHERE id = :user_id
            """),
            {"user_id": user_id}
        )

    return {"message": "Logged out successfully"}

#-----------------------------



# ✅ Allow frontend (Angular) to connect
origins = [
    "http://localhost:5173",
    "https://ashy-forest-033f46e0f.7.azurestaticapps.net"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Register routes
app.include_router(chat_router)

# ✅ Startup event (DB optional)
@app.on_event("startup")
async def startup():
    try:
        print("Attempting to create tables...")
        await create_tables()
    except Exception as e:
        print("⚠️ DB not ready yet — continuing without DB")
        print(e)


# ✅ Health check with RBAC
@app.get("/health")
def health_check(user=Depends(require_role("viewer"))):
    return {
        "status": "ok",
        "user": user
    }


# from database side api
app.include_router(projects.router)
app.include_router(users.router)
app.include_router(conversations.router)
app.include_router(audit.router)
