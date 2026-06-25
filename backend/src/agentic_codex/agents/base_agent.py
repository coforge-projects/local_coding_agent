from typing import List, Dict, Any
from agentic_codex.llm.azure_client import generate_response


class BaseAgent:
    def __init__(self, name: str):
        self.name = name

    async def run(self, messages: List[Dict[str, str]]) -> str:
        """
        Core method every agent will use.
        Calls the LLM with given messages.
        """
        response = await generate_response(messages)
        return response

    def format_user_message(self, content: str) -> Dict[str, str]:
        return {"role": "user", "content": content}

    def format_system_message(self, content: str) -> Dict[str, str]:
        return {"role": "system", "content": content}

    def format_assistant_message(self, content: str) -> Dict[str, str]:
        return {"role": "assistant", "content": content}
