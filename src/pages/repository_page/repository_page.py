from playwright.sync_api import Page

from src.pages.base_page import BasePage
from src.pages.repository_page.repo_code_page import RepoCodePage
from src.pages.repository_page.top_bar_menu import TopBarMenuPo


class RepositoryPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.top_bar_menu = TopBarMenuPo(self.page)
        self.repo_code_page = RepoCodePage(self.page)

    def open_code_page(self) -> None:
        self.top_bar_menu.click_on_code_link()
        self.repo_code_page.is_open()
