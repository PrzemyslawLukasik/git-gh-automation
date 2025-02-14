from dataclasses import dataclass

from playwright.sync_api import Locator, Page, expect


@dataclass
class TopBarLocators:
    """GitHub TopBar locators"""

    def __init__(self, page: Page) -> None:
        self.page = page

    def ham_menu(self) -> Locator:
        return self.page.get_by_role("button", name="Open global navigation menu")

    def seaarch_field(self) -> Locator:
        return self.page.get_by_role("button", name="Type / to search")

    def create_new_button(self) -> Locator:
        return self.page.get_by_role("button", name="Create something new")

    def create_repository_menu_item(self) -> Locator:
        return self.page.get_by_role("menuitem", name="New repository")

    def user_menu_icon(self) -> Locator:
        return self.page.get_by_role("button", name="Open user navigation menu")


class TopBarPo:
    """GitHub Top menu bar items actions"""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.locators = TopBarLocators(self.page)

    def is_user_loggedin(self) -> bool:
        return not expect(self.locators.user_menu_icon()).to_be_visible(timeout=10_000)
