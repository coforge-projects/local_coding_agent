from typing import List, Dict

from agentic_codex.llm.azure_client import generate_response
from agentic_codex.mcp.tool_definitions import get_tool_descriptions


class BaseAgent:
    def __init__(self, name: str):
        self.name = name

    async def run(self, messages: List[Dict[str, str]]) -> str:
        """
        Core method every agent uses.
        """

        tool_descriptions = get_tool_descriptions()

        system_message = {
            "role": "system",
            "content": (
                f"You are {self.name}.\n\n"
                f"Available MCP tools:\n"
                f"{tool_descriptions}"
            )
        }

        response = await generate_response(
            [system_message] + messages
        )

        return response

    def format_user_message(self, content: str) -> Dict[str, str]:
        return {"role": "user", "content": content}

    def format_system_message(self, content: str) -> Dict[str, str]:
        return {"role": "system", "content": content}

    def format_assistant_message(self, content: str) -> Dict[str, str]:
        return {"role": "assistant", "content": content}