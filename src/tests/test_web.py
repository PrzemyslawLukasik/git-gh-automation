import os

import pytest
from playwright.sync_api import APIRequestContext, APIResponse, Page

from src.endpoints.repositories import Repositories
from src.fixtures.api_fixture import api_request_context
from src.helpers.generators import generate_new_repo_data_ui


@pytest.mark.UI
def test_open_login_page(dashboard_page) -> None:
    dashboard_page.visit()
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
