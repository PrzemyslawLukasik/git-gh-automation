from dataclasses import dataclass

from playwright.sync_api import Locator, Page, expect


@dataclass
class TopBarMenuLocator:
    def __init__(self, page: Page) -> None:
        self.page = page

    def code_link(self) -> Locator:
        return self.page.get_by_role("link", name="Code")

    def pull_requests_link(self) -> Locator:
        return self.page.get_by_role("link", name="Pull requests", exact=True)


class TopBarMenuPo:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.locators = TopBarMenuLocator(self.page)

    def click_on_code_link(self) -> None:
        self.locators.code_link().click()

    def click_on_pull_requests(self) -> None:
        self.locators.pull_requests_link().click()
