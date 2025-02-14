import pytest
from playwright.sync_api import (
    Browser,
    BrowserContext,
    Page,
    StorageState,
    sync_playwright,
)
from typing_extensions import Generator

from src.pages.login_page import LoginPage
from src.pages.top_bar_po import TopBarPo


@pytest.fixture(scope="session")
def admin_storage_state(browser: Browser) -> Generator[StorageState, None, None]:
    context = browser.new_context()
    page = context.new_page()
    # Login to AUT
    login_page = LoginPage(page)
    top_bar = TopBarPo(page)
    login_page.visit()
    login_page.login()
    top_bar.is_user_loggedin()
    # Store context
    storage_state = context.storage_state()
    page.close()
    yield storage_state


# Fixture for the admin page with a new context
@pytest.fixture(scope="function")
def page(browser: Browser, admin_storage_state):
    context = browser.new_context(storage_state=admin_storage_state)
    context.tracing.start(screenshots=True, snapshots=True)
    page = context.new_page()
    yield page
    context.close()
