import os
from dataclasses import dataclass

from playwright.sync_api import Locator, Page, expect

from src.pages.base_page import BasePage


@dataclass
class PullRequestLocators:
    def __init__(self, page: Page) -> None:
        self.page = page

    def merge_pull_request_button(self) -> Locator:
        return self.page.get_by_role("button", name="Merge pull request")

    def confirm_merge_button(self) -> Locator:
        return self.page.get_by_role("button", name="Confirm merge")

    def merged_image(self) -> Locator:
        return self.page.get_by_role("img", name="Merged")


class PullRequestPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.locators = PullRequestLocators(self.page)

    def click_on_merge_pr_button(self) -> None:
        self.locators.merge_pull_request_button().scroll_into_view_if_needed()
        self.locators.merge_pull_request_button().click(timeout=3_000)

    def click_on_confirm_merge_button(self) -> None:
        self.locators.confirm_merge_button().scroll_into_view_if_needed()
        self.locators.confirm_merge_button().click(timeout=3_000)

    def is_confirm_merge_image_visible(self) -> None:
        expect(self.locators.merged_image()).to_be_visible(timeout=10_000)

    def confirm_and_merge(self) -> None:
        self.click_on_merge_pr_button()
        self.click_on_confirm_merge_button()
        self.is_confirm_merge_image_visible()
