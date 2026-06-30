from typing import List, Dict

from agentic_codex.agents.base_agent import BaseAgent


class CodingAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="coding-agent")

    async def run(self, messages: List[Dict[str, str]]) -> str:
        """
        General-purpose conversational agent.
        Does NOT execute tools.
        """

        system_prompt = self.format_system_message(
            "You are a helpful coding assistant.\n\n"
            "Respond in natural language.\n"
            "Do NOT return JSON actions.\n"
            "Do NOT call tools.\n"
            "Do NOT return structured tool responses.\n"
            "Simply answer the user's question clearly."
        )

        full_messages = [system_prompt] + messages

        return await super().run(full_messages)