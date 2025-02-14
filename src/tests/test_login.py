import os

import pytest
from playwright.sync_api import Page


@pytest.mark.UI
def test_open_login_page(page: Page) -> None:
    page.goto("https://github.com/dashboard")
    page.pause()
