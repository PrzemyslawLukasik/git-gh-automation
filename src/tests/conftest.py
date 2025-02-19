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
from src.pages.new_repository_creation_page import NewRepositoryPage
from src.pages.repository_page.repo_code_page import RepoCodePage
from src.pages.repository_page.repository_page import RepositoryPage
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


@pytest.fixture
def login_page(page: Page) -> Generator[LoginPage, None, None]:
    login_page = LoginPage(page)
    yield login_page


@pytest.fixture
def new_repo_create_page(page: Page) -> Generator[NewRepositoryPage, None, None]:
    new_repo_page = NewRepositoryPage(page)
    yield new_repo_page


@pytest.fixture
def top_bar_po(page: Page) -> Generator[TopBarPo, None, None]:
    top_bar = TopBarPo(page)
    yield top_bar


@pytest.fixture
def repo_code_page(page: Page) -> Generator[RepoCodePage, None, None]:
    repo_code_page = RepoCodePage(page)
    yield repo_code_page


@pytest.fixture
def repository_page(page: Page) -> Generator[RepositoryPage, None, None]:
    repository_page = RepositoryPage(page)
    yield repository_page
