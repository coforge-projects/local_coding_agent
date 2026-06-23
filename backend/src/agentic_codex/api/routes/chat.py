from fastapi import APIRouter
from agentic_codex.api.schemas.chat import ChatRequest, ChatResponse, ChatMessage
import uuid
from datetime import datetime
import json

# ✅ tools
from agentic_codex.tools.file_ops import create_file, read_file, write_file
from agentic_codex.tools.safe_code_exec import execute_python

router = APIRouter()

projects = {}


@router.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest):
    project_id = payload.project_id
    conversation_id = payload.conversation_id
    message = payload.message

    if project_id not in projects:
        projects[project_id] = {}

    project_conversations = projects[project_id]

    if not conversation_id:
        conversation_id = str(uuid.uuid4())
        project_conversations[conversation_id] = []

    if conversation_id not in project_conversations:
        project_conversations[conversation_id] = []

    # ✅ store user message
    project_conversations[conversation_id].append({
        "id": str(uuid.uuid4()),
        "role": "user",
        "content": message,
        "timestamp": datetime.utcnow().isoformat()
    })

    from agentic_codex.llm.azure_client import generate_response

    history = project_conversations[conversation_id]

    messages = [{"role": msg["role"], "content": msg["content"]} for msg in history]

    response_text = await generate_response(messages)

    try:
        json_part = None

        # ✅ extract JSON from response
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
                    result = create_file(project_id, input_value)
                    last_file = input_value

                elif action == "write_file":
                    create_file(project_id, input_value)
                    result = write_file(project_id, input_value, content_value)
                    last_file = input_value

                elif action == "read_file":
                    result = read_file(project_id, input_value)

                elif action == "execute_python":
                    result = execute_python(project_id, input_value)

                    # ✅ REAL DEBUG LOOP (code + error)
                    if "Error:" in result and last_file:
                        error_msg = result
                        code = read_file(project_id, last_file)

                        fix_prompt = [
                            {
                                "role": "system",
                                "content": "Fix Python code. Return ONLY corrected code."
                            },
                            {
                                "role": "user",
                                "content": f"Code:\n{code}\n\nError:\n{error_msg}"
                            }
                        ]

                        fix_response = await generate_response(fix_prompt)

                        # ✅ clean extracted code
                        fixed_code = fix_response.strip().strip("```python").strip("```")

                        write_file(project_id, last_file, fixed_code)

                        # ✅ retry
                        result = execute_python(project_id, last_file)

                else:
                    continue

                results.append(result)

            if results:
                response_text = "\n".join(results)

    except Exception as e:
        print("Action parsing failed:", e)

    project_conversations[conversation_id].append({
        "id": str(uuid.uuid4()),
        "role": "assistant",
        "content": response_text,
        "timestamp": datetime.utcnow().isoformat()
    })

    return ChatResponse(
        conversation_id=conversation_id,
        message=ChatMessage(
            id=str(uuid.uuid4()),
            role="assistant",
            content=response_text,
            tokens_used=10
        )
    )
