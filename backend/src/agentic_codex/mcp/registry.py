from agentic_codex.mcp.tools import register_tools
from agentic_codex.mcp.resources import register_resources
from agentic_codex.mcp.prompts import register_prompts


def register_mcp_components(mcp, conn_str):
    """
    Register all MCP components.
    """

    register_tools(mcp, conn_str)
    register_resources(mcp)
    register_prompts(mcp)