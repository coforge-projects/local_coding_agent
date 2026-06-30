from agentic_codex.mcp.tools_metadata import TOOL_METADATA


def get_tool_descriptions():
    return "\n".join(
        f"- {tool['name']}: {tool['description']}"
        for tool in TOOL_METADATA
    )