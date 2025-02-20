import pytest
from playwright.sync_api import APIRequestContext

from src.endpoints.branches import Branches
from src.endpoints.commits import Commits
from src.endpoints.repositories import Repositories
from src.fixtures.api_fixture import api_request_context, repo_create_delete
from src.helpers.misc import filter_names


@pytest.mark.API
def test_get_repositories(api_request_context: APIRequestContext) -> None:
    req = Repositories().user_repositories_list(api_request_context)
    status, response = req
    assert 200 == status, f"Incorrect response status: {status}"
    assert response.json()[0]["name"], f"REQ = {req}"


@pytest.mark.API
@pytest.mark.commits
def test_get_commits_list(api_request_context: APIRequestContext) -> None:
    req = Commits().get_commits(api_request_context, "Test_repo")
    status, response = req
    assert 200 == status, f"Incorrect response status: {status}"
    assert response.json()[0], f"REQ = {response}"


@pytest.mark.API
def test_repository_create_and_delete(
    api_request_context, repo_create_delete: str
) -> None:
    new_repo = repo_create_delete
    req = Repositories().user_repositories_list(api_request_context)
    status, response = req
    assert 200 == status, f"Incorrect response status: {status}"
    assert filter_names(
        response.json(), new_repo
    ), f"Something went wrong: {new_repo}\n {response.json()}"


@pytest.mark.API
def test_get_branches_list(api_request_context, repo_create_delete) -> None:
    new_repo = repo_create_delete
    req = Branches().get_branches(api_request_context, new_repo)
    status, response = req
    assert 200 == status, f"Incorrect status code: {status}"
    assert filter_names(response.json(), "main"), "No branches list"
