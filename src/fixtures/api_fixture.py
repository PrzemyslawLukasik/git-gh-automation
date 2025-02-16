import os
from typing import Generator

import pytest
from playwright.sync_api import APIRequestContext, Playwright, sync_playwright


@pytest.fixture(scope="function")
def api_request_context(
    playwright: Playwright,
) -> Generator[APIRequestContext, None, None]:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {os.environ['API_SECRET']}",
    }
    yield playwright.request.new_context(
        base_url=f"{os.environ['API_URL']}",
        extra_http_headers=headers,
        ignore_https_errors=True,
    )
