from dotenv import load_dotenv
import os
from urllib.parse import quote_plus

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from .models import Base

load_dotenv()

SQL_SERVER = os.getenv("SQL_SERVER")
SQL_DATABASE = os.getenv("SQL_DATABASE")
SQL_USERNAME = os.getenv("SQL_USERNAME")
SQL_PASSWORD = quote_plus(os.getenv("SQL_PASSWORD"))

DATABASE_URL = (
    f"mssql+aioodbc://{SQL_USERNAME}:{SQL_PASSWORD}"
    f"@{SQL_SERVER}:1433/{SQL_DATABASE}"
    "?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no"
)

print("✅ FINAL DB URL:", DATABASE_URL)  # DEBUG

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session