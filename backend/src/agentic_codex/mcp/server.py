from mcp.server.fastmcp import FastMCP

mcp = FastMCP("agentic-codex")

# ✅ Example tool (test)
@mcp.tool()
def ping():
    return "MCP server is running"

# ✅ Example filesystem-style tool (optional start)
@mcp.tool()
def create_file(project_id: str, filename: str):
    from pathlib import Path

    file_path = Path(f"./projects/{project_id}/{filename}")
    file_path.parent.mkdir(parents=True, exist_ok=True)

    if not file_path.exists():
        file_path.write_text("")

    return f"File {filename} created"

# ✅ Start MCP server
if __name__ == "__main__":
    mcp.run()
