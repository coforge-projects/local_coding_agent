from agentic_codex.workflows.graph import build_graph


async def run_graph(messages, project_id):
    graph = build_graph()

    result = await graph.ainvoke(
    {
        "messages": messages,
        "project_id": project_id,
        "plan": "",
        "response": "",
        "selected_tool_category": ""
    }
)

    return result["response"]