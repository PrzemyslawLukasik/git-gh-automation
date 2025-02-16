from dataclasses import dataclass

from playwright.sync_api import Locator, Page, expect

from src.pages.base_page import BasePage


@dataclass
class RepoCodePageLocators:
    def __init__(self, page: Page) -> None:
        self.page = page

    def code_button(self) -> Locator:
        return self.page.get_by_role("button", name="Code")


class RepoCodePage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.page = page
        self.locators = RepoCodePageLocators(self.page)

    def is_open(self) -> bool:
        return not expect(self.locators.code_button()).to_be_visible(timeout=5_000)
