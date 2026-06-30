from agentic_codex.workflows.state import AgentState

from agentic_codex.agents.planner_agent import PlannerAgent
from agentic_codex.agents.executor_agent import ExecutorAgent
from agentic_codex.agents.coding_agent import CodingAgent


async def planner_node(state: AgentState):
    planner = PlannerAgent()

    plan = await planner.run(state["messages"])

    return {
        **state,
        "plan": plan
    }


async def executor_node(state: AgentState):
    executor = ExecutorAgent(
        project_id=state["project_id"]
    )

    execution_input = [
        {
            "role": "system",
            "content": f"Plan:\n{state['plan']}"
        },
        *state["messages"]
    ]

    response = await executor.run(
        execution_input
    )

    return {
        **state,
        "response": response
    }


async def coding_node(state: AgentState):
    coder = CodingAgent()

    response = await coder.run(
        state["messages"]
    )

    return {
        **state,
        "response": response
    }