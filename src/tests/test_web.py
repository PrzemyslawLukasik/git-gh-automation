import os

import pytest
from git import Repo
from playwright.sync_api import APIRequestContext, APIResponse, Page

from src.endpoints.repositories import Repositories
from src.fixtures.api_fixture import api_request_context, repo_create_delete
from src.helpers.generators import generate_new_repo_data_ui
from src.helpers.git_helper import (
    clone_repository,
    copy_file_to_repository,
    create_repo_folder,
)


@pytest.mark.UI
def test_open_login_page(dashboard_page) -> None:
    # Login
    dashboard_page.visit()
    # Verify user is logged in
    dashboard_page.is_open()


@pytest.mark.UI
def test_create_repository(
    api_request_context,
    dashboard_page,
    new_repo_create_page,
    repo_code_page,
) -> None:
    # Open Dashboard
    dashboard_page.visit()

    # Create a new repository
    dashboard_page.click_new_button()
    repository_data: dict = next(generate_new_repo_data_ui())
    new_repo_create_page.create_repository(data=repository_data)

    # Verify repository is created
    repo_code_page.is_correct_repo_open(repository_data["repository_name"])

    # Clean
    Repositories().delete_repository(
        api_request_context, repository_data["repository_name"]
    )


@pytest.mark.UI
@pytest.mark.git
def test_pushed_files_visible(repo_create_delete, repo_code_page) -> None:
    # Pre-conditions
    repo_name = repo_create_delete
    repo_url: str = f"{os.environ['REPO_URL']}/{os.environ['API_USER']}/{repo_name}"
    payload_file_name: str = "file_test_1.py"
    payload_file_url: str = f"src/payload/{payload_file_name}"
    commit_message = "Upload of file_test_1.py"

    # Create local folder for user
    repo_folder: str = create_repo_folder(str(repo_name))

    # Clone remote repository to local folders
    repo: Repo = clone_repository(repo_url, repo_folder)

    # Copy file and push to the repository path
    copy_file_to_repository(repo, payload_file_url, repo_folder, payload_file_name)
    repo.git.add(payload_file_name)
    repo.git.commit("-m", commit_message)
    repo.git.push("origin", "main")

    # Go to the repository page
    repo_code_page.visit_repo(repo_name)

    # Verify file in repository
    repo_code_page.is_file_visible(payload_file_name)


@pytest.mark.UI
@pytest.mark.git
@pytest.mark.merge
def test_create_and_merge_branch(
    repo_create_delete,
    repo_code_page,
    top_bar_menu,
    pull_requests_page,
    compare_changes_page,
    pull_request_page,
) -> None:
    # Pre-conditions
    repo_name = repo_create_delete
    repo_url: str = f"{os.environ['REPO_URL']}/{os.environ['API_USER']}/{repo_name}"
    payload_file_name: str = "file_test_1.py"
    payload_file_url: str = f"src/payload/{payload_file_name}"
    commit_message = "Upload of file_test_1.py"
    branch_name = "test_branch_1"

    repo_folder: str = create_repo_folder(str(repo_name))
    repo: Repo = clone_repository(repo_url, repo_folder)
    repo.git.checkout("-b", branch_name)
    copy_file_to_repository(repo, payload_file_url, repo_folder, payload_file_name)
    repo.git.add(payload_file_name)
    repo.git.commit("-m", commit_message)
    repo.git.push("origin", branch_name)

    # Go to Pull Requests
    repo_code_page.visit_repo(repo_name)
    top_bar_menu.click_on_pull_requests()

    # Create a new Pull request
    pull_requests_page.click_on_new_pull_request_button()
    compare_changes_page.create_pull_request(
        base_branch="main", compare_branch=branch_name
    )

    # Merge PR
    pull_request_page.confirm_and_merge()

    # Verify change on main branch
    repo_code_page.visit_repo(repo_name)
    repo_code_page.is_file_visible(payload_file_name)
