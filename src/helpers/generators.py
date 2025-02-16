import random
import string
from typing import Generator
from uuid import uuid4


def generate_uuid() -> str:
    """
    Returns generated UUID
    """

    get_uuid = str(uuid4())
    return get_uuid


def generate_string(
    length: int = 10, letters: str = (string.ascii_lowercase + string.ascii_uppercase)
) -> str:
    """
    Returns random 10 chars string
    """
    get_string = "".join(random.choice(letters) for i in range(length))
    return get_string


def generate_new_repo_data_ui() -> Generator[dict, None, None]:
    generated_data = generate_string()
    yield {
        "repository_name": "Repo_name_" + generated_data,
        "branch_name": "master",
    }


def generate_new_repo_data_api() -> Generator[dict, None, None]:
    generated_data = generate_string()
    yield {
        "full_name": f"Test Repo {generated_data}",
        "is_private": False,
        "scm": "git",
        "project": {"key": "TES"},
    }
