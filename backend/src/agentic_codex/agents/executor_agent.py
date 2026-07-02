from typing import List, Dict
import json

from agentic_codex.agents.base_agent import BaseAgent
from agentic_codex.tools.file_ops import read_file, write_file
from agentic_codex.tools.safe_code_exec import execute_python

from agentic_codex.mcp.tool_registry import get_tool_registry
from agentic_codex.mcp.tool_definitions import get_tool_descriptions
from agentic_codex.mcp.mcp_executor import MCPExecutor


class ExecutorAgent(BaseAgent):
    def __init__(self, project_id: str):
        super().__init__(name="executor-agent")
        self.project_id = project_id

    async def run(self, messages: List[Dict[str, str]]) -> str:
        tool_list = get_tool_descriptions()

        system_prompt = {
            "role": "system",
            "content": (
                "You are an executor agent.\n"
                "Always return actions in JSON format.\n\n"
                f"Available tools:\n{tool_list}\n\n"
                "When writing Python code, always include print() "
                "so output is visible."
            )
        }

        response_text = await super().run(
            [system_prompt] + messages
        )

        try:
            json_part = None

            start = response_text.find("[")
            end = response_text.rfind("]") + 1

            if start != -1 and end != -1:
                json_part = response_text[start:end]
            else:
                start = response_text.find("{")
                end = response_text.rfind("}") + 1

                if start != -1 and end != -1:
                    json_part = response_text[start:end]

            if json_part:
                action_list = json.loads(json_part)

                if isinstance(action_list, dict):
                    action_list = [action_list]

                results = []
                last_file = None

                mcp_executor = MCPExecutor(
                    self.project_id
                )

                tool_registry = get_tool_registry(
                    self.project_id
                )

                for action_item in action_list:
                    action = action_item.get("action")

                    input_value = action_item.get(
                        "input",
                        ""
                    )

                    content_value = action_item.get(
                        "content",
                        ""
                    )

                    if input_value:
                        if "." in input_value:
                            parts = input_value.split(".")
                            input_value = (
                                parts[0]
                                + "."
                                + parts[1].split()[0]
                            )
                        else:
                            input_value = input_value.split()[0]

                    if action not in tool_registry:
                        continue

                    result = await mcp_executor.invoke(
                        action,
                        input_value,
                        content_value
                    )

                    if action in [
                        "create_file",
                        "write_file"
                    ]:
                        last_file = input_value

                    error_indicators = [
                        "Error:",
                        "Exception:",
                        "Traceback",
                        "SyntaxError",
                        "NameError",
                        "TypeError",
                        "ImportError",
                        "IndentationError"
                    ]

                    has_error = (
                        isinstance(result, str)
                        and any(
                            indicator in result
                            for indicator in error_indicators
                        )
                    )

                    debug_file = None

                    if action == "execute_python":
                        debug_file = input_value
                    elif last_file:
                        debug_file = last_file

                    if (
                        action == "execute_python"
                        and has_error
                        and debug_file
                    ):
                        error_msg = result

                        code = read_file(
                            self.project_id,
                            debug_file
                        )

                        fix_prompt = [
                            {
                                "role": "system",
                                "content": (
                                    "Fix the Python code.\n"
                                    "Return ONLY valid Python code.\n"
                                    "No markdown.\n"
                                    "No explanation.\n"
                                    "Preserve original intent."
                                )
                            },
                            {
                                "role": "user",
                                "content": (
                                    f"Code:\n{code}\n\n"
                                    f"Error:\n{error_msg}"
                                )
                            }
                        ]

                        fix_response = await super().run(
                            fix_prompt
                        )

                        fixed_code = (
                            fix_response
                            .replace("```python", "")
                            .replace("```", "")
                            .strip()
                        )

                        write_file(
                            self.project_id,
                            debug_file,
                            fixed_code
                        )

                        rerun_result = execute_python(
                            self.project_id,
                            debug_file
                        )

                        result = (
                            f"{error_msg}\n\n"
                            f"Auto-debug attempted.\n\n"
                            f"{rerun_result}"
                        )

                    results.append(str(result))

                if results:
                    return "\n".join(results)

        except Exception as e:
            return f"Execution error: {str(e)}"

        return response_text