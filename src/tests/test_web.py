import os

import pytest
from playwright.sync_api import APIRequestContext, APIResponse, Page

from src.endpoints.repositories import Repositories
from src.fixtures.api_fixture import api_request_context


@pytest.mark.UI
def test_open_login_page(page: Page) -> None:
    page.goto("https://github.com/dashboard")
    page.pause()
