import os
from dataclasses import dataclass

from playwright.sync_api import Locator, Page, expect

from src.pages.base_page import BasePage


@dataclass
class DashboardLocator:
    def __init__(self, page: Page) -> None:
        self.page = page

    def new_button(self) -> Locator:
        return self.page.get_by_role("link", name="New")

    def search_repo_field(self) -> Locator:
        return self.page.get_by_role("textbox", name="Find a repository…")

    def dashboard_header(self) -> Locator:
        return self.page.get_by_role("link", name="Dashboard")


class DashboardPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.locators = DashboardLocator(self.page)
        self.url = "/dashboard"

    def is_open(self) -> bool:
        expect(self.locators.dashboard_header()).to_be_visible(timeout=5_000)

    def click_new_button(self) -> None:
        self.locators.new_button().click()
