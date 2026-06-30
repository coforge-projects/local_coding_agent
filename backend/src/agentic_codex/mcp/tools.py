from pathlib import Path
import aioodbc
import os


def register_tools(mcp, conn_str):

    @mcp.tool()
    def ping():
        return "MCP server is running"

    @mcp.tool()
    def create_file(project_id: str, filename: str):
        file_path = Path(f"./projects/{project_id}/{filename}")
        file_path.parent.mkdir(parents=True, exist_ok=True)

        if not file_path.exists():
            file_path.write_text("")

        return f"File {filename} created"

    @mcp.tool()
    async def sql__query(sql: str):
        try:
            async with aioodbc.create_pool(dsn=conn_str) as pool:
                async with pool.acquire() as conn:
                    async with conn.cursor() as cur:
                        await cur.execute(sql)

                        columns = [column[0] for column in cur.description]
                        rows = await cur.fetchall()

                        return {
                            "result": [
                                dict(zip(columns, row))
                                for row in rows
                            ]
                        }

        except Exception as e:
            return {"error": str(e)}

    @mcp.tool()
    async def sql__execute(sql: str, params: list = None):
        try:
            async with aioodbc.create_pool(dsn=conn_str) as pool:
                async with pool.acquire() as conn:
                    async with conn.cursor() as cur:
                        await cur.execute(sql, params or [])
                        await conn.commit()

            return {"status": "success"}

        except Exception as e:
            return {"error": str(e)}