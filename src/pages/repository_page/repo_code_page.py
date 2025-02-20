import os
from dataclasses import dataclass

from playwright.sync_api import Locator, Page, expect

from src.pages.base_page import BasePage


@dataclass
class RepoCodePageLocators:
    def __init__(self, page: Page) -> None:
        self.page = page

    def code_button(self) -> Locator:
        return self.page.get_by_role("button", name="Code")

    def repo_title(self, name: str) -> Locator:
        return self.page.locator("#repo-title-component").get_by_role("link", name=name)

    def file_by_name(self, name: str) -> Locator:
        return (
            self.page.get_by_role("table")
            .get_by_role("row", name=name)
            .filter(has_not=self.page.get_by_test_id("screen-reader-heading"))
        )

    # branch selection modal

    def branch_button(self) -> Locator:
        return self.page.get_by_test_id("anchor-button")

    def branch_search_field(self) -> Locator:
        return self.page.get_by_role("textbox", name="Filter branches")

    def branch_item(self, branch_name: str) -> Locator:
        return self.page.get_by_role("menuitemradio", name=branch_name)


class RepoCodePage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.page = page
        self.locators = RepoCodePageLocators(self.page)

    def visit_repo(self, repo_name: str) -> None:
        self.page.goto(f"{os.environ['URL']}/{os.environ['API_USER']}/{repo_name}")
        self.is_correct_repo_open(repo_name)

    def is_open(self) -> bool:
        return not expect(self.locators.code_button()).to_be_visible(timeout=5_000)

    def is_correct_repo_open(self, name: str) -> bool:
        expect(self.locators.repo_title(name)).to_be_visible(timeout=5_000)

    def is_file_visible(self, name: str) -> None:
        expect(self.locators.file_by_name(name)).to_be_visible()

    def click_on_branch_button(self) -> None:
        self.locators.branch_button().click()

    def fill_branch_search_field(self, branch_name: str) -> None:
        self.locators.branch_search_field().fill(branch_name)

    def is_branch_visible(self, branch_name: str) -> None:
        expect(self.locators.branch_item(branch_name)).to_be_visible()

    def click_branch_item(self, branch_name: str) -> None:
        self.locators.branch_item(branch_name).click(timeout=3_000)

    def select_branch(self, branch_name: str) -> None:
        self.click_on_branch_button()
        self.fill_branch_search_field(branch_name)
        self.is_branch_visible(branch_name)
        self.click_branch_item(branch_name)
