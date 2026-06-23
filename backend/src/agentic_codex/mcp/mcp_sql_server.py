import os
from dotenv import load_dotenv
from mcp.server import Server

#  Load environment variables
load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")


#  Try importing SQLAlchemy
try:
    import sqlalchemy as sa
    from sqlalchemy.ext.asyncio import create_async_engine
    DB_AVAILABLE = True
except:
    DB_AVAILABLE = False


server = Server("azure-sql-mcp")


#  QUERY TOOL (READ)
@server.tool()
async def sql__query(query: str):
    if not DATABASE_URL:
        return {"error": "DATABASE_URL not set"}

    if not DB_AVAILABLE:
        return {"error": "DB not available in this environment"}

    try:
        engine = create_async_engine(DATABASE_URL)

        async with engine.connect() as conn:
            result = await conn.execute(sa.text(query))
            rows = result.fetchall()

        return {"result": [dict(row._mapping) for row in rows]}

    except Exception as e:
        return {"error": str(e)}


#  EXECUTE TOOL (WRITE)
@server.tool()
async def sql__execute(query: str):
    if not DATABASE_URL:
        return {"error": "DATABASE_URL not set"}

    if not DB_AVAILABLE:
        return {"error": "DB not available in this environment"}

    try:
        engine = create_async_engine(DATABASE_URL)

        async with engine.begin() as conn:
            await conn.execute(sa.text(query))

        return {"status": "success"}

    except Exception as e:
        return {"error": str(e)}


#  Start MCP server
if __name__ == "__main__":
    server.run()