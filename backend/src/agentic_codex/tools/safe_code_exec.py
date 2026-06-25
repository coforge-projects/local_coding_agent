import subprocess
from pathlib import Path
import sys


def execute_python(project_id: str, filename: str):
    file_path = Path(f"./projects/{project_id}/{filename}")

    if not file_path.exists():
        return f"File '{filename}' not found."

    try:
        result = subprocess.run(
            [sys.executable, str(file_path)],  # ✅ fixed
            capture_output=True,
            text=True,
            timeout=5
        )

        output = result.stdout.strip()
        error = result.stderr.strip()

        if error:
            return f"Error:\n{error}"

        if output:
            return f"Output:\n{output}"

        return "⚠️ Code executed but produced no output."

    except subprocess.TimeoutExpired:
        return "Execution timed out."