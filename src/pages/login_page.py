import os
from dataclasses import dataclass

from playwright.sync_api import Locator, Page, expect

from src.pages.base_page import BasePage


@dataclass
class LoginPageLocator:
    def __init__(self, page: Page) -> None:
        self.page = page

    def sign_in_header(self) -> Locator:
        return self.page.get_by_role("heading", name="Sign in to GitHub")

    def user_name_field(self) -> Locator:
        return self.page.get_by_role("textbox", name="Username or email address")

    def password_field(self) -> Locator:
        return self.page.get_by_role("textbox", name="Password")

    def sign_in_button(self) -> Locator:
        return self.page.get_by_role("button", name="Sign in", exact=True)


@dataclass
class LoginPageStatics:
    username: str = os.environ["USERNAME"]
    password: str = os.environ["PASSWORD"]


class LoginPage(BasePage):

    """Login Page
    Includes all locators and actions that cen be performad on the login page
    """

    def __init__(self, page: Page) -> None:
        super().__init__(page=page)

        self.locators = LoginPageLocator(self.page)
        self.statics = LoginPageStatics()

        self.url = (
            "https://github.com/login?return_to=https%3A%2F%2Fgithub.com%2Fdashboard"
        )

    def is_login_page_opened(self) -> bool:
        expect(self.locators.sign_in_header()).to_be_visible(timeout=5_000)

    def fill_username_field(self, username: str) -> None:
        username = username or self.statics.username
        self.locators.user_name_field().fill(username)
        expect(self.locators.user_name_field()).to_have_value(username)

    def fill_password_field(self, password: str) -> None:
        password = password or self.statics.password
        self.locators.password_field().fill(password)
        expect(self.locators.password_field()).to_have_value(password)

    def login(self, username: str = "", password: str = "") -> None:
        username = username or self.statics.username
        password = password or self.statics.password

        self.fill_username_field(username=username)
        self.fill_password_field(password=password)
        self.locators.sign_in_button().click()
