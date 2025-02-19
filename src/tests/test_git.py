import os

import pytest
from git import Repo

from src.fixtures.api_fixture import api_request_context, repo_create_delete
from src.helpers.files_helper import copy_file_to_repo
from src.helpers.git_helper import clone_repository, create_repo_folder, push_changes


@pytest.mark.git
def test_clone_repository(repo_create_delete: str) -> None:
    # Create repository
    repo_name: str = repo_create_delete
    repo_url: str = f"{os.environ['URL']}/{os.environ['API_USER']}/{repo_name}"

    # Create local folder
    repo_folder: str = create_repo_folder(repo_name)

    # Clone remote repository to local folder
    repo: Repo = clone_repository(repo_url, repo_folder)

    # Verify repository cloned
    assert repo.description, "Repository not clonned correctly!"


@pytest.mark.git
def test_add_files_and_commit(repo_create_delete: str) -> None:
    # Prepare data
    repo_name: str = repo_create_delete
    repo_url: str = f"{os.environ['URL']}/{os.environ['API_USER']}/{repo_name}"
    payload_file_name: str = "README.md"
    payload_file_url: str = f"src/payload/{payload_file_name}"
    commit_message = "Update of README.md"

    # Create local folder
    repo_folder: str = create_repo_folder(repo_name)

    # Clone remote repository to local folder
    repo: Repo = clone_repository(repo_url, repo_folder)

    # Copy / create file to the repository path
    copy_file_to_repo(payload_file_url, repo_folder)
    assert payload_file_name in repo.untracked_files, "README.md file not changed!"

    # Perform `git add` action
    repo.index.add(payload_file_name)

    # Verify file is staged
    assert not repo.untracked_files, "Readme file still in unstaged!"
    assert (
        payload_file_name in list(repo.index.entries)[0][0]
    ), "Readme file not staged!"

    # Perform `git commit`
    commit = repo.index.commit(commit_message)

    # Verify commit created
    assert commit.message in repo.active_branch.commit.message, "Changes not commited!"


@pytest.mark.git
def test_push_changes_to_remote(repo_create_delete: str) -> None:
    # Prepare data
    repo_name: str = repo_create_delete
    repo_url: str = f"{os.environ['REPO_URL']}/{os.environ['API_USER']}/{repo_name}"
    payload_file_name: str = "README.md"
    payload_file_url: str = f"src/payload/{payload_file_name}"
    commit_message = "Update of README.md in repo_1"

    # Create local folders for 2 users
    repo_folder_1: str = create_repo_folder(str(repo_name) + "_1")
    repo_folder_2: str = create_repo_folder(str(repo_name) + "_2")

    # Clone remote repository to local folders
    repo_1: Repo = clone_repository(repo_url, repo_folder_1)
    repo_2: Repo = clone_repository(repo_url, repo_folder_2)

    # Copy / create file to the repository path
    copy_file_to_repo(payload_file_url, repo_folder_1)
    assert payload_file_name in repo_1.untracked_files, "README.md file not changed!"

    # Perform `git add` action
    repo_1.index.add(payload_file_name)

    # Verify file is staged
    assert not repo_1.untracked_files, "Readme file still in unstaged!"
    assert (
        payload_file_name in list(repo_1.index.entries)[0][0]
    ), "Readme file not staged!"

    # Perform `git commit`
    commit = repo_1.index.commit(commit_message)

    # Verify commit created
    assert (
        commit.message in repo_1.active_branch.commit.message
    ), "Changes not commited!"

    # Push changes
    repo_1.remote(name="origin")
    push_changes(repo_1)

    origin_2 = repo_2.remote(name="origin")
    origin_2.pull()

    commit = origin_2.refs[0].commit
    summary = commit.summary
    assert commit_message in summary, f"Repository 2 not updated: {summary}"
