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
    git_ssh_cmd = "ssh -i .ssh/test_rsa"
    # repo.config_writer("repository").set_value("user", "name", "pl-at").release()
    repo = Repo.clone_from(
        remote_path, local_path, env=dict(GIT_SSH_COMMAND=git_ssh_cmd)
    )
    repo.config_writer("repository").set_value("user", "name", "pl-at").release()
    repo.config_writer("repository").set_value(
        "user", "email", "plukasik.projectq+at1@gmail.com"
    ).release()

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


def push_changes(repo: Repo):
    ssh_cmd = "ssh -i .ssh/test_rsa"
    repo.config_writer("repository").set_value("user", "name", "pl-at").release()
    repo.config_writer("repository").set_value(
        "user", "email", "plukasik.projectq+at1@gmail.com"
    ).release()
    repo.config_writer("repository").set_value(
        "credential", "helper", "sourcetree"
    ).release()
    with repo.git.custom_environment(GIT_SSH_COMMAND=ssh_cmd):
        repo.remotes.origin.fetch()
        repo.remotes.origin.push(refspec="main:main")
