from typing import List, Dict
from agentic_codex.agents.base_agent import BaseAgent


class PlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="planner-agent")

    async def run(self, messages: List[Dict[str, str]]) -> str:
        """
        Generates a step-by-step plan from user input.
        """

        system_prompt = self.format_system_message(
            "You are a planning agent.\n\n"
            "Break the user's request into clear, ordered steps.\n"
            "Keep steps concise and practical.\n"
            "Do NOT execute anything — only plan.\n\n"
            "Return output like:\n"
            "1. Step one\n"
            "2. Step two\n"
            "3. Step three"
        )

        full_messages = [system_prompt] + messages

        response = await super().run(full_messages)
        return response
