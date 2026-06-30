from langgraph.graph import StateGraph, END
from agentic_codex.workflows.tool_selection_node import tool_selection_node
from agentic_codex.workflows.state import AgentState
from agentic_codex.workflows.database_node import database_node

from agentic_codex.workflows.nodes import (
    planner_node,
    executor_node,
    coding_node
)


def should_execute(state: AgentState):
    user_message = state["messages"][-1]["content"].lower()

    execution_keywords = [
        "create",
        "write",
        "run",
        "execute",
        "fix",
        "edit",
        "update",
        "debug"
    ]

    if any(keyword in user_message for keyword in execution_keywords):
        return "executor"

    return "coding"

def route_tool_category(state: AgentState):
    category = state.get("selected_tool_category")

    if category == "database":
        return "database"

    if category in ["filesystem", "execution"]:
        return "executor"

    return "coding"

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("planner", planner_node)
    graph.add_node("tool_selection", tool_selection_node)
    graph.add_node("database", database_node)
    graph.add_node("executor", executor_node)
    graph.add_node("coding", coding_node)

    graph.set_entry_point("planner")

    graph.add_edge(
    "planner",
    "tool_selection"
    )

    graph.add_conditional_edges(
        "tool_selection",
        route_tool_category,
        {
            "database": "database",
            "executor": "executor",
            "coding": "coding"
        }
    )


    graph.add_edge("executor", END)
    graph.add_edge("coding", END)
    graph.add_edge("database", END)

    return graph.compile()