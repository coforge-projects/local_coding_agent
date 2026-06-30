from typing import List, Dict

from agentic_codex.workflows.runner import run_graph


class Supervisor:
    def __init__(self, project_id: str):
        self.project_id = project_id

    async def run(self, messages: List[Dict[str, str]]) -> str:
        return await run_graph(
            messages=messages,
            project_id=self.project_id
        )