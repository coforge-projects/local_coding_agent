from pathlib import Path


BASE_PROJECTS_DIR = (
    Path(__file__)
    .resolve()
    .parents[4]
    / "projects"
)


def get_project_path(project_id: str) -> Path:
    return BASE_PROJECTS_DIR / project_id


def create_file(project_id: str, filename: str):
    file_path = get_project_path(project_id) / filename

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if not file_path.exists():
        file_path.write_text(
            "# New file created by AI"
        )

    return f"File '{filename}' created successfully."


def read_file(project_id: str, filename: str):
    file_path = get_project_path(project_id) / filename

    if file_path.exists():
        return file_path.read_text()

    return f"File '{filename}' not found."


def write_file(
    project_id: str,
    filename: str,
    content: str
):
    file_path = get_project_path(project_id) / filename

    if not file_path.exists():
        return f"File '{filename}' not found."

    file_path.write_text(content)

    return f"File '{filename}' updated successfully."