import os

import pytest
from playwright.sync_api import APIRequestContext, APIResponse, Page

from src.endpoints.repositories import Repositories
from src.fixtures.api_fixture import api_request_context


@pytest.mark.API
def test_get_public_repositories(api_request_context: APIRequestContext) -> None:
    req = Repositories().user_repositories_list(api_request_context)
    status, response = req
    print(status, response.json()[0]["name"])
    assert response.json()[0]["name"], f"REQ = {req}"
