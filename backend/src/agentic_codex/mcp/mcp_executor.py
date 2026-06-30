import inspect

from agentic_codex.mcp.tool_registry import get_tool_registry


class MCPExecutor:
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.registry = get_tool_registry(project_id)

    async def invoke(
        self,
        tool_name: str,
        input_value: str = "",
        content_value: str = ""
    ):
        if tool_name not in self.registry:
            return f"Unknown MCP tool: {tool_name}"

        tool = self.registry[tool_name]

        result = tool(
            input_value,
            content_value
        )

        if inspect.isawaitable(result):
            result = await result

        return result