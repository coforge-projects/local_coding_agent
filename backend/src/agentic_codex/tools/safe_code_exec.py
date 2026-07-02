import subprocess
import sys

from pathlib import Path


BASE_PROJECTS_DIR = (
    Path(__file__)
    .resolve()
    .parents[4]
    / "projects"
)


def get_project_path(project_id: str) -> Path:
    return BASE_PROJECTS_DIR / project_id


def execute_python(
    project_id: str,
    filename: str
):
    file_path = (
        get_project_path(project_id)
        / filename
    ).resolve()

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

        return (
            "⚠️ Code executed but produced no output."
        )

    except subprocess.TimeoutExpired:
        return "Execution timed out."