import json

from agentic_codex.workflows.state import AgentState

from agentic_codex.agents.planner_agent import PlannerAgent
from agentic_codex.agents.executor_agent import ExecutorAgent
from agentic_codex.agents.coding_agent import CodingAgent


async def planner_node(state: AgentState):
    planner = PlannerAgent()

    plan = await planner.run(
        state["messages"]
    )

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


async def validation_node(state: AgentState):
    response = state.get(
        "response",
        ""
    ).lower()

    failure_patterns = [
        "error",
        "exception",
        "traceback",
        "failed"
    ]

    for pattern in failure_patterns:
        if pattern in response:
            return {
                **state,
                "success": False,
                "validation_reason": (
                    f"Detected '{pattern}' "
                    "in execution response"
                )
            }

    return {
        **state,
        "success": True,
        "validation_reason": "Validation passed"
    }


async def reflection_node(state: AgentState):
    coder = CodingAgent()

    user_request = (
        state["messages"][-1]["content"]
        if state["messages"]
        else ""
    )

    reflection_prompt = [
        {
            "role": "user",
            "content": f"""
User Request:
{user_request}

Execution Plan:
{state.get("plan", "")}

Execution Result:
{state.get("response", "")}

Validation Result:
Success = {state.get("success", False)}

Validation Reason:
{state.get("validation_reason", "")}

Determine:

1. Was the user's request completed?
2. What is missing, if anything?
3. Should another execution attempt be made?

Return ONLY valid JSON in this format:

{{
    "reflection": "your analysis",
    "needs_retry": true
}}

or

{{
    "reflection": "your analysis",
    "needs_retry": false
}}
"""
        }
    ]

    response = await coder.run(
        reflection_prompt
    )

    try:
        result = json.loads(response)

        return {
            **state,
            "reflection": result.get(
                "reflection",
                "No reflection generated"
            ),
            "needs_retry": result.get(
                "needs_retry",
                False
            )
        }

    except Exception:
        return {
            **state,
            "reflection": response,
            "needs_retry": False
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