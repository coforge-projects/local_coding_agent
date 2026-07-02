from agentic_codex.workflows.state import AgentState


async def tool_selection_node(state: AgentState):
    user_message = (
        state["messages"][-1]["content"]
        .lower()
    )

    database_keywords = [
        "sql",
        "database",
        "query",
        "table",
        "select",
        "insert",
        "update database",
        "delete from"
    ]

    filesystem_keywords = [
        "file",
        ".py",
        ".js",
        ".ts",
        ".json",
        ".html",
        ".css",
        "create",
        "write",
        "read",
        "build",
        "generate",
        "scaffold",
        "develop",
        "implement",
        "make",
        "project",
        "application",
        "api",
        "fastapi",
        "flask",
        "django",
        "react",
        "angular",
        "node",
        "backend",
        "frontend"
    ]

    execution_keywords = [
        "run",
        "execute",
        "debug",
        "fix",
        "test",
        "retry"
    ]

    if any(
        keyword in user_message
        for keyword in database_keywords
    ):
        state["selected_tool_category"] = (
            "database"
        )

    elif any(
        keyword in user_message
        for keyword in filesystem_keywords
    ):
        state["selected_tool_category"] = (
            "filesystem"
        )

    elif any(
        keyword in user_message
        for keyword in execution_keywords
    ):
        state["selected_tool_category"] = (
            "execution"
        )

    else:
        state["selected_tool_category"] = (
            "general"
        )

    return state