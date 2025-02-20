import os
from dataclasses import dataclass

from playwright.sync_api import Locator, Page, expect

from src.pages.base_page import BasePage


@dataclass
class CompareChangesLocators:
    def __init__(self, page: Page) -> None:
        self.page = page

    def base_branch_select_button(self) -> Locator:
        return self.page.locator("summary").filter(has_text="base:")

    def compare_branch_select_button(self) -> Locator:
        return self.page.locator("summary").filter(has_text="compare:")

    def branch_search_field(self) -> Locator:
        return self.page.get_by_role("textbox", name="Find a branch")

    def branch_item(self, branch_name: str) -> Locator:
        return self.page.get_by_role("menuitemradio", name="test_branch")

    def able_to_merge_info(self) -> Locator:
        return self.page.get_by_text("Able to merge.")

    def create_pr_button(self) -> Locator:
        return self.page.get_by_role("button", name="Create pull request")


class CompareChangesPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.locators = CompareChangesLocators(self.page)

    def click_on_compare_branch_button(self) -> None:
        self.locators.compare_branch_select_button().click()

    def fill_branch_search_field(self, branch_name: str) -> None:
        self.locators.branch_search_field().fill(branch_name)

    def is_branch_visible(self, branch_name: str) -> None:
        expect(self.locators.branch_item(branch_name)).to_be_visible()

    def click_branch_item(self, branch_name: str) -> None:
        self.locators.branch_item(branch_name).click(timeout=3_000)

    def is_able_to_merge_visible(self) -> None:
        expect(self.locators.able_to_merge_info()).to_be_visible(timeout=5_000)

    def click_on_create_pull_request_button(self) -> None:
        expect(self.locators.able_to_merge_info()).to_be_visible(timeout=5_000)
        self.locators.create_pr_button().click(timeout=3_000)

    def select_branch(self, branch_name: str) -> None:
        self.click_on_compare_branch_button()
        self.fill_branch_search_field(branch_name)
        self.is_branch_visible(branch_name)
        self.click_branch_item(branch_name)

    def create_pull_request(self, base_branch: str, compare_branch: str) -> None:
        self.select_branch(compare_branch)
        self.click_on_create_pull_request_button()
        self.locators.create_pr_button().scroll_into_view_if_needed()
        self.click_on_create_pull_request_button()
