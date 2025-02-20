import pytest
from playwright.sync_api import (
    Browser,
    BrowserContext,
    Page,
    StorageState,
    sync_playwright,
)
from typing_extensions import Generator

from src.pages.dashboard import DashboardPage
from src.pages.login_page import LoginPage
from src.pages.new_repository_creation_page import NewRepositoryPage
from src.pages.repository_page.compare_changes_page import CompareChangesPage
from src.pages.repository_page.pull_request_page import PullRequestPage
from src.pages.repository_page.pull_requests_page import PullRequestsPage
from src.pages.repository_page.repo_code_page import RepoCodePage
from src.pages.repository_page.repository_page import RepositoryPage
from src.pages.repository_page.top_bar_menu import TopBarMenuPo
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


@pytest.fixture
def dashboard_page(page: Page) -> Generator[DashboardPage, None, None]:
    dashboard_page = DashboardPage(page)
    yield dashboard_page


@pytest.fixture
def top_bar_menu(page: Page) -> Generator[TopBarMenuPo, None, None]:
    top_bar_menu = TopBarMenuPo(page)
    yield top_bar_menu


@pytest.fixture
def pull_requests_page(page: Page) -> Generator[PullRequestsPage, None, None]:
    pull_requests_page = PullRequestsPage(page)
    yield pull_requests_page


@pytest.fixture
def pull_request_page(page: Page) -> Generator[PullRequestPage, None, None]:
    pull_request_page = PullRequestPage(page)
    yield pull_request_page


@pytest.fixture
def compare_changes_page(page: Page) -> Generator[CompareChangesPage, None, None]:
    compare_changes_page = CompareChangesPage(page)
    yield compare_changes_page
