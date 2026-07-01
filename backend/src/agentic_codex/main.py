from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from agentic_codex.db.database import create_tables

# from agentic_codex.auth.auth_dependencies import require_role    #for temporarily disableing the msa login

from agentic_codex.api.routes.chat import router as chat_router

from agentic_codex.api import projects, users , conversations, audit  # importing api's

from fastapi import HTTPException
from sqlalchemy import text
from agentic_codex.db.database import engine


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
                SELECT email, password
                FROM users
                WHERE email = :email
            """)
            
            result = await conn.execute(query, {"email": email})
            user = result.fetchone()

            if not user:
                raise HTTPException(status_code=401, detail="Invalid credentials")

            user_password = user[1]

            if user_password != password:
                raise HTTPException(status_code=401, detail="Invalid credentials")

            return {"message": "Login successful"}

    except Exception as e:
        print("Login error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")


#-----------------------------



# ✅ Allow frontend (Angular) to connect
origins = [
    "http://localhost:5173",  # ✅ React local dev
    "https://ashy-forest-033f46e0f.7.azurestaticapps.net"  # ✅ your deployed frontend
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
# def health_check(user=Depends(require_role("viewer"))):
def health_check():
    return {
        "status": "ok",
        # "user": user
    }


# from database side api
app.include_router(projects.router)
app.include_router(users.router)
app.include_router(conversations.router)
app.include_router(audit.router)
