import os
import asyncio
from dotenv import load_dotenv
import aioodbc

from mcp.server.fastmcp import FastMCP

#  Load env
load_dotenv()

#  ODBC connection string
CONN_STR = os.getenv("SERVER_CONNECTION_STRING")

mcp = FastMCP("azure-sql-mcp")


#  SELECT queries (used for fetching data from database)
@mcp.tool()
async def sql__query(sql: str):
    try:
        async with aioodbc.create_pool(dsn=CONN_STR) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(sql)
                    columns = [column[0] for column in cur.description]
                    rows = await cur.fetchall()

                    result = [
                        dict(zip(columns, row))
                        for row in rows
                    ]

                    return {"result": result}

    except Exception as e:
        return {"error": str(e)}


#  INSERT / UPDATE / DELETE (used for modifying data with parameters)
@mcp.tool()
async def sql__execute(sql: str, params: list = None):
    try:
        async with aioodbc.create_pool(dsn=CONN_STR) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(sql, params or [])
                    await conn.commit()

        return {"status": "success"}

    except Exception as e:
        return {"error": str(e)}


#  Start server
if __name__ == "__main__":
    mcp.run()