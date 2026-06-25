from typing import List, Dict

from agentic_codex.agents.planner_agent import PlannerAgent
from agentic_codex.agents.executor_agent import ExecutorAgent
from agentic_codex.agents.coding_agent import CodingAgent


class Supervisor:
    def __init__(self, project_id: str):
        self.project_id = project_id

        # ✅ initialize agents
        self.planner = PlannerAgent()
        self.executor = ExecutorAgent(project_id=project_id)
        self.coder = CodingAgent()

    async def run(self, messages: List[Dict[str, str]]) -> str:
        """
        Controls the full agent workflow
        """

        # ✅ Step 1: Planning
        plan = await self.planner.run(messages)

        # ✅ Step 2: Decide execution vs normal response
        if any(keyword in messages[-1]["content"].lower() for keyword in ["create", "write", "run", "execute"]):
            
            # ✅ Step 3: Execute actions
            execution_input = [
                {"role": "system", "content": f"Plan:\n{plan}"},
                *messages
            ]

            result = await self.executor.run(execution_input)
            return result

        else:
            # ✅ fallback → just respond normally
            response = await self.coder.run(messages)
            return response
