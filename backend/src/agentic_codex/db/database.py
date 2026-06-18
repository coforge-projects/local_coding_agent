from dotenv import load_dotenv
import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from .models import Base


load_dotenv()      

# Read env variables
SQL_SERVER = os.getenv("SQL_SERVER")
SQL_DATABASE = os.getenv("SQL_DATABASE")
SQL_USERNAME = os.getenv("SQL_USERNAME")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")



# Azure SQL connection URL
DATABASE_URL = (
    f"mssql+aioodbc://{SQL_USERNAME}:{SQL_PASSWORD}"
    f"@{SQL_SERVER}:1433/{SQL_DATABASE}"
    "?driver=ODBC+Driver+18+for+SQL+Server"
)


#  Async Engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True
)

#  Async Session
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


#  Create tables
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
