from agentic_codex.tools.file_ops import (
    create_file,
    read_file,
    write_file,
)

from agentic_codex.tools.safe_code_exec import execute_python

from agentic_codex.mcp.tools_metadata import TOOL_METADATA
from agentic_codex.mcp.tools import register_tools

import os
import aioodbc


def get_tool_registry(project_id: str):
    registry = {
        "create_file": lambda filename, content=None: create_file(
            project_id,
            filename
        ),

        "write_file": lambda filename, content=None: write_file(
            project_id,
            filename,
            content
        ),

        "read_file": lambda filename, content=None: read_file(
            project_id,
            filename
        ),

        "execute_python": lambda filename, content=None: execute_python(
            project_id,
            filename
        ),

        "sql__query": lambda sql, content=None: sql_query(sql),

        "sql__execute": lambda sql, params=None: sql_execute(
            sql,
            params
        ),
    }

    return registry


def get_available_tool_names():
    return [
        tool["name"]
        for tool in TOOL_METADATA
    ]

import os
import aioodbc


async def sql_query(sql: str):
    conn_str = os.getenv("SERVER_CONNECTION_STRING")

    try:
        async with aioodbc.create_pool(dsn=conn_str) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(sql)

                    columns = [column[0] for column in cur.description]
                    rows = await cur.fetchall()

                    return [
                        dict(zip(columns, row))
                        for row in rows
                    ]

    except Exception as e:
        return f"SQL Error: {str(e)}"


async def sql_execute(sql: str, params=None):
    conn_str = os.getenv("SERVER_CONNECTION_STRING")

    try:
        async with aioodbc.create_pool(dsn=conn_str) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(sql, params or [])
                    await conn.commit()

        return "SQL execution successful"

    except Exception as e:
        return f"SQL Error: {str(e)}"