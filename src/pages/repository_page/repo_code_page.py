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


class RepoCodePage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.page = page
        self.locators = RepoCodePageLocators(self.page)

    def is_open(self) -> bool:
        return not expect(self.locators.code_button()).to_be_visible(timeout=5_000)

    def is_correct_repo_open(self, name: str) -> bool:
        expect(self.locators.repo_title(name)).to_be_visible(timeout=5_000)
