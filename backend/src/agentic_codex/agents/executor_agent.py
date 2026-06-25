from typing import List, Dict
import json

from agentic_codex.agents.base_agent import BaseAgent
from agentic_codex.tools.file_ops import create_file, read_file, write_file
from agentic_codex.tools.safe_code_exec import execute_python


class ExecutorAgent(BaseAgent):
    def __init__(self, project_id: str):
        super().__init__(name="executor-agent")
        self.project_id = project_id

    async def run(self, messages: List[Dict[str, str]]) -> str:
        # ✅ better system instruction
        system_prompt = {
            "role": "system",
            "content": (
                "Execute coding tasks using tools.\n"
                "Always return actions in JSON.\n"
                "When writing Python code, ensure it uses print() for output."
            )
        }

        response_text = await super().run([system_prompt] + messages)

        try:
            json_part = None

            start = response_text.find('[')
            end = response_text.rfind(']') + 1

            if start != -1 and end != -1:
                json_part = response_text[start:end]
            else:
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                if start != -1 and end != -1:
                    json_part = response_text[start:end]

            if json_part:
                action_list = json.loads(json_part)

                if isinstance(action_list, dict):
                    action_list = [action_list]

                results = []
                last_file = None

                for action_item in action_list:
                    action = action_item.get("action")
                    input_value = action_item.get("input", "")
                    content_value = action_item.get("content", "")

                    # ✅ sanitize filename
                    if "." in input_value:
                        parts = input_value.split(".")
                        input_value = parts[0] + "." + parts[1].split()[0]
                    else:
                        input_value = input_value.split()[0]

                    if action == "create_file":
                        result = create_file(self.project_id, input_value)
                        last_file = input_value

                    elif action == "write_file":
                        # ✅ DO NOT recreate file
                        result = write_file(self.project_id, input_value, content_value)
                        last_file = input_value

                    elif action == "read_file":
                        result = read_file(self.project_id, input_value)

                    elif action == "execute_python":
                        result = execute_python(self.project_id, input_value)

                        # ✅ DEBUG LOOP
                        if "Error:" in result and last_file:
                            error_msg = result
                            code = read_file(self.project_id, last_file)

                            fix_prompt = [
                                {
                                    "role": "system",
                                    "content": "Fix Python code. Return ONLY corrected code with proper print() if needed."
                                },
                                {
                                    "role": "user",
                                    "content": f"Code:\n{code}\n\nError:\n{error_msg}"
                                }
                            ]

                            # ✅ IMPORTANT: no recursion
                            fix_response = await super().run(fix_prompt)

                            fixed_code = fix_response.strip().replace("```python", "").replace("```", "")

                            write_file(self.project_id, last_file, fixed_code)

                            result = execute_python(self.project_id, last_file)

                    else:
                        continue

                    results.append(result)

                if results:
                    return "\n".join(results)

        except Exception as e:
            return f"Execution error: {str(e)}"

        return response_text