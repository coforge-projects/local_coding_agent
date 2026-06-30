import os
from dotenv import load_dotenv

from mcp.server.fastmcp import FastMCP

from agentic_codex.mcp.registry import register_mcp_components

load_dotenv()

# ✅ Azure SQL connection string
CONN_STR = os.getenv("SERVER_CONNECTION_STRING")

# ✅ MCP instance
mcp = FastMCP("agentic-codex")

# ✅ Register all MCP components
register_mcp_components(mcp, CONN_STR)

# ✅ START MCP SERVER
if __name__ == "__main__":
    mcp.run()