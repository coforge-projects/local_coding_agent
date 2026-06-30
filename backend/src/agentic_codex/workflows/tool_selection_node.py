from agentic_codex.workflows.state import AgentState


async def tool_selection_node(state: AgentState):
    user_message = state["messages"][-1]["content"].lower()

    if any(
        keyword in user_message
        for keyword in [
            "sql",
            "database",
            "query",
            "table"
        ]
    ):
        state["selected_tool_category"] = "database"

    elif any(
        keyword in user_message
        for keyword in [
            "file",
            ".py",
            "create",
            "write",
            "read"
        ]
    ):
        state["selected_tool_category"] = "filesystem"

    elif any(
        keyword in user_message
        for keyword in [
            "run",
            "execute",
            "debug",
            "fix"
        ]
    ):
        state["selected_tool_category"] = "execution"

    else:
        state["selected_tool_category"] = "general"

    return state