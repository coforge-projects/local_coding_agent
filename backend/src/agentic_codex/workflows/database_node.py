from agentic_codex.workflows.state import AgentState
from agentic_codex.mcp.mcp_executor import MCPExecutor


async def database_node(state: AgentState):
    user_message = state["messages"][-1]["content"]

    mcp = MCPExecutor(
        project_id=state["project_id"]
    )

    if "projects" in user_message.lower():
        response = await mcp.invoke(
            "sql__query",
            "SELECT * FROM projects"
        )
    else:
        response = "No database action identified."

    return {
        **state,
        "response": str(response)
    }
