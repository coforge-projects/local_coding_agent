import subprocess
from pathlib import Path
import sys


def execute_python(project_id: str, filename: str):
    file_path = Path(f"./projects/{project_id}/{filename}").resolve()

    print(f"EXECUTING FILE: {file_path}")

    if not file_path.exists():
        return f"File '{filename}' not found."

    try:
        result = subprocess.run(
            [sys.executable, str(file_path)],
            capture_output=True,
            text=True,
            timeout=5,
            cwd=file_path.parent
        )

        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        print(f"STDOUT: {repr(stdout)}")
        print(f"STDERR: {repr(stderr)}")

        if stderr:
            return f"Error:\n{stderr}"

        if stdout:
            return f"Output:\n{stdout}"

        return "⚠️ Code executed but produced no output."

    except subprocess.TimeoutExpired:
        return "Execution timed out."