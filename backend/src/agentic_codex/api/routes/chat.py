from fastapi import APIRouter, Depends
from agentic_codex.api.schemas.chat import ChatRequest, ChatResponse, ChatMessage
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
import json

# ✅ DB
from agentic_codex.db.database import get_db
from agentic_codex.db.repos.message_repo import MessageRepo
from agentic_codex.db.repos.conversation_repo import ConversationRepo
from agentic_codex.db.repos.project_repo import ProjectRepo  # ✅ NEW

# ✅ tools
from agentic_codex.tools.file_ops import create_file, read_file, write_file
from agentic_codex.tools.safe_code_exec import execute_python

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest, db: AsyncSession = Depends(get_db)):
    project_id = payload.project_id
    conversation_id = payload.conversation_id
    message = payload.message

    message_repo = MessageRepo(db)
    conversation_repo = ConversationRepo(db)
    project_repo = ProjectRepo(db)  # ✅ NEW

    # ✅ 1. VALIDATE PROJECT
    project = await project_repo.get_by_id(project_id)

    if not project:
        # ✅ auto-create project (safe fallback)
        project = await project_repo.create({
            "id": uuid.uuid4(),
            "name": f"Project-{project_id}",
            "desc": "Auto-created project",
            "owner_id": None,
            "language": "python"
        })
        project_id = project.id

    # ✅ 2. HANDLE CONVERSATION
    if not conversation_id:
        convo = await conversation_repo.create({
            "id": uuid.uuid4(),
            "project_id": project_id,
            "user_id": None,
            "title": "New Conversation"
        })
        conversation_id = convo.id
    else:
        convo = await conversation_repo.get_by_id(conversation_id)
        if not convo:
            return {"detail": "Conversation not found"}

    # ✅ 3. SAVE USER MESSAGE
    await message_repo.create({
        "id": uuid.uuid4(),
        "conversation_id": conversation_id,
        "role": "user",
        "content": message,
        "tokens_used": 0
    })

    # ✅ 4. FETCH HISTORY
    history = await message_repo.list_last_n(conversation_id, n=10)

    messages = [
        {"role": msg.role, "content": msg.content}
        for msg in reversed(history)
    ]

    from agentic_codex.llm.azure_client import generate_response

    response_text = await generate_response(messages)

    # ✅ 5. ACTION SYSTEM (UNCHANGED)
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

                    # ✅ DEBUG LOOP
                    if "Error:" in result and last_file:
                        error_msg = result
                        code = read_file(project_id, last_file)

                        fix_prompt = [
                            {"role": "system", "content": "Fix Python code. Return ONLY corrected code."},
                            {"role": "user", "content": f"Code:\n{code}\n\nError:\n{error_msg}"}
                        ]

                        fix_response = await generate_response(fix_prompt)
                        fixed_code = fix_response.strip().strip("```python").strip("```")

                        write_file(project_id, last_file, fixed_code)
                        result = execute_python(project_id, last_file)

                else:
                    continue

                results.append(result)

            if results:
                response_text = "\n".join(results)

    except Exception as e:
        print("Action parsing failed:", e)

    # ✅ 6. SAVE ASSISTANT MESSAGE
    await message_repo.create({
        "id": uuid.uuid4(),
        "conversation_id": conversation_id,
        "role": "assistant",
        "content": response_text,
        "tokens_used": 0
    })

    return ChatResponse(
        conversation_id=str(conversation_id),
        message=ChatMessage(
            id=str(uuid.uuid4()),
            role="assistant",
            content=response_text,
            tokens_used=10
        )
    )
