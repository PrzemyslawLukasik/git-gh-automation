import os

from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.base_url = os.environ["URL"]
        self.url = ""

    def visit(self) -> None:
        self.page.goto(self.base_url + self.url)
