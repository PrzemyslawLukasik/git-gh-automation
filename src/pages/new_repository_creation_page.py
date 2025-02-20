import os
from dataclasses import dataclass
from typing import Optional

from playwright.sync_api import Locator, Page, expect

from src.helpers.generators import generate_new_repo_data_ui, generate_string
from src.pages.base_page import BasePage


@dataclass
class NewRepositoryLocators:
    def __init__(self, page: Page) -> None:
        self.page = page

    def new_repository_header(self) -> Locator:
        return self.page.get_by_role("heading", name="Create a new repository")

    def repository_name_field(self) -> Locator:
        return self.page.get_by_role("textbox", name="Repository name *")

    def description_field(self) -> Locator:
        return self.page.get_by_role("textbox", name="Description")

    def public_repo_checkbox(self) -> Locator:
        return self.page.get_by_role("radio", name="Public")

    def private_repo_checkbox(self) -> Locator:
        return self.page.get_by_role("radio", name="Private")

    def add_readme_checkbox(self) -> Locator:
        return self.page.get_by_role("checkbox", name="Add a README file")

    def create_repository_button(self) -> Locator:
        return self.page.get_by_role("button", name="Create repository")

    def repo_name_available_check(self) -> Locator:
        return self.page.locator("#RepoNameInput-is-available")


@dataclass
class NewRepositoryStatics:
    repository_mname = next(generate_new_repo_data_ui())["repository_name"]
    description = generate_string()


class NewRepositoryPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page=page)

        self.url = "/new"

        self.locators = NewRepositoryLocators(self.page)
        self.statisc = NewRepositoryStatics()

    def is_page_opened(self) -> bool:
        return not expect(self.locators.new_repository_header()).to_be_visible(
            timeout=10_000
        )

    def fill_repository_name(self, repo_name: str) -> None:
        self.locators.repository_name_field().fill(repo_name)
        expect(self.locators.repository_name_field()).to_have_value(repo_name)
        expect(self.locators.repo_name_available_check()).to_be_visible(timeout=5_000)

    def fill_description_filed(self, description: str) -> None:
        self.locators.description_field().fill(description)
        expect(self.locators.description_field()).to_have_value(description)

    def click_public_repo_checkbox(self) -> None:
        self.locators.public_repo_checkbox().click()

    def click_private_repo_checkbox(self) -> None:
        self.locators.private_repo_checkbox().click()

    def click_add_readme(self) -> None:
        self.locators.add_readme_checkbox().scroll_into_view_if_needed()
        self.locators.add_readme_checkbox().click()

    def click_create_repository_button(self) -> None:
        self.locators.create_repository_button().scroll_into_view_if_needed()
        self.locators.create_repository_button().click()

    def create_repository(self, data: Optional[dict]) -> None:
        if data["repository_name"]:
            repo_name = data["repository_name"]
        else:
            repo_name = self.statisc.repository_mname
        if data["description"]:
            description = data["description"]
        else:
            description = self.statisc.description
        self.fill_repository_name(repo_name=repo_name)
        self.fill_description_filed(description=description)
        if data["private"]:
            self.click_public_repo_checkbox()
        if data["auto_init"]:
            self.click_add_readme()
        self.click_create_repository_button()
