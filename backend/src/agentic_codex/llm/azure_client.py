import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2025-04-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_API_ENDPOINT")
)


async def generate_response(messages):
    prompt = (
        "You are an AI coding agent.\n\n"

        "Think briefly, then act.\n\n"

        "Always return actions in JSON when needed:\n"
        '[ { "action": "action_name", "input": "file.py" } ]\n\n'

        "For writing code:\n"
        '{ "action": "write_file", "input": "file.py", "content": "code here" }\n\n'

        "IMPORTANT:\n"
        "- Keep filenames clean\n"
        "- Return only JSON for actions\n"
        "- For debugging, return ONLY fixed code\n\n"

        "Available actions:\n"
        "- create_file\n"
        "- read_file\n"
        "- write_file\n"
        "- execute_python\n\n"
    )

    for msg in messages:
        prompt += f"{msg['role']}: {msg['content']}\n"

    response = client.responses.create(
        model=os.getenv("AZURE_OPENAI_API_DEPLOYMENT"),
        input=prompt
    )

    return response.output_text
