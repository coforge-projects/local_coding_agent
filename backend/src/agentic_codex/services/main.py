from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from agentic_codex.db.database import create_tables
from agentic_codex.auth.auth_dependencies import require_role
from agentic_codex.api.routes.chat import router as chat_router

from agentic_codex.api import projects, users , conversations, audit  # importing api's



app = FastAPI()

# ✅ Allow frontend (Angular) to connect
origins = [
    "http://localhost:4200",
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
