import os
from typing import Generator

import pytest
from playwright.sync_api import APIRequestContext, Playwright, sync_playwright

from src.endpoints.repositories import Repositories
from src.helpers.generators import generate_new_repo_data_api


@pytest.fixture(scope="function")
def api_request_context(
    playwright: Playwright,
) -> Generator[APIRequestContext, None, None]:
    headers = {
        "X-GitHub-Api-Version": "2022-11-28",
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {os.environ['API_SECRET']}",
    }
    yield playwright.request.new_context(
        base_url=f"{os.environ['API_URL']}",
        extra_http_headers=headers,
        ignore_https_errors=True,
    )


@pytest.fixture
def repo_create_delete(
    api_request_context: APIRequestContext,
) -> Generator[tuple[int, str], None, None]:
    data = next(generate_new_repo_data_api())
    status, repo_name = Repositories().create_repository(api_request_context, data)
    yield repo_name
    Repositories().delete_repository(api_request_context, repo_name)
