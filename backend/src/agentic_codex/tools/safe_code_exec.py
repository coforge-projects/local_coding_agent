import subprocess
from pathlib import Path

def execute_python(project_id: str, filename: str):
    file_path = Path(f"./projects/{project_id}/{filename}")

    if not file_path.exists():
        return f"File '{filename}' not found."

    try:
        result = subprocess.run(
            ["python", str(file_path)],
            capture_output=True,
            text=True,
            timeout=5
        )

        output = result.stdout.strip()
        error = result.stderr.strip()

        if output:
            return f"Output:\n{output}"
        elif error:
            return f"Error:\n{error}"
        else:
            return "Execution completed (no output)."

    except subprocess.TimeoutExpired:
        return "Execution timed out."