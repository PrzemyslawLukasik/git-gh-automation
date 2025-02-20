import pytest
from playwright.sync_api import APIRequestContext

from src.endpoints.commits import Commits
from src.endpoints.repositories import Repositories
from src.fixtures.api_fixture import api_request_context, repo_create_delete


@pytest.mark.API
def test_get_repositories(api_request_context: APIRequestContext) -> None:
    req = Repositories().user_repositories_list(api_request_context)
    _, response = req
    assert response.json()[0]["name"], f"REQ = {req}"


@pytest.mark.API
@pytest.mark.commits
def test_get_commits_list(api_request_context: APIRequestContext) -> None:
    req = Commits().get_commits(api_request_context, "Test_repo")
    _, response = req
    assert response.json()[0], f"REQ = {response}"


@pytest.mark.API
def test_repository_create_and_delete(repo_create_delete: str) -> None:
    new_repo = repo_create_delete
    assert new_repo, f"Something went wrong: {new_repo}"
