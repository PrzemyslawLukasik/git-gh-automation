import shutil
from pathlib import Path


def copy_file_to_repo(src: Path, dest: Path) -> None:
    shutil.copy(src=src, dst=dest)


def read_the_file(file_path: Path) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def read_file_to_table(src: Path) -> list[str]:
    table: list = []
    with open(src, "r", encoding="utf-8") as f:
        for line in f:
            table.append(line)
    return table


def replace_file_content(file_path: Path, content: str) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
