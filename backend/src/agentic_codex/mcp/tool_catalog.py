from agentic_codex.mcp.tools_metadata import TOOL_METADATA


AVAILABLE_TOOLS = {
    tool["name"]: tool["description"]
    for tool in TOOL_METADATA
}