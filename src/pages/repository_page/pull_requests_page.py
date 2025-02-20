import os
from dataclasses import dataclass

from playwright.sync_api import Locator, Page, expect

from src.pages.base_page import BasePage


@dataclass
class PullRequestsLocators:
    def __init__(self, page: Page) -> None:
        self.page = page

    def new_pull_request_button(self) -> Locator:
        return self.page.get_by_role("link", name="New pull request")

    def branch_item(self, branch_name: str) -> Locator:
        return self.page.get_by_role("menuitemradio", name=branch_name)


class PullRequestsPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.locators = PullRequestsLocators(self.page)

    def click_on_new_pull_request_button(self) -> None:
        self.locators.new_pull_request_button().click()
