import os
import shutil
from pathlib import Path

from git import Repo


def create_repo_folder(folder_name: str) -> Path:
    base_dir = os.path.abspath("/tmp/")
    repo_dir = os.path.join(os.path.abspath(base_dir), folder_name)
    return Path(repo_dir)


def use_existing_repo(repo_path: Path) -> Repo:
    repo = Repo(repo_path)
    return repo


def clone_repository(remote_path, local_path: Path) -> Repo:
    repo = Repo.clone_from(remote_path, local_path)
    return repo


def get_latest_commit(repo: Repo) -> Repo:
    return repo.head.commit.tree


def remove_repo(repo_dir: Path) -> None:
    shutil.rmtree(repo_dir)


def add_file(repo: Repo, file_name: str) -> None:
    add_file = [file_name]
    repo.index.add(add_file)


def commit_change(repo: Repo, message: str) -> None:
    repo.index.commit(message)
