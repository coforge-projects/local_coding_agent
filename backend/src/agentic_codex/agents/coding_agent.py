from typing import List, Dict
from agentic_codex.agents.base_agent import BaseAgent


class CodingAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="coding-agent")

    async def run(self, messages: List[Dict[str, str]]) -> str:
        """
        Main coding agent logic.
        For now, just passes messages to LLM.
        """
        # ✅ Optional system prompt (keeps behavior consistent)
        system_prompt = self.format_system_message(
            "You are a coding assistant. Follow instructions carefully and return structured responses."
        )

        # ✅ prepend system prompt
        full_messages = [system_prompt] + messages

        response = await super().run(full_messages)
        return response
