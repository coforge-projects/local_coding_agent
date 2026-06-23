from pathlib import Path

def create_file(project_id: str, filename: str):
    file_path = Path(f"./projects/{project_id}/{filename}")
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text("# New file created by AI")

    return f"File '{filename}' created successfully."


def read_file(project_id: str, filename: str):
    file_path = Path(f"./projects/{project_id}/{filename}")

    if file_path.exists():
        content = file_path.read_text()
        return f"File content:\n\n{content}"
    else:
        return f"File '{filename}' not found."
    
def write_file(project_id: str, filename: str, content: str):
    file_path = Path(f"./projects/{project_id}/{filename}")
    
    if not file_path.exists():
        return f"File '{filename}' not found."

    file_path.write_text(content)
    return f"File '{filename}' updated successfully."