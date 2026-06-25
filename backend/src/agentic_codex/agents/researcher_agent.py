from typing import List, Dict
from agentic_codex.agents.base_agent import BaseAgent


class ResearcherAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="researcher-agent")

    async def run(self, messages: List[Dict[str, str]]) -> str:
        """
        Provides explanations, documentation, or research-style responses.
        """

        system_prompt = self.format_system_message(
            "You are a research assistant.\n\n"
            "Provide clear explanations, relevant context, and helpful details.\n"
            "Focus on improving understanding before execution.\n"
            "Avoid taking actions or writing files."
        )

        full_messages = [system_prompt] + messages

        response = await super().run(full_messages)
        return response
