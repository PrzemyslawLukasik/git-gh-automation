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
